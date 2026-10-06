# Catalog maintenance

## Repository structure

```text
studio-kits/
├── README.md                    # Public catalog and installation guide
├── registry.toml                # Discovery source of truth
├── CONTRIBUTING.md              # Submission workflow
├── LICENSE                     # Catalog documentation and tooling
├── AGENTS.md                    # Editing and commit requirements
├── requirements-dev.txt         # Local and CI validation dependencies
├── schema/registry.schema.json  # Schema for parsed TOML
├── scripts/catalog.py           # Metadata validation and README generation
├── tests/test_catalog.py        # CLI behavior checks
├── docs/
│   ├── maintenance.md           # This guide
│   └── task-kits-repo.md        # Original design vision
└── .github/
    ├── pull_request_template.md
    └── workflows/validate-kit-submission.yml
```

## Current checks

The schema validates registry version `1`, required fields, field types,
description length, GitHub repository references, slug format, allowed statuses,
and exactly one of the two broad categories. Specific category tags are open
lowercase slugs. Unknown fields are rejected to catch misspellings.

`scripts/catalog.py` additionally rejects duplicate IDs across kits and tools,
duplicate repository/kit pairs (repository names are case-insensitive), and
surrounding whitespace in display fields. It escapes display text when generating
Markdown. Listings include a clickable `owner/repository` label; publisher names
remain in the registry for discovery metadata. Entries appear in registry order within each category; related tools
follow native kits.

An omitted `kit` means that installation delegates kit selection to Studio.
For a multi-kit repository, always set `kit` so catalog consumers can identify the
specific kit to install.
The current checks cannot identify two differently expressed entries that select
the same upstream kit without inspecting its manifest.

CI runs metadata validation, checks that the generated README catalog matches,
and runs the CLI tests. It does not contact or execute external kit repositories,
check releases, parse kit manifests, validate resource paths, or verify publishers.

## Review external submissions

Maintainers should check that the repository is public, the root kit manifest
parses, the selected slug and version exist, and README and license files are
present. Review the submitted Studio validation results. Confirm that the
description and category accurately describe the kit. Related tools are reviewed
as standalone tools and are not required to have a kit manifest.

`official` means maintained by the Constructor Studio project, regardless of
which account hosts this catalog. For `verified-publisher`, record the ownership
evidence and the maintainer's decision in the listing PR. It verifies repository
control, not source quality. Otherwise use `community` for third-party kits.

## Update the catalog

Follow the environment setup in [CONTRIBUTING.md](../CONTRIBUTING.md), then run:

```bash
python scripts/catalog.py --write
python scripts/catalog.py --check
python -m unittest discover -s tests -v
```

`--write` and `--check` both validate first. Failed validation leaves the README
untouched. The script requires exactly one ordered pair of catalog markers and
preserves content outside them.

Each kit's license applies to that kit; the catalog license does not relicense
external sources. This repository stores links and metadata, not kit packages.

## Later phases

External repository checks can be added as a separate step for new or changed
listings. Read and validate manifests first. Running publisher scripts requires
a separate execution policy and isolation from credentials.

CLI discovery and a future static catalog can consume `registry.toml` without
changing the publishing model. They are not included in this first version.

The ignored `.local/preview/` directory is a local review aid, not a deployed
website. Its content can be regenerated or removed independently of the catalog.
