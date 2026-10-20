#!/usr/bin/env python3
"""Campfire bot players for QA (stdlib only).

One daemon runs many bots; each bot is a TCP client of the host phone's Campfire room
(NDJSON, port 47821). Every message a bot receives or sends is appended to <log-dir>/<name>.jsonl.

  python3 campbot.py serve --code 1234 --v 5 --log-dir runs/x/bots   # daemon (foreground)
  python3 campbot.py ctl add bot_1 fox            # connect + hello (+ ping every 3 s)
  python3 campbot.py ctl send bot_1 '{"type":"mafReady","round":1}'   # `v` is stamped unless given
  python3 campbot.py ctl raw bot_1 '{"v":3,"type":"ping"}'            # exact line, no stamping
  python3 campbot.py ctl mute bot_1               # stop pinging, socket stays open (silent drop)
  python3 campbot.py ctl drop bot_1               # close the socket without `leave`
  python3 campbot.py ctl reconnect bot_1          # new socket, hello with the stored seatToken
  python3 campbot.py ctl leave bot_1              # send `leave`
  python3 campbot.py ctl last bot_1 game          # last received message of a type
  python3 campbot.py ctl types bot_1              # counts of received message types
  python3 campbot.py ctl list                     # every bot: seatId, connected, pinging
  python3 campbot.py ctl code 5678                # room code for later hellos
  python3 campbot.py ctl probe                    # discovery probe with the current code
Synthetic names only (bot_1, guest_1 ...).
"""
import argparse
import json
import os
import socket
import socketserver
import sys
import threading
import time

CTL_PORT = 47900


class Bot:
    def __init__(self, farm, name, avatar):
        self.farm = farm
        self.name = name
        self.avatar = avatar
        self.sock = None
        self.seat_id = None
        self.seat_token = None
        self.pinging = False
        self.connected = False
        self.last = {}
        self.counts = {}
        self.lock = threading.Lock()
        self.log_path = os.path.join(farm.log_dir, f"{name}.jsonl")

    def log(self, direction, msg):
        rec = {"t": round(time.time(), 3), "dir": direction, "msg": msg}
        with open(self.log_path, "a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def connect(self, use_token):
        self.close()
        s = socket.create_connection((self.farm.host, self.farm.port), timeout=5)
        s.settimeout(None)
        self.sock = s
        self.connected = True
        self.pinging = True
        threading.Thread(target=self._reader, args=(s,), daemon=True).start()
        hello = {"type": "hello", "code": self.farm.code, "nickname": self.name, "avatar": self.avatar}
        if use_token and self.seat_token:
            hello["seatToken"] = self.seat_token
        self.send(hello)

    def _reader(self, s):
        buf = b""
        while True:
            try:
                chunk = s.recv(65536)
            except OSError:
                break
            if not chunk:
                break
            buf += chunk
            while b"\n" in buf:
                line, buf = buf.split(b"\n", 1)
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except ValueError:
                    self.log("in-raw", line.decode("utf8", "replace"))
                    continue
                t = msg.get("type", "?")
                if t != "pong":
                    self.log("in", msg)
                with self.lock:
                    self.last[t] = msg
                    self.counts[t] = self.counts.get(t, 0) + 1
                if t == "welcome":
                    self.seat_id = msg.get("seatId")
                    self.seat_token = msg.get("seatToken")
        if self.sock is s:
            self.connected = False
            self.pinging = False
            self.log("event", {"closed": True})

    def send(self, msg, stamp=True):
        if stamp and "v" not in msg:
            msg = {"v": self.farm.v, **msg}
        self.send_raw(json.dumps(msg))
        if msg.get("type") != "ping":
            self.log("out", msg)

    def send_raw(self, line):
        if not self.sock:
            raise RuntimeError("not connected")
        self.sock.sendall((line + "\n").encode("utf8"))

    def close(self):
        s, self.sock = self.sock, None
        self.connected = False
        self.pinging = False
        if s:
            try:
                s.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            s.close()


class Farm:
    def __init__(self, host, port, code, v, log_dir):
        self.host, self.port, self.code, self.v, self.log_dir = host, port, code, v, log_dir
        self.bots = {}
        os.makedirs(log_dir, exist_ok=True)
        threading.Thread(target=self._pinger, daemon=True).start()

    def _pinger(self):
        while True:
            time.sleep(3)
            for bot in list(self.bots.values()):
                if bot.pinging and bot.sock:
                    try:
                        bot.send({"type": "ping"})
                    except OSError:
                        bot.pinging = False

    def handle(self, args):
        cmd, rest = args[0], args[1:]
        if cmd == "code":
            self.code = rest[0]
            return {"ok": True, "code": self.code}
        if cmd == "list":
            return {b.name: {"seatId": b.seat_id, "connected": b.connected, "pinging": b.pinging}
                    for b in self.bots.values()}
        if cmd == "probe":
            s = socket.create_connection((self.host, self.port), timeout=3)
            s.sendall((json.dumps({"v": self.v, "type": "probe", "code": rest[0] if rest else self.code}) + "\n").encode())
            s.settimeout(3)
            data = s.recv(4096)
            s.close()
            return {"ok": True, "reply": data.decode().strip()}
        name = rest[0]
        if cmd == "add":
            bot = Bot(self, name, rest[1] if len(rest) > 1 else "fox")
            self.bots[name] = bot
            bot.connect(use_token=False)
            time.sleep(0.6)
            return {"ok": True, "seatId": bot.seat_id, "last": list(bot.counts)}
        bot = self.bots[name]
        if cmd == "send":
            bot.send(json.loads(rest[1]))
        elif cmd == "raw":
            bot.send_raw(rest[1])
            bot.log("out-raw", rest[1])
        elif cmd == "mute":
            bot.pinging = False
        elif cmd == "unmute":
            bot.pinging = True
        elif cmd == "drop":
            bot.close()
        elif cmd == "reconnect":
            bot.connect(use_token=True)
            time.sleep(0.6)
        elif cmd == "fresh":
            bot.connect(use_token=False)
            time.sleep(0.6)
        elif cmd == "leave":
            bot.send({"type": "leave"})
        elif cmd == "last":
            with bot.lock:
                return {"ok": True, "msg": bot.last.get(rest[1])}
        elif cmd == "types":
            with bot.lock:
                return {"ok": True, "counts": dict(bot.counts), "seatId": bot.seat_id,
                        "connected": bot.connected}
        else:
            return {"ok": False, "error": f"unknown {cmd}"}
        return {"ok": True, "seatId": bot.seat_id, "connected": bot.connected}


def serve(a):
    farm = Farm(a.host, a.port, a.code, a.v, a.log_dir)

    class H(socketserver.StreamRequestHandler):
        def handle(self):
            try:
                args = json.loads(self.rfile.readline())
                out = farm.handle(args)
            except Exception as e:  # report every control error back to the caller
                out = {"ok": False, "error": repr(e)}
            self.wfile.write((json.dumps(out, ensure_ascii=False) + "\n").encode())

    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("127.0.0.1", a.ctl), H) as srv:
        print(f"campbot ctl on 127.0.0.1:{a.ctl}, room {a.host}:{a.port} v{a.v}", flush=True)
        srv.serve_forever()


def ctl(args, port):
    s = socket.create_connection(("127.0.0.1", port), timeout=15)
    s.sendall((json.dumps(args) + "\n").encode())
    data = b""
    while not data.endswith(b"\n"):
        chunk = s.recv(65536)
        if not chunk:
            break
        data += chunk
    print(data.decode().strip())


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "ctl":
        ctl(sys.argv[2:], int(os.environ.get("CAMPBOT_CTL", CTL_PORT)))
        return
    p = argparse.ArgumentParser()
    p.add_argument("mode", choices=["serve"])
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=47821)
    p.add_argument("--code", default="0000")
    p.add_argument("--v", type=int, default=5)
    p.add_argument("--ctl", type=int, default=CTL_PORT)
    p.add_argument("--log-dir", default="bots")
    serve(p.parse_args())


if __name__ == "__main__":
    main()
