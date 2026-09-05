# Starfarer for Homebrew

The tap prepares the desktop cask automatically after each verified release.
Until the first release is published, the install command is unavailable.

Install the Starfarer desktop and its bundled local planet daemon on Apple
silicon with macOS 13 or newer:

```sh
brew install --cask nsttt/starfarer/starfarer
open -a Starfarer
```

Previews may use ad-hoc signatures without Apple notarization. The cask states
when this applies. If macOS blocks the first launch, use **System Settings →
Privacy & Security → Open Anyway** after attempting to open Starfarer. See
[Apple's instructions](https://support.apple.com/en-us/102445). Homebrew keeps
quarantine enabled; the cask does not change system security settings.

On first launch, the app verifies and installs its bundled runtime under
`~/.local/share/starfarer/v1` and starts a per-user launchd service. Node and the
native helpers are included. No separate daemon formula or `brew services`
command is needed. macOS may ask for Local Network access when enrolling peers.

Linux moons require Apple's Rosetta support. If it is missing:

```sh
softwareupdate --install-rosetta
```

Closing the app leaves the daemon and sessions running. The launchd service
starts at login; it is not a system-wide service for other users.

## Upgrade

```sh
brew update
brew upgrade --cask nsttt/starfarer/starfarer
```

This replaces the desktop. The running daemon keeps its installed runtime so an
app upgrade cannot interrupt a session. Finish or jump away all local sessions,
quit the desktop, then select the new bundled runtime:

```sh
starfarer_cli="/Applications/Starfarer.app/Contents/Resources/runtime/bin/starfarer-planet"
"$starfarer_cli" service stop
"$starfarer_cli" install
"$starfarer_cli" service install
"$starfarer_cli" status
open -a Starfarer
```

Adjust the app path if you used Homebrew's `--appdir` option. Set
`STARFARER_PLANET_ROOT` for a non-default planet. Existing identities, enrollment,
session disks, and previous runtime copies remain in place.

## Uninstall

```sh
brew uninstall --cask nsttt/starfarer/starfarer
```

Uninstall removes the desktop. The independent daemon and planet data remain,
including with `--zap`, which removes only desktop caches and preferences.
To also stop the local service, finish or jump away its sessions and run
`"$starfarer_cli" service stop` using the app path above before uninstalling.

If the app is already gone, find the installed CLI from the runtime recorded in
the default planet's `runtime.json`:

```sh
starfarer_workspace=$(plutil -extract workspace raw -o - \
  "$HOME/.local/share/starfarer/v1/runtime.json")
starfarer_cli="$(dirname "$starfarer_workspace")/starfarer-planet"
"$starfarer_cli" service stop
```

Stopping the service does not archive sessions or delete their data. Keep the
planet directory and its recovery artifacts until any unfinished work has been
recovered.

## Tap maintenance

The update workflow checks the public release manifest hourly and can also run
manually. It validates the release URL and version, generates the cask, runs
Homebrew's checks, and fetches the DMG to verify its checksum before committing.
It refuses downgrades and changed checksums or signing modes for an existing version. No token
for the private source repository is needed.
