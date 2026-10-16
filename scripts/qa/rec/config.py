"""QA config shared by every script: irbis-docs/qa/qa.config.json, overridable by environment variables.

  package      Android applicationId of the build under test          (QA_PKG)
  activity     launch activity, relative to the package                 (QA_ACTIVITY)
  event_tag    prefix of the app's dev/staging QA event log lines       (QA_EVENT_TAG)
  location_event  event the app emits when it reads a location fix      (QA_LOCATION_EVENT)
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))          # irbis-docs
QA_ROOT = os.path.join(DOCS, "qa")
CACHE = os.path.expanduser("~/.cache/irbis-qa")
VENV_PY = os.path.expanduser("~/.claude/venvs/qa/bin/python")
os.makedirs(CACHE, exist_ok=True)

_DEFAULTS = {"package": "com.irbis", "activity": ".MainActivity", "event_tag": "IRBIS_QA",
             "location_event": "location_received"}


def load():
    cfg = dict(_DEFAULTS)
    path = os.path.join(QA_ROOT, "qa.config.json")
    if os.path.exists(path):
        cfg.update(json.load(open(path, encoding="utf-8")))
    for key, env in (("package", "QA_PKG"), ("activity", "QA_ACTIVITY"), ("event_tag", "QA_EVENT_TAG"),
                     ("location_event", "QA_LOCATION_EVENT")):
        if os.environ.get(env):
            cfg[key] = os.environ[env]
    return cfg


CFG = load()
