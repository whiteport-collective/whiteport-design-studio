"""Kortläsaren: när ett minneskort eller en kamera med DCIM ansluts kopieras allt till det
aktiva projektets inkorg, kontrollerat mot kortet. Kortet rörs aldrig.

    python card_watch.py            # bevakar tills datorn stängs av
    python card_watch.py --once     # kopierar från de kort som sitter i nu och slutar

Inställningen ligger i ~/.wds/media.json på varje dator:
    {"person": "marten", "inkorg": "G:/Shared drives/Visita Kommunikation/projects/2026-10-21-studiebesok-stockholm/inkorg"}

Allt hamnar i <inkorg>/<person>/. Mediaarbetaren eller Viska sorterar det sedan.
Varje kopiering skrivs i ~/.wds/card_watch.log, och datorn visar en notis när den är klar.
"""
import argparse, datetime as dt, json, string, subprocess, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
MEDIA_COPY = HERE.parent / "media-copy" / "media_copy.py"
CONFIG = Path.home() / ".wds" / "media.json"
LOG = Path.home() / ".wds" / "card_watch.log"


def cards():
    """Enheter med en DCIM-mapp i roten (kort i kortläsare, eller kamera i PC-läge)."""
    found = []
    for letter in string.ascii_uppercase[3:]:
        root = Path(f"{letter}:/")
        try:
            if (root / "DCIM").is_dir():
                found.append(root)
        except OSError:
            pass
    return found


def notify(title, text):
    ps = ("Add-Type -AssemblyName System.Windows.Forms; $n = New-Object System.Windows.Forms.NotifyIcon; "
          "$n.Icon = [System.Drawing.SystemIcons]::Information; $n.Visible = $true; "
          f"$n.ShowBalloonTip(10000, '{title}', '{text}', 'Info'); Start-Sleep 11; $n.Dispose()")
    subprocess.Popen(["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command", ps])


def log(text):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{dt.datetime.now():%Y-%m-%d %H:%M:%S} {text}\n")
    print(text, flush=True)


def copy(card: Path, cfg):
    dest = Path(cfg["inkorg"]) / cfg["person"]
    log(f"Kort {card} hittat, kopierar till {dest}")
    r = subprocess.run([sys.executable, str(MEDIA_COPY), "copy", str(card), str(dest), "--apply"],
                       capture_output=True, text=True, encoding="utf-8")
    log(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()[-300:])
    if r.returncode == 0:
        notify("Kortet är kopierat", f"Allt från {card} ligger i inkorgen. Formatera kortet i kameran när Drive har synkat.")
    elif r.returncode == 2:
        notify("Kortet är kopierat, med krockar", "Några filer krockade och kopierades inte. Formatera inte kortet; Viska tittar på det.")
    else:
        notify("Kopieringen avbröts", "Något gick fel. Formatera inte kortet. Se ~/.wds/card_watch.log.")
    return r.returncode


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--every", type=int, default=10)
    a = ap.parse_args()
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    seen = set() if a.once else set(cards())  # kort som satt i redan vid start kopieras inte av sig själva
    while True:
        now = set(cards())
        for card in sorted(now - seen) if not a.once else sorted(now):
            copy(card, cfg)
        seen = now
        if a.once:
            break
        time.sleep(a.every)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
