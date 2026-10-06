# Studio Kits

**Workflows for software, product, and scientific work.**

A catalog of installable [Constructor Studio](https://github.com/constructorfabric/studio) kits.
Kits add skills, workflows, artifact templates, and checks to your Studio project.
Each kit lives in its publisher's repository; this repository helps you find it.

[Browse kits](#software--product-development) · [Install a kit](#install-a-kit) · [Add your kit](CONTRIBUTING.md) · [Registry](registry.toml)

<!-- BEGIN CATALOG -->

## Software & Product Development

1. [**SDLC**](https://github.com/constructorfabric/studio-kit-sdlc) — Software delivery workflows from requirements and architecture to implementation and review. [`constructorfabric/studio-kit-sdlc`](https://github.com/constructorfabric/studio-kit-sdlc)
2. [**Competitive Analysis**](https://github.com/constructorfabric/studio-kits-pm) — Evidence-first competitive research for product discovery, positioning, and prioritization. [`constructorfabric/studio-kits-pm`](https://github.com/constructorfabric/studio-kits-pm)

## Science

1. [**Quantum Information**](https://github.com/omniscale-ai/studio-kit-qi) — Machine-checkable claims, certificates, and verification workflows for quantum information research. [`omniscale-ai/studio-kit-qi`](https://github.com/omniscale-ai/studio-kit-qi)
2. [**Spectro**](https://github.com/omniscale-ai/studio-kit-spectro) — Evidence-gated workflows for spectral analysis, model fitting, calibration, and scientific findings. [`omniscale-ai/studio-kit-spectro`](https://github.com/omniscale-ai/studio-kit-spectro)
3. [**Reference Audit**](https://github.com/constructorfabric/reference-audit) — Checks scientific references and flags citations that do not resolve to real publications. [`constructorfabric/reference-audit`](https://github.com/constructorfabric/reference-audit) · **Related tool**

<!-- END CATALOG -->

Reference Audit is a standalone tool. See its repository for setup and usage.

## Install a kit

From an existing Studio project with the `cfs` CLI installed:

```bash
cfs kit install omniscale-ai/studio-kit-spectro
cfs generate-agents
```

For a repository containing multiple kits, select one with `--kit`:

```bash
cfs kit install constructorfabric/studio-kits-pm --kit compete
cfs generate-agents
```

To pin a release or commit, add `--version <tag-or-sha>` to the install command.
Open the kit's README for its workflows, prerequisites, and usage examples.

## Publish your kit

Maintain your kit in your own public GitHub repository. Add a
`.cf-studio-kit.toml` manifest, README, license, and version, then submit a
pull request to this catalog.

Read the [submission guide](CONTRIBUTING.md) to add an entry to `registry.toml`
and regenerate the catalog. Publishers retain ownership and maintenance of their kits.

## About the catalog

The [registry](registry.toml) stores discovery metadata. Each kit's
`.cf-studio-kit.toml` defines its installable resources. The catalog lists above
are generated from the registry.

Registry statuses describe the publisher relationship:

| Status | Meaning |
| --- | --- |
| `official` | Maintained by the Constructor Studio project. |
| `verified-publisher` | Maintainers have verified the publisher's control of the repository. |
| `community` | A third-party listing without publisher verification. |

This is a catalog hosted at [NRGGIT/studio-kits](https://github.com/NRGGIT/studio-kits).
The `official` label refers to a kit's publisher; it does not imply that this catalog
is operated by Constructor. Third-party entries start as `community`.

Listing is for discovery. Catalog CI currently validates metadata and README consistency;
it does not run or audit external kits. Review a kit's source and requirements before use.
See [maintenance and validation](docs/maintenance.md) for the exact checks.

## Contribute

Add a kit, improve a description, or report a stale listing through a
[pull request](https://github.com/NRGGIT/studio-kits/pulls) or
[issue](https://github.com/NRGGIT/studio-kits/issues).
Contributions are welcome from any publisher.

The catalog's documentation and tooling use the [Apache License 2.0](LICENSE).
Linked kits retain their own licenses.
