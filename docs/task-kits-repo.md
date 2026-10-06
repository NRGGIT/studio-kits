# Constructor Studio Kits

Constructor Studio can be extended with **kits**: installable packages that add domain-specific workflows, skills, artifact types, templates, validation rules, scripts, and deterministic checks.

A kit is developed and maintained in its own GitHub repository. The Studio Kits catalog provides a central place to discover available kits without moving kit source code into a central repository.

The proposed model is intentionally lightweight:

```text
Kit repository
    ↓
.cf-studio-kit.toml
    ↓
GitHub release / tag
    ↓
Pull Request to Studio Kits catalog
    ↓
Catalog validation
    ↓
README / registry / CLI / future website
```

The kit itself always remains in the publisher's repository.

---

# Catalog

## Software & Product Development

1. [**SDLC**](https://github.com/constructorfabric/studio-kit-sdlc) — End-to-end software delivery workflows from requirements and architecture to implementation and review. **[Constructor]**
2. [**Competitive Analysis**](https://github.com/constructorfabric/studio-kits-pm) — Evidence-first competitive research for product discovery, positioning, and prioritization. **[Constructor]**

## Science

1. [**Quantum Information**](https://github.com/omniscale-ai/studio-kit-qi) — Machine-checkable claims, certificates, and verification workflows for quantum information research. **[Omniscale AI]**
2. [**Spectro**](https://github.com/omniscale-ai/studio-kit-spectro) — Evidence-gated workflows for spectral analysis, model fitting, calibration, and scientific findings. **[Omniscale AI]**
3. [**Reference Audit**](https://github.com/constructorfabric/reference-audit) — Verifies scientific references and detects citations that do not resolve to real publications. **[Constructor]**

> `reference-audit` is currently a standalone scientific tool rather than a native Constructor Studio kit. It can remain in the catalog as a related tool, or become a full kit later by adding a valid `.cf-studio-kit.toml`.

---

# Catalog Principles

The catalog should be:

- easy to browse directly on GitHub;
- easy for third-party authors to contribute to;
- machine-readable;
- independent of the GitHub organization that owns a kit;
- usable by the CLI later;
- usable by a future web catalog without redesigning the publication model;
- lightweight enough that no marketplace backend is required initially.

The catalog should **not host kit source code**.

Instead:

```text
constructorfabric/studio-kits
        │
        ├── README.md
        ├── registry.toml
        └── schema/
             registry.schema.json

External kit repositories
        │
        ├── constructorfabric/studio-kit-sdlc
        ├── constructorfabric/studio-kits-pm
        ├── omniscale-ai/studio-kit-qi
        └── omniscale-ai/studio-kit-spectro
```

The central repository acts only as an index.

---

# Recommended Repository

A dedicated repository could be created:

```text
github.com/constructorfabric/studio-kits
```

Suggested structure:

```text
studio-kits/
├── README.md
├── registry.toml
├── CONTRIBUTING.md
├── schema/
│   └── registry.schema.json
└── .github/
    └── workflows/
        └── validate-kit-submission.yml
```

Responsibilities:

- `README.md` — human-readable catalog;
- `registry.toml` — machine-readable source of truth for discovery;
- `CONTRIBUTING.md` — rules for submitting a kit;
- `registry.schema.json` — registry validation;
- GitHub Actions — validate Pull Requests automatically.

---

# Why Not Use Only README.md

A Markdown-only list is sufficient while there are only a few kits, but it becomes limiting once Studio needs:

- CLI search;
- categories;
- filtering;
- publisher information;
- version compatibility;
- kit status;
- web pages;
- automated validation;
- automatic catalog generation.

Therefore the recommended model is:

```text
registry.toml
      │
      ├──→ README.md
      ├──→ cfs kit search
      └──→ future /kits website
```

`registry.toml` should eventually become the source of truth.

The README can be generated automatically from it.

---

# Registry Format

The registry should contain **discovery metadata only**.

It should not duplicate every resource from `.cf-studio-kit.toml`.

Example:

```toml
registry_version = "1"

[[kits]]
id = "sdlc"
name = "SDLC"
description = "Artifact-first software delivery from requirements to implementation."
repository = "constructorfabric/studio-kit-sdlc"
publisher = "Constructor"
categories = ["software-development", "product", "architecture"]
status = "official"

[[kits]]
id = "competitive-analysis"
name = "Competitive Analysis"
description = "Evidence-first competitive research for product discovery and prioritization."
repository = "constructorfabric/studio-kits-pm"
kit = "compete"
publisher = "Constructor"
categories = ["product-management", "competitive-intelligence"]
status = "official"

[[kits]]
id = "quantum-information"
name = "Quantum Information"
description = "Machine-checkable claims and certificate workflows for quantum information research."
repository = "omniscale-ai/studio-kit-qi"
publisher = "Omniscale AI"
categories = ["science", "quantum-information", "verification"]
status = "verified-publisher"

[[kits]]
id = "spectro"
name = "Spectro"
description = "Evidence-gated workflows for spectral fitting, calibration, and scientific findings."
repository = "omniscale-ai/studio-kit-spectro"
publisher = "Omniscale AI"
categories = ["science", "spectroscopy", "data-analysis"]
status = "verified-publisher"
```

For a multi-kit repository:

```toml
[[kits]]
id = "competitive-analysis"
name = "Competitive Analysis"
repository = "constructorfabric/studio-kits-pm"
kit = "compete"
publisher = "Constructor"
categories = ["software-product-development"]
status = "official"
```

The optional `kit` field identifies the specific kit inside a multi-kit repository.

---

# Kit Manifest

Each installable kit should have a canonical:

```text
.cf-studio-kit.toml
```

Constructor Studio already supports this format, so it should remain the package-level source of truth.

Example:

```toml
manifest_version = "1.0"

[[kits]]
slug = "my-kit"
name = "My Kit"
version = "1.0.0"
```

The manifest should define the resources installed by the kit.

For example:

```toml
[[kits.resources]]
id = "analysis_workflow"
kind = "skill"
source = "workflows/analyze.md"
install_path = "workflows/analyze.md"
type = "file"
user_modifiable = false
public = true
description = "Run the main analysis workflow"
```

The kit manifest describes **what is installed**.

The registry describes **how the kit is discovered**.

These are different responsibilities.

---

# Recommended Discovery Metadata in Kit Manifests

The current manifests already contain installation metadata such as:

- slug;
- name;
- version;
- resources.

It would be useful to optionally add discovery metadata directly to the kit manifest.

Example:

```toml
manifest_version = "1.0"

[[kits]]
slug = "studio-kit-qi"
name = "Constructor Studio Quantum Information Kit"
version = "1.0.0"

description = """
Machine-checkable impossibility claims and
certificate-based workflows for quantum information.
"""

authors = ["Omniscale AI"]
license = "Apache-2.0"

categories = [
  "science",
  "quantum-information",
  "verification"
]

studio_version = ">=1.3"

homepage = "https://github.com/omniscale-ai/studio-kit-qi"
```

This makes it possible for the catalog to automatically validate or import metadata.

---

# Permissions and Capabilities

If kits are able to execute scripts, tools, or external commands, the manifest should eventually expose these capabilities.

For example:

```toml
permissions = [
  "shell"
]
```

Potential future capabilities could include:

```toml
permissions = [
  "shell",
  "network",
  "filesystem-write"
]
```

This should not necessarily be implemented immediately, but it is useful to design for it early.

A user installing a third-party kit should be able to understand whether the kit:

- only provides Markdown workflows;
- runs local scripts;
- writes files;
- accesses external services;
- requires credentials;
- invokes external tools.

---

# Recommended Kit Repository Structure

A typical standalone kit repository:

```text
my-studio-kit/
├── .cf-studio-kit.toml
├── README.md
├── LICENSE
├── artifacts/
├── workflows/
├── scripts/
└── tests/
```

Not all directories are required.

`.cf-studio-kit.toml` determines what actually belongs to the installable package.

For a multi-kit repository:

```text
studio-kits-pm/
├── .cf-studio-kit.toml
├── README.md
├── LICENSE
└── kits/
    ├── compete/
    │   ├── README.md
    │   ├── artifacts/
    │   ├── workflows/
    │   └── scripts/
    └── future-kit/
        ├── README.md
        ├── artifacts/
        └── workflows/
```

The root `.cf-studio-kit.toml` contains multiple:

```toml
[[kits]]
```

entries.

---

# Installing Kits

Standalone kit:

```bash
cfs kit install constructorfabric/studio-kit-sdlc
```

Third-party kit:

```bash
cfs kit install omniscale-ai/studio-kit-qi
```

Multi-kit repository:

```bash
cfs kit install constructorfabric/studio-kits-pm --kit compete
```

Pin a version:

```bash
cfs kit install owner/repository --version <tag-or-sha>
```

Then regenerate agent integrations:

```bash
cfs generate-agents
```

---

# Contributing a Kit

Constructor Studio kits are published from their own GitHub repositories and added to the central catalog through a Pull Request.

The author remains responsible for maintaining the kit.

The catalog is responsible for:

- discovery;
- metadata;
- structural validation;
- categorization;
- publisher information.

---

# Submission Requirements

Before submitting a kit, make sure the repository contains the following.

## 1. `.cf-studio-kit.toml`

The canonical Constructor Studio kit manifest.

At minimum:

```toml
manifest_version = "1.0"

[[kits]]
slug = "my-kit"
name = "My Kit"
version = "1.0.0"
```

The manifest should declare all installable resources.

---

## 2. README.md

The repository should explain:

- what the kit does;
- who it is for;
- which workflows it contains;
- what artifacts or outputs it produces;
- how to install it;
- any external requirements.

Example installation:

```bash
cfs kit install owner/repository
```

For a multi-kit repository:

```bash
cfs kit install owner/repository --kit my-kit
```

---

## 3. License

The repository must include a clear license.

Example:

```text
LICENSE
```

Open-source licenses are strongly recommended for public catalog entries.

---

## 4. Version

The kit must have an explicit version in:

```text
.cf-studio-kit.toml
```

For example:

```toml
version = "1.2.0"
```

Published kit versions should preferably correspond to:

- Git tags;
- or GitHub Releases.

---

## 5. Validation

Before opening a Pull Request:

```bash
cfs validate-kits .
```

Authors should also run:

```bash
cfs kit normalize --dry-run . --json
```

If the kit contains PDSL workflows or rules:

```bash
cfs pdsl validate workflows/*.md
```

For multi-kit repositories, validate all kits.

---

# Adding a Kit to the Catalog

Once the kit repository is published:

1. Fork `constructorfabric/studio-kits`.
2. Add the kit to `registry.toml`.
3. Add or regenerate the corresponding README catalog entry.
4. Open a Pull Request.

Example catalog entry:

```markdown
1. [**My Kit**](https://github.com/example/my-studio-kit) — One-line description of what the kit does. **[Example Org]**
```

Example registry entry:

```toml
[[kits]]
id = "my-kit"
name = "My Kit"
description = "One-line description of what the kit does."
repository = "example/my-studio-kit"
publisher = "Example Org"
categories = ["science"]
status = "community"
```

---

# Catalog Description Rules

Catalog entries should be deliberately short.

Recommended form:

```text
Name — one-line description. [Publisher]
```

Good:

```text
Spectro — Evidence-gated workflows for spectral analysis, model fitting, calibration, and scientific findings. [Omniscale AI]
```

Avoid:

```text
Spectro — A revolutionary comprehensive AI-powered platform that helps scientists
perform many different kinds of analyses using a unique system...
```

Descriptions should:

- fit on roughly one line;
- describe what the kit actually enables;
- avoid marketing claims;
- avoid implementation details;
- avoid repeating "Constructor Studio Kit";
- be understandable without opening the repository.

---

# Categories

Categories should remain broad enough that the catalog stays browsable.

Initial top-level categories:

```text
Software & Product Development
Science
```

Possible future top-level categories:

```text
Data & Analytics
Security
Operations
Education
Business
```

Avoid creating a new top-level category for every field.

More specific classification should live in registry tags:

```toml
categories = [
  "science",
  "quantum-information",
  "verification"
]
```

---

# Current Grouping

## Software & Product Development

Includes activities around:

- product discovery;
- competitive analysis;
- requirements;
- architecture;
- implementation;
- testing;
- delivery;
- review.

Current kits:

```text
SDLC
Competitive Analysis
```

## Science

Includes workflows around:

- scientific research;
- analysis;
- evidence validation;
- reproducibility;
- scientific claims;
- experimental data;
- literature and references.

Current projects:

```text
Quantum Information
Spectro
Reference Audit
```

---

# Kit Status

Suggested statuses:

## Official

Maintained by the Constructor Studio project.

Example:

```toml
status = "official"
```

Possible examples:

- SDLC;
- Constructor-maintained Product Management kits.

---

## Verified Publisher

Maintained by a known third-party publisher whose ownership has been verified.

Example:

```toml
status = "verified-publisher"
```

This does not mean Constructor audited every line of code.

It means the catalog can verify who controls the repository.

Example:

```text
Omniscale AI
```

---

## Community

A third-party kit that follows the Studio packaging format.

Example:

```toml
status = "community"
```

Community kits should pass structural validation but should not imply endorsement.

---

# Important Trust Distinction

Being listed in the catalog means:

- the package is structurally compatible with Studio;
- its manifest is valid;
- required metadata exists;
- the repository is accessible.

It should **not automatically mean**:

- Constructor audited the source code;
- Constructor endorses scientific claims made by the kit;
- Constructor guarantees security;
- Constructor guarantees maintenance;
- Constructor guarantees compatibility with every future Studio version.

The catalog should make this distinction explicit.

---

# Pull Request Validation

Catalog Pull Requests should automatically check:

- repository exists;
- repository is public;
- `.cf-studio-kit.toml` exists;
- manifest parses correctly;
- referenced kit slug exists;
- version exists;
- README exists;
- license exists;
- `cfs validate-kits .` passes;
- catalog entry is not duplicated;
- categories are valid;
- status value is valid.

For a multi-kit repository:

```text
repository = "constructorfabric/studio-kits-pm"
kit = "compete"
```

CI must verify that the `compete` kit exists in the repository manifest.

---

# Proposed CI Flow

```text
Pull Request
     ↓
Read registry.toml diff
     ↓
Find new/changed kit entries
     ↓
Clone external repository
     ↓
Read .cf-studio-kit.toml
     ↓
Verify slug
     ↓
Run cfs validate-kits .
     ↓
Verify README + LICENSE
     ↓
Validate registry schema
     ↓
PASS / FAIL
```

This reduces manual review to things such as:

- is the category sensible?
- is the one-line description accurate?
- is the publisher represented correctly?
- should the entry be official/community/verified?

---

# Publisher Verification

A simple initial publisher verification method is enough.

For example:

- the publisher controls the GitHub organization containing the kit;
- the submitted PR comes from that publisher or references an approval;
- repository ownership can be verified from GitHub.

No complex publisher account system is required initially.

---

# Reference Audit

`reference-audit` currently behaves differently from the native Studio kits.

It is primarily a standalone scientific tool:

```text
constructorfabric/reference-audit
```

It currently does not use the same root `.cf-studio-kit.toml` packaging structure as:

- SDLC;
- Quantum Information;
- Spectro;
- Product Management kits.

There are two reasonable options.

## Option A — Keep It as a Related Tool

Display it under Science:

```text
Reference Audit — Verifies scientific references and detects citations that do not resolve to real publications. [Constructor]
```

But mark it as:

```text
Related Tool
```

rather than an installable kit.

## Option B — Convert It into a Kit

Add:

```text
.cf-studio-kit.toml
```

and expose its relevant workflows through Studio.

Alternatively create:

```text
constructorfabric/studio-kit-reference-audit
```

which integrates the existing tool into Studio.

This would make it installable through:

```bash
cfs kit install constructorfabric/studio-kit-reference-audit
```

---

# Current Kit Examples

## SDLC

Repository:

```text
constructorfabric/studio-kit-sdlc
```

Conceptual pipeline:

```text
PRD
 ↓
ADR + DESIGN
 ↓
DECOMPOSITION
 ↓
FEATURE
 ↓
CODE + TESTS
```

Install:

```bash
cfs kit install constructorfabric/studio-kit-sdlc
```

---

## Competitive Analysis

Repository:

```text
constructorfabric/studio-kits-pm
```

Kit:

```text
compete
```

Typical areas:

- research requests;
- company discovery;
- candidate registers;
- company profiles;
- feature taxonomies;
- comparison matrices;
- competitive monitoring.

Install:

```bash
cfs kit install constructorfabric/studio-kits-pm --kit compete
```

---

## Quantum Information

Repository:

```text
omniscale-ai/studio-kit-qi
```

Conceptual pipeline:

```text
CLAIM
  ↓
CERTIFICATE
  ↓
CHECK-RUN
```

Typical areas:

- machine-checkable claims;
- exact certificates;
- proof decomposition;
- claim graphs;
- counterexample search;
- reproducible verification.

Install:

```bash
cfs kit install omniscale-ai/studio-kit-qi
```

---

## Spectro

Repository:

```text
omniscale-ai/studio-kit-spectro
```

Conceptual pipeline:

```text
DATASET
   ↓
ARTEFACT-SCAN
   ↓
FIT
   ↓
VERDICT
   ↓
FINDING
```

Typical areas:

- spectrum analysis;
- model fitting;
- calibration;
- fit validity;
- parameter validation;
- scientific findings.

Install:

```bash
cfs kit install omniscale-ai/studio-kit-spectro
```

---

# CLI Discovery

Once `registry.toml` exists, Studio can later add catalog discovery without introducing a marketplace backend.

Example:

```bash
cfs kit search quantum
```

Possible output:

```text
Quantum Information
omniscale-ai/studio-kit-qi

Machine-checkable claims and certificate workflows
for quantum information research.

Publisher: Omniscale AI
Status: Verified Publisher
Category: Science / Quantum Information

Install:
cfs kit install omniscale-ai/studio-kit-qi
```

Other useful commands:

```bash
cfs kit search
```

```bash
cfs kit search science
```

```bash
cfs kit search --publisher omniscale-ai
```

```bash
cfs kit search --category science
```

Potential future command:

```bash
cfs kit info quantum-information
```

---

# Future Web Catalog

A website can later consume exactly the same registry:

```text
registry.toml
       ↓
static generator
       ↓
studio.../kits
```

A basic kit page could display:

```text
Quantum Information

Publisher
Omniscale AI

Status
Verified Publisher

Category
Science → Quantum Information

Description
Machine-checkable claims and certificate workflows
for quantum information research.

Repository
github.com/omniscale-ai/studio-kit-qi

Install
cfs kit install omniscale-ai/studio-kit-qi

Version
1.0.0

License
Apache-2.0
```

The website therefore does not need its own database initially.

---

# Evolution Path

The ecosystem can grow incrementally.

## Stage 1 — GitHub Catalog

```text
README.md
+
registry.toml
+
PR-based submissions
```

This is enough for the current number of kits.

---

## Stage 2 — Automated Validation

Add GitHub Actions:

```text
PR
 ↓
manifest validation
 ↓
repository validation
 ↓
catalog generation
```

---

## Stage 3 — CLI Discovery

Add:

```bash
cfs kit search
cfs kit info
```

Both consume the same registry.

---

## Stage 4 — Static Website

Generate:

```text
/kits
/kits/sdlc
/kits/quantum-information
/kits/spectro
```

from the registry.

---

## Stage 5 — Rich Marketplace Features

Only when the ecosystem becomes large enough, consider:

- download statistics;
- compatibility matrix;
- search ranking;
- dependency management;
- publisher profiles;
- signatures;
- trust scores;
- update channels;
- deprecation status;
- security advisories.

These should not be prerequisites for launching the catalog.

---

# Things Not Needed Initially

Do not build initially:

```text
marketplace backend
database
user accounts
publisher dashboard
package hosting
ratings
reviews
download infrastructure
payment system
```

GitHub already provides:

- source hosting;
- repository ownership;
- releases;
- tags;
- issues;
- Pull Requests;
- CI;
- contribution workflow.

The Studio catalog can reuse those mechanisms.

---

# Recommended Source-of-Truth Model

There are three separate layers.

## Package Source of Truth

Inside each kit repository:

```text
.cf-studio-kit.toml
```

Defines:

- kit identity;
- version;
- installable resources;
- paths;
- public skills;
- templates;
- checks;
- scripts;
- installation behavior.

---

## Discovery Source of Truth

Inside:

```text
constructorfabric/studio-kits
```

Use:

```text
registry.toml
```

Defines:

- catalog ID;
- repository;
- kit slug for multi-kit repositories;
- publisher;
- categories;
- description;
- catalog status.

---

## Human View

Generated or maintained in:

```text
README.md
```

Optimized for quick browsing.

---

# Final Recommended User Experience

A developer visits:

```text
github.com/constructorfabric/studio-kits
```

The first thing they see is:

```markdown
## Software & Product Development

1. SDLC — End-to-end software delivery workflows from requirements and architecture to implementation and review. [Constructor]
2. Competitive Analysis — Evidence-first competitive research for product discovery, positioning, and prioritization. [Constructor]

## Science

1. Quantum Information — Machine-checkable claims, certificates, and verification workflows for quantum information research. [Omniscale AI]
2. Spectro — Evidence-gated workflows for spectral analysis, model fitting, calibration, and scientific findings. [Omniscale AI]
3. Reference Audit — Verifies scientific references and detects citations that do not resolve to real publications. [Constructor]
```

Each kit name links directly to its GitHub repository.

The author workflow is:

```text
Create kit
   ↓
Add .cf-studio-kit.toml
   ↓
Validate kit
   ↓
Publish repository
   ↓
Tag release
   ↓
PR to Studio Kits catalog
   ↓
CI validates
   ↓
Maintainer reviews metadata
   ↓
Merge
   ↓
Kit appears in catalog
```

The user workflow is:

```text
Browse catalog
   ↓
Open kit repository
   ↓
Review README / source
   ↓
Install
```

For example:

```bash
cfs kit install omniscale-ai/studio-kit-spectro
```

---

# Recommended First Implementation

The smallest useful implementation is:

```text
1. Create constructorfabric/studio-kits
2. Add README.md with grouped numbered catalog
3. Add registry.toml
4. Add CONTRIBUTING.md
5. Add simple registry validation CI
6. Accept new kits through Pull Requests
```

Then add external repository validation:

```text
7. CI fetches submitted kit repository
8. Checks .cf-studio-kit.toml
9. Runs cfs validate-kits .
10. Checks README + LICENSE
```

After the catalog has meaningful adoption:

```text
11. Add cfs kit search
12. Generate README from registry.toml
13. Generate a static web catalog from the same registry
```

This keeps the first version extremely small while leaving a clean path toward a mature extension ecosystem.