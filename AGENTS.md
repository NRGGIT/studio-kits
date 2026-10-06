# Working on Studio Kits

- This repository is a discovery catalog; kit source belongs in publisher repositories.
- Edit `registry.toml` to change listings, then run `python scripts/catalog.py --write`.
- Preserve the README catalog markers. Do not edit generated listings directly.
- Use Python 3.11+ and the dependencies in `requirements-dev.txt`.
- Before completing changes, run `python scripts/catalog.py --check` and
  `python -m unittest discover -s tests -v`.
- Do not promote a third-party publisher to `verified-publisher` without documented
  repository ownership evidence and a maintainer decision.
- Always add a DCO sign-off to commits with `git commit --signoff` (or `-s`), using
  the configured Git name and email.
- Before pushing or creating a pull request, verify every new commit contains a
  matching `Signed-off-by:` trailer.
