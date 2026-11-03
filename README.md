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
| `web.client` | `0.1.0` | [YoloShellWeb](https://github.com/AgentsMesh/YoloShellWeb) |

## Distribution boundary

Yolo's current `yolo plugin` CLI links a local plugin directory with
`yolo plugin link <dir> --trust`. This registry is the versioned distribution
index; an install command that consumes these specs is future work. The specs
remain useful for version history, source pinning and review.

## License

MIT. See [LICENSE](LICENSE).
