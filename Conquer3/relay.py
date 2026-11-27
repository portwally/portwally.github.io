#!/usr/bin/env python3
"""The relay for Conquer 3: Sandstorm's network games: two Apple IIgs that
cannot call each other both call out to this, and it passes each one's
bytes to the other. It needs Python 3 and nothing else.

  python3 relay.py [port] [--log FILE]

The port is 6502 if none is given. Players type this computer's name or
address and the port into SETTINGS' RELAY, "name:port". For players
outside your own network, the port must be reachable from the Internet:
forward it (TCP) in your router to this computer, and let it through
this computer's firewall. Ctrl-C stops it.

How it works: a machine connects and sends one line - HOST (the answer:
"CODE xxxx", four letters, for the host to tell the other player) or
JOIN xxxx (a code nobody hosts: "NO"). When the second has joined, both
get "GO", and from then on every byte of the one goes to the other. One
hanging up closes the other's line, what is on its way sent first.

Its limits, for a relay anyone can reach: a machine must say HOST or JOIN
within 30 seconds, in 64 bytes; a host waits 30 minutes for the other
player; a game whose line has been silent for 10 minutes is closed (the
game sends something twice a second, even paused); a machine that takes
nothing it is sent for a minute is closed; 512 lines at most, 16 from
one address (but any number from this computer itself).

For the tests (tools/locktest.sh and others), not for players:
  --lag MS   holds every byte back that many milliseconds (a slow line)
  --keep     one hanging up leaves the other's line open, what it sends
             going nowhere (two emulators never stop at the same moment)
  --wait     a JOIN before its HOST waits for it
  "HOST xxxx" asks for that code ("NO" if it is taken).
  RELAYDUMP=1 in the environment: the last bytes of everything passed on
  into the log as well."""
import os, random, selectors, socket, sys, time

HELLO_SECS, HELLO_BYTES = 30, 64        # (the limits above)
HOST_SECS = 30 * 60
QUIET_SECS = 10 * 60
STUCK_SECS, OUT_MAX = 60, 1 << 20       # (nothing taken for so long; so much waiting)
MAX_LINES, PER_ADDR = 512, 16
BYE_SECS = 2                            # (a line being closed: so long for its last bytes)

args = sys.argv[1:]
if "-h" in args or "--help" in args:
    print(__doc__)
    sys.exit(0)
lag = 0.0
log = None
if "--lag" in args:
    i = args.index("--lag"); lag = float(args[i + 1]) / 1000; del args[i:i + 2]
keep = "--keep" in args
if keep:
    args.remove("--keep")
dump = os.environ.get("RELAYDUMP")
joinwait = "--wait" in args
if joinwait:
    args.remove("--wait")
if "--log" in args:
    i = args.index("--log"); log = open(args[i + 1], "a", buffering=1); del args[i:i + 2]
port = int(args[0]) if args else 6502

def say(s):
    if log:
        log.write("%.3f %s\n" % (time.time(), s))

class Line:
    def __init__(self, sock, addr):
        self.sock, self.addr = sock, addr
        self.buf, self.peer, self.code = b"", None, None
        self.queue = []                 # (when, bytes) on their way to us (--lag)
        self.out = bytearray()          # what the socket has not taken yet
        self.passed = 0
        self.alone = False              # (--keep: the other has hung up)
        self.born = self.heard = self.moved = time.time()
        self.bye = None                 # being closed: until when
        self.shut = False               # (its end said: FIN sent)
        self.events = selectors.EVENT_READ

sel = selectors.DefaultSelector()
srv = socket.socket()
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("0.0.0.0", port))
srv.listen(16)
srv.setblocking(False)
sel.register(srv, selectors.EVENT_READ, None)
waiting = {}                            # code -> the host's line
joiners = {}                            # code -> a line that came to join it first
lines = []
say("listening on %d, lag %d ms" % (port, lag * 1000))
print("The relay listens on port %d. Ctrl-C stops it." % port, flush=True)

def watch(l):
    ev = selectors.EVENT_READ | (selectors.EVENT_WRITE if l.out else 0)
    if ev != l.events:
        l.events = ev
        sel.modify(l.sock, ev, l)

def flush(l):
    """As much of what waits for l as its socket takes now."""
    while l.out:
        try:
            n = l.sock.send(l.out)
        except (BlockingIOError, InterruptedError):
            break
        except OSError:
            close(l)
            return
        del l.out[:n]
        l.moved = time.time()
    if l not in lines:
        return
    if l.bye and not l.out and not l.shut:
        l.shut = True                   # (all sent: the end of what it gets)
        try:
            l.sock.shutdown(socket.SHUT_WR)
        except OSError:
            pass
    watch(l)

def send(l, data):
    if l not in lines or l.bye:
        return
    if not l.out:
        l.moved = time.time()
    l.out += data
    if len(l.out) > OUT_MAX:
        say("closed: takes nothing (%s)" % l.addr)
        close(l)
        return
    flush(l)

def finish(p):
    """p's partner is gone, or p is refused: what is on its way to it sent,
    then the end of what it gets said (FIN), and what it still sends read
    and dropped (BYE_SECS at most) - closed with unread bytes, the socket
    would be reset, and a reset can lose those last bytes on their way to
    it (the partner's word that it leaves)."""
    for _, data in p.queue:
        p.out += data
    p.queue = []
    p.bye = time.time() + BYE_SECS
    flush(p)

def close(l):
    if l not in lines:
        return
    lines.remove(l)
    say("closed (%d bytes passed on from it)" % l.passed)
    try:
        sel.unregister(l.sock)
    except Exception:
        pass
    l.sock.close()
    if l.code in waiting and waiting[l.code] is l:
        del waiting[l.code]
    if l.code in joiners and joiners[l.code] is l:
        del joiners[l.code]
    if l.peer:
        p, l.peer = l.peer, None
        p.peer = None
        if keep:
            p.alone = True
        else:
            finish(p)

def refuse(l, line):
    say("refused: %r" % line)
    send(l, b"NO\n")
    finish(l)

def pair(h, l):
    l.peer, h.peer = h, l
    h.heard = l.heard = time.time()
    send(h, b"GO\n")
    send(l, b"GO\n")
    say("joined: " + h.code)

def command(l, line):
    word = line.split()
    want = word[1].decode(errors="replace").upper() if len(word) > 1 else None
    if word[:1] == [b"HOST"] and (want is None or (len(want) == 4 and want not in waiting)):
        code = want
        while code is None or code in waiting:
            code = "".join(random.choice("ABCDEFGHJKLMNPRSTUVWXYZ") for _ in range(4))
        l.code = code
        l.born = time.time()            # (from now: a host waiting)
        send(l, b"CODE " + code.encode() + b"\n")
        say("host: code " + code)
        if code in joiners:
            pair(l, joiners.pop(code))
        else:
            waiting[code] = l
    elif word[:1] == [b"JOIN"] and want in waiting:
        l.code = want
        pair(waiting.pop(want), l)
    elif word[:1] == [b"JOIN"] and joinwait and want and len(want) == 4 and want not in joiners:
        l.code = want
        l.born = time.time()
        joiners[want] = l
        say("join waits: " + want)
    else:
        refuse(l, line)

def accept():
    try:
        c, a = srv.accept()
    except OSError:
        return
    here = a[0].startswith("127.")
    if len(lines) >= MAX_LINES or (not here and sum(l.addr == a[0] for l in lines) >= PER_ADDR):
        say("too many: %s" % a[0])
        c.close()
        return
    c.setblocking(False)
    c.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    l = Line(c, a[0])
    lines.append(l)
    sel.register(c, selectors.EVENT_READ, l)
    say("connect %s:%d" % a)

def heard(l):
    try:
        data = l.sock.recv(4096)
    except (BlockingIOError, InterruptedError):
        return
    except OSError:
        data = b""
    if not data:
        close(l)
        return
    l.heard = time.time()
    if l.bye or l.alone:
        return                          # (dropped)
    if l.peer is None:                  # (not joined yet: its one line)
        l.buf += data
        if l.code is None:
            if b"\n" in l.buf:
                line, l.buf = l.buf.split(b"\n", 1)
                command(l, line)
            elif len(l.buf) > HELLO_BYTES:
                refuse(l, l.buf[:HELLO_BYTES])
                return
        elif len(l.buf) > 4096:         # (a host sending much before anyone joined)
            refuse(l, b"(too much before GO)")
            return
        data, l.buf = (l.buf, b"") if l.peer else (b"", l.buf)
    if data and l.peer:
        l.peer.heard = l.heard          # (a game's line: heard from either end)
        if lag:
            l.peer.queue.append((time.time() + lag, data))
        else:
            send(l.peer, data)
        l.passed += len(data)
        if dump:
            say("%s -> %s" % (l.code or "?", data[-24:].hex()))

def limits(now):
    for l in list(lines):
        if l not in lines:
            continue
        if l.bye:
            if now > l.bye:
                close(l)
        elif l.out and now - l.moved > STUCK_SECS:
            say("closed: takes nothing (%s)" % l.addr)
            close(l)
        elif l.peer is None and l.code is None and now - l.born > HELLO_SECS:
            refuse(l, b"(nothing said)")
        elif l.peer is None and l.code is not None and not l.alone and now - l.born > HOST_SECS:
            say("waited too long: " + l.code)
            finish(l)
            if waiting.get(l.code) is l:
                del waiting[l.code]
            if joiners.get(l.code) is l:
                del joiners[l.code]
        elif l.peer and now - l.heard > QUIET_SECS:
            say("silent too long: " + str(l.code))
            close(l)

last = 0.0
try:
    while True:
        now = time.time()
        due = [l.queue[0][0] for l in lines if l.queue]
        for key, ev in sel.select(timeout=max(0, min(due) - now) if due else 1.0):
            if key.data is None:
                accept()
                continue
            l = key.data
            if l not in lines:
                continue
            if ev & selectors.EVENT_WRITE:
                flush(l)
            if ev & selectors.EVENT_READ and l in lines:
                heard(l)
        now = time.time()
        for l in list(lines):
            while l in lines and l.queue and l.queue[0][0] <= now:
                send(l, l.queue.pop(0)[1])
        if now - last >= 1.0:
            last = now
            limits(now)
except KeyboardInterrupt:
    print()
