#!/usr/bin/env python3
"""Repository checks that the plugin directory, the Copilot listing and the release job depend on.
Stdlib only. Run from anywhere:

  python tests/test_repo.py

The Claude plugin directory listing has auto-publish on and picks master up on its scheduled check,
so a manifest mismatch or an over-long description has to fail here first.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = ROOT / "skills" / "obsidian-notes"
FAILS = []


def check(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        FAILS.append(name)


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    out = {}
    for line in (m.group(1).splitlines() if m else []):
        k, _, v = line.partition(":")
        v = v.strip()
        if len(v) >= 2 and v[0] == v[-1] == '"':
            v = json.loads(v)  # the description is a JSON-style double-quoted string
        out[k.strip()] = v
    return out, text


def main():
    claude = load(".claude-plugin/plugin.json")
    root = load("plugin.json")
    market = load(".claude-plugin/marketplace.json")
    version = claude.get("version", "")

    check("plugin.json versions agree (.claude-plugin and root)", version == root.get("version"), (version, root.get("version")))
    check("version is semantic", re.fullmatch(r"\d+\.\d+\.\d+", version or "") is not None, version)
    check("plugin names agree", claude["name"] == root["name"] == market["plugins"][0]["name"] == "obsidian-notes")
    check("marketplace source is the repo root", market["plugins"][0].get("source") == "./")
    for key in ("description", "license", "repository", "homepage"):
        check(f"plugin.json has {key}", bool(claude.get(key)))
    for key in ("documentationUrl", "supportUrl", "privacyPolicyUrl"):
        check(f"directory field {key} is https", str(claude.get(key, "")).startswith("https://"), claude.get(key))
    icon = ROOT / ".claude-plugin" / "icon.png"
    check("directory icon present and a PNG", icon.exists() and icon.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n")

    fm, body = frontmatter(SKILL_DIR / "SKILL.md")
    desc = fm.get("description", "")
    check("SKILL.md name matches its folder", fm.get("name") == SKILL_DIR.name, fm.get("name"))
    check("SKILL.md description within the 1,024-character spec cap", 0 < len(desc) <= 1024, len(desc))
    check("SKILL.md description says when to use it", "Use whenever" in desc)
    # Body budget: the worth study measured about 2,000 tokens after the 2026-10-01 trim; keep it there.
    words = len(body.split())
    check("SKILL.md body stays under 1,800 words", words < 1800, words)

    changelog = (SKILL_DIR / "CHANGELOG.md").read_text(encoding="utf-8")
    check(f"CHANGELOG mentions version {version}", version in changelog)

    state = json.loads((SKILL_DIR / "evergreen.json").read_text(encoding="utf-8"))
    check("evergreen.json names the skill", state.get("name") == "obsidian-notes")
    check("evergreen.json next_due is after last_checked", state.get("next_due", "") > state.get("last_checked", ""))
    evals = json.loads((SKILL_DIR / "evals" / "evals.json").read_text(encoding="utf-8"))
    cases = evals.get("evals", evals.get("cases", []))
    check("evals.json parses and has cases", isinstance(cases, list) and len(cases) > 0)

    for script in ("vault_lint.py", "test_vault_lint.py"):
        src = (SKILL_DIR / "scripts" / script).read_bytes()
        check(f"{script} uses LF line endings", b"\r\n" not in src)
        imports = set(re.findall(rb"^(?:import|from) (\w+)", src, re.M))
        third_party = {i.decode() for i in imports} - set(sys.stdlib_module_names if hasattr(sys, "stdlib_module_names") else []) - {"__future__"}
        check(f"{script} imports the standard library only", not third_party or not hasattr(sys, "stdlib_module_names"), third_party)

    p = subprocess.run([sys.executable, str(SKILL_DIR / "scripts" / "vault_lint.py"), "--help"], capture_output=True, text=True)
    check("vault_lint.py --help runs", p.returncode == 0 and "--fix-index" in p.stdout, p.stderr[-200:])

    if FAILS:
        print(f"\n{len(FAILS)} check(s) failed: " + ", ".join(FAILS))
        sys.exit(1)
    print("\nall checks passed")


if __name__ == "__main__":
    main()
