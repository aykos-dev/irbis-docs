import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), *[".."] * 4, "scripts", "qa", "rec"))
from drv import *  # noqa
import re  # noqa
try:
    from _feature import *  # noqa
except ImportError:
    pass

META = {
 "title": "Tokens: ~15-min access, refresh rotates, reuse revokes the family, refresh stored hashed",
 "priority": "P0",
 "group": "Core",
 "requirement": "AC9 — token lifetimes, rotation, reuse, hashing",
 "env": "API (HTTP)",
 "precondition": [
  "API up",
  "QA-USER"
 ],
 "steps": [
  "Sign up; decode the access token's exp − iat",
  "Refresh with R1 → R2",
  "Refresh again with R1 (reuse)",
  "Refresh with R2",
  "Query the DB for the raw token"
 ],
 "expected": [
  "Access lifetime 900 s (exp − iat) and expiresIn 900 — API response",
  "Refresh with R1 returns a new pair with a different refresh token — API response",
  "Reusing R1 → 401 REFRESH_REUSED, then R2 is refused too (family revoked) — API response",
  "DB holds no row whose token_hash equals the raw refresh token — DB"
 ],
 "focus": "",
 "caption": {
  "expected": ""
 }
}


def run(c):
    import base64
    c.pre("API up")
    st, d, _ = api("POST", "/v1/auth/sign-up", {"username": uname("tok"), "password": PW, "locale": "en", "acceptTerms": True})
    c.checkpoint("sign-up", st == 201, st)
    r1, a1 = d["refreshToken"], d["accessToken"]
    seg = a1.split(".")[1]; seg += "=" * (-len(seg) % 4)
    claims = json.loads(base64.urlsafe_b64decode(seg))
    life = claims["exp"] - claims["iat"]
    c.result(1, life == 900 and d.get("expiresIn") == 900, f"exp-iat={life}, expiresIn={d.get('expiresIn')}")
    s2, d2, _ = api("POST", "/v1/auth/refresh", {"refreshToken": r1})
    r2 = d2.get("refreshToken")
    c.result(2, s2 == 200 and r2 and r2 != r1, f"refresh→{s2}, rotated={bool(r2 and r2 != r1)}")
    s3, d3, _ = api("POST", "/v1/auth/refresh", {"refreshToken": r1})
    s4, d4, _ = api("POST", "/v1/auth/refresh", {"refreshToken": r2})
    c.result(3, s3 == 401 and d3.get("code") == "REFRESH_REUSED" and s4 == 401, f"reuse→{s3} {d3.get('code')}, new token after reuse→{s4} {d4.get('code')}")
    raw = sql(f"select count(*) from refresh_tokens where token_hash in ('{r1}','{r2}')")
    c.result(4, raw == "0", f"rows matching the raw token: {raw}")
