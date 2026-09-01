# Using Git with SSH on Raspberry Pi (GitHub)

GitHub no longer accepts account passwords for Git operations over HTTPS. This guide sets up SSH key authentication instead, which is faster and doesn't require re-entering credentials.

## 1. Generate an SSH Key

On the Raspberry Pi:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

- Press **Enter** to accept the default save location (`~/.ssh/id_ed25519`)
- Press **Enter** twice more to skip a passphrase, or set one for extra security
  - If you set a passphrase, you'll need to enter it on each push/pull unless you use `ssh-agent`

## 2. Copy the Public Key

```bash
cat ~/.ssh/id_ed25519.pub
```

Select and copy the full output line (starts with `ssh-ed25519 AAAA...`).

## 3. Add the Key to GitHub

1. In a browser, go to **github.com → Settings → SSH and GPG keys → New SSH key**
2. **Title:** something identifiable (e.g. `RPi5 Robotics Lab`)
3. **Key type:** Authentication Key
4. **Key:** paste the copied line
5. Click **Add SSH key**

## 4. Test the Connection

```bash
ssh -T git@github.com
```

- First connection will ask to confirm the host fingerprint — type `yes`
- Successful output looks like:
  ```
  Hi <your-username>! You've successfully authenticated, but GitHub does not provide shell access.
  ```

## 5. Set Your Git Identity (One-Time Per Machine)

Before you can commit, Git needs to know who you are. If you skip this, `git commit` will fail with `Author identity unknown`.

```bash
git config --global user.email "your_email@example.com"
git config --global user.name "Your Name"
```

- Use the same email as your GitHub account so commits link to your profile
- `--global` sets this for all repos on this machine; omit it to set an identity for just the current repo

## 6. Clone a Repository via SSH

Use the **SSH URL** (not the HTTPS one) — found on GitHub via **Code → SSH** tab on the repo page:

```bash
git clone git@github.com:username/repository.git
```

To clone into the *current* (already-created) folder instead of a new subfolder:

```bash
git clone git@github.com:username/repository.git .
```

> ⚠️ The target folder must be empty when cloning with a trailing `.`

## 7. Verify the Remote Uses SSH

After cloning (or for existing repos originally cloned via HTTPS):

```bash
git remote -v
```

Expected output:

```
origin  git@github.com:username/repository.git (fetch)
origin  git@github.com:username/repository.git (push)
```

If it shows an `https://` URL instead, switch it to SSH:

```bash
git remote set-url origin git@github.com:username/repository.git
```

## Quick Reference

| Task | Command |
|---|---|
| Generate SSH key | `ssh-keygen -t ed25519 -C "email"` |
| Show public key | `cat ~/.ssh/id_ed25519.pub` |
| Test GitHub auth | `ssh -T git@github.com` |
| Set Git identity | `git config --global user.email "email"` / `git config --global user.name "name"` |
| Clone repo | `git clone git@github.com:user/repo.git` |
| Check remote URL | `git remote -v` |
| Fix remote to SSH | `git remote set-url origin git@github.com:user/repo.git` |
| Set merge as default pull strategy | `git config pull.rebase false` |

## 8. Resolving Divergent Branches on Pull

If `git pull` fails with `fatal: Need to specify how to reconcile divergent branches`, it means your local branch and the remote branch have both moved forward independently (e.g. you committed locally while the remote also had new commits pushed).

For a solo/lab repo, the simplest fix is to default to a merge:

```bash
git config pull.rebase false
git pull
```

This may open your default text editor (often `nano`) to confirm a merge commit message — save and exit:
- In `nano`: press `Ctrl+O`, `Enter`, then `Ctrl+X`

**Alternative — rebase** (cleaner, linear history, but rewrites local commits on top of remote ones):
```bash
git config pull.rebase true
git pull
```

Add `--global` to either command to set it as the default for all repos on this machine, not just the current one:
```bash
git config --global pull.rebase false
```



- **Prompted for username/password on clone** → You used the HTTPS URL by mistake. Re-check it starts with `git@github.com:`, not `https://github.com/`.
- **"Host key verification failed"** → The SSH host key changed (common after reinstalling/reflashing the Pi's OS or reconnecting to a different device on the same IP). Clear the stale entry with `ssh-keygen -R <hostname-or-ip>` and reconnect.
- **Permission denied (publickey)** → The key wasn't added to GitHub, or you're using the wrong key. Re-run `cat ~/.ssh/id_ed25519.pub` and confirm it matches what's saved in GitHub settings.
- **"Author identity unknown" on commit** → Git identity isn't set on this machine yet. Run the `git config --global user.email`/`user.name` commands from Step 5.
- **"Need to specify how to reconcile divergent branches" on pull** → Local and remote branches both have new commits. Run `git config pull.rebase false` then `git pull` (see Step 8).
