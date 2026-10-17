"""auth feature: PLAN (rendered into Test_auth.md), SCREENS (for the standards suite), shared helpers.

Throwaway QA accounts live on the LOCAL dev database only. The run password is generated once per machine into
~/.cache/irbis-qa/auth_pw (never committed, never printed); QA usernames are `qa_<case>_<n>`."""
import json
import os
import re
import secrets
import subprocess
import time
import urllib.error
import urllib.request

from drv import PKG, back, deep_link, find, has, keyboard_shown, nodes, relaunch, sh, tap, type_text, wait, wait_any, wait_gone  # noqa: F401

from config import DOCS  # noqa: E402

API = "http://localhost:3000"
API_LOG = os.environ.get("QA_API_LOG", "/private/tmp/claude-501/-Users-sardor-work-irbis-irbis-docs/ad52b833-b574-44a3-88df-2262ff5f2f40/scratchpad/api-qa.log")
CACHE_DIR = os.path.expanduser("~/.cache/irbis-qa")


def _cached(name, make):
    os.makedirs(CACHE_DIR, exist_ok=True)
    p = os.path.join(CACHE_DIR, name)
    if not os.path.exists(p):
        open(p, "w").write(make())
        os.chmod(p, 0o600)
    return open(p).read().strip()


PW = _cached("auth_pw", lambda: "Qa" + secrets.token_hex(5))        # 12 chars, throwaway local password
PW2 = _cached("auth_pw2", lambda: "Qb" + secrets.token_hex(5))      # second password (reset / change cases)
PW6 = PW[:6]                                                        # exactly 6 characters
PHONE_DIGITS = "9000000"                                           # + two case digits → +998 90 000 00 xx


def uname(tag):
    return f"qa_{tag}_{int(time.time()) % 10**7}"


# ---------------- API / DB / log helpers (Mac side) ----------------
def api(method, path, body=None, token=None):
    """(status, json, headers) — body/response never printed by callers."""
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header("content-type", "application/json")
    if token:
        req.add_header("authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else {}), dict(r.headers)
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw or b"{}"), dict(e.headers)
        except ValueError:
            return e.code, {}, dict(e.headers)


def sql(q):
    """Run SQL on the LOCAL dev database (credentials stay inside the container). Returns stdout."""
    r = subprocess.run(["docker", "exec", "irbis-api-db-1", "sh", "-c",
                        'psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -At -c "$1"', "_", q],
                       capture_output=True, text=True)
    return r.stdout.strip()


def before_case():
    """Called by runcase.py before every case: clear the log-in failure history on the LOCAL dev DB, so one case's
    wrong passwords (per-username lockout, per-IP limit — all cases share the emulator's IP) never block the next."""
    sql("delete from login_attempts")


def user_id(username):
    return sql(f"select id from users where username='{username}'")


def sms_codes(uid):
    """All fake-SMS codes the API logged for this user id, oldest first (read from the dev log; never printed)."""
    out = []
    try:
        for line in open(API_LOG, errors="replace"):
            m = re.search(r"SMS code for user ([0-9a-f-]{36}): (\d{6})", line)
            if m and m.group(1) == uid:
                out.append(m.group(2))
    except OSError:
        pass
    return out


def wait_new_code(uid, before, timeout=10):
    """The code logged after `before` earlier ones (a count), or None."""
    end = time.time() + timeout
    while time.time() < end:
        codes = sms_codes(uid)
        if len(codes) > before:
            return codes[-1]
        time.sleep(0.3)
    return None


def make_user(tag, password=None, phone=None, verified=False):
    """Create a throwaway account through the API. Returns dict(username, id, access, refresh)."""
    name = uname(tag)
    body = {"username": name, "password": password or PW, "locale": "en", "acceptTerms": True}
    if phone:
        body["recoveryPhone"] = phone
    st, d, _ = api("POST", "/v1/auth/sign-up", body)
    if st != 201:
        raise RuntimeError(f"make_user {tag}: sign-up returned {st} {d.get('code')}")
    u = {"username": name, "id": d["me"]["id"], "access": d["accessToken"], "refresh": d["refreshToken"]}
    if phone and verified:
        code = wait_new_code(u["id"], 0)
        st, _, _ = api("POST", "/v1/me/recovery-phone/verify", {"code": code}, u["access"])
        if st != 200:
            raise RuntimeError(f"make_user {tag}: verify returned {st}")
    return u


def phone_digits(n=11):
    return f"{PHONE_DIGITS}{n % 100:02d}"


def phone(n=11):
    """Full +998 number for API bodies (the UI field takes phone_digits)."""
    return "+998" + phone_digits(n)


# ---------------- device helpers ----------------
def hide_kb():
    if keyboard_shown():
        back()
        time.sleep(0.4)


def clear_field(tid):
    tap(tid, exact=True)
    sh("input", "keyevent", "123")
    sh("input", "keyevent", *(["67"] * 70))


def fill(tid, text, clear=False):
    if not find(tid, exact=True):
        hide_kb()
        for _ in range(3):
            sh("input", "swipe", "540", "1700", "540", "900", "300")
            time.sleep(0.6)
            if find(tid, exact=True):
                break
    if clear:
        clear_field(tid)
    else:
        tap(tid, exact=True)
    time.sleep(0.2)
    type_text(text)
    time.sleep(0.2)


def texts():
    return [n["text"] for n in nodes() if n["text"]]


def field_text(tid):
    n = find(tid, exact=True)
    return n["text"] if n else None


def tap_submit():
    hide_kb()
    if not find("auth.submit", exact=True):
        sh("input", "swipe", "540", "1700", "540", "900", "300")
        time.sleep(0.6)
    tap("auth.submit", exact=True)


def launch_app():
    relaunch()
    return wait("nav.tab-profile", 20, exact=True)


def goto_profile():
    tap("nav.tab-profile", exact=True)
    return wait_any(["profile.guest", "profile.account", "profile.account-loading"], 15)


def sign_out_ui():
    if wait("profile.account", 10, exact=True):
        tap("profile.sign-out", exact=True)
        return wait("profile.guest", 10, exact=True)
    return True


def ensure_guest():
    """Cold start, Profile tab, sign out through the app if an account is signed in. True when guest Profile shows."""
    if not launch_app():
        return False
    where = goto_profile()
    if where and where != "profile.guest":
        wait("profile.sign-out", 15, exact=True)
        tap("profile.sign-out", exact=True)
        return wait("profile.guest", 10, exact=True)
    return where == "profile.guest"


def open_login():
    ok = ensure_guest()
    if ok:
        tap("profile.guest-login", exact=True)
        ok = wait("auth.login", 10, exact=True)
    return ok


def open_signup():
    ok = ensure_guest()
    if ok:
        tap("profile.guest-signup", exact=True)
        ok = wait("auth.signup", 10, exact=True)
    return ok


def open_forgot():
    ok = open_login()
    if ok:
        tap("auth.forgot-link", exact=True)
        ok = wait("auth.forgot", 10, exact=True)
    return ok


def ui_login(username, password, expect="profile.account"):
    """On the log-in screen: fill, submit, wait for `expect`."""
    fill("auth.username", username)
    fill("auth.password", password)
    tap_submit()
    return wait(expect, 15, exact=True)


def ui_login_from_guest(username, password):
    ok = open_login()
    return ok and ui_login(username, password)


def ui_signup(username, password, phone_d=None, terms=True):
    fill("auth.username", username)
    time.sleep(1.5)  # live availability check settles (text is localised, so wait by time)
    fill("auth.password", password)
    if phone_d:
        fill("auth.phone", phone_d)
    hide_kb()
    if terms:
        tap("auth.terms", exact=True)
    tap_submit()


def open_debug():
    launch_app()
    goto_profile()
    if not find("profile.debug", exact=True):
        sh("input", "swipe", "540", "1700", "540", "900", "300")
    tap("profile.debug", exact=True)
    return wait("debug.screen", 15, exact=True)


def open_signed_in(u, password=None):
    """Guest state → logged in as u through the app UI (u from make_user)."""
    return ui_login_from_guest(u["username"], password or PW)


def std_account():
    """One throwaway account for the signed-in-profile standards screen (created once, name cached)."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    p = os.path.join(CACHE_DIR, "auth_std_user")
    if os.path.exists(p):
        name = open(p).read().strip()
        if user_id(name):
            return name
    u = make_user("std")
    open(p, "w").write(u["username"])
    return u["username"]


PLAN = {
    "spec": "features/auth.md",
    "resources": [("Android", "emulator pixel-8a emulating the S25 Ultra (session.py up); devRelease APK uz.irbis.app.dev"),
                  ("Backend", "irbis-api `npm run start:dev` on :3000, log in a file; Postgres container `irbis-api-db-1`; "
                              "`adb reverse tcp:3000 tcp:3000`; fake SMS sender logs `SMS code for user <id>: <code>`"),
                  ("Isolation", "`before_case()` clears `login_attempts` before every case, so lockouts and the per-IP limit "
                                "never carry over; every case makes its own `qa_<case>_<n>` user"),
                  ("Covered elsewhere", "AC12 – AC16 (web admin, admin API, CLI): irbis-web and irbis-api repo tests — no device cases"),
                  ("Timers (not on the device)", "lock expiry after 15 min, per-IP limit, Send again unlock at 60 s, silent refresh "
                                                 "after the ~15-min access token: irbis-api auth.rules.spec.ts + auth-session.e2e-spec.ts, "
                                                 "irbis-app reset.test.tsx + session.test.tsx (fake clock)")],
    "test_data": [("QA-USER", "throwaway account `qa_<case>_<n>`, password generated per machine (not committed)",
                   "created through the API (`make_user`) on the LOCAL dev DB only"),
                  ("QA-PHONE", "synthetic recovery phone +998 90 000 00 xx", "sign-up / recovery-phone body"),
                  ("QA-VERIFIED", "QA-USER with a verified recovery phone",
                   "sign-up with phone + `/v1/me/recovery-phone/verify` with the code from the API log"),
                  ("QA-BLOCKED", "QA-USER with blocked_at + block_reason_code set",
                   "`update users set blocked_at=now(), block_reason_code='spam'` on the local dev DB"),
                  ("SMS-LOG", "dev-only FakeSmsSender line in the API log", "read by the script, never printed")],
}


def _open_gate():
    if not open_debug():
        return False
    tap("debug.open-gate", exact=True)
    return wait("auth.gate", 10, exact=True)


SCREENS = {
    "login": {"open": lambda c=None: open_login(), "root": "auth.login"},
    "signup": {"open": lambda c=None: open_signup(), "root": "auth.signup"},
    "forgot": {"open": lambda c=None: open_forgot(), "root": "auth.forgot"},
    "guest-profile": {"open": lambda c=None: ensure_guest(), "root": "profile.guest"},
    "gate": {"open": lambda c=None: _open_gate(), "root": "auth.gate"},
    "account-profile": {"open": lambda c=None: ui_login_from_guest(std_account(), PW), "root": "profile.account"},
}
