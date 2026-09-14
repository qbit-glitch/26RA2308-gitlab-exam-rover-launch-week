"""Small helpers shared by the task graders."""
from __future__ import annotations

import re
from typing import Callable, List, Optional

from .context import Ctx
from .facts import Commit
from .textutil import oneline_entries, parse_branch_list, parse_config_list

PLACEHOLDER_NAMES = {"", "your full name", "your name"}
PLACEHOLDER_EMAILS = {"", "your.email@example.com"}
TREE_ALIAS = "log --oneline --graph --decorate --all"
SHA = r"[0-9a-f]{7,40}"
BEN = "ben@kestrel.example"
CHITRA = "chitra@kestrel.example"


def student_name(ctx: Ctx) -> str:
    """The student's user.name: from the clone when it can be read, else from the pasted config (step 1.1)."""
    if ctx.repo_mode:
        value = ctx.facts.config_value("user.name")
        if value:
            return value
    return parse_config_list(ctx.step("1.1")).get("user.name", "")


def live(ctx: Ctx, test: Callable[[], bool]) -> bool:
    """A live-repo condition that counts as met when the grader runs in --outputs-only mode."""
    return True if not ctx.repo_mode else bool(test())


def has(text: str, pattern: str) -> bool:
    """True when the regular expression matches somewhere in the text (multi-line mode)."""
    return re.search(pattern, text, re.MULTILINE) is not None


def count(text: str, pattern: str) -> int:
    """How many times the regular expression matches."""
    return len(re.findall(pattern, text, re.MULTILINE))


def lines(text: str) -> List[str]:
    """The non-blank, stripped lines of a pasted output."""
    return [ln.strip() for ln in text.split("\n") if ln.strip()]


def commit_sha(text: str, subject: str, branch: str = r"[^\]]+?") -> str:
    """The SHA in the first '[<branch> <sha>] <subject>' line of a pasted 'git commit' ('' if none)."""
    match = re.search(rf"\[{branch} (?:\(root-commit\) )?({SHA})\] {re.escape(subject)}", text)
    return match.group(1) if match else ""


def sha_is(ctx: Ctx, token: str, subject: Optional[str] = None) -> bool:
    """True when 'token' names a commit in the clone (with this subject, when one is given)."""
    if not token:
        return False
    if not ctx.repo_mode:
        return True
    facts = ctx.facts
    return facts.commit_exists(token) and (subject is None or facts.subject(token) == subject)


def graph_subjects(text: str) -> List[str]:
    """Subjects of the '* <sha> ...' lines of a pasted 'git log --graph', decoration removed, in order.

    Other lines that start with a number (a fetch or push range, for example) are not commits of the graph."""
    out: List[str] = []
    for line in text.split("\n"):
        if re.match(rf"^[ |\\/_]*\*\s+{SHA}\b", line):
            for entry in oneline_entries(line):
                out.append(re.sub(r"^\([^)]*\)\s*", "", entry.subject).strip())
    return out


def short_of(commit: Optional[Commit]) -> str:
    """First 7 characters of a commit's SHA ('' for None)."""
    return commit.sha[:7] if commit else ""


def same_prefix(token: str, full: str) -> bool:
    """True when 'token' (at least 7 characters) is an abbreviation of the full SHA."""
    token = token.lower().strip()
    return len(token) >= 7 and bool(full) and full.lower().startswith(token)


def branch_names(text: str) -> List[str]:
    """Branch names of a pasted 'git branch' style output, in order; Git's '(use ...)' hint lines are not branches."""
    return [row.name for row in parse_branch_list(text) if not row.name.startswith("(")]
