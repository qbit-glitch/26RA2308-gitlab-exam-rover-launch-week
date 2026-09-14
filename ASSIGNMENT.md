# Git Lab Exam: Kestrel-1 Rover, Launch Week

**Course:** 26RA2308 Git for Software Development and Collaboration
**Covers:** Theory Modules I to V (Experiments 1 to 12). **Format:** the same as Experiments 7, 8 and 9
**Time allowed:** 90 minutes. **Marks:** 20

---

## The story

It is 09:00 on Monday at the Kestrel-1 rover lab and you have just joined the team. **Asha** writes the Python
firmware, **Ben** plans the routes and cuts the releases, **Chitra** tunes the camera detector. Release `v0.2` goes
out on Friday afternoon and the lab has three rules:

> **1. Nothing is lost: every change is a commit.  2. `main` receives work only through a branch.
> 3. A release is a tag, and nobody rewrites what is already shared.**

Your week is squeezed into ninety minutes. You set the project up and keep the field data out of it (Module I). You
stage and commit, and undo your own mistakes (Module II). You open branches, merge them, settle a conflict and rebase
(Module III). You share the work through a remote of your own, survive a rejected push, and tag the release
(Modules IV and V). Every command in this exam is a command from the theory modules: `git clone`, `git config`,
`.gitignore` and `git check-ignore`, `git rm --cached`, `git add -p`, `git commit -am`, `--amend`, `git mv`,
`git log --follow`, `git restore`, `git reset --hard`, `git reflog`, `git revert`, `git stash`, `git branch`,
`git switch`, detached HEAD, `git merge` (fast-forward, three-way, conflict, `--abort`), `git rebase`, `git remote`,
`git push -u`, `git fetch`, `git pull`, `git pull --rebase`, `git tag` and `git ls-remote`.

## What you need

`git` (version 2.23 or newer, for `git switch`), `python3` and `nano`. You need **no** GitHub account for this exam.
Check with `git --version && python3 --version && nano --version`. If your terminal does not print English
messages, run `export LC_ALL=C` first, because the grader reads what Git prints. If a long output opens in a pager
(a screen with `:` or `(END)` at the bottom), press `q` to leave it.

## How to edit a file with nano

Files are changed in two ways in this exam: with `nano`, when the step says `nano`, and with the shell lines
(`echo`, `printf`, `cat >>`) exactly as shown.

1. `nano <file>` opens the file (a new file is created when you save). The cursor starts at the **top**.
2. Type exactly the text shown, pressing `Enter` between the lines. Do **not** press `Enter` after the last line:
   nano ends the file with a line break by itself.
3. `Ctrl+K` **cuts the line the cursor is on** (the next line moves up under the cursor) and `↓` moves the cursor
   down one line. Steps that replace a line tell you exactly how often to press them.
4. Save with `Ctrl+O` and then `Enter` (that confirms the file name). Leave with `Ctrl+X`.

If nano says "Save modified buffer?", press `Y` and then `Enter`. If you made a mistake before saving, press
`Ctrl+X`, then `N`, and start again. Whenever the text shows `Your Full Name`, type your own name, exactly as in
`git config user.name`.

## Rules

1. Work **only inside your own clone** (`kestrel-exam`) and in the sibling folders the tasks create. The only place
   you push to is `origin`, the bare repository you make yourself in Task 6. Never push to `upstream`, and never
   use `--force` (or `-f`).
2. Use only the commands this handout shows. In particular `git reset` belongs to Task 3, and `git rebase` (also
   inside `git pull --rebase`) to Tasks 5 and 6. Do not use `git cherry-pick`.
3. Type the commands yourself. The grader checks that your pasted output matches what is really in your
   repository (your commit numbers, your branches, your tags), so output copied from a classmate is detected.
4. Keep the commit messages, branch names and the lines you type exactly as written.
5. **Files come and go when you switch.** `ASSIGNMENT.md` and `tests/grade.py` exist only on `main` and on branches
   made from its latest commit. When you stand on an old commit (Task 4) they disappear from the folder, and they
   come back when you return to `main`. Run the grader from `main`. While you stand on an old commit, change only the
   files a task tells you to, and read this handout from the PDF or from GitHub, not from the folder: otherwise Git
   may refuse to switch back to `main`.
6. The tasks build on each other, so do them in order. If you skipped one, the **catch-up box** at the start of a
   later task brings your clone to the state you need.

## How you hand in your work

1. In Task 1 you copy `submission/outputs.template.txt` to `submission/outputs.txt`.
2. After **each numbered step** (**1.1**, **1.2**, ...), paste what the terminal printed under the matching
   `--- N.M` line of `submission/outputs.txt`, replacing `(paste output here)`. Do not edit or delete the
   `=== TASK` and `--- N.M` lines. Where a step has several commands, paste the output of all of them, one after the
   other. Type your answers after the colon of the `ANSWER-n :` lines (the line just below each `# Qn` question).
   Any editor is fine for `submission/outputs.txt`, for example a second terminal with nano, or VS Code.
3. Fill in your name and registration number at the top of the file.
4. Run the automatic grader whenever you want to see where you stand (from branch `main`):

   ```bash
   python3 tests/grade.py
   ```

   It prints **PASS** or **FAIL** for every task, tells you exactly which check failed, and shows your score out of
   20. You can fix a mistake and run it again as often as you like. The grader never uses the internet: it reads
   your clone and your `outputs.txt`.
5. When you are done, show the final grader output to your instructor (it is also saved in
   `submission/results.txt`), and submit `submission/outputs.txt` as instructed. The file is not committed on
   purpose: `.gitignore` keeps it local.

## Time plan

| Task | Time on the clock | Topic | Suggested time | Marks |
|---|---|---|---|---|
| 1 | 09:00 | Arrive and keep the data out (Module I) | 8 min | 2 |
| 2 | 09:08 | Stage, commit and read the history (Module II) | 14 min | 4 |
| 3 | 09:22 | Undo, recover and shelve (Module II) | 12 min | 3 |
| 4 | 09:34 | Branches and merges (Module III) | 16 min | 4 |
| 5 | 09:50 | Conflict, abort and rebase (Module III) | 14 min | 3 |
| 6 | 10:04 | Your own remote, a rejected push and a release (Modules IV and V) | 16 min | 4 |
| | | Buffer for running the grader and fixing mistakes | 10 min | |

---

## Task 1: Monday 09:00, arrive and keep the data out (2 marks)

Get your own copy of the project, tell Git who you are, and look at where Git keeps its history. Then deal with
Chitra's field log, `data/raw/run_042.csv`, which she committed by accident: data stays on the laptop.

```bash
git clone https://github.com/qbit-glitch/26RA2308-gitlab-exam-rover-launch-week.git kestrel-exam
cd kestrel-exam
cp submission/outputs.template.txt submission/outputs.txt
git config user.name "Your Full Name"
git config user.email "your.email@example.com"
git config alias.tree "log --oneline --graph --decorate --all"
git config pull.rebase false
git config merge.ff true
git config merge.conflictstyle merge
```

Use your own real name and e-mail (not the placeholders above, and not one of the teammates'). Do **not** use
`--global` here: these settings are **local** to this repository, and the last three make sure that settings on
your machine cannot change what Git prints in this exam. Your instructor may give you a different clone URL.

* **1.1** Run `git config --local --list` and paste the output. This is the third level of configuration
  (system, global, **local**); the local one wins.
* **1.2** Run `ls .git` and paste the output. Then type your answer to `ANSWER-1` in the file: which folder inside
  `.git` holds all the commits?

Write the rules into `.gitignore`. A rule alone will not do the job: see why, then fix it properly.

```bash
printf '\n# Data and model weights\ndata/raw/\n*.csv\n' >> .gitignore
git check-ignore -v data/raw/run_043.csv
```

* **1.3** Paste the output of `git check-ignore -v`. It names the file, the line and the rule that ignores a
  **new** file. (`run_042.csv` is still tracked: a rule only stops new files.)

```bash
git rm --cached data/raw/run_042.csv
git status --short
ls data/raw
```

* **1.4** Paste the output of all three commands. `--cached` removes the file from Git but keeps it on your disk.
  Read the two status letters: ` M` is a change that is not staged, `D ` is a staged deletion.

```bash
git add .gitignore
git commit -m "chore: ignore raw data and stop tracking run_042"
```

* **1.5** Paste the output of the `git commit` command.

## Task 2: Monday 09:08, stage, commit and read the history (4 marks)

Asha asks for three small things in `src/controller.py`: a version label on the first line, a speed clamp at the
end, and a changelog. Make the two edits first. Open the file:

```bash
nano src/controller.py
```

Type this one line, press `Enter`, then press `Ctrl+K` **once** (this cuts the old first line, which is now the
second one), then save and exit:

```text
# Kestrel-1 controller (v0.2) - Your Full Name
```

Add the clamp at the end of the file:

```bash
cat >> src/controller.py <<'EOF'


def clamp(speed):
    """Keep the speed inside 0..MAX_SPEED."""
    return max(0, min(MAX_SPEED, speed))
EOF
```

Each commit should have one purpose, so stage only the first hunk. Git asks about each hunk: type `y` and `Enter`
for the first (the label), `n` and `Enter` for the second (the clamp). Then look at what is staged:

```bash
git add -p src/controller.py
git diff --staged
git status --short
```

* **2.1** Paste the output of all three commands (the hunks and the questions, the staged diff, and the status).
  Only the label is staged, and the file is listed with `MM` (changed in the index **and** changed again after it).

```bash
git commit -m "docs(control): label controller version"
```

* **2.2** Paste the output.

The clamp is a change to a tracked file, so `-a` can stage and commit it in one go:

```bash
git commit -am "feat(control): add speed clamp"
```

* **2.3** Paste the output.

You forgot the changelog. Add it **to the last commit** instead of making a new one (you have not pushed, so
rewriting is safe), and fix the message at the same time:

```bash
echo "- 0.2: motor speed clamp" > CHANGELOG.md
git add CHANGELOG.md
git commit --amend -m "feat(control): clamp motor speed to 0-255"
```

* **2.4** Paste the output of the `git commit` command. Amending makes a **new** commit with a new number.

Ben wants the team notes in a `docs` folder. Rename the file with Git, as one operation, and follow its history
across the rename:

```bash
mkdir docs
git mv NOTES.txt docs/team-notes.txt
git commit -m "refactor: move team notes into docs"
git log --oneline --follow -- docs/team-notes.txt
```

* **2.5** Paste the output of the `git mv`, the `git commit` and the `git log` commands (look for `rename`).
  Without `--follow` the log would stop at the rename.

## Task 3: Monday 09:22, undo, recover and shelve (3 marks)

Everybody makes mistakes; Git lets you undo them if you pick the right tool. Work on `main`.

**A change you do not want.** Add a bad line, look at it, throw it away:

```bash
echo "MAX_SPEED = 9999" >> src/controller.py
git status --short
git restore src/controller.py
git status --short
```

* **3.1** Paste the output of the two `git status --short` commands (the first shows the change, the second is
  empty).

**Two commits, the last one wrong.** Make them:

```bash
echo "turn_gain = 1.0" > params.txt
git add params.txt
git commit -m "feat(control): add turn gain parameter"
echo "turn_gain = 9.9" > params.txt
git commit -am "fix(control): raise turn gain to 9.9"
```

The 9.9 is far too high. Throw the commit away completely:

```bash
git reset --hard HEAD~1
git status --short
```

* **3.2** Paste the output. `--hard` moves `HEAD` back **and throws the files away**: the 9.9 is gone from the
  folder and from the log. There is no `--hard` undo, except the safety net of Git itself:

```bash
git reflog -5
```

* **3.3** Paste the output. `reflog` records every place `HEAD` has been. Find the line
  `commit: fix(control): raise turn gain to 9.9`, copy its number (the first column) and type it as `ANSWER-2`.

```bash
git reset --hard <SHA of ANSWER-2>
cat params.txt
```

* **3.4** Paste the output of both commands. You are back with 9.9. Now do the right thing for a commit that may
  already be shared: add a commit that cancels it, and leave the history alone.

```bash
git revert --no-edit HEAD
cat params.txt
```

* **3.5** Paste the output of both commands. (`--no-edit` keeps Git's own message so no editor opens.)

**Unfinished work.** Chitra needs you now, but you are halfway through a tuning change. Shelve it, come back, and
finish it:

```bash
echo "turn_gain = 3.0" > params.txt
git stash push -m "wip: tuning turn gain"
git stash list
git stash pop
git stash list
git commit -am "fix(control): set turn gain to 3.0"
```

* **3.6** Paste the output of the `git stash` and `git commit` commands. `pop` brings the changes back **and
  removes** the stash (the second list is empty).

## Task 4: Monday 09:34, branches and merges (4 marks)

Stay on `main` to begin with.

```bash
git branch -a
```

* **4.1** Paste the output. The names starting with `remotes/origin/` are Git's memory of the shared copy. Then
  type `ANSWER-3`: how many branches, **apart from main**, does the shared copy hold?

Ben needs a path planner, so it gets its own branch. Create it, commit a stub on it, and go back to `main` to see
that the stub is not there:

```bash
git switch -c feature/path-planning
echo "def plan(): pass" > tools/planner.py
git add tools/planner.py
git commit -m "feat(nav): add path planner stub"
git switch main
ls tools
```

* **4.2** Paste the output of the `git switch`, `git commit` and `ls` commands. Switching rebuilds your folder:
  `planner.py` is on one branch only.

Chitra needs last month's release. Check out the release tag directly. **Read rule 5 first:** the folder is about
to change, and you must change only the file this step names.

```bash
git switch --detach v0.1.0
echo "Reproduced the baseline - Your Full Name" > baseline-notes.txt
git add baseline-notes.txt
git commit -m "temp: experiment from old commit"
git switch -c experiment/detached-recovery
git log --oneline -2
```

* **4.3** Paste the output of all the commands that print something. You were on a commit, not on a branch: a
  **detached HEAD**, and a commit made there belongs to no branch until `switch -c` saves it. The number in the
  square brackets of the `git commit` line is the new commit; type it as `ANSWER-4`.

Merge day. First a feature that nobody else touched meanwhile:

```bash
git switch main
git switch -c feature/logging
echo "import logging" > src/logger.py
git add src/logger.py
git commit -m "feat: add logging import"
git switch main
git merge feature/logging
git branch -d feature/logging
```

* **4.4** Paste the output of the last two commands. Read the word `Fast-forward`: no new commit was made, `main`
  just slid forward. The branch is finished, so the safe delete `-d` is allowed.

Now a feature, **and** a change on `main` made in the meantime, so the two lines of work must be joined:

```bash
git switch -c feature/battery
echo "def battery(): pass" > src/battery.py
git add src/battery.py
git commit -m "feat: add battery monitor"
git switch main
echo "# v0.2 in progress" >> README.md
git commit -am "docs: note version 0.2"
git merge feature/battery -m "merge: battery"
```

* **4.5** Paste the output of `git merge`. It says `Merge made by the 'ort' strategy.` (an older Git says
  `'recursive'`).

```bash
git tree
git cat-file -p HEAD
```

* **4.6** Paste the output of both commands. The history forks and joins again: look for the `|\` line. `cat-file`
  shows the raw commit: a normal commit has one `parent` line, a merge commit has two. The first is where `main`
  was, the second is the tip of `feature/battery`. Type the **second** `parent` number as `ANSWER-5`.

## Task 5: Monday 09:50, conflict, abort and rebase (3 marks)

Chitra's branch `origin/fix/echo-timeout` changes the same line as Ben does: Ben wants the echo timeout at 40 ms,
Chitra at 30 ms. Git cannot choose between two edits of one line, so it stops and asks you. First Ben's change, on
`main`. Open the file:

```bash
nano src/limits.py
```

Type this one line, press `Enter`, then `Ctrl+K` **once** (it cuts the old first line), save and exit:

```text
SENSOR_TIMEOUT_MS = 40
```

```bash
git commit -am "perf(sensor): set echo timeout to 40 ms"
```

* **5.1** Paste the output of the `git commit` command.

```bash
git merge origin/fix/echo-timeout
git status
cat src/limits.py
```

* **5.2** Paste the output of all three commands. The merge is **supposed to stop** with `CONFLICT` and
  `Automatic merge failed`. Find `You have unmerged paths` and `both modified`. Git wrote both versions into the
  file, between markers: `<<<<<<< HEAD` (the line on `main`, Ben's 40), `=======`, then the line from Chitra's
  branch (30), then `>>>>>>> origin/fix/echo-timeout`. The markers are only text: if you commit them, they become
  part of the code.

The team decides to keep **Chitra's 30**, because her camera timing needs it. Resolve the file in nano:

```bash
nano src/limits.py
```

Type this one line and press `Enter` after it (the cursor is now at the start of the `<<<<<<<` line):

```text
# Indoor limit: keep Chitra's 30 ms (camera timing) - Your Full Name
```

Then press `Ctrl+K` **three times** (this cuts `<<<<<<< HEAD`, Ben's line and `=======`), press `↓` **once** (the
cursor is now on Chitra's line, so this moves it down to the `>>>>>>>` line) and press `Ctrl+K` **once** more. The
file must now be exactly these four lines. Save and exit.

```text
# Indoor limit: keep Chitra's 30 ms (camera timing) - Your Full Name
SENSOR_TIMEOUT_MS = 30
SENSOR_MAX_CM = 400
SENSOR_MIN_CM = 2
```

Test before you commit, check that no marker is left, tell Git the file is settled, and finish the merge:

```bash
python3 tests/test_rover.py
grep -c "<<<<<<<" src/limits.py
git add src/limits.py
git commit -m "merge: settle echo timeout at 30 ms"
```

* **5.3** Paste the output of the tests, of `grep -c` and of `git commit`. The tests must end with `OK`, and
  `grep -c` must print `0`.

A second conflict. Asha's lower indoor speed limit (5) collides with Chitra's fast mode (25) in `src/config.py`.
Ben says: "Fast mode waits until after the release." So do not resolve it: go back to exactly where you were.

```bash
git merge origin/feature/fast-mode
git merge --abort
git status
```

* **5.4** Paste the output of all three commands. The first stops with another `CONFLICT`; after `--abort` the
  status says `nothing to commit, working tree clean`. (`--abort` works only in the middle of a merge.)

Last, tidy a private branch with **rebase**: it replays your commits on top of the latest `main`.

```bash
git switch -c feature/lidar
echo "def lidar_scan(): pass" > src/lidar.py
git add src/lidar.py
git commit -m "feat(sensor): add lidar stub"
git switch main
echo "0.2-dev" > VERSION
git commit -am "chore: bump version to 0.2-dev"
git switch feature/lidar
git rebase main
git log --oneline --graph -4
```

* **5.5** Paste the output of `git rebase main` and `git log`. The rebase ends with `Successfully rebased and updated
  refs/heads/feature/lidar.` Your commit is a **copy** with a new number, in a straight line on top of
  `chore: bump version to 0.2-dev`.

```bash
git switch main
```

## Task 6: Monday 10:04, your own remote, a rejected push and a release (4 marks)

The code lived only on the lab laptop. It is time to share it, and you set up the shared copy yourself. You need no
website for this: a **bare** repository (a repository without a working folder) plays the part of GitHub. The
teammates' commits will arrive in it too.

> **Catch-up box: only if you skipped Task 2.** Run this line once. It does what Task 6 needs from Task 2. If you
> did Task 2, do **not** run it. There is nothing to paste for it.
>
> ```bash
> test -f docs/team-notes.txt || { mkdir -p docs; git mv NOTES.txt docs/team-notes.txt; git commit -m "refactor: move team notes into docs"; }
> ```

Work on `main` with a clean tree (`git status`). The clone's `origin` points at the **course** repository; renaming
it to `upstream` frees the name `origin` for **your own** repository:

```bash
git remote rename origin upstream
git init --bare ../kestrel-remote.git
git -C ../kestrel-remote.git symbolic-ref HEAD refs/heads/main
git remote add origin ../kestrel-remote.git
git branch -M main
git remote -v
```

* **6.1** Paste the output of `git remote -v`. Each remote is listed twice (fetch and push): `upstream` is the course
  repository, `origin` is yours.

```bash
git push -u origin main
git branch -vv
```

* **6.2** Paste the output of both commands. `* [new branch]` means your repository did not have `main` yet. The
  option `-u` makes your local `main` remember that it goes with `origin/main`: it is the word in square brackets.
  Then type `ANSWER-6`: which remote name now points to the **course** repository?

Ben works from his own laptop and pushes a note to the shared copy. (These lines play Ben: a second clone, his
identity, one commit and one push.)

```bash
git clone ../kestrel-remote.git ../teammate
git -C ../teammate config user.name "Ben Iyer"
git -C ../teammate config user.email "ben@kestrel.example"
echo "- Ben: route plan v2 is ready" >> ../teammate/docs/team-notes.txt
git -C ../teammate commit -am "docs: add route plan note"
git -C ../teammate push origin main
```

Your laptop does not know yet. **Look** before you **take**: `git fetch` downloads what the remote has and updates
`origin/main`, but it does not touch your files or your `main`. Then `git pull` (a fetch followed by a merge)
takes it.

```bash
git fetch origin
git status
git pull origin main
```

* **6.3** Paste the output of all three commands. Find the line `<old>..<new>  main -> origin/main` (Ben's commit
  arriving), `behind 'origin/main' by 1 commit, and can be fast-forwarded`, and then `Fast-forward`.

Ben pushes a second note. **Do not** run `git fetch` or `git pull` yet: your laptop has no idea. You make your own
commit meanwhile, in a different file, so nothing can clash, and push it:

```bash
echo "- Ben: field test on Friday" >> ../teammate/docs/team-notes.txt
git -C ../teammate commit -am "docs: add field test note"
git -C ../teammate push origin main
echo "0.3-dev" > VERSION
git commit -am "chore: start version 0.3-dev"
git push origin main
```

* **6.4** Paste the output of your `git commit` and `git push` (the lines that play Ben print nothing you need). The
  push is **supposed to be rejected**: `! [rejected]` and `(fetch first)`. The shared copy has a commit that you do
  not have, and Git will not overwrite it. Never "fix" this with `--force`.

The right answer: bring Ben's commit down, and put your commit **on top of it**. `--rebase` replays your commit after
Ben's, so history stays one straight line. (Your commit is not pushed yet, so rewriting it breaks nobody.)

```bash
git pull --rebase origin main
git log --oneline --graph -4
git push origin main
```

* **6.5** Paste the output of all three commands. The rebase ends with `Successfully rebased and updated
  refs/heads/main.`; your commit is on top, with Ben's two notes just under it, and it has a **new number**: a rebase
  makes a new commit. This time the push works: `<old>..<new>  main -> main`. Then type `ANSWER-7`: the commit
  number of Ben's commit `docs: add field test note` (see the log).

Release time: a release is a tag. A **lightweight** tag is just a name on a commit; an **annotated** tag (`-a`) also
stores who made it, when, and why, and releases deserve that. `git push` skips tags: you send a tag by name.

```bash
git tag -a v0.2.0 -m "Second field release of Kestrel-1"
git tag
git push origin v0.2.0
git ls-remote --tags origin
```

* **6.6** Paste the output of all four commands (`git tag -a` prints nothing). `git tag` lists your tag and the
  old `v0.1.0`; `git ls-remote` asks the shared copy: it holds your tag, and for an annotated tag a second line
  ending in `^{}` (the commit it points to). Then type `ANSWER-8`: following Semantic Versioning, you are at
  `v1.4.2` and make (a) a bug fix, (b) a new compatible feature, (c) a breaking change. Give the three next
  versions, separated by spaces.

## Finish

```bash
git switch main
python3 tests/grade.py
```

You want to see `PASS` for all six tasks and `TOTAL: 20/20`. Anything marked `FAIL` is listed with the reason; fix
it and run the grader again. Run it from `main`.

## Marks

| Task | Marks | How it is checked |
|---|---|---|
| 1 | 2 | your identity is set in the clone and matches your pasted config; `ls .git` and the answer; the `.gitignore` rule, `rm --cached` and a commit that changes only `.gitignore` and removes `run_042.csv` from Git |
| 2 | 4 | `add -p` with two hunks and a staged diff holding only the label; both commits; the amend (the reflog shows it, the commit holds `CHANGELOG.md`); the rename and `--follow` |
| 3 | 3 | `restore` and `reset --hard`; the `reflog` answer and the recovery; a real revert commit and the stash round trip (no stash left, `params.txt` = 3.0) |
| 4 | 4 | the branches, the planner commit on its own branch; the detached commit saved on a branch (one answer); a real fast-forward and a merge commit with the right two parents; the graph, `cat-file` and one answer |
| 5 | 3 | the conflict is pasted; the resolved file passes the tests and keeps 30, and the merge commit has the right parents; the abort left `main` untouched and the rebased branch is a straight line |
| 6 | 4 | the two remotes, `push -u` and one answer; `fetch`, `status`, `pull` and the rejected push; the rebase, your commit really on top of Ben's with a new number, and one answer; the annotated tag really exists, was pushed, and one answer |

A task shows **PASS** only when every check in it passes, and you earn marks for each check that passes even if the
task as a whole fails. Each mark covers one or two steps: a mark is earned only when **all** the parts of its check
are right.

## If something goes wrong

* **A step printed nothing.** Some commands print nothing when they work (`git branch <name>`, `git mv`, `git restore`).
  That is normal: paste the output of the other commands of the step, and leave out the silent one.
* **`nothing to commit` after a nano edit.** You probably did not save: reopen the file and use `Ctrl+O`, `Enter`,
  `Ctrl+X`. Or the file is new and needs `git add` first.
* **An editor opened and asked for a commit message.** You left out `-m "..."`. Save and exit (nano: `Ctrl+O`, `Enter`,
  `Ctrl+X`; vim: `Esc`, then `:wq` and `Enter`). Then fix the message with `git commit --amend -m "<the message of the
  step>"` (before you push).
* **`git add -p` (2.1) asked something else, or you answered wrongly.** Type `q` and `Enter` to quit, run
  `git restore --staged src/controller.py` and start 2.1 again.
* **`git switch` says your changes would be overwritten.** Commit your work first, or shelve it with `git stash`, then
  switch.
* **`tests/grade.py` or `ASSIGNMENT.md` is missing.** You are standing on an old commit. Run `git switch main`.
* **The merge in 5.2 did not stop with a conflict.** Step 5.1 was not done (or not committed) before the merge. Run
  `git log --oneline -3` and read it.
* **The merge went wrong and you want to start it again.** While a merge is in progress, `git merge --abort` puts
  everything back as it was before that merge. Then run the merge command again.
* **You saved the wrong text in nano during the conflict.** Run `git checkout --merge src/limits.py`: it rewrites the file
  with the conflict markers, so you can edit it again.
* **`git commit` says `Committing is not possible because you have unmerged files`.** You forgot
  `git add src/limits.py`. Run it, then commit again.
* **`python3 tests/test_rover.py` prints `FAIL` or an error.** A marker line left in `src/limits.py`, or two
  `SENSOR_TIMEOUT_MS` lines, mean the nano step was not finished. Open the file again and remove them.
* **A commit landed on the wrong branch.** Do not try to undo it with `reset` outside Task 3. Tell your instructor; the
  grader will show it.
* **`fatal: not a git repository`.** You are not inside your clone: `cd kestrel-exam` (or `cd ..` from a sibling folder).
* **Step 6.2 is rejected.** `../kestrel-remote.git` already existed with other work. Delete the folder
  (`rm -rf ../kestrel-remote.git`) and run the set-up lines of Task 6 again.
* **Step 6.4 was not rejected.** You ran `git fetch` or `git pull` after Ben's second commit. Make a new commit (change
  `VERSION` again with a different line) and continue; you lose only the check that reads the rejection.
* **`git pull --rebase` stops and says `CONFLICT`.** You changed a file that Ben changed (`docs/team-notes.txt`). Run
  `git rebase --abort`, then `git status` and ask your instructor.
* **You made a mistake early on and everything is tangled.** Delete the folders `kestrel-exam`, `kestrel-remote.git`
  and `teammate`, clone again and redo the tasks (your pasted outputs must be produced in the new clone).
