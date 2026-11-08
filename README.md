# hdots

Default dotfiles for [Hafnium](https://github.com/euandeas/hafnium), managed with
[mise dotfiles](https://mise.jdx.dev/dotfiles.html). It plays the role
[zdots](https://github.com/zirconium-dev/zdots) plays for Zirconium, but uses mise
instead of chezmoi.

## How it works

mise merges config layers. A more local layer replaces an entry with the same target:

```
/etc/mise/conf.d/hafnium.toml     ← system layer   (this repo, shipped as the hafnium-dots RPM)
~/.config/mise/config.toml        ← global layer   (your personal dotfiles; wins)
```

The RPM installs:

| Path | What |
|---|---|
| `/etc/mise/conf.d/hafnium.toml` | The `[dotfiles]` entries (see [`mise/hafnium.toml`](mise/hafnium.toml)) |
| `/usr/share/hafnium/dots/` | Default file contents ([`dots/`](dots)) |
| `/usr/bin/hafnium-dots` | Wrapper: `apply` (missing only), `reset <target>`, `reset-all`, `status` |
| `hafnium-dots.service` (user) | Runs `hafnium-dots apply` at login, before niri starts |

There are two kinds of entry:

- **Managed** entries are symlinks into `/usr/share/hafnium/dots`, so they follow
  `dnf upgrade`. Only `~/.config/niri/config.kdl` is managed. It includes Hafnium's
  defaults, then DMS's generated files, then **`~/.config/niri/local.kdl`**, which wins.
- **Seed** entries use `mode = "copy"` with `create_if_missing = true`. They're
  written once and then they're yours: `~/.config/niri/local.kdl`,
  `~/.config/ghostty/config`, and two DMS files:
  `~/.config/dms/settings.json` selects the Flexoki theme shipped at
  `/usr/share/hafnium/themes/flexoki.json`, and `~/.local/state/dms/session.json`
  sets dark mode with the Flexoki orb wallpapers in `/usr/share/backgrounds/hafnium/`,
  which switch with light/dark mode. Both DMS files are partial: DMS fills in
  its own defaults for everything else.

Keybinds come from DMS itself: on first login `hafnium-dots apply` runs
`dms setup binds` (and `alttab`, `layout`, `windowrules`, `cursor`) for any
`~/.config/niri/dms/*.kdl` file that's missing. DMS manages them from its settings
UI after that. Hafnium only adds Mod+E for Nautilus.

`hafnium-dots apply` deploys only targets in the `missing` state. A target in the
`differs` state means you changed it or a file is in the way, so it's skipped.
That's the same idea as Zirconium's `yes s | chezmoi apply`.

## Overriding a default

Put an entry with the same target in your own `~/.config/mise/config.toml`:

```toml
[dotfiles]
"~/.config/ghostty/config" = { source = "ghostty/config" }       # replaces Hafnium's seed
"~/.config/niri/config.kdl" = { source = "niri/config.kdl" }     # replaces the managed entrypoint
```

Turn off an entry without replacing it:

```toml
[dotfiles]
"~/.config/ghostty/config" = { enabled = false }
```

To make changes for every user on a machine, edit `/etc/niri/local.kdl`.

## Building

[`.github/workflows/check.yml`](.github/workflows/check.yml) runs Hafnium's checks
against each commit here. It builds `hafnium-dots`, dry-runs the install, deploys
these dotfiles in a throwaway `$HOME` (DMS defaults included) and runs `niri validate`.

The [hafnium](https://github.com/euandeas/hafnium) repo's *Build package repo*
workflow builds and publishes `hafnium-dots` to `https://euandeas.github.io/hafnium/repo/`.
After a push to `main`, this repo triggers it if the `HAFNIUM_DISPATCH_TOKEN` secret
is set: a fine-grained token with **Actions: Read and write** on `euandeas/hafnium`.
Otherwise it runs nightly, or by hand:

```sh
gh workflow run repo.yml -R euandeas/hafnium
```

To build the RPM locally:

```sh
make srpm outdir=out && rpmbuild --rebuild out/*.src.rpm
```

## Credits

Inspired by [zdots](https://github.com/zirconium-dev/zdots). Keybinds are DMS's own
defaults, generated on the machine.
