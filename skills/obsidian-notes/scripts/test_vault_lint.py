#!/usr/bin/env python3
"""Self-test for vault_lint.py. Stdlib only; builds fixtures in a temp dir.

  python skills/obsidian-notes/scripts/test_vault_lint.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "vault_lint.py"
FIXTURE = HERE.parent / "evals" / "fixtures" / "vault"
FAILS = []


def run(*args, cwd=None):
    p = subprocess.run([sys.executable, str(SCRIPT), *map(str, args)], capture_output=True, text=True, cwd=cwd)
    return p.returncode, p.stdout + p.stderr


def scan_json(root, *extra):
    p = subprocess.run([sys.executable, str(SCRIPT), str(root), "--json", *map(str, extra)], capture_output=True, text=True)
    return p.returncode, json.loads(p.stdout)


def check(name, cond, detail=""):
    print(("ok   " if cond else "FAIL ") + name + (f"  ({detail})" if detail and not cond else ""))
    if not cond:
        FAILS.append(name)


def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def main():
    tmp = Path(tempfile.mkdtemp(prefix="vault-lint-test-"))
    try:
        # 1. The shipped fixture: known counts.
        v = tmp / "fixture"
        shutil.copytree(FIXTURE, v)
        code, d = scan_json(v)
        check("fixture exit code is 1 (errors present)", code == 1, code)
        check("fixture: one broken markdown link", len(d["broken_md_links"]) == 1, d["broken_md_links"])
        check("fixture: one ambiguous wikilink", len(d["ambiguous_wikilinks"]) == 1, d["ambiguous_wikilinks"])
        check("fixture: duplicate basename Beta.md", len(d["duplicate_basenames"]) == 1, d["duplicate_basenames"])
        check("fixture: two folders without an index", sorted(d["folders_without_index"]) == ["notes", "plans"], d["folders_without_index"])
        check("fixture: no frontmatter errors", d["frontmatter_errors"] == [], d["frontmatter_errors"])

        # 2. --fix-index writes indexes and links them from the parent.
        code, out = run(v, "--fix-index")
        check("fix-index wrote notes/INDEX.md", (v / "notes" / "INDEX.md").exists())
        check("fix-index wrote plans/INDEX.md", (v / "plans" / "INDEX.md").exists())
        readme = (v / "README.md").read_text(encoding="utf-8")
        check("fix-index linked the new indexes from README.md", "notes/INDEX.md" in readme and "plans/INDEX.md" in readme)
        code, d = scan_json(v)
        check("after fix-index: no folders without index", d["folders_without_index"] == [], d["folders_without_index"])
        check("after fix-index: no orphans", d["orphans"] == [], d["orphans"])
        check("after fix-index: INDEX.md is not a duplicate basename", all(x["basename"].lower() != "index.md" for x in d["duplicate_basenames"]))
        code, out = run(v, "--fix-index")
        check("fix-index is idempotent", "nothing" in out, out.strip().splitlines()[-1] if out.strip() else "")

        # 3. --to-markdown-links converts unambiguous wikilinks, keeps ambiguous ones and embeds, skips code.
        w = tmp / "wiki"
        write(w / "README.md", "# Root\n\nSee [[gamma]], [[gamma#Top|the top]], [[Beta]], ![[pic.png]] and `[[code]]`.\n\n```\n[[fenced]]\n```\n")
        write(w / "notes" / "gamma.md", "# Gamma\n")
        write(w / "notes" / "Beta.md", "# Beta\n")
        write(w / "plans" / "Beta.md", "# Beta plan\n")
        (w / "pic.png").write_bytes(b"\x89PNG\r\n")
        run(w, "--to-markdown-links")
        text = (w / "README.md").read_text(encoding="utf-8")
        check("wikilink converted to relative markdown link", "[gamma](notes/gamma.md)" in text, text)
        check("alias and anchor preserved", "[the top](notes/gamma.md#Top)" in text, text)
        check("ambiguous wikilink left alone", "[[Beta]]" in text, text)
        check("embed left alone", "![[pic.png]]" in text, text)
        check("inline code left alone", "`[[code]]`" in text, text)
        check("fenced code left alone", "\n[[fenced]]\n" in text, text)

        # 4. Link resolution rules: folder -> README.md, bare name -> .md, %20, anchors, external, code spans.
        r = tmp / "resolve"
        write(r / "README.md", "# Root\n\n[docs](docs) [bare](docs/two%20words) [enc](docs/two%20words.md#h) [ext](https://example.com) [anchor](#here) `[x](nope.md)` ![img](img.png)\n")
        write(r / "docs" / "README.md", "# Docs\n\nBack to [root](../README.md). [sib](two%20words.md)\n")
        write(r / "docs" / "two words.md", "# Two\n")
        (r / "img.png").write_bytes(b"\x89PNG\r\n")
        code, d = scan_json(r)
        check("resolution: no broken links", d["broken_md_links"] == [], d["broken_md_links"])
        check("resolution: exit 0", code == 0, code)
        check("resolution: no orphans (README links docs, docs links two words)", d["orphans"] == [], d["orphans"])
        check("resolution: folder covered by its README", d["folders_without_index"] == [], d["folders_without_index"])
        write(r / "README.md", "# Root\n\n[missing](docs/none.md) ![img](nope.png)\n")
        code, d = scan_json(r)
        check("resolution: missing link and embed both reported", len(d["broken_md_links"]) == 2, d["broken_md_links"])

        # 5. A parent index that links every file in a subfolder covers that folder (everlast layout).
        e = tmp / "everlast"
        write(e / "INDEX.md", "# Index\n\nGenerated by `everlast.py index`; do not hand-edit.\n\n- [A](decisions/a.md)\n- [B](solutions/b.md)\n")
        write(e / "decisions" / "a.md", "# A\n")
        write(e / "solutions" / "b.md", "# B\n")
        code, d = scan_json(e)
        check("everlast layout: subfolders covered by the root index", d["folders_without_index"] == [], d["folders_without_index"])
        run(e, "--fix-index")
        check("fix-index never edits a generated everlast index", "- [decisions/]" not in (e / "INDEX.md").read_text(encoding="utf-8"))

        # 6. Frontmatter.
        f = tmp / "fm"
        write(f / "README.md", "---\ntitle: Root\ntags:\n  - a\n  - b\nnote: \"a: colon\"\n---\n# Root\n\n[bad](bad.md) [crlf](crlf.md) [bom](bom.md)\n")
        write(f / "bad.md", "---\nno key here\n---\n# Bad\n")
        (f / "crlf.md").write_bytes(b"---\r\ntitle: CRLF\r\n---\r\n# CRLF\r\n")
        (f / "bom.md").write_bytes(b"\xef\xbb\xbf---\ntitle: BOM\n---\n# BOM\n")
        code, d = scan_json(f)
        check("frontmatter: list and quoted colon accepted", not any(x["file"] == "README.md" for x in d["frontmatter_errors"]), d["frontmatter_errors"])
        check("frontmatter: line without key reported", any(x["file"] == "bad.md" for x in d["frontmatter_errors"]), d["frontmatter_errors"])
        check("frontmatter: CRLF accepted", not any(x["file"] == "crlf.md" for x in d["frontmatter_errors"]), d["frontmatter_errors"])
        check("frontmatter: UTF-8 BOM accepted", not any(x["file"] == "bom.md" for x in d["frontmatter_errors"]), d["frontmatter_errors"])

        # 7. --exclude and SKIP_DIRS.
        x = tmp / "excl"
        write(x / "README.md", "# Root\n")
        write(x / "node_modules" / "pkg" / "README.md", "# Pkg\n\n[nope](missing.md)\n")
        write(x / "build-notes" / "old.md", "# Old\n\n[nope](missing.md)\n")
        code, d = scan_json(x, "--exclude", "build-notes")
        check("excluded folders are not scanned", d["files"] == 1 and d["broken_md_links"] == [], (d["files"], d["broken_md_links"]))

        # 8. --vault-init writes app.json and gitignore lines, idempotently.
        vi = tmp / "vault"
        write(vi / "README.md", "# Root\n")
        (vi / "Library").mkdir()
        write(vi / ".gitignore", "*.log")
        run(vi, "--vault-init", "--ignore", "Custom")
        app = json.loads((vi / ".obsidian" / "app.json").read_text(encoding="utf-8"))
        check("vault-init: markdown links and relative format", app.get("useMarkdownLinks") is True and app.get("newLinkFormat") == "relative", app)
        check("vault-init: existing build folder ignored", "Library/" in app.get("userIgnoreFilters", []), app)
        gi = (vi / ".gitignore").read_text(encoding="utf-8")
        check("vault-init: gitignore keeps old lines and adds workspace.json", "*.log" in gi and ".obsidian/workspace.json" in gi, gi)
        run(vi, "--vault-init")
        gi2 = (vi / ".gitignore").read_text(encoding="utf-8")
        check("vault-init: idempotent gitignore", gi2.count(".obsidian/workspace.json") == 1, gi2)

        # 9. --probe prints JSON and never fails.
        code, out = run("--probe")
        check("probe exits 0 and prints JSON", code == 0 and '"cli_on_path"' in out, out[:200])

        # 11. Review fixes of 2026-09-18 (C-20260918-4): each case reproduces a confirmed defect.
        # 11a. Non-ASCII file names must not crash the text report when stdout is a pipe (Windows cp1252).
        u = tmp / "unicode"
        write(u / "README.md", "# Root\n\n[j](%E6%97%A5%E6%9C%AC%E8%AA%9E.md) [l](%C5%82%C3%B3d%C5%BA.md)\n")
        write(u / "日本語.md", "# 日本語\n")
        write(u / "łódź.md", "# łódź\n")
        code, out = run(u)
        check("unicode names: text report exits 0 without a traceback", code == 0 and "Traceback" not in out, out[-300:])
        # 11b. A link whose case differs from the file on disk is a 404 on GitHub and Linux.
        c = tmp / "case"
        write(c / "README.md", "# Root\n\n[a](Notes/Alpha.md) [b](notes/alpha.md) [ok](notes/Alpha.md)\n")
        write(c / "notes" / "Alpha.md", "# Alpha\n")
        code, d = scan_json(c)
        check("case mismatch reported as broken (two of three links)", len(d["broken_md_links"]) == 2 and all("case" in x["target"] for x in d["broken_md_links"]), d["broken_md_links"])
        # 11c. Folder-qualified wikilinks whose stem ends in d, m or a dot resolved wrongly (rstrip bug); the converter must use the same rule.
        q = tmp / "qualified"
        write(q / "README.md", "# Root\n\n[[notes/random]] [[notes/build]] [[notes/Beta]] [[Beta]]\n")
        for name in ("random", "build", "Beta"):
            write(q / "notes" / f"{name}.md", f"# {name}\n")
            write(q / "plans" / f"{name}.md", f"# {name} plan\n")
        code, d = scan_json(q)
        check("path-qualified wikilinks resolve; only the bare one is ambiguous", d["broken_wikilinks"] == [] and len(d["ambiguous_wikilinks"]) == 1, (d["broken_wikilinks"], d["ambiguous_wikilinks"]))
        run(q, "--to-markdown-links")
        t = (q / "README.md").read_text(encoding="utf-8")
        check("converter rewrites path-qualified wikilinks and keeps the ambiguous one", "[notes/Beta](notes/Beta.md)" in t and "[notes/random](notes/random.md)" in t and "[[Beta]]" in t, t)
        # 11d. Anchors are percent-encoded; wikilinks inside frontmatter are left alone; CRLF survives a rewrite.
        h = tmp / "anchor"
        (h / "README.md").parent.mkdir(parents=True, exist_ok=True)
        (h / "README.md").write_bytes(b"---\r\nrelated: \"[[gamma]]\"\r\n---\r\n# Root\r\n\r\n[[gamma#My Heading]] [[gamma#^blk|ref]] [[#Local]]\r\n")
        write(h / "gamma.md", "# Gamma\n\n## My Heading\n")
        run(h, "--to-markdown-links")
        raw = (h / "README.md").read_bytes()
        t = raw.decode("utf-8")
        check("anchor encoded in the converted link", "[gamma](gamma.md#My%20Heading)" in t, t)
        check("block reference keeps its caret", "[ref](gamma.md#%5Eblk)" in t or "[ref](gamma.md#^blk)" in t, t)
        check("same-file heading wikilink converted", "[Local](#Local)" in t, t)
        check("frontmatter wikilink untouched", 'related: "[[gamma]]"' in t, t)
        check("CRLF preserved by the converter", raw.count(b"\r\n") >= 6 and b"\n\n" not in raw.replace(b"\r\n", b""), raw)
        # 11e. --fix-index on a tree with no index anywhere: one line per child, pass-through folders linked, --json stays parseable.
        n = tmp / "nested"
        write(n / "top.md", "# Top\n")
        write(n / "notes" / "a.md", "# A\n")
        write(n / "notes" / "deeper" / "b.md", "# B\n")
        write(n / "empty" / "grand" / "c.md", "# C\n")
        code, d = scan_json(n, "--fix-index")
        check("json with --fix-index is parseable and lists written files", len(d.get("written", [])) >= 4, d.get("written"))
        rootidx = (n / "INDEX.md").read_text(encoding="utf-8")
        check("root index links each child folder once", rootidx.count("[notes/]") == 1 and "[notes/](notes/INDEX.md)" in rootidx, rootidx)
        check("pass-through folder linked via the nearest index below", "empty/grand/INDEX.md" in rootidx, rootidx)
        check("nested fix-index leaves no orphans and no folders without index", d["orphans"] == [] and d["folders_without_index"] == [], (d["orphans"], d["folders_without_index"]))
        # 11f. A missing root is an error, not a clean run.
        code, out = run(tmp / "does-not-exist")
        check("missing root exits 2", code == 2, code)
        # 11g. Links with a literal space are reported; <...> destinations are resolved; escaped-pipe wikilinks resolve; attachments resolve.
        s = tmp / "space"
        write(s / "README.md", "# Root\n\n[a](notes/two words.md) [b](<notes/two words.md>) [t](notes/two%20words.md \"title\") [[gamma\\|alias]] [[doc.pdf]] [[img.png]]\n")
        write(s / "notes" / "two words.md", "# Two\n")
        write(s / "gamma.md", "# Gamma\n")
        (s / "doc.pdf").write_bytes(b"%PDF-1.4\n")
        (s / "img.png").write_bytes(b"\x89PNG\r\n")
        code, d = scan_json(s)
        check("space in link target reported once, <...> and quoted-title forms accepted", len(d["broken_md_links"]) == 1 and "space" in d["broken_md_links"][0]["target"], d["broken_md_links"])
        check("escaped-pipe wikilink and attachment wikilinks resolve", d["broken_wikilinks"] == [] and d["ambiguous_wikilinks"] == [], (d["broken_wikilinks"], d["ambiguous_wikilinks"]))
        # 11h. Nested fences, blockquoted fences, HTML comments and reference-style links.
        g = tmp / "fences"
        write(g / "README.md", "# Root\n\n````md\n```\n[x](nope.md)\n```\n````\n\n> ```\n> [y](nope.md)\n> ```\n\n<!-- [z](nope.md) -->\n\n[ref link][r]\n\n[r]: notes/real.md\n")
        write(g / "notes" / "real.md", "# Real\n")
        code, d = scan_json(g)
        check("links inside nested and quoted fences and comments ignored", d["broken_md_links"] == [], d["broken_md_links"])
        check("reference-style definition credits its target", d["orphans"] == [], d["orphans"])
        # 11i. Titles: H1 after frontmatter (not a YAML comment), brackets escaped, BOM tolerated.
        b = tmp / "titles"
        write(b / "README.md", "# Root\n")
        write(b / "notes" / "x.md", "---\n# not a title\ntitle: X\n---\n# [WIP] Real title\n")
        (b / "notes" / "y.md").write_bytes(b"\xef\xbb\xbf# Bom title\n")
        run(b, "--fix-index")
        idx = (b / "notes" / "INDEX.md").read_text(encoding="utf-8")
        check("index uses the H1 after frontmatter with brackets escaped", "[\\[WIP\\] Real title](x.md)" in idx, idx)
        check("index uses the H1 behind a BOM", "[Bom title](y.md)" in idx, idx)
        code, d = scan_json(b)
        check("escaped-bracket index line parses as a link (x.md not an orphan)", d["orphans"] == [], d["orphans"])
        # 11j. --vault-init: --ignore names are always written; gitignore compares whole lines.
        vi2 = tmp / "vault2"
        write(vi2 / "README.md", "# Root\n")
        write(vi2 / ".gitignore", ".obsidian/cache-extra\n")
        run(vi2, "--vault-init", "--ignore", "Library")
        app = json.loads((vi2 / ".obsidian" / "app.json").read_text(encoding="utf-8"))
        gi = (vi2 / ".gitignore").read_text(encoding="utf-8")
        check("--ignore folder written even when absent", "Library/" in app["userIgnoreFilters"], app)
        check("gitignore line added despite a substring match", ".obsidian/cache\n" in gi, gi)
        # 11k. A link that leaves the root is a warning, not a silent pass.
        o = tmp / "outer"
        write(o / "outside.md", "# Outside\n")
        write(o / "vault" / "README.md", "# Root\n\n[out](../outside.md)\n")
        code, d = scan_json(o / "vault")
        check("link outside the root reported as a warning", len(d["links_outside_root"]) == 1 and d["broken_md_links"] == [], (d["links_outside_root"], d["broken_md_links"]))

        # 10. The repo's own docs pass the lint (fixtures excluded).
        repo = HERE.parent.parent.parent
        code, d = scan_json(repo, "--exclude", "fixtures")
        check("repo docs: no broken links, no wikilinks", d["broken_md_links"] == [] and d["broken_wikilinks"] == [] and d["wikilinks"] == 0,
              (d["broken_md_links"], d["broken_wikilinks"], d["wikilinks"]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if FAILS:
        print(f"\n{len(FAILS)} check(s) failed: " + ", ".join(FAILS))
        sys.exit(1)
    print("\nall checks passed")


if __name__ == "__main__":
    main()
