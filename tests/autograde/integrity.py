"""Detects pasted output that does not belong to the repository being graded."""
from __future__ import annotations

import re
from typing import List, Set

from .context import Ctx
from .textutil import line_shas

BRACKET_SHA_RE = re.compile(r"\[[^\]]*? ([0-9a-f]{7,40})\]")
RANGE_SHA_RE = re.compile(r"(?m)^\s+([0-9a-f]{7,40})\.\.([0-9a-f]{7,40})\s")
UPDATING_SHA_RE = re.compile(r"(?m)^Updating ([0-9a-f]{7,40})\.\.([0-9a-f]{7,40})\s*$")
HEAD_NOW_RE = re.compile(r"(?m)^HEAD is now at ([0-9a-f]{7,40}) ")
WAS_RE = re.compile(r"\(was ([0-9a-f]{7,40})\)")
TO_LINE_RE = re.compile(r"(?m)^To (\S+)\s*$")


def integrity_warnings(ctx: Ctx) -> List[str]:
    """Return human-readable warnings; an empty list means the pasted text matches this repo."""
    if not ctx.repo_mode:
        return []
    facts = ctx.facts
    warnings: List[str] = []
    allowed = {facts.config_value("remote.origin.url"), facts.config_value("remote.upstream.url")} - {""}
    wrong_target: Set[str] = set()
    foreign: Set[str] = set()
    for text in ctx.steps.values():
        for match in TO_LINE_RE.finditer(text):
            if allowed and match.group(1) not in allowed:
                wrong_target.add(match.group(1))
        tokens = line_shas(text) + BRACKET_SHA_RE.findall(text) + HEAD_NOW_RE.findall(text) + WAS_RE.findall(text)
        for pair in RANGE_SHA_RE.findall(text) + UPDATING_SHA_RE.findall(text):
            tokens += list(pair)
        for token in tokens:
            if not facts.commit_exists(token):
                foreign.add(token)
    if wrong_target:
        warnings.append("a pasted push names another repository than this clone's remotes: " + ", ".join(sorted(wrong_target)))
    if foreign:
        shown = ", ".join(sorted(foreign)[:6])
        warnings.append(f"{len(foreign)} commit SHA(s) in the pasted text do not exist in this repository "
                        f"(e.g. {shown}); the outputs were not produced in this clone")
    return warnings
