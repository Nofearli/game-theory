# Installation

`game-theory` is a plain skill folder: a `SKILL.md` plus supporting files. "Installing" it means
putting the folder where your agent looks for skills.

## 1. One-liner (recommended)

**Windows (PowerShell)**

```powershell
git clone https://github.com/<your-user>/game-theory.git "$env:USERPROFILE\.workbuddy-ai\skills\game-theory"
```

**macOS / Linux (bash)**

```bash
git clone https://github.com/<your-user>/game-theory.git ~/.workbuddy-ai/skills/game-theory
```

Replace `<your-user>` with the GitHub account that owns the repo.

## 2. Using the bundled install script

From a checkout of this repo:

```powershell
# Windows
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

```bash
# macOS / Linux
bash ./install.sh
```

The scripts copy the skill into the default skills directory (`~/.workbuddy-ai/skills/game-theory`)
and print the destination. Pass a different directory as the first argument to override:

```bash
bash ./install.sh /path/to/skills
```

## 3. Where skills live

| Agent | User-level skills directory | Project-level |
|---|---|---|
| WorkBuddy | `~/.workbuddy-ai/skills/` | `<project>/.workbuddy-ai/skills/` |
| Claude Code | `~/.claude/skills/` | `<project>/.claude/skills/` |
| Codex | `~/.codex/skills/` | `<project>/.codex/skills/` |

Use the user-level directory to have the skill available in every project.

## 4. Verify the installation

```bash
cd ~/.workbuddy-ai/skills/game-theory
python tests/run_tests.py        # expect: 37 passed, 0 failed
```

Requirements: Python 3.9+ with `numpy`, `scipy`, `matplotlib`.

```bash
pip install numpy scipy matplotlib
```

## 5. Updating

```bash
cd ~/.workbuddy-ai/skills/game-theory
git pull
```

## 6. Uninstalling

Delete the folder:

```bash
rm -rf ~/.workbuddy-ai/skills/game-theory          # macOS / Linux
```

```powershell
Remove-Item -Recurse -Force "$env:USERPROFILE\.workbuddy-ai\skills\game-theory"   # Windows
```

## 7. Using it without installing

You can also point an agent at the checkout directly — the skill is self-contained, so running
`examples/` or reading `SKILL.md` from anywhere works. Installing just makes it auto-discoverable.
