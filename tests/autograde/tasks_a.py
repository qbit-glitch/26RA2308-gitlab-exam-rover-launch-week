"""Graders for Tasks 1 to 3 (Modules I and II: set-up, .gitignore, commits, history, undo, stash)."""
from __future__ import annotations

import re

from .common import (
    PLACEHOLDER_EMAILS, PLACEHOLDER_NAMES, SHA, TREE_ALIAS, commit_sha, count, has, live, sha_is, student_name,
)
from .context import Ctx
from .framework import Task
from .textutil import get_answer, get_answer_sha, parse_config_list, same_sha


def grade_task1(ctx: Ctx) -> Task:
    """Task 1: identity, a look inside .git, .gitignore, check-ignore, rm --cached."""
    t = Task(1, "Arrive and keep the data out", 2, ctx.repo_mode)
    f = ctx.facts
    cfg = parse_config_list(ctx.step("1.1"))
    name, email = f.config_value("user.name"), f.config_value("user.email")
    s12 = ctx.step("1.2")
    t.check(1, "1.1 config list shows your own name, e-mail and the tree alias (not placeholders, not a teammate's, the same as "
               "the clone really has); 1.2 ls .git shows objects, refs, HEAD, config and index; ANSWER-1 is objects",
            lambda: cfg.get("user.name", "").lower() not in PLACEHOLDER_NAMES and "@" in cfg.get("user.email", "")
            and cfg.get("user.email", "").lower() not in PLACEHOLDER_EMAILS and cfg.get("alias.tree") == TREE_ALIAS
            and live(ctx, lambda: cfg.get("user.name") == name and cfg.get("user.email") == email
                     and name.lower() not in f.published_names() and email.lower() not in f.published_emails()
                     and f.config_value("alias.tree") == TREE_ALIAS)
            and all(n in s12.split() for n in ("objects", "refs", "HEAD", "config", "index"))
            and get_answer(ctx.text, 1).lower() == "objects")
    s13, s14, s15 = ctx.step("1.3"), ctx.step("1.4"), ctx.step("1.5")
    subject = "chore: ignore raw data and stop tracking run_042"
    commit = f.find(subject)
    ignore = (f.file_at("refs/heads/main", ".gitignore") or "").split("\n")
    t.check(1, "1.3 check-ignore names the rule 'data/raw/'; 1.4 rm --cached keeps the file on disk (status ' M .gitignore' and "
               "'D  data/raw/run_042.csv'); 1.5 the commit is pasted; live repo: it changes only .gitignore and removes run_042.csv from Git",
            lambda: has(s13, r"\.gitignore:\d+:data/raw/\s+data/raw/run_043\.csv") and "rm 'data/raw/run_042.csv'" in s14
            and has(s14, r"(?m)^ M \.gitignore$") and has(s14, r"(?m)^D  data/raw/run_042\.csv$") and "run_042.csv" in s14.split()
            and sha_is(ctx, commit_sha(s15, subject, "main"), subject) and "delete mode 100644 data/raw/run_042.csv" in s15
            and live(ctx, lambda: commit is not None and f.changes(commit.sha) == {".gitignore": "M", "data/raw/run_042.csv": "D"}
                     and "data/raw/" in ignore and "*.csv" in ignore and "__pycache__/" in ignore
                     and f.file_at("refs/heads/main", "data/raw/run_042.csv") is None),
            why=lambda: f"no commit '{subject}' with exactly those changes on main")
    return t


def grade_task2(ctx: Ctx) -> Task:
    """Task 2: add -p, commit -am, --amend, git mv, log --follow."""
    t = Task(2, "Stage, commit and read the history", 4, ctx.repo_mode)
    f = ctx.facts
    name = student_name(ctx)
    label = f"+# Kestrel-1 controller (v0.2) - {name}"
    s21 = ctx.step("2.1")
    cut = s21.rfind("diff --git")  # the add -p session comes first, then 'git diff --staged' starts with its own header
    session, staged = s21[:max(cut, 0)], s21[max(cut, 0):]
    t.check(1, "2.1 git add -p offered two hunks (Stage this hunk ... twice); the staged diff holds only the label line "
               "(not the clamp function) and status shows MM",
            lambda: bool(name) and cut > 0 and count(session, r"Stage this hunk") >= 2 and label in staged.split("\n")
            and "def clamp" not in staged and has(staged, r"(?m)^MM src/controller\.py$"))
    label_subject = "docs(control): label controller version"
    s22, s23 = ctx.step("2.2"), ctx.step("2.3")
    t.check(1, "2.2 the label commit is pasted (one line changed); 2.3 commit -am committed the clamp (5 lines added) without a "
               "separate git add; both numbers exist in your repository",
            lambda: sha_is(ctx, commit_sha(s22, label_subject, "main"), label_subject) and "1 insertion(+), 1 deletion(-)" in s22
            and sha_is(ctx, commit_sha(s23, "feat(control): add speed clamp", "main")) and "1 file changed, 5 insertions(+)" in s23)
    final = "feat(control): clamp motor speed to 0-255"
    s24 = ctx.step("2.4")
    amended = f.find(final)
    t.check(1, "2.4 amend -m renamed the last commit and added CHANGELOG.md to it ('create mode', 'Date:'); live repo: the commit "
               "holds CHANGELOG.md and controller.py, the old message is gone, and the reflog shows the amend",
            lambda: sha_is(ctx, commit_sha(s24, final, "main"), final) and "create mode 100644 CHANGELOG.md" in s24
            and "Date:" in s24 and live(ctx, lambda: amended is not None
            and f.changes(amended.sha) == {"CHANGELOG.md": "A", "src/controller.py": "M"}
            and f.find("feat(control): add speed clamp") is None
            and any(m.startswith("commit (amend)") for m in f.head_reflog())
            and (f.file_at("refs/heads/main", "src/controller.py") or "").split("\n")[0] == label[1:]))
    s25 = ctx.step("2.5")
    t.check(1, "2.5 git mv: rename NOTES.txt => docs/team-notes.txt; --follow lists the rename and also 'chore: initialise repository "
               "structure'; live repo: the commit exists and NOTES.txt is gone from main",
            lambda: "rename NOTES.txt => docs/team-notes.txt" in s25
            and has(s25, rf"(?m)^{SHA} (?:\([^)]*\) )?refactor: move team notes into docs$")
            and has(s25, rf"(?m)^{SHA} (?:\([^)]*\) )?chore: initialise repository structure$")
            and live(ctx, lambda: f.find("refactor: move team notes into docs") is not None
                     and f.file_at("refs/heads/main", "docs/team-notes.txt") is not None
                     and f.file_at("refs/heads/main", "NOTES.txt") is None))
    return t


def grade_task3(ctx: Ctx) -> Task:
    """Task 3: restore, reset --hard, reflog, revert, stash."""
    t = Task(3, "Undo, recover and shelve", 3, ctx.repo_mode)
    f = ctx.facts
    s31, s32 = ctx.step("3.1"), ctx.step("3.2")
    main_controller = f.file_at("refs/heads/main", "src/controller.py") or ""
    t.check(1, "3.1 restore: status showed ' M src/controller.py' and the bad line (MAX_SPEED = 9999) is not in your repository; "
               "3.2 reset --hard went back one commit ('HEAD is now at ... add turn gain parameter') and nothing is left to show",
            lambda: has(s31, r"(?m)^ M src/controller\.py$") and live(ctx, lambda: "9999" not in main_controller)
            and has(s32, rf"HEAD is now at {SHA} feat\(control\): add turn gain parameter") and not has(s32, r"(?m)^.. params\.txt$"))
    ans2 = get_answer_sha(ctx.text, 2)
    s33, s34 = ctx.step("3.3"), ctx.step("3.4")
    t.check(1, "3.3 reflog still lists the lost commit and ANSWER-2 is its number (the 9.9 commit); 3.4 reset --hard to that number "
               "brings it back ('HEAD is now at <ANSWER-2> ...') and params.txt says 9.9",
            lambda: bool(ans2) and has(s33, rf"(?m)^{ans2[:7]}\w* HEAD@\{{\d+\}}: commit: fix\(control\): raise turn gain to 9\.9$")
            and sha_is(ctx, ans2, "fix(control): raise turn gain to 9.9")
            and has(s34, rf"HEAD is now at {SHA} fix\(control\): raise turn gain to 9\.9") and "turn_gain = 9.9" in s34
            and same_sha(re.search(rf"HEAD is now at ({SHA}) ", s34).group(1), ans2))
    revert_subject = 'Revert "fix(control): raise turn gain to 9.9"'
    s35, s36 = ctx.step("3.5"), ctx.step("3.6")
    bad = f.find("fix(control): raise turn gain to 9.9")
    revert = f.find(revert_subject)
    t.check(1, "3.5 revert --no-edit added a new commit that cancels the 9.9 commit (params.txt says 1.0 again); 3.6 stash push "
               "saved the work, stash pop brought it back ('Dropped refs/stash@{0}', the list is empty) and it was committed; "
               "live repo: a real revert commit, no stash left, params.txt = 3.0",
            lambda: commit_sha(s35, revert_subject, "main") != "" and "turn_gain = 1.0" in s35.split("\n")
            and "Saved working directory and index state On main: wip: tuning turn gain" in s36
            and s36.count("stash@{0}: On main: wip: tuning turn gain") == 1 and "Dropped refs/stash@{0}" in s36
            and commit_sha(s36, "fix(control): set turn gain to 3.0", "main") != ""
            and live(ctx, lambda: bad is not None and revert is not None and revert.parents == [bad.sha]
                     and f.git("show", "-s", "--format=%b", revert.sha).count(f"This reverts commit {bad.sha}") == 1
                     and f.git("stash", "list").strip() == ""
                     and (f.file_at("refs/heads/main", "params.txt") or "") == "turn_gain = 3.0\n"),
            why=lambda: "the revert must be a normal commit right after the 9.9 commit (not a reset); the stash must be popped and committed")
    return t
