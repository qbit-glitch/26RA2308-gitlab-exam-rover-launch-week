"""Graders for Tasks 4 and 5 (Module III: branches, detached HEAD, merges, a conflict, abort and rebase)."""
from __future__ import annotations

import re

from .common import CHITRA, SHA, commit_sha, graph_subjects, has, live, same_prefix, sha_is, student_name
from .context import Ctx
from .framework import Task
from .textutil import get_answer_int, get_answer_sha


def grade_task4(ctx: Ctx) -> Task:
    """Task 4: branch -a, switch -c, detached HEAD, fast-forward, three-way merge, cat-file."""
    t = Task(4, "Branches and merges", 4, ctx.repo_mode)
    f = ctx.facts
    s41, s42 = ctx.step("4.1"), ctx.step("4.2")
    planner = f.find_anywhere("feat(nav): add path planner stub")
    names = s42.split()  # `ls` prints in columns on a terminal, so look at words, not lines
    t.check(1, "4.1 branch -a lists the three branches of the shared copy under remotes/origin/ and ANSWER-3 is 2; 4.2 a new branch, "
               "the planner commit (create mode tools/planner.py), back on main the folder has no planner.py; live repo: the commit "
               "is on feature/path-planning only",
            lambda: all(f"remotes/origin/{b}" in s41 for b in ("main", "feature/fast-mode", "fix/echo-timeout"))
            and get_answer_int(ctx.text, 3) == "2" and "Switched to a new branch 'feature/path-planning'" in s42
            and bool(commit_sha(s42, "feat(nav): add path planner stub", "feature/path-planning"))
            and "create mode 100644 tools/planner.py" in s42 and "Switched to branch 'main'" in s42
            and "planner.py" not in names and "detector.py" in names
            and live(ctx, lambda: planner is not None and f.changes(planner.sha) == {"tools/planner.py": "A"}
                     and f.file_at("refs/heads/feature/path-planning", "tools/planner.py") is not None
                     and f.file_at("refs/heads/main", "tools/planner.py") is None))
    s43 = ctx.step("4.3")
    made = commit_sha(s43, "temp: experiment from old commit", "detached HEAD")
    release = f.rev("v0.1.0")
    t.check(1, "4.3 detached at the v0.1.0 commit, committed there and saved on a branch; ANSWER-4 is the new commit, whose parent "
               "is the release, which holds baseline-notes.txt with your name; experiment/detached-recovery points at it",
            lambda: has(s43, rf"HEAD is now at {SHA} release: v0\.1 field build") and bool(made)
            and "Switched to a new branch 'experiment/detached-recovery'" in s43
            and has(s43, rf"(?m)^{made[:7]}\w* .*temp: experiment from old commit$")
            and same_prefix(get_answer_sha(ctx.text, 4), f.rev(made) or made)
            and live(ctx, lambda: f.parents(f.rev(made)) == [release]
                     and student_name(ctx) in (f.file_at(f.rev(made), "baseline-notes.txt") or "")
                     and f.rev("refs/heads/experiment/detached-recovery") == f.rev(made)),
            why=lambda: "4.3 must make a commit on top of v0.1.0 while detached, then save it with switch -c")
    s44, s45 = ctx.step("4.4"), ctx.step("4.5")
    logger = f.find("feat: add logging import")
    merge = f.find("merge: battery")
    battery = f.find_anywhere("feat: add battery monitor")
    docs = f.find("docs: note version 0.2")
    t.check(1, "4.4 'Fast-forward' (no new commit) and 'Deleted branch feature/logging'; 4.5 \"Merge made by the 'ort' strategy.\"; "
               "live repo: the logging commit sits on main's own line, and 'merge: battery' has two parents: the docs commit "
               "on main, then the tip of feature/battery",
            lambda: has(s44, rf"(?m)^Updating {SHA}\.\.{SHA}$") and "Fast-forward" in s44 and "src/logger.py" in s44
            and has(s44, rf"Deleted branch feature/logging \(was {SHA}\)")
            and has(s45, r"Merge made by the '(ort|recursive)' strategy\.") and "src/battery.py" in s45
            and live(ctx, lambda: logger is not None and logger.sha in f.first_parent_shas() and len(logger.parents) == 1
                     and "feature/logging" not in f.local_branches()
                     and merge is not None and docs is not None and battery is not None
                     and merge.parents == [docs.sha, battery.sha] and f.rev("refs/heads/feature/battery") == battery.sha))
    s46 = ctx.step("4.6")
    parents = re.findall(r"(?m)^parent ([0-9a-f]{40})$", s46)
    t.check(1, "4.6 the graph forks and joins (a '|\\' line) with 'merge: battery' at HEAD -> main; cat-file -p HEAD shows two "
               "'parent' lines; ANSWER-5 is the second parent (the tip of feature/battery)",
            lambda: has(s46, r"(?m)^[ |*]*\|\\") and has(s46, r"\(HEAD -> main[,)].*merge: battery")
            and len(parents) == 2 and has(s46, r"(?m)^merge: battery$") and sha_is(ctx, parents[0]) and sha_is(ctx, parents[1])
            and same_prefix(get_answer_sha(ctx.text, 5), parents[1])
            and live(ctx, lambda: battery is not None and same_prefix(get_answer_sha(ctx.text, 5), battery.sha)))
    return t


def grade_task5(ctx: Ctx) -> Task:
    """Task 5: a conflict resolved, a conflict aborted, a rebase."""
    t = Task(5, "Conflict, abort and rebase", 3, ctx.repo_mode)
    f = ctx.facts
    name = student_name(ctx)
    s51, s52 = ctx.step("5.1"), ctx.step("5.2")
    forty = f.find("perf(sensor): set echo timeout to 40 ms")
    t.check(1, "5.1 the 40 ms commit is pasted; 5.2 the merge stopped: 'CONFLICT (content)', 'Automatic merge failed', status "
               "'both modified', and the file holds 40 above ======= and 30 below; live repo: the 40 ms commit exists",
            lambda: bool(commit_sha(s51, "perf(sensor): set echo timeout to 40 ms", "main"))
            and "CONFLICT (content): Merge conflict in src/limits.py" in s52 and "Automatic merge failed" in s52
            and "You have unmerged paths" in s52 and has(s52, r"both modified:\s+src/limits\.py")
            and has(s52, r"(?m)^<<<<<<< HEAD\nSENSOR_TIMEOUT_MS = 40\n=======\nSENSOR_TIMEOUT_MS = 30\n>>>>>>> \S*fix/echo-timeout$")
            and live(ctx, lambda: forty is not None and "SENSOR_TIMEOUT_MS = 40" in (f.file_at(forty.sha, "src/limits.py") or "")))
    s53 = ctx.step("5.3")
    limits = f.file_at("refs/heads/main", "src/limits.py") or ""
    expected_tail = ["SENSOR_TIMEOUT_MS = 30", "SENSOR_MAX_CM = 400", "SENSOR_MIN_CM = 2"]
    settle = f.find("merge: settle echo timeout at 30 ms")
    chitra = f.find_anywhere("fix(sensor): set echo timeout to 30 ms")
    t.check(1, "5.3 the tests passed (OK) and grep -c found 0 markers; the merge commit is pasted; live repo: limits.py is your comment "
               "line (with your name) and the three lines, Chitra's 30 kept, no markers; 'merge: settle echo timeout at 30 ms' "
               "has two parents: the 40 ms commit and Chitra's commit",
            lambda: has(s53, r"(?m)^OK$") and has(s53, r"Ran \d+ tests?") and has(s53, r"(?m)^0$")
            and bool(commit_sha(s53, "merge: settle echo timeout at 30 ms", "main"))
            and live(ctx, lambda: limits.split("\n")[1:4] == expected_tail and limits.split("\n")[0].startswith("#")
                     and name in limits.split("\n")[0] and limits.endswith("\n") and len(limits.strip().split("\n")) == 4
                     and settle is not None and forty is not None and chitra is not None and chitra.email == CHITRA
                     and settle.parents == [forty.sha, chitra.sha]))
    s54, s55 = ctx.step("5.4"), ctx.step("5.5")
    fast = f.find_anywhere("feat(control): add fast mode")
    bump = f.find("chore: bump version to 0.2-dev")
    lidar = f.find_anywhere("feat(sensor): add lidar stub")
    subjects = graph_subjects(s55)
    t.check(1, "5.4 the second merge stopped too (CONFLICT in src/config.py) and --abort gave a clean tree; 5.5 rebase printed "
               "'Successfully rebased and updated refs/heads/feature/lidar.' and the lidar commit is in a straight line on top of "
               "the version bump; live repo: fast mode was not merged (config.py still says SPEED = 5) and the lidar commit's "
               "parent is the bump (replayed, not merged)",
            lambda: "CONFLICT (content): Merge conflict in src/config.py" in s54 and "Automatic merge failed" in s54
            and "nothing to commit, working tree clean" in s54
            and "Successfully rebased and updated refs/heads/feature/lidar." in s55
            and subjects[:2] == ["feat(sensor): add lidar stub", "chore: bump version to 0.2-dev"]
            and live(ctx, lambda: fast is not None and not f.is_ancestor(fast.sha, "refs/heads/main")
                     and "SPEED = 5" in (f.file_at("refs/heads/main", "src/config.py") or "") and f.working_tree_clean()
                     and lidar is not None and bump is not None and lidar.parents == [bump.sha]
                     and f.rev("refs/heads/feature/lidar") == lidar.sha))
    return t
