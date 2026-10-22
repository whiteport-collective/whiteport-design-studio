"""Kopierar media från ett minneskort till en inspelningsmapp, utan att något någonsin skrivs över.

    python media_copy.py scan <källa>
    python media_copy.py copy <källa> <mål> [--from "YYYY-MM-DD HH:MM"] [--to "YYYY-MM-DD HH:MM"] [--model <kamera>] [--move] [--apply]

scan  listar mediet i källan: antal per typ, kameror och tidsluckor, så att agenten kan föreslå
      hur dagen delas upp på platser och källor.
copy  visar planen (torrkörning) och kopierar med --apply. Varje fil kopieras till en .part-fil,
      kontrolleras mot källans sha256 och döps sedan om. En fil som redan finns med samma innehåll
      hoppas över. En fil som finns med annat innehåll är en krock: den kopieras inte, och skriptet
      slutar med kod 2. Varje kopierad fil får en rad i <inspelning>/ingest.csv.
      --move flyttar i stället, från en inkorg: på samma enhet döps filen om, annars kopieras den,
      kontrolleras och tas bort ur källan. En fil som redan finns med samma innehåll tas bort ur källan.
      Använd aldrig --move mot ett minneskort.

Tidpunkten kommer från exiftool (DateTimeOriginal, annars CreateDate), annars filens ändringstid.
"""
import argparse, csv, datetime as dt, hashlib, json, os, shutil, subprocess, sys
from collections import Counter
from pathlib import Path

MEDIA = {".rw2", ".raw", ".dng", ".cr3", ".cr2", ".nef", ".arw", ".raf", ".orf",
         ".jpg", ".jpeg", ".heic", ".hif", ".png", ".tif", ".tiff",
         ".mp4", ".mov", ".mts", ".m2ts", ".avi", ".mxf", ".braw",
         ".wav", ".mp3", ".m4a", ".aac"}
GAP = dt.timedelta(minutes=45)


def files(src: Path):
    return sorted(p for p in src.rglob("*") if p.is_file() and p.suffix.lower() in MEDIA)


def meta(paths):
    """Tidpunkt och kamera per fil, i en exiftool-körning."""
    out = {}
    if paths and shutil.which("exiftool"):
        args = ["exiftool", "-json", "-q", "-DateTimeOriginal", "-CreateDate", "-Model", "-charset", "filename=utf8"]
        r = subprocess.run(args + [str(p) for p in paths], capture_output=True, text=True, encoding="utf-8")
        for row in json.loads(r.stdout or "[]"):
            out[Path(row["SourceFile"]).resolve()] = row
    result = {}
    for p in paths:
        row = out.get(p.resolve(), {})
        when = None
        for key in ("DateTimeOriginal", "CreateDate"):
            v = str(row.get(key, ""))[:19]
            try:
                when = dt.datetime.strptime(v, "%Y:%m:%d %H:%M:%S")
                break
            except ValueError:
                pass
        if when is None:
            when = dt.datetime.fromtimestamp(p.stat().st_mtime)
        result[p] = (when, row.get("Model", "okänd"))
    return result


def sha256(p: Path):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def scan(src: Path):
    ps = files(src)
    if not ps:
        print(f"Inga mediefiler i {src}")
        return 0
    m = meta(ps)
    print(f"{len(ps)} filer, {sum(p.stat().st_size for p in ps) / 1e9:.1f} GB i {src}")
    print("Typer:   " + ", ".join(f"{k} {v}" for k, v in Counter(p.suffix.lower() for p in ps).most_common()))
    print("Kameror: " + ", ".join(f"{k} {v}" for k, v in Counter(c for _, c in m.values()).most_common()))
    ordered = sorted(m.items(), key=lambda kv: kv[1][0])
    start = prev = ordered[0][1][0]
    count = 0
    print("Pass (en ny rad efter mer än 45 minuters uppehåll):")
    for p, (when, _) in ordered:
        if when - prev > GAP:
            print(f"  {start:%Y-%m-%d %H:%M} – {prev:%H:%M}  {count} filer")
            start, count = when, 0
        prev, count = when, count + 1
    print(f"  {start:%Y-%m-%d %H:%M} – {prev:%H:%M}  {count} filer")
    return 0


def copy(src: Path, dest: Path, t_from, t_to, model, move: bool, apply: bool):
    ps = files(src)
    m = meta(ps)
    chosen = [p for p in ps if (t_from is None or m[p][0] >= t_from) and (t_to is None or m[p][0] <= t_to)
              and (model is None or m[p][1] == model)]
    plan, same, clash = [], [], []
    for p in chosen:
        target = dest / p.name
        if target.exists():
            (same if target.stat().st_size == p.stat().st_size and sha256(target) == sha256(p) else clash).append(p)
        else:
            plan.append(p)
    names = Counter(p.name for p in plan)
    for p in [p for p in plan if names[p.name] > 1]:
        clash.append(p)
    plan = [p for p in plan if names[p.name] == 1]

    verb = "flyttas" if move else "kopieras"
    print(f"Till {dest}")
    print(f"  {verb}: {len(plan)} filer, {sum(p.stat().st_size for p in plan) / 1e9:.1f} GB")
    print(f"  finns redan (samma innehåll, hoppas över): {len(same)}")
    print(f"  krockar (samma namn, annat innehåll, kopieras inte): {len(clash)}")
    for p in clash:
        print(f"    KROCK {p}")
    if not apply:
        print("Torrkörning. Kör igen med --apply för att kopiera.")
        return 2 if clash else 0

    dest.mkdir(parents=True, exist_ok=True)
    same_drive = move and os.path.splitdrive(src.resolve())[0].lower() == os.path.splitdrive(dest.resolve())[0].lower()
    log = dest.parent.parent / "ingest.csv"
    new_log = not log.exists()
    with open(log, "a", newline="", encoding="utf-8-sig" if new_log else "utf-8") as f:
        w = csv.writer(f)
        if new_log:
            w.writerow(["när", "åtgärd", "fil", "källa", "tagen", "kamera", "bytes", "sha256"])
        for i, p in enumerate(plan, 1):
            target, part = dest / p.name, dest / (p.name + ".part")
            digest, size = sha256(p), p.stat().st_size
            if target.exists():
                print(f"KROCK under kopieringen: {target} dök upp. Hoppar över.")
                clash.append(p)
                continue
            if same_drive:
                os.rename(p, target)
            else:
                shutil.copy2(p, part)
                if sha256(part) != digest:
                    part.unlink()
                    print(f"FEL: kopian av {p} stämmer inte med originalet. Avbryter.")
                    return 1
                os.replace(part, target)
                if move:
                    p.unlink()
            when, cam = m[p]
            w.writerow([dt.datetime.now().isoformat(timespec="seconds"), "flyttad" if move else "kopierad",
                        target.relative_to(dest.parent.parent).as_posix(), str(p), when.isoformat(), cam, size, digest])
            if i % 50 == 0:
                print(f"  {i}/{len(plan)}")
        if move:
            for p in same:
                p.unlink()
    print(f"Klart: {len(plan) - len([p for p in clash if p in plan])} filer {'flyttade' if move else 'kopierade'} och kontrollerade. Logg: {log}")
    return 2 if clash else 0


def when_arg(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M") if s else None


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan"); s.add_argument("source", type=Path)
    c = sub.add_parser("copy"); c.add_argument("source", type=Path); c.add_argument("dest", type=Path)
    c.add_argument("--from", dest="t_from"); c.add_argument("--to", dest="t_to"); c.add_argument("--model")
    c.add_argument("--move", action="store_true"); c.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    if a.cmd == "scan":
        sys.exit(scan(a.source))
    sys.exit(copy(a.source, a.dest, when_arg(a.t_from), when_arg(a.t_to), a.model, a.move, a.apply))
