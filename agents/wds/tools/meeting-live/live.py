#!/usr/bin/env python3
"""
live.py: ett Fireflies-möte live till en lokal fil. Del av WDS (agents/wds/tools/meeting-live.md).

Ingen server, ingen MCP. Fireflies realtid (socket.io) skrivs rad för rad till en jsonl-fil,
och agenten bevakar filen med watch.

    python live.py list                          # pågående möten
    python live.py join [--number 1 | --id ID]   # strömma till .wds/live/<tid>-<titel>.jsonl (körs i bakgrunden)
    python live.py join --continue <fil>         # fortsätt i samma fil efter ett avbrott, fyller luckan
    python live.py watch <fil> [--every 30]      # skriv ut nya repliker i klumpar, slutar när mötet är slut
    python live.py transcript <fil>              # hela mötet som läsbar text
    python live.py archive <fil> [<fil> …] [--out communication/meetings] [--lang sv] [--media <mediamappen>]
                                                 # hela mötet till repots mötesarkiv, med registret
                                                 # (--out är mappen; slutar den på .md är det filen)

join återansluter själv om Fireflies tappar anslutningen, i samma fil, och fyller luckan ur
Fireflies sparade transkript. archive hämtar Fireflies färdiga transkript när det finns.

Nyckeln: miljövariabeln FIREFLIES_API_KEY, hämtad ur Bitwarden vid körning. Den skrivs aldrig till fil.
Kräver: pip install "python-socketio[client]"
"""

import io
import json
import os
import re
import sys
import threading
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib import request

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)

GRAPHQL = "https://api.fireflies.ai/graphql"
REALTIME = "wss://api.fireflies.ai"
IDLE_FLUSH = 3.0      # sekunder utan uppdatering innan en replik räknas som klar
POLL_ACTIVE = 60      # hur ofta join kollar att mötet fortfarande pågår
FIRST_BATCH = 40      # watch visar högst så många rader första gången


def arg(name, default=None):
    a = sys.argv
    return a[a.index(name) + 1] if name in a and a.index(name) + 1 < len(a) else default


def key():
    k = os.environ.get("FIREFLIES_API_KEY")
    if not k:
        print('FIREFLIES_API_KEY saknas. Hämta den ur Bitwarden: export FIREFLIES_API_KEY="$(bw get password \'Fireflies API Key\')"')
        sys.exit(1)
    return k


def graphql(query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = request.Request(GRAPHQL, data=body, headers={
        "Authorization": f"Bearer {key()}", "Content-Type": "application/json", "User-Agent": "wds-meeting-live"})
    with request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    if data.get("errors"):
        raise RuntimeError(f"Fireflies: {json.dumps(data['errors'], ensure_ascii=False)}")
    return data["data"]


def active_meetings():
    q = """query($states: [MeetingState!]) { active_meetings(input: { states: $states }) {
             id title organizer_email start_time state } }"""
    ms = graphql(q, {"states": ["active", "paused"]})["active_meetings"] or []
    return sorted(ms, key=lambda m: m.get("start_time") or "", reverse=True)


def transcript(meeting_id):
    q = """query($id: String!) { transcript(id: $id) { id title date participants
             sentences { speaker_name text start_time end_time } } }"""
    return graphql(q, {"id": meeting_id})["transcript"]


def clock(sec):
    try:
        s = int(float(sec))
    except (TypeError, ValueError):
        return "--:--"
    return f"{s // 3600}:{s % 3600 // 60:02d}:{s % 60:02d}" if s >= 3600 else f"{s // 60:02d}:{s % 60:02d}"


def slug(text):
    t = text.lower().translate(str.maketrans("åäö", "aao"))
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")[:50] or "mote"


# ── list ────────────────────────────────────────────────────────────────

def cmd_list():
    ms = active_meetings()
    if not ms:
        print("Inga pågående möten. Starta inspelningen i Fireflies och försök igen om 30 sekunder.")
    for i, m in enumerate(ms, 1):
        print(f"{i}. {m['title']} | {m['id']} | {m.get('start_time') or '?'} | {m.get('state') or 'active'}")


# ── join ────────────────────────────────────────────────────────────────

RECONNECT_AFTER = 20  # sekunder utan anslutning innan join bygger en ny


def norm(text):
    return re.sub(r"\W+", " ", (text or "").lower()).strip()


class Writer:
    """Lägger till rader i mötesfilen. Kommer ihåg allt som redan skrivits, så att en ny anslutning
    eller en lucka som fylls aldrig skriver samma replik två gånger."""

    def __init__(self, path):
        self.path, self.n, self.lock, self.seen = path, 0, threading.Lock(), {}
        if path.exists():
            for row in read_rows(path):
                if "text" in row:
                    self.n = max(self.n, int(row.get("n") or 0))
                    self._remember(row)

    def _remember(self, row):
        try:
            start = float(row.get("start") or 0)
        except (TypeError, ValueError):
            start = 0.0
        self.seen.setdefault(norm(row["text"]), []).append(start)

    def _is_dup(self, row):
        key = norm(row.get("text"))
        if not key:
            return True
        try:
            start = float(row.get("start") or 0)
        except (TypeError, ValueError):
            start = 0.0
        # Samma text inom 15 sekunder är samma replik, även när liveutskriften och den färdiga skiljer lite i tid.
        return any(abs(start - s) < 15 for s in self.seen.get(key, []))

    def write(self, row):
        with self.lock:
            if "text" in row:
                if self._is_dup(row):
                    return False
                self._remember(row)
                self.n += 1
                row = {"n": self.n, **row}
            with open(self.path, "a", encoding="utf-8") as f:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
            return True


def fill(w, t, flag):
    """Skriver in det Fireflies redan har sparat och som saknas i filen. Returnerar antalet nya repliker."""
    return sum(w.write({"start": s.get("start_time"), "speaker": s.get("speaker_name"), "text": s.get("text"), flag: True})
               for s in (t.get("sentences") or []))


def now():
    return datetime.now().isoformat(timespec="seconds")


def cmd_join():
    try:
        import socketio
    except ImportError:
        print('Paketet saknas: python -m pip install "python-socketio[client]"')
        sys.exit(1)

    cont = arg("--continue")
    if cont:
        path = Path(cont)
        meeting_id = arg("--id") or next((r["meeting_id"] for r in read_rows(path) if r.get("meeting_id")), None)
        if not meeting_id:
            print(f"Hittar inget mötes-id i {path}. Ange --id.")
            sys.exit(1)
    else:
        meeting_id = arg("--id")
        if not meeting_id:
            ms = active_meetings()
            pick = int(arg("--number", "1"))
            if len(ms) < pick:
                print("Inget pågående möte på den platsen. Starta inspelningen i Fireflies och försök igen om 30 sekunder.")
                sys.exit(1)
            meeting_id = ms[pick - 1]["id"]

    t = transcript(meeting_id)
    if not cont:
        out = Path(arg("--out", ".wds/live"))
        out.mkdir(parents=True, exist_ok=True)
        path = out / f"{datetime.now():%Y-%m-%d_%H-%M}-{slug(t['title'])}.jsonl"
    w = Writer(path)
    w.write({"event": "rejoined" if cont else "joined", "title": t["title"], "meeting_id": meeting_id,
             "participants": t.get("participants") or [], "at": now()})
    added = fill(w, t, "fill" if cont else "seed")
    print(f'Ansluten till "{t["title"]}"')
    print(f"Fil: {path.resolve()}")
    print(f"{added} repliker från Fireflies inskrivna. Strömmar live. Ctrl+C avslutar.")

    pending, plock, done = {}, threading.Lock(), threading.Event()
    state = {"up": False, "since": time.time()}

    def flush(older_than=None):
        t0 = time.time()
        with plock:
            ready = [cid for cid, (ev, ts) in pending.items() if older_than is None or t0 - ts >= older_than]
            for cid in ready:
                ev, _ = pending.pop(cid)
                w.write({"start": ev.get("start_time"), "speaker": ev.get("speaker_name"), "text": ev.get("text"), "id": cid})

    def finish(reason):
        if done.is_set():
            return
        flush()
        w.write({"event": "ended", "reason": reason, "at": now()})
        print(f"Mötet är slut ({reason}). Fil: {path.resolve()}")
        done.set()

    def client():
        sio = socketio.Client(reconnection=False)

        @sio.on("auth.success")
        def _auth():
            print("Fireflies: inloggad.")

        @sio.on("connection.established")
        def _connected():
            state["up"] = True
            w.write({"event": "connected", "at": now()})
            print("Fireflies: realtid ansluten.")

        @sio.on("transcription.broadcast")
        def _segment(event):
            ev = event.get("payload", event) if isinstance(event, dict) else {}
            cid = str(ev.get("chunk_id") or ev.get("start_time"))
            # En ny bit betyder att de tidigare är klara. Samma bit kan komma flera gånger medan den växer.
            with plock:
                for c in [c for c in pending if c != cid]:
                    e, _ = pending.pop(c)
                    w.write({"start": e.get("start_time"), "speaker": e.get("speaker_name"), "text": e.get("text"), "id": c})
                pending[cid] = (ev, time.time())

        @sio.on("auth.failed")
        def _auth_failed(payload=None):
            w.write({"event": "error", "message": f"auth failed: {payload}"})
            finish("auth-failed")

        @sio.on("connection.error")
        def _conn_error(payload=None):
            state.update(up=False, since=time.time())
            w.write({"event": "error", "message": f"connection error: {payload}"})

        @sio.event
        def disconnect(*_):
            if not done.is_set():
                state.update(up=False, since=time.time())
                w.write({"event": "disconnected", "at": now()})

        return sio

    def idle_flusher():
        while not done.wait(1):
            flush(older_than=IDLE_FLUSH)

    def still_live():
        misses = 0
        while not done.wait(POLL_ACTIVE):
            try:
                ids = {m["id"] for m in active_meetings()}
                misses = 0 if meeting_id in ids else misses + 1
            except Exception as e:
                w.write({"event": "error", "message": f"active_meetings: {e}"})
            if misses >= 2:
                finish("mötet pågår inte längre i Fireflies")

    threading.Thread(target=idle_flusher, daemon=True).start()
    threading.Thread(target=still_live, daemon=True).start()

    try:
        while not done.is_set():
            state.update(up=False, since=time.time())
            sio = client()
            try:
                sio.connect(REALTIME, socketio_path="/ws/realtime", transports=["websocket"],
                            auth={"token": f"Bearer {key()}", "transcriptId": meeting_id}, wait_timeout=20)
            except Exception as e:
                w.write({"event": "error", "message": f"connect: {e}"})
            # Håll anslutningen så länge den lever. Är den nere längre än RECONNECT_AFTER byggs en ny.
            while not done.is_set() and (state["up"] or time.time() - state["since"] < RECONNECT_AFTER):
                done.wait(1)
            try:
                sio.disconnect()
            except Exception:
                pass
            if done.is_set():
                break
            w.write({"event": "reconnecting", "at": now()})
            print("Fireflies: anslutningen föll, ansluter igen och fyller luckan.")
            try:
                n = fill(w, transcript(meeting_id), "fill")
                if n:
                    w.write({"event": "filled", "count": n, "at": now()})
            except Exception as e:
                w.write({"event": "error", "message": f"fill: {e}"})
            done.wait(3)
    except KeyboardInterrupt:
        finish("avbrutet")


# ── watch ───────────────────────────────────────────────────────────────

def line_text(row):
    if "text" in row:
        return f"[{clock(row.get('start'))}] {row.get('speaker') or '?'}: {row['text']}"
    ev = row.get("event")
    if ev in ("joined", "rejoined"):
        return f"== Ansluten: {row.get('title')} =="
    if ev == "frame":
        return f"== Bild {clock(row.get('start'))}: {row.get('file')} =="
    if ev == "status":
        levels = ", ".join(f"{k} {'inget ljud' if v is None else f'{v} dB'}" for k, v in (row.get("levels") or {}).items())
        s = f"== Status {clock(row.get('start'))}: {levels}"
        if row.get("lag") is not None:
            s += f" · text {row['lag']} s efter talet"
        if row.get("skipped"):
            s += f" · {row['skipped']} s hoppades över live (kommer med i den grundliga utskriften)"
        if row.get("echo"):
            s += f" · {row['echo']} s eko från högtalarna i mikrofonen"
        return s + " =="
    if ev == "reconnecting":
        return "== Anslutningen föll, ansluter igen =="
    if ev == "filled":
        return f"== Luckan fylld med {row.get('count')} repliker från Fireflies =="
    if ev == "ended":
        return f"== MÖTET ÄR SLUT: {row.get('reason')} =="
    if ev == "error":
        return f"== FEL: {row.get('message')} =="
    return f"== {ev} =="


def read_rows(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def cmd_watch():
    path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    if not path or not path.exists():
        print(f"== FEL: filen finns inte: {path} ==")
        sys.exit(1)
    every = float(arg("--every", "30"))
    seen_file = path.with_suffix(".seen")
    seen = int(seen_file.read_text()) if seen_file.exists() else 0
    while True:
        rows = read_rows(path)
        new = rows[seen:]
        if new:
            if seen == 0 and len(new) > FIRST_BATCH:
                print(f"({len(new) - FIRST_BATCH} tidigare rader finns i filen)\n" + "\n".join(map(line_text, new[-FIRST_BATCH:])))
            else:
                print("\n".join(map(line_text, new)))
            seen = len(rows)
            seen_file.write_text(str(seen))
            if any(r.get("event") == "ended" for r in new):
                return
        time.sleep(every)


# ── transcript ──────────────────────────────────────────────────────────

def cmd_transcript():
    path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    if not path or not path.exists():
        print(f"Filen finns inte: {path}")
        sys.exit(1)
    print("\n".join(line_text(r) for r in read_rows(path)))


# ── archive ─────────────────────────────────────────────────────────────

LABELS = {
    "en": {"note": "Machine transcript: names and terms may be wrong, and speakers may be mixed up. "
                   "Times are minutes:seconds from the start of the recording.",
           "part": "Part", "final": "Fireflies, final transcript", "live": "Fireflies, live transcript",
           "local": "local transcription", "speakers": "Speakers", "summary": "Summary",
           "index_title": "Meetings", "index_intro": "Every recorded meeting, with the whole transcript. The archive only grows.",
           "cols": "| Date | Meeting | Length | Fireflies | Transcript | Summary |"},
    "sv": {"note": "Maskinell utskrift: namn och facktermer kan vara fel, och talarna kan vara förväxlade. "
                   "Tiden är minuter:sekunder från inspelningens start.",
           "part": "Del", "final": "Fireflies, färdigt transkript", "live": "Fireflies, liveutskrift",
           "local": "lokal utskrift", "speakers": "Talare", "summary": "Sammanfattning",
           "index_title": "Möten", "index_intro": "Alla inspelade möten, med hela transkriptet. Arkivet fylls bara på.",
           "cols": "| Datum | Möte | Längd | Fireflies | Transkript | Sammanfattning |"},
}


def transcript_full(meeting_id):
    q = """query($id: String!) { transcript(id: $id) { id title date duration
             sentences { speaker_name text start_time } } }"""
    return graphql(q, {"id": meeting_id})["transcript"]


def local_span(rs):
    """Start och slut för en lokal inspelning: starten i huvudet, längden ur slutradens duration, annars
    dess klockslag, annars den sista repliken. None om huvudet saknar tid."""
    head = next((r for r in rs if r.get("event") in ("joined", "rejoined") and r.get("at")), None)
    if not head:
        return None
    start = datetime.fromisoformat(head["at"])
    end = next((r for r in rs if r.get("event") == "ended"), {})
    if end.get("duration"):
        secs = float(end["duration"])
    elif end.get("at") and end["at"] > head["at"]:
        secs = (datetime.fromisoformat(end["at"]) - start).total_seconds()
    else:
        secs = max((float(r.get("start") or 0) for r in rs if "text" in r), default=0.0)
    return start, start + timedelta(seconds=secs)


def cmd_archive():
    files = [Path(a) for a in sys.argv[2:] if a.endswith(".jsonl")]
    if not files:
        print("Ange mötesfilerna: python live.py archive <fil.jsonl> [<fil.jsonl> …] [--out communication/meetings] [--lang sv]")
        sys.exit(1)
    out = Path(arg("--out", "communication/meetings"))
    L = LABELS.get(arg("--lang", "en"), LABELS["en"])
    rows = {f: read_rows(f) for f in files}
    heads = [r for rs in rows.values() for r in rs if r.get("event") in ("joined", "rejoined")]
    mid_of = {f: next((r["meeting_id"] for r in rs if r.get("meeting_id")), None) for f, rs in rows.items()}
    meeting_ids = list(dict.fromkeys(m for m in mid_of.values() if m))
    title = arg("--title") or next((r["title"] for r in heads if r.get("meeting_id")), None) or (heads[0]["title"] if heads else "Meeting")
    ats = sorted(r["at"] for rs in rows.values() for r in rs if r.get("at"))
    # En lokal inspelning: start i huvudet, längd i slutraden. final.jsonl från refine.py hade förut ingen sluttid,
    # så huvudet blev "11:08–11:08" och längden tom.
    recs = [s for s in (local_span(rs) for f, rs in rows.items() if not mid_of[f]) if s]
    ats = sorted(ats + [t.isoformat(timespec="seconds") for s in recs for t in s])
    day = ats[0][:10] if ats else datetime.now().strftime("%Y-%m-%d")
    span = f"{ats[0][11:16]}–{ats[-1][11:16]}" if ats else ""

    parts, minutes = [], 0
    for mid in meeting_ids:
        lines, source = None, L["live"]
        if "--no-fetch" not in sys.argv:
            try:
                t = transcript_full(mid)
                lines = [(s.get("start_time"), s.get("speaker_name"), s.get("text")) for s in t.get("sentences") or []]
                source = L["final"]
                minutes += round(float(t.get("duration") or 0))
            except Exception as e:
                print(f"Kunde inte hämta det färdiga transkriptet för {mid} ({e}). Använder liveutskriften.")
        if not lines:
            # Liveutskriften från alla filer för mötet, utan dubbletter från nya anslutningar.
            seen, kept = {}, []
            for f in files:
                if mid_of[f] != mid:
                    continue
                for r in rows[f]:
                    if "text" not in r:
                        continue
                    key, st = norm(r["text"]), float(r.get("start") or 0)
                    if key and not any(abs(st - s) < 15 for s in seen.get(key, [])):
                        seen.setdefault(key, []).append(st)
                        kept.append((st, r.get("speaker"), r["text"]))
            lines = sorted(kept, key=lambda x: x[0])
        parts.append((f"Fireflies `{mid}`", source, lines))
    for f in files:
        if not mid_of[f]:
            local = [(r.get("start"), r.get("speaker"), r["text"]) for r in rows[f] if "text" in r]
            head = next((r.get("title") for r in rows[f] if r.get("title")), L["local"])
            parts.append((head, L["local"], local))
    if not minutes and recs:
        minutes = round((max(e for _, e in recs) - min(s for s, _ in recs)).total_seconds() / 60)

    speakers = sorted({s for _, _, ls in parts for _, s, _ in ls if s})
    name = f"{day}-{slug(title)}.md"
    # --out är mappen. Ett filnamn på .md gav förut en mapp med det namnet och ett register bredvid den
    # (<fil>.md.md); nu blir det utskriftens namn i den mappen.
    if out.suffix == ".md":
        out, name = out.parent, out.name
    doc = [f"# {title}, {day}", ""]
    doc.append(" · ".join(x for x in (span, f"{L['speakers']}: {', '.join(speakers)}" if speakers else "",
                                      ", ".join(f"Fireflies `{m}`" for m in meeting_ids)) if x))
    media = arg("--media")
    if media:
        doc += ["", f"Media: `{media}`"]
    doc += ["", L["note"], "", "---", ""]
    for i, (head, source, lines) in enumerate(parts, 1):
        if len(parts) > 1:
            doc += [f"## {L['part']} {i}: {head} ({source})", ""]
        else:
            doc += [f"_{source}_", ""]
        doc += [f"[{clock(st)}] {sp or '?'}: {tx}" for st, sp, tx in lines] + [""]
    out.mkdir(parents=True, exist_ok=True)
    (out / name).write_text("\n".join(doc), encoding="utf-8", newline="\n")
    print(f"Arkiverat: {out / name} ({sum(len(l) for _, _, l in parts)} repliker, {len(parts)} del(ar))")

    index = out.parent / f"{out.name}.md"
    if not index.exists():
        index.write_text(f"# {L['index_title']}\n\n{L['index_intro']}\n\n{L['cols']}\n|---|---|---|---|---|---|\n",
                         encoding="utf-8", newline="\n")
    text = index.read_text(encoding="utf-8")
    if name not in text:
        length = f"{minutes} min" if minutes else ""
        ids = " ".join(f"`{m}`" for m in meeting_ids) or (f"media: `{media}`" if media else "")
        row = f"| {day} | {title} | {length} | {ids} | [{name}]({out.name}/{name}) |  |"
        index.write_text(text.rstrip("\n") + "\n" + row + "\n", encoding="utf-8", newline="\n")
        print(f"Ny rad i {index}. Fyll i sammanfattningen när den är skriven.")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    {"list": cmd_list, "join": cmd_join, "watch": cmd_watch, "transcript": cmd_transcript, "archive": cmd_archive}.get(cmd, lambda: print(__doc__))()
