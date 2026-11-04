# YoloShellPlugins

Versioned plugin registry for [YoloShell](https://github.com/AgentsMesh/YoloShell),
modeled on the CocoaPods Specs repository. Each published plugin version is an
immutable spec under `Specs/<id>/<version>.json`; the spec records the exact
plugin manifest and the source repository, path, tag and commit.

## Layout

```text
Specs/
  web.client/
    0.1.0.json
scripts/
  validate.py
  check-lines.sh
```

## Spec fields

- `schema_version`: always `1`.
- `id`: dotted lowercase plugin id, for example `web.client`; `yolo.` is reserved.
- `version`: semver, for example `0.1.0`.
- `name`, `description`: must match the plugin manifest.
- `source.repository`: GitHub HTTPS repository containing the plugin.
- `source.path`: plugin directory inside that repository.
- `source.tag`: release tag for this version.
- `source.commit`: exact 40-character commit SHA.
- `manifest`: the complete `yolo-plugin.json` document for that version.

## Adding a version

1. Tag the plugin source repository for the new version.
2. Add `Specs/<id>/<version>.json` with the exact manifest from that tag.
3. Run `python3 -I scripts/validate.py` and `sh scripts/check-lines.sh`.
4. Open a pull request. Published version files are immutable; fix a release by
   publishing a new version, not by editing an existing spec.

## Current plugins

| Id | Version | Source |
| --- | --- | --- |
| `web.client` | `0.1.2` | [YoloShellWeb](https://github.com/AgentsMesh/YoloShellWeb) |
| `web.client` | `0.1.1` | [YoloShellWeb](https://github.com/AgentsMesh/YoloShellWeb) |
| `web.client` | `0.1.0` | [YoloShellWeb](https://github.com/AgentsMesh/YoloShellWeb) |

`web.client` 0.1.0 pinned a client-only source root; the client imports the
sibling `sdk/`, so an installed 0.1.0 plugin cannot start. Use 0.1.1 or newer.

## Install

Yolo's `yolo plugin install` consumes these specs:

```sh
yolo plugin install web.client --trust
yolo plugin install web.client --version 0.1.2 --trust
# a fork or test registry
yolo plugin install web.client --registry <git-url> --trust
```

The installer clones this registry, resolves the newest version unless
`--version` is given, clones the pinned source commit, verifies the spec against
the source manifest, copies the plugin into a private managed directory and
prints the source and digest. It requires the explicit `--trust` preview before
linking. Installing over a linked version stops and restarts a running plugin
when its manifest declares a `stop` action. `yolo plugin link <dir> --trust`
remains available for local plugin development. The web client is a Bun
process; `bun` must be on `PATH` when Yolo starts it.

## License

MIT. See [LICENSE](LICENSE).
