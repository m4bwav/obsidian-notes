#!/usr/bin/env python3
"""check_vault.py - grade the fixture vault on its end state, not on which tool produced it.

  python evals/check_vault.py <vault> [--task index|convert] [--loose]

Exits 0 only when the vault is right, 1 when it is not (one line per problem), 2 when <vault> is not a folder.
The fixture's traps: [[Beta]] is ambiguous (notes/Beta.md and plans/Beta.md), [[gamma]] resolves to notes/gamma.md,
[missing](nope.md) is broken on purpose, plans/loose.md is an orphan, notes/ and plans/ have no index.

Both tasks require:
  - every note survives (matched by its H1, so a rename is fine);
  - every relative markdown link resolves, with the case on disk (GitHub and Linux are case-sensitive), except nope.md;
  - README.md still links nope.md and no nope.md was invented: a broken link is the user's call;
  - README.md still points at Beta: [[Beta]] left alone, or a link that now resolves to one of the two Beta notes.
--task index (default), lint and index:
  - notes/ and plans/ each hold an index file (README, INDEX, _index, MOC, index or <folder>.md) that links every
    other note in the folder with a relative markdown link (--loose: any link that resolves to exactly one file);
  - every note is reachable from the root README.md, so the new indexes are themselves linked (skipped with --loose).
--task convert, wikilinks to links that work on GitHub:
  - no wikilink that resolves to exactly one file is left.
Standard library only.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from urllib.parse import unquote

INDEX_NAMES = {"readme.md", "index.md", "_index.md", "moc.md"}
TITLES = ["Beta", "Gamma", "Beta plan", "Loose plan"]
FENCE = re.compile(r"^(```|~~~).*?^\1", re.M | re.S)
FRONTMATTER = re.compile(r"\A---\n.*?\n---\n", re.S)
WIKI = re.compile(r"!?\[\[([^\]|#]*)(#[^\]|]*)?(\|[^\]]*)?\]\]")
MDLINK = re.compile(r"!?\[[^\]]*\]\(\s*(<[^>]+>|[^)\s]+)(?:\s+\"[^\"]*\")?\s*\)")
REFDEF = re.compile(r"^\s*\[[^\]]+\]:\s*(<[^>]+>|\S+)", re.M)


def body(p: Path) -> str:
    s = p.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    return FENCE.sub("", FRONTMATTER.sub("", s))


VAULT = Path(".")


def exists_exact(p: Path) -> bool:
    """True when p exists with exactly this case in every part below the vault (Windows and macOS match any case;
    Path.resolve() would hand back the case on disk, so the parts are walked by name)."""
    rel = os.path.relpath(os.path.normpath(os.path.abspath(p)), os.path.normpath(os.path.abspath(VAULT)))
    if rel.startswith(".."):
        return p.exists()
    cur = VAULT
    for part in Path(rel).parts:
        if part == ".":
            continue
        if not cur.is_dir() or part not in {c.name for c in cur.iterdir()}:
            return False
        cur = cur / part
    return True


def md_targets(text: str) -> list[str]:
    out = []
    for raw in MDLINK.findall(text) + REFDEF.findall(text):
        t = raw[1:-1] if raw.startswith("<") else raw
        if re.match(r"^[a-z][a-z0-9+.-]*:", t, re.I) or t.startswith("#"):
            continue
        out.append(unquote(t.split("#")[0]))
    return [t for t in out if t]


def resolve_md(src: Path, target: str) -> Path | None:
    p = src.parent / target
    if exists_exact(p) and p.is_dir():
        for c in sorted(p.iterdir()):
            if c.name.lower() in INDEX_NAMES or c.stem.lower() == p.name.lower():
                return c
        return None
    return p if exists_exact(p) and p.is_file() else None


def resolve_wiki(vault: Path, notes: list[Path], target: str) -> list[Path]:
    t = target.strip().replace("\\", "/")
    if not t:
        return []
    want = t.lower() if t.lower().endswith(".md") else t.lower() + ".md"
    if "/" in t:
        return [n for n in notes if n.relative_to(vault).as_posix().lower() == want.lstrip("/")]
    return [n for n in notes if n.name.lower() == want]


def h1(p: Path) -> str | None:
    m = re.search(r"^#\s+(.+?)\s*$", body(p), re.M)
    return m.group(1) if m else None


def is_index(p: Path) -> bool:
    return p.name.lower() in INDEX_NAMES or p.stem.lower() == p.parent.name.lower()


def check(vault: Path, task: str, loose: bool) -> list[str]:
    global VAULT
    VAULT = vault
    notes = sorted(p for p in vault.rglob("*.md") if not any(part.startswith(".") for part in p.relative_to(vault).parts))
    problems: list[str] = []
    readme = vault / "README.md"
    if not readme.is_file():
        return ["README.md (the vault's entry point) is gone"]

    titles = {h1(n) for n in notes}
    problems += [f"note '{t}' is gone (no file has '# {t}')" for t in TITLES if t not in titles]

    edges: dict[Path, set[Path]] = {}
    for n in notes:
        text, rel = body(n), n.relative_to(vault).as_posix()
        out = edges.setdefault(n.resolve(), set())
        for t in md_targets(text):
            hit = resolve_md(n, t)
            if hit is not None:
                out.add(hit.resolve())
            elif not (n == readme and t == "nope.md"):
                problems.append(f"{rel}: markdown link to '{t}' does not resolve (case counts)")
        for target, _, _ in WIKI.findall(text):
            hits = resolve_wiki(vault, notes, target)
            if len(hits) == 1:
                out.add(hits[0].resolve())
                if task == "convert":
                    problems.append(f"{rel}: [[{target}]] resolves to one file and was not converted")
            elif not hits and target.strip():
                problems.append(f"{rel}: [[{target}]] does not resolve")

    rtext = body(readme)
    if "nope.md" not in md_targets(rtext):
        problems.append("README.md: the broken [missing](nope.md) link was removed instead of left for the user")
    if (vault / "nope.md").exists():
        problems.append("nope.md was created: the broken link is the user's call, not a guess")
    beta_ok = any(len(resolve_wiki(vault, notes, t)) > 1 for t, _, _ in WIKI.findall(rtext)) or any(
        h1(Path(p)) in ("Beta", "Beta plan") for p in edges.get(readme.resolve(), set()))
    if not beta_ok:
        problems.append("README.md: the link to Beta is gone (leave [[Beta]] or point it at one Beta note)")

    if task == "index":
        for folder in ("notes", "plans"):
            d = vault / folder
            members = [n for n in notes if n.parent == d]
            idx = [n for n in members if is_index(n)]
            if not idx:
                problems.append(f"{folder}/: no index file")
                continue
            linked: set[Path] = set()
            for i in idx:
                if loose:
                    linked |= edges.get(i.resolve(), set())
                else:
                    linked |= {h.resolve() for t in md_targets(body(i)) if (h := resolve_md(i, t)) is not None}
            for n in members:
                if n not in idx and n.resolve() not in linked:
                    kind = "a link that resolves" if loose else "a relative markdown link"
                    problems.append(f"{folder}/: the index does not link {n.name} with {kind}")
        if not loose:
            seen, todo = {readme.resolve()}, [readme.resolve()]
            while todo:
                for nxt in edges.get(todo.pop(), set()):
                    if nxt not in seen:
                        seen.add(nxt)
                        todo.append(nxt)
            problems += [f"{n.relative_to(vault).as_posix()}: not reachable from README.md"
                         for n in notes if n.resolve() not in seen]
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("vault")
    ap.add_argument("--task", choices=("index", "convert"), default="index")
    ap.add_argument("--loose", action="store_true", help="index task: accept any resolving link, skip reachability")
    a = ap.parse_args()
    vault = Path(a.vault)
    if not vault.is_dir():
        print(f"not a folder: {vault}")
        return 2
    problems = check(vault, a.task, a.loose)
    for p in problems:
        print(p)
    print(f"{'FAIL' if problems else 'PASS'} ({a.task}{', loose' if a.loose else ''}): {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
