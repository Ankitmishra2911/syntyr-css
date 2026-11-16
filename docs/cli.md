# Optional Syntyr CLI (alpha.5 source candidate)

**Syntyr CSS never requires a CLI, Python, Node.js or application JavaScript.**
The developer-only CLI runs offline on Python 3.10+ and never executes registry
markup. It is distributed separately from the CSS ZIP.

## Run from the source tree

```sh
python3 scripts/syntyr_cli.py version
python3 scripts/syntyr_cli.py list --category blocks
python3 scripts/syntyr_cli.py add resource-workspace --project /path/to/app
python3 scripts/syntyr_cli.py add resource-workspace --project /path/to/app --apply
python3 scripts/syntyr_cli.py verify --project /path/to/app
python3 scripts/syntyr_cli.py check --semantic --format json path/to/index.html
python3 scripts/syntyr_cli.py check --semantic --fail-on warning path/to/index.html
```

The default add operation is a **read-only preview**. Installation requires
explicit `--apply`. It creates assets only under the project's
`syntyr/` directory and records SHA-256 hashes and installed items in
`syntyr.lock.json`. Repeated installs of identical assets are safe.
Modified or unexpected existing files are not overwritten. An installation
failure rolls back only unchanged files created by that invocation.

`syntyr verify` compares installed bytes with the lockfile, returning
exit code 0 when clean, 1 when content has drifted, or 2 for an invalid/
missing lockfile or command error. Resolve drift manually before adding items.
There is deliberately no force, upgrade, remote fetch, execute or delete command.
Manual customization is supported, but doing so breaks strict managed-file
verification until you intentionally reconcile the lockfile.

`syntyr check` delegates to the existing static HTML validator.
It does not render templates, validate a running application or inspect
JavaScript/bundler imports. Its diagnostics return 1 for errors, 0 for
warnings-only or clean files, 2 for invalid inputs. Keep CSS and contract
versions matched. Opt-in duplicate CSS diagnosis is being developed separately
in PR #174 and is not yet available in this CLI branch.

## Portable CLI ZIP

```sh
python3 scripts/package_cli.py /tmp/syntyr-cli.zip
unzip /tmp/syntyr-cli.zip
python3 syntyr-cli-0.3.0-alpha.5/scripts/syntyr_cli.py --help
```

The bundle includes the matching registry, Syntyr contract, version and Python
scripts; it runs from any directory without a source checkout or internet access.
The build fails if committed registry JSON differs from its canonical generator,
or the validator contract version differs from `VERSION`.
The ZIP is a **source candidate**, not a published release.

All file writes must be reviewed in the dry-run plan. No automated cross-version
upgrades are supported; installations from a different version are rejected.

## Limits

This is a local advisory tool, not a browser runtime dependency, a secure
multi-user installation service, or a full HTML accessibility audit. Project
directories are assumed to be controlled by the invoking developer; do not
run the installer against directories being concurrently manipulated by
untrusted processes.
