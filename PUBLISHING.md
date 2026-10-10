# Publishing this repo to GitHub

Notes for the **repo owner** (consumers only need `INSTALL.md`).

## 1. Prerequisites

- `git` (2.30+)
- `gh` — GitHub CLI. On this machine it is installed **without admin rights** at:

  ```
  C:\Users\29480\AppData\Local\Programs\gh\bin\gh.exe
  ```

  and that `bin` directory has been added to the user `PATH` (open a **new** terminal for it
  to take effect). Verify with `gh --version`.

## 2. One-time: log in

```bash
gh auth login          # choose: GitHub.com -> HTTPS -> Login with a web browser
```

This stores a credential for `git push` as well (it configures the credential helper for you).

Optional — set your commit identity so the commit author is correct:

```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
# then re-author the existing commit:
git -C ~/.workbuddy-ai/skills/game-theory commit --amend --reset-author --no-edit
```

## 3. Create the remote and push (one command)

```bash
gh repo create game-theory --private \
  --source="$HOME/.workbuddy-ai/skills/game-theory" \
  --push
```

`gh` creates the private repo, adds it as `origin`, and pushes `main`. Afterwards the repo is at
`https://github.com/<your-user>/game-theory`.

If you prefer the web UI: create an **empty** private repo (no README / .gitignore / license),
then

```bash
cd ~/.workbuddy-ai/skills/game-theory
git remote add origin https://github.com/<your-user>/game-theory.git
git push -u origin main
```

## 4. Everyday updates

```bash
cd ~/.workbuddy-ai/skills/game-theory
git add -A
git commit -m "update: <what changed>"
git push
```

CI (`.github/workflows/test.yml`) runs the 37 invariant tests plus the examples on every push —
check the **Actions** tab. A red run means the skill is broken; fix before relying on it.

## 5. Pulling on another machine

```bash
git clone https://github.com/<your-user>/game-theory.git ~/.workbuddy-ai/skills/game-theory
```

Because the repo root **is** the skill folder, cloning installs it. `git pull` updates it.

## 6. Troubleshooting

| Symptom | Cause / fix |
|---|---|
| `InternetOpenUrl() failed. 0x80072efd` during `winget install GitHub.cli` | The environment's HTTP proxy returns `502` for `github.com` release downloads. Workaround used here: fetch the release asset through `api.github.com` (which the proxy allows) and unzip it — see §1. |
| `CONNECT tunnel failed, response 502` from `curl https://github.com/...` | Same proxy limitation. `api.github.com` and `objects.githubusercontent.com` are reachable; `github.com` is not. |
| `gh: command not found` right after install | The `PATH` change only applies to **new** terminals. Or call the full path. |
| `msiexec` exit code `67` | The MSI installer needs administrator rights. Use the portable `.zip` release instead. |
| Push asks for a password | GitHub no longer accepts account passwords. Use `gh auth login`, or a Personal Access Token with the `repo` scope. |
