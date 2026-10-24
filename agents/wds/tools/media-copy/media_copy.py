"""Kopierar media från ett minneskort eller en inkorg till en inspelning, utan att något någonsin skrivs över.

    python media_copy.py scan <källa>
    python media_copy.py cameras <källa> --gear <user.md> [<user.md> ...]
    python media_copy.py check <källa> [--photographer "Mårten Angner"]
    python media_copy.py register <user.md> --serial <nr> --make <märke> --model <modell> --person <person> --name <kamera>
    python media_copy.py sort <källa> <projektmapp> <datum>-<plats> --gear <user.md> [<user.md> ...] [--from ...] [--to ...] [--move] [--apply]
    python media_copy.py copy <källa> <mål> [--from "YYYY-MM-DD HH:MM"] [--to "YYYY-MM-DD HH:MM"] [--model <kamera>] [--serial <nr>] [--move] [--apply]

scan  listar mediet i källan: antal per typ, kameror och tidsluckor, så att agenten kan föreslå
      hur dagen delas upp på platser och källor.
copy  visar planen (torrkörning) och kopierar med --apply. Varje fil kopieras till en .part-fil,
      kontrolleras mot källans sha256 och döps sedan om. En fil som redan finns med samma innehåll
      hoppas över. En fil som finns med annat innehåll är en krock: den kopieras inte, och skriptet
      slutar med kod 2. Varje kopierad fil får en rad i <inspelning>/ingest.csv.
      --move flyttar i stället, från en inkorg: på samma enhet döps filen om, annars kopieras den,
      kontrolleras och tas bort ur källan. En fil som redan finns med samma innehåll tas bort ur källan.
      Använd aldrig --move mot ett minneskort.

cameras   kamerorna i källan (märke, modell, serienummer, antal filer) mot utrustningen i personernas själsfiler
          (avsnittet GEAR i users/<användare>/user.md): person och namn, eller OKÄND. Kod 3 om någon kamera saknas.
check     kamerans metadata per kamera: fotograf och upphovsrätt (Artist, Copyright), ägare (OwnerName),
          serienummer, tidszon (OffsetTimeOriginal), klockan (en tid i framtiden eller långt bakåt) och vitbalansen
          (låst på en förinställning som Daylight i stället för Auto).
          Säger vad som saknas eller är fel, så att personen kan ställa in det i kameran.
register  lägger till eller uppdaterar en kamera i en persons user.md, i tabellen under ## GEAR (skapas om den saknas).
sort      kopierar en inspelning (en tidsram) till <projektmapp>/<datum>-<plats>/<person>/<kamera>/ för varje kamera,
          med person och kamera ur utrustningen. Kameror som ingen har hoppas över (kod 3).

Tidpunkten kommer från exiftool (DateTimeOriginal, annars CreateDate), annars filens ändringstid.
Kameran känns igen på SerialNumber (eller InternalSerialNumber); telefoner, som saknar serienummer, på märke och modell.
"""
import argparse, csv, datetime as dt, hashlib, json, os, re, shutil, subprocess, sys, tempfile
from collections import Counter
from pathlib import Path

MEDIA = {".rw2", ".raw", ".dng", ".cr3", ".cr2", ".nef", ".arw", ".raf", ".orf",
         ".jpg", ".jpeg", ".heic", ".hif", ".png", ".tif", ".tiff",
         ".mp4", ".mov", ".mts", ".m2ts", ".avi", ".mxf", ".braw",
         ".wav", ".mp3", ".m4a", ".aac"}
GAP = dt.timedelta(minutes=45)


def files(src: Path):
    return sorted(p for p in src.rglob("*") if p.is_file() and p.suffix.lower() in MEDIA
                  and ".proxy." not in p.name and "-tvattad" not in p.name)


def meta(paths):
    """Tidpunkt och kamera per fil, i en exiftool-körning."""
    out = {}
    if paths and shutil.which("exiftool"):
        # Fillistan går via en argumentfil: många långa sökvägar spränger Windows kommandorad.
        with tempfile.NamedTemporaryFile("w", suffix=".args", delete=False, encoding="utf-8") as f:
            f.write("\n".join(str(p) for p in paths))
        args = ["exiftool", "-json", "-q", "-DateTimeOriginal", "-CreateDate", "-Make", "-Model", "-SerialNumber",
                "-InternalSerialNumber", "-Artist", "-Copyright", "-OwnerName", "-OffsetTimeOriginal", "-WhiteBalance",
                "-charset", "filename=utf8", "-@", f.name]
        r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8")
        os.unlink(f.name)
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
        TAGS[p] = row
    return result


TAGS = {}   # alla exiftool-fält per fil, från senaste meta()


def serial(row) -> str:
    return str(row.get("SerialNumber") or row.get("InternalSerialNumber") or "").strip()


def camera_key(row):
    """(serienummer, märke, modell): kameran som skrivit filen."""
    return serial(row), str(row.get("Make", "")).strip(), str(row.get("Model", "okänd")).strip()


COLS = ["serial", "make", "model", "person", "camera", "checked", "notes"]
HEADER = "| serial | make | model | person | camera | checked | notes |"


def read_register(paths):
    """Utrustningen i personernas själsfiler: tabellen under ## GEAR i users/<användare>/user.md
    (| serial | make | model | person | camera | checked | notes |). Flera filer läses ihop."""
    rows = []
    for path in ([paths] if isinstance(paths, Path) else paths):
        if not path.exists():
            continue
        in_table = False
        for line in path.read_text(encoding="utf-8").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")] if line.startswith("|") else None
            if cells and cells[0].lower() in ("serial", "serienummer"):
                in_table = True
                continue
            if not cells:
                in_table = False
                continue
            if in_table and len(cells) >= 5 and not set("".join(cells)) <= set("-: "):
                rows.append(dict(zip(COLS, cells + [""] * len(COLS))))
    return rows


def lookup(reg, key):
    sn, make, model = key
    if sn:
        hit = [r for r in reg if r["serial"] == sn]
        if hit:
            return hit[0]
    hit = [r for r in reg if not r["serial"] and r["model"].lower() == model.lower()]
    return hit[0] if len(hit) == 1 else None


def groups(ps, m):
    out = {}
    for p in ps:
        out.setdefault(camera_key(TAGS.get(p, {})), []).append(p)
    return out


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


def copy(src: Path, dest: Path, t_from, t_to, model, move: bool, apply: bool, sn=None, ps=None, m=None):
    if ps is None:
        ps = files(src)
        m = meta(ps)
    chosen = [p for p in ps if (t_from is None or m[p][0] >= t_from) and (t_to is None or m[p][0] <= t_to)
              and (model is None or m[p][1] == model) and (sn is None or serial(TAGS.get(p, {})) == sn)]
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


def cameras(src: Path, register):
    ps = files(src)
    m = meta(ps)
    reg = read_register(register)
    unknown = 0
    for key, fs in sorted(groups(ps, m).items(), key=lambda kv: -len(kv[1])):
        hit = lookup(reg, key)
        who = f"{hit['person']}/{hit['camera']}" if hit else "OKÄND, registreras först"
        unknown += hit is None
        when = sorted(m[p][0] for p in fs)
        print(f"{key[1]} {key[2]} sn {key[0] or '-'}: {len(fs)} filer, {when[0]:%Y-%m-%d %H:%M} – {when[-1]:%Y-%m-%d %H:%M} → {who}")
    return 3 if unknown else 0


def check(src: Path, photographer=None):
    """Kamerans metadata per kamera: det som saknas eller är fel, och vad personen ska ställa in."""
    ps = files(src)
    m = meta(ps)
    now = dt.datetime.now()
    problems = 0
    for key, fs in groups(ps, m).items():
        rows = [TAGS.get(p, {}) for p in fs]
        imgs = [r for r, p in zip(rows, fs) if p.suffix.lower() not in (".mp4", ".mov", ".mts", ".m2ts", ".wav")] or rows
        first = lambda tag: next((str(r[tag]).strip() for r in imgs if str(r.get(tag, "")).strip()), "")
        notes = []
        artist, copyright_, owner = first("Artist"), first("Copyright"), first("OwnerName")
        if not artist:
            notes.append("fotografen (Artist) är inte inställd")
        elif photographer and photographer.lower() not in artist.lower():
            notes.append(f"fotografen är '{artist}', inte {photographer}")
        if not copyright_:
            notes.append("upphovsrätten (Copyright) är inte inställd")
        if not key[0] and key[1].lower() not in ("apple", "samsung", "google"):
            notes.append("inget serienummer i filerna; kameran kan inte skiljas från en likadan")
        if not first("OffsetTimeOriginal"):
            notes.append("ingen tidszon i filerna (OffsetTimeOriginal); ställ in tidszon i kameran")
        wb = Counter(str(r.get("WhiteBalance", "")).strip() for r in imgs if str(r.get("WhiteBalance", "")).strip())
        locked = {k: v for k, v in wb.items() if not k.lower().startswith("auto")}
        if locked:
            notes.append("vitbalansen var låst på " + ", ".join(f"{k} ({v} filer)" for k, v in locked.items())
                         + "; välj Auto (AWB) om det inte var meningen. RAW-filerna går att rätta, JPEG-filerna har färgen inbakad")
        times = sorted(m[p][0] for p in fs)
        if times[-1] > now + dt.timedelta(minutes=10):
            notes.append(f"klockan går före: senaste bilden är tagen {times[-1]:%Y-%m-%d %H:%M}, i framtiden")
        if times[0].year < 2015:
            notes.append(f"klockan är troligen inte inställd: {times[0]:%Y-%m-%d}")
        problems += bool(notes)
        print(f"{key[1]} {key[2]} sn {key[0] or '-'} ({len(fs)} filer): fotograf '{artist or '-'}', upphovsrätt '{copyright_ or '-'}', ägare '{owner or '-'}'")
        for n in notes:
            print(f"  - {n}")
        if not notes:
            print("  metadata ser rätt ut")
    return 4 if problems else 0


def register_camera(path: Path, sn, make, model, person, name, note=""):
    """Skriver kameran i personens user.md, i tabellen under ## GEAR. Resten av filen rörs inte."""
    row = f"| {sn} | {make} | {model} | {person} | {name} | {dt.date.today():%Y-%m-%d} | {note} |"
    lines = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    head = next((i for i, l in enumerate(lines) if l.startswith("|") and l.strip("| ").lower().startswith(("serial", "serienummer"))), None)
    if head is None:
        lines += ["", "## GEAR: cameras and equipment",
                  "Read by every WDS agent. Viska recognizes a camera by the serial number in its files "
                  "(agents/wds/data/media-storage.md in the WDS repo).", "", HEADER, "|---|---|---|---|---|---|---|"]
        head = len(lines) - 2
    end = head + 2
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    replaced = False
    for i in range(head + 2, end):
        cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        if (sn and cells[0] == sn) or (not sn and not cells[0] and len(cells) > 2 and cells[2].lower() == model.lower()):
            lines[i], replaced = row, True
    if not replaced:
        lines.insert(end, row)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(("uppdaterad i " if replaced else "registrerad i ") + f"{path}: {row}")
    return 0


def sort(src: Path, project: Path, shoot: str, register, t_from, t_to, move: bool, apply: bool):
    ps = files(src)
    m = meta(ps)
    reg = read_register(register)
    worst = 0
    for key, fs in groups(ps, m).items():
        inside = [p for p in fs if (t_from is None or m[p][0] >= t_from) and (t_to is None or m[p][0] <= t_to)]
        if not inside:
            continue
        hit = lookup(reg, key)
        if not hit:
            print(f"OKÄND kamera {key[1]} {key[2]} sn {key[0] or '-'}: {len(inside)} filer hoppas över; registrera den i ägarens user.md först")
            worst = max(worst, 3)
            continue
        code = copy(src, project / shoot / hit["person"] / hit["camera"], t_from, t_to, None, move, apply, None, inside, m)
        worst = max(worst, code)
    return worst


def when_arg(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M") if s else None


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan"); s.add_argument("source", type=Path)
    k = sub.add_parser("cameras"); k.add_argument("source", type=Path); k.add_argument("--gear", type=Path, nargs="+", required=True)
    h = sub.add_parser("check"); h.add_argument("source", type=Path); h.add_argument("--photographer")
    r = sub.add_parser("register"); r.add_argument("user_md", type=Path)
    for f in ("--serial", "--make", "--model", "--person", "--name", "--note"):
        r.add_argument(f, default="")
    o = sub.add_parser("sort"); o.add_argument("source", type=Path); o.add_argument("project", type=Path)
    o.add_argument("shoot"); o.add_argument("--gear", type=Path, nargs="+", required=True)
    o.add_argument("--from", dest="t_from"); o.add_argument("--to", dest="t_to")
    o.add_argument("--move", action="store_true"); o.add_argument("--apply", action="store_true")
    c = sub.add_parser("copy"); c.add_argument("source", type=Path); c.add_argument("dest", type=Path)
    c.add_argument("--from", dest="t_from"); c.add_argument("--to", dest="t_to"); c.add_argument("--model"); c.add_argument("--serial")
    c.add_argument("--move", action="store_true"); c.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    if a.cmd == "scan":
        sys.exit(scan(a.source))
    if a.cmd == "cameras":
        sys.exit(cameras(a.source, a.gear))
    if a.cmd == "check":
        sys.exit(check(a.source, a.photographer))
    if a.cmd == "register":
        sys.exit(register_camera(a.user_md, a.serial, a.make, a.model, a.person, a.name, a.note))
    if a.cmd == "sort":
        sys.exit(sort(a.source, a.project, a.shoot, a.gear, when_arg(a.t_from), when_arg(a.t_to), a.move, a.apply))
    sys.exit(copy(a.source, a.dest, when_arg(a.t_from), when_arg(a.t_to), a.model, a.move, a.apply, a.serial))
