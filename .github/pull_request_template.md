## Catalog change

Describe the kit or listing correction, its intended audience, and category.

Repository:
Release/tag:
Kit slug (if selecting from a multi-kit repository):
Publisher relationship / ownership evidence:
License:

## Checks

- [ ] Updated `registry.toml` and regenerated the README with `python scripts/catalog.py --write`.
- [ ] Ran `python scripts/catalog.py --check` and `python -m unittest discover -s tests -v`.
- [ ] All new commits have a matching DCO `Signed-off-by:` trailer.

For a new native kit:

- [ ] Public repository has a root `.cf-studio-kit.toml`, README, license, and explicit kit version.
- [ ] Selected slug matches the manifest; installation instructions are documented.
- [ ] Ran `cfs validate-kits .` and `cfs kit normalize --dry-run . --json` in the kit repository.
- [ ] Ran PDSL validation if applicable.

Paste kit validation results and any limitations here. Related-tool submissions
do not require a Studio manifest or Studio validation results.
