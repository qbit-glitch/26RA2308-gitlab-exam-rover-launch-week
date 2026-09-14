"""Ground truth about the student's repository. Read-only: never changes the repo and never uses the network."""
from __future__ import annotations

import os
import subprocess
from typing import Dict, List, NamedTuple, Optional, Set, Tuple

STAFF_SUBJECT = "chore: add lab exam assignment and grader"
GIT_TIMEOUT = 60
SEP = "\x1f"


class GitError(RuntimeError):
    """Raised when the repository is not set up the way the grader expects."""


class Commit(NamedTuple):
    """A commit with the fields the graders need."""

    sha: str
    author: str
    email: str
    subject: str
    parents: List[str]


def run_git_rc(repo: str, *args: str) -> Tuple[int, str]:
    """Run git in 'repo' and return (exit code, stdout); a git call that hangs is stopped and reported as 124."""
    env = dict(os.environ, LC_ALL="C", GIT_PAGER="cat", GIT_TERMINAL_PROMPT="0")
    try:
        proc = subprocess.run(["git", *args], cwd=repo, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, encoding="utf-8", errors="replace", timeout=GIT_TIMEOUT)
    except subprocess.TimeoutExpired:
        return 124, ""
    return proc.returncode, proc.stdout


def run_git(repo: str, *args: str) -> str:
    """Run git in 'repo' and return stdout ('' on failure)."""
    return run_git_rc(repo, *args)[1]


_FORMAT = SEP.join(["%H", "%an", "%ae", "%s", "%P"])


def _parse(raw: str) -> List[Commit]:
    """Turn 'git log --format=_FORMAT' output into commits."""
    out: List[Commit] = []
    for line in raw.splitlines():
        parts = line.split(SEP)
        if len(parts) == 5:
            out.append(Commit(parts[0], parts[1], parts[2], parts[3], parts[4].split()))
    return out


class Facts:
    """Everything the grader needs to know about the repository."""

    def __init__(self, repo: str) -> None:
        self.repo = repo
        if run_git_rc(repo, "rev-parse", "--verify", "-q", "refs/heads/main^{commit}")[0] != 0:
            raise GitError("branch main not found. Run the grader inside your clone of the lab repository.")
        log = _parse(run_git(repo, "log", "refs/heads/main", f"--format={_FORMAT}"))
        staff = [c for c in log if c.subject == STAFF_SUBJECT]
        if not staff:
            raise GitError(f"the starting commit '{STAFF_SUBJECT}' is not in the history of main. "
                           "Run the grader inside your clone of the lab repository (made with 'git clone').")
        self.base: str = staff[-1].sha
        self.published: List[Commit] = _parse(run_git(repo, "log", self.base, f"--format={_FORMAT}"))

    # -- the course history -------------------------------------------------------------
    def published_emails(self) -> Set[str]:
        """E-mail addresses of the people who wrote the course history."""
        return {c.email.lower() for c in self.published}

    def published_names(self) -> Set[str]:
        """Names of the people who wrote the course history."""
        return {c.author.lower() for c in self.published}

    # -- generic reads --------------------------------------------------------------------
    def git(self, *args: str) -> str:
        """stdout of a git command run in the clone ('' on failure)."""
        return run_git(self.repo, *args)

    def config_value(self, key: str) -> str:
        """Value of a repository-local config key ('' if unset)."""
        return run_git(self.repo, "config", "--local", "--get", key).strip()

    def rev(self, ref: str) -> str:
        """Full SHA of the commit 'ref' names, peeling tags ('' if it does not exist)."""
        return run_git(self.repo, "rev-parse", "--verify", "-q", f"{ref}^{{commit}}").strip()

    def raw_rev(self, ref: str) -> str:
        """Full SHA of the object 'ref' itself names (a tag object for an annotated tag; '' if none)."""
        return run_git(self.repo, "rev-parse", "--verify", "-q", ref).strip()

    def commit_exists(self, token: str) -> bool:
        """True if 'token' names a commit object in this repository."""
        return run_git_rc(self.repo, "cat-file", "-e", f"{token}^{{commit}}")[0] == 0

    def is_ancestor(self, ancestor: str, descendant: str) -> bool:
        """True if commit 'ancestor' is 'descendant' itself or part of its history."""
        return run_git_rc(self.repo, "merge-base", "--is-ancestor", ancestor, descendant)[0] == 0

    def file_at(self, ref: str, path: str) -> Optional[str]:
        """Content of 'path' at 'ref' (None if absent)."""
        code, out = run_git_rc(self.repo, "show", f"{ref}:{path}")
        return out if code == 0 else None

    def reflog(self, ref: str) -> List[str]:
        """Reflog messages of 'ref', newest first (empty if there is no reflog)."""
        return run_git(self.repo, "log", "-g", "--format=%gs", ref, "--").splitlines()

    def head_reflog(self) -> List[str]:
        """HEAD reflog messages, newest first."""
        return self.reflog("HEAD")

    def commit(self, sha: str) -> Optional[Commit]:
        """The commit 'sha' names (None if there is none)."""
        found = _parse(run_git(self.repo, "log", "-1", f"--format={_FORMAT}", sha, "--"))
        return found[0] if found else None

    def parents(self, sha: str) -> List[str]:
        """Full SHAs of the parents of 'sha' (empty for a root commit or an unknown commit)."""
        found = self.commit(sha)
        return found.parents if found else []

    def subject(self, sha: str) -> str:
        """Subject line of commit 'sha' ('' if unknown)."""
        found = self.commit(sha)
        return found.subject if found else ""

    def changes(self, sha: str) -> Dict[str, str]:
        """{path: status letter} a single-parent commit changed (renames are reported as 'R')."""
        out: Dict[str, str] = {}
        for line in run_git(self.repo, "diff-tree", "--no-commit-id", "--name-status", "-r", "-M", sha).splitlines():
            parts = line.split("\t")
            if len(parts) >= 2:
                out[parts[-1]] = parts[0][0]
        return out

    # -- finding commits ------------------------------------------------------------------
    def history(self, ref: str = "refs/heads/main") -> List[Commit]:
        """Commits reachable from 'ref' above the starting commit, newest first (merged branches included)."""
        return _parse(run_git(self.repo, "log", f"{self.base}..{ref}", f"--format={_FORMAT}"))

    def find(self, subject: str, ref: str = "refs/heads/main", email: Optional[str] = None) -> Optional[Commit]:
        """Newest commit above the starting commit reachable from 'ref' with this exact subject."""
        for commit in self.history(ref):
            if commit.subject == subject and (email is None or commit.email.lower() == email):
                return commit
        return None

    def find_anywhere(self, subject: str) -> Optional[Commit]:
        """Newest commit with this subject reachable from any branch, tag or remote-tracking branch."""
        for commit in _parse(run_git(self.repo, "log", "--all", f"--format={_FORMAT}")):
            if commit.subject == subject:
                return commit
        return None

    def first_parent_shas(self, ref: str = "refs/heads/main") -> List[str]:
        """Commits of the main line of 'ref' (first parents only), newest first."""
        return run_git(self.repo, "rev-list", "--first-parent", ref).split()

    def local_branches(self) -> List[str]:
        """Names of the local branches."""
        return run_git(self.repo, "for-each-ref", "--format=%(refname:short)", "refs/heads").split()

    def refs_containing(self, sha: str) -> List[str]:
        """Branches and tags that contain commit 'sha' (empty when it is on no branch)."""
        return run_git(self.repo, "for-each-ref", "--contains", sha, "--format=%(refname)").split()

    def working_tree_clean(self) -> bool:
        """True when 'git status --porcelain' prints nothing and no merge or rebase is in progress."""
        clean = run_git(self.repo, "status", "--porcelain").strip() == ""
        merging = run_git_rc(self.repo, "rev-parse", "-q", "--verify", "MERGE_HEAD")[0] == 0
        rebasing = any(os.path.exists(os.path.join(self.repo, run_git(self.repo, "rev-parse", "--git-path", name).strip()))
                       for name in ("rebase-merge", "rebase-apply"))
        return clean and not merging and not rebasing
