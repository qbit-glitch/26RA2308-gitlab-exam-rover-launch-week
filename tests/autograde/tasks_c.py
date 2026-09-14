"""Grader for Task 6 (Modules IV and V: your own remote, fetch and pull, a rejected push, rebase, tags)."""
from __future__ import annotations

import re
from typing import Dict

from .common import BEN, SHA, commit_sha, graph_subjects, has, lines, live, same_prefix
from .context import Ctx
from .framework import Task
from .textutil import get_answer, get_answer_sha, parse_branch_list, same_sha

REMOTE_LINE_RE = re.compile(r"(?m)^(\S+)\s+(\S+)\s+\((fetch|push)\)\s*$")
FETCH_RANGE_RE = re.compile(rf"(?m)^\s+({SHA})\.\.({SHA})\s+main\s+->\s+origin/main\s*$")
PUSH_RANGE_RE = re.compile(rf"(?m)^\s+({SHA})\.\.({SHA})\s+main\s+->\s+main\s*$")
UPDATING_RE = re.compile(rf"(?m)^Updating ({SHA})\.\.({SHA})\s*$")


def parse_remotes(text: str) -> Dict[str, Dict[str, str]]:
    """Read 'git remote -v' output into {remote name: {'fetch': url, 'push': url}}."""
    remotes: Dict[str, Dict[str, str]] = {}
    for name, url, kind in REMOTE_LINE_RE.findall(text):
        remotes.setdefault(name, {})[kind] = url
    return remotes


def grade_task6(ctx: Ctx) -> Task:
    """Task 6: a remote of your own, push -u, fetch and pull, a rejected push, pull --rebase, an annotated tag."""
    t = Task(6, "Your own remote, a rejected push and a release", 4, ctx.repo_mode)
    f = ctx.facts
    remotes = parse_remotes(ctx.step("6.1"))
    origin, upstream = remotes.get("origin", {}), remotes.get("upstream", {})
    s62 = ctx.step("6.2")
    rows = {r.name: r for r in parse_branch_list(s62)}
    t.check(1, "6.1 remote -v lists exactly origin (your bare repository, kestrel-remote.git) and upstream (the course repository), "
               "the same as the clone's settings; 6.2 push -u: '* [new branch]  main -> main', main tracks [origin/main]; "
               "ANSWER-6 is upstream; live repo: upstream/main is the course's last commit",
            lambda: set(remotes) == {"origin", "upstream"} and origin.get("fetch") == origin.get("push")
            and origin.get("fetch", "").rstrip("/").endswith("kestrel-remote.git") and upstream.get("fetch") == upstream.get("push")
            and upstream.get("fetch") != origin.get("fetch")
            and live(ctx, lambda: origin.get("fetch") == f.config_value("remote.origin.url")
                     and upstream.get("fetch") == f.config_value("remote.upstream.url")
                     and f.rev("refs/remotes/upstream/main") == f.base and f.config_value("branch.main.remote") == "origin"
                     and f.config_value("branch.main.merge") == "refs/heads/main")
            and has(s62, r"\* \[new branch\]\s+main -> main")
            and has(s62, r"(?i)branch 'main' set up to track (?:remote branch 'main' from 'origin'|'origin/main')")
            and has(s62, r"(?m)^To \S*kestrel-remote\.git$")
            and "main" in rows and rows["main"].current and re.search(r"\[origin/main[\]:]", rows["main"].rest) is not None
            and get_answer(ctx.text, 6).lower() == "upstream")
    s63, s64 = ctx.step("6.3"), ctx.step("6.4")
    ben1 = f.find("docs: add route plan note", email=BEN)
    ben2 = f.find("docs: add field test note", email=BEN)
    fetched = FETCH_RANGE_RE.search(s63)
    updating = UPDATING_RE.search(s63)
    local_subject = "chore: start version 0.3-dev"
    before = commit_sha(s64, local_subject, "main")
    t.check(1, "6.3 fetch printed '<old>..<new>  main -> origin/main' (<new> is Ben's commit), status says behind 'origin/main' by 1 "
               "commit and can be fast-forwarded, pull was a Fast-forward to that commit; 6.4 your commit is pasted and the push "
               "was rejected: '! [rejected]  main -> main (fetch first)'",
            lambda: fetched is not None and live(ctx, lambda: ben1 is not None and same_prefix(fetched.group(2), ben1.sha))
            and "behind 'origin/main' by 1 commit" in s63 and "can be fast-forwarded" in s63
            and updating is not None and "Fast-forward" in s63 and same_sha(updating.group(2), fetched.group(2))
            and bool(before) and has(s64, r"! \[rejected\]\s+main -> main \(fetch first\)") and "failed to push some refs" in s64)
    s65 = ctx.step("6.5")
    mine = f.find(local_subject)
    pushed = PUSH_RANGE_RE.search(s65)
    sub = graph_subjects(s65)
    t.check(1, "6.5 pull --rebase printed 'Successfully rebased and updated refs/heads/main.'; the graph is a straight line (your "
               "commit on Ben's 'docs: add field test note' on his first note); the push worked; ANSWER-7 is Ben's commit number; "
               "live repo: your commit sits directly on Ben's second commit with a NEW number (the rebase rewrote it)",
            lambda: "Successfully rebased and updated refs/heads/main." in s65
            and sub[:3] == [local_subject, "docs: add field test note", "docs: add route plan note"]
            and not has(s65, r"(?m)^[ ]*\|") and pushed is not None
            and live(ctx, lambda: mine is not None and ben2 is not None and same_prefix(pushed.group(2), mine.sha)
                     and f.is_ancestor(mine.sha, "refs/remotes/origin/main") and mine.parents == [ben2.sha]
                     and bool(before) and not same_prefix(before, mine.sha) and same_prefix(get_answer_sha(ctx.text, 7), ben2.sha)),
            why=lambda: "after 'pull --rebase' your commit must be on top of Ben's commit and have a different number than in 6.4")
    s66 = ctx.step("6.6")
    tag_object = f.raw_rev("refs/tags/v0.2.0")
    peeled = f.rev("refs/tags/v0.2.0")
    names = [x for x in lines(s66) if x.startswith("v")]
    answer = get_answer(ctx.text, 8).replace(",", " ").split()
    t.check(1, "6.6 git tag lists v0.1.0 and v0.2.0; the tag was pushed by name ('* [new tag]  v0.2.0 -> v0.2.0'); ls-remote shows "
               "your tag's real number and a second line ending in ^{}; ANSWER-8 is v1.4.3 v1.5.0 v2.0.0; live repo: v0.2.0 is "
               "annotated (message 'Second field release of Kestrel-1'), tagged by you, on a commit of main",
            lambda: names[:2] == ["v0.1.0", "v0.2.0"] and has(s66, r"\* \[new tag\]\s+v0\.2\.0 -> v0\.2\.0")
            and has(s66, r"refs/tags/v0\.2\.0\^\{\}") and answer == ["v1.4.3", "v1.5.0", "v2.0.0"]
            and live(ctx, lambda: bool(tag_object) and tag_object in s66 and peeled in s66
                     and f.git("cat-file", "-t", "refs/tags/v0.2.0").strip() == "tag"
                     and f.git("tag", "-l", "--format=%(contents:subject)", "v0.2.0").strip() == "Second field release of Kestrel-1"
                     and f.config_value("user.email") in f.git("tag", "-l", "--format=%(taggeremail)", "v0.2.0")
                     and f.is_ancestor(peeled, "refs/heads/main")))
    return t
