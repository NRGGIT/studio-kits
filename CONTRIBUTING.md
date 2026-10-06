# Add your kit

Studio Kits is a discovery catalog. You maintain the source, releases, and
documentation in your own repository. Contributions go through pull requests
to [NRGGIT/studio-kits](https://github.com/NRGGIT/studio-kits).

## Prepare your repository

Your kit repository should be public and include:

- A root `.cf-studio-kit.toml` manifest with a kit slug, name, explicit version,
  and declarations for all installable resources.
- A README explaining the audience, workflows, outputs, installation, and
  external requirements, including any credentials or scripts it uses.
- A license that clearly covers the kit's contents.
- A release or tag matching the published version, where possible.

For a repository with several kits, declare each kit in the root manifest using
its own `[[kits]]` entry. The registry's optional `kit` field must match that kit's slug.

Before submitting, run the Studio checks in your kit repository:

```bash
cfs validate-kits .
cfs kit normalize --dry-run . --json
```

If you include PDSL workflows or rules, also run `cfs pdsl validate` on those files.
Include the results and any relevant limitations in your pull request.

## Add a registry entry

Fork and clone this catalog. Add an entry to [registry.toml](registry.toml):

```toml
[[kits]]
id = "my-kit"
name = "My Kit"
description = "One sentence explaining the work this kit enables."
repository = "your-org/my-studio-kit"
publisher = "Your Organization"
categories = ["science", "data-analysis"]
status = "community"
```

Add `kit = "your-slug"` when selecting a kit from a repository containing several kits.
Use `owner/repository` for `repository`, without a URL or branch suffix.

Choose exactly one broad category: `software-product-development` or `science`.
Add specific tags to the same array using lowercase words separated by hyphens.
Use a unique, stable `id`; keep descriptions short and factual, without Markdown or
marketing claims. Use the same publisher name across that publisher's entries.

Start third-party submissions with `status = "community"`. Maintainers assign
`official` to Constructor-maintained kits and `verified-publisher` only after
reviewing evidence of repository control. Neither status is a source-code audit.

## Regenerate and validate

Use Python 3.11 or newer:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/catalog.py --write
python scripts/catalog.py --check
python -m unittest discover -s tests -v
```

Replace `python3.12` with your installed Python 3.11+ interpreter if necessary.
Only the README section between the catalog markers is regenerated. Edit the
registry to change a listing; edit the rest of the README directly.

## Open a pull request

Submit your registry change and regenerated README together. Include:

- The kit repository and release/tag, with the selected slug if needed.
- A short description of what the kit does and who it is for.
- Kit validation results and the repository's license.
- Your relationship to the publisher, with ownership evidence when requesting verification.

Catalog CI checks the registry and README. Maintainers review the external kit
repository, description, category, and publisher relationship before accepting a listing.

Sign off commits using your configured Git name and email:

```bash
git commit --signoff -m "catalog: add my-kit"
```

The sign-off records your certification under the
[Developer Certificate of Origin](https://developercertificate.org/).
Verify that every new commit contains a matching `Signed-off-by:` trailer before
pushing or opening a pull request.

## Submit a related tool

A useful tool without a Studio kit manifest can be proposed under
`[[related_tools]]`. Use the same discovery fields, but omit `kit` and `status`.
It will be labeled **Related tool** and will have no Studio installation command.
Maintainers review whether it belongs in the catalog.

## Improve an existing listing

Corrections, stale-link reports, and category improvements are welcome.
Use an [issue](https://github.com/NRGGIT/studio-kits/issues) to flag a problem,
or update the registry and regenerate the README in a pull request.
