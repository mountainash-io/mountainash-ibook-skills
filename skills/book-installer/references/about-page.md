---
name: about-page
description: Generates the about.md page for package documentation, explaining why the package exists, what it adds to its foundations, the design ideas behind it, where it fits, and who maintains it.
---

# About page generator

This guide generates `docs/about.md` for package documentation. After the home page, About is the second page that sets the scene. The home page says what the package does and who it is for. About says why it exists and how its authors think about the problem. It must not read like a chapter, and it must not repeat the chapter list.

## What this guide creates

1. `docs/about.md`, with the sections below.
2. A navigation entry in `mkdocs.yml`.

## Sources

Every claim on the page comes from a source you have read. Never invent history, motivation, statistics or quotes. Read, in this order:

| Source | Use it for |
|---|---|
| The package README | The one-line pitch, what the package adds to its foundations, links to runnable examples |
| Design or principles documents (for mountainash packages, `mountainash-central/01.principles/<package>/`) | The motivation and the design ideas, and the problems they prevent |
| The package profile (`docs-site/profile/facets/*.json`, especially `broader-hype`) | Benefits and before/after framing |
| `mkdocs.yml` (`site_author`, `repo_url`, `copyright`) and the package license file | Maintainer, repository, license and copyright |
| Source code | Checking every behavioural claim; run a short script when a claim is about runtime behaviour |

If a source for a section does not exist, write the plain version without it or leave the section out. Do not fill a gap with plausible filler.

## Page structure

Write the sections in this order. Apply the humanizer pass from the chapter-content-generator skill: sentence-case headings, no dashes, no puffery, no bold inline-header lists.

### 1. Title and tagline

```markdown
---
title: 'About'
description: 'Why {{PACKAGE}} exists, the design ideas behind it, where it fits, and who maintains it'
---

[← Back to Home](index.md)

# About {{PACKAGE}}

**{{TAGLINE: one bold sentence that contrasts what the foundation does with what this package decides}}**
```

### 2. Why it exists

Two or three short paragraphs telling the story: what the foundation (the library or tool the package builds on) already handles, where that stops being enough, the concrete problems that appear, and the one idea the package uses to answer them. Write it as situations the reader recognises, not as a feature list.

### 3. What it adds to {{FOUNDATION}}

One sentence on what the foundation supplies, then a two-column table (`Area`, `What you get`) of what the package adds. Five to seven rows; only what most users need.

### 4. Design ideas

Three to six ideas, each a short paragraph that opens with the idea stated plainly as its own sentence ("Carry the recipe, not the values.") followed by what it means for the reader. Take them from the design or principles documents; include only ideas that change how a user writes code, and leave out internal mechanics and status labels.

### 5. Where it fits

The project or ecosystem the package belongs to, what other packages use it for, and what deliberately lives elsewhere.

### 6. Who maintains it

The maintainer, the public repository, where runnable examples live, the edit-link workflow for corrections, and a link to the Contact page.

### 7. License

The package license, matching the repository's license file, and the copyright line.

## Example

From the mountainash-settings documentation (abridged):

```markdown
# About mountainash-settings

**Pydantic validates your settings. mountainash-settings decides where they come from, when they load and who gets to see them.**

## Why it exists

Pydantic Settings already reads environment variables and `.env` files into a typed model. That is enough for a single script. It starts to strain when an application grows into services, scheduled jobs and worker processes.

Two problems show up at that point. ... mountainash-settings answers both the same way. Your code carries a recipe, a `SettingsParameters` object, and asks for the settings where the work actually runs.

## Design ideas

Carry the recipe, not the values. Pass `SettingsParameters` through your application and retrieve settings at the point of use. Fewer objects hold live credentials, and workers can rebuild exactly the configuration they need.

Configuration is fixed for the life of a process. Once a configuration has been read, later calls reuse it, even if the file on disk changes. A new process picks up a changed deployment.
```

## Update navigation

Add the page near the bottom of the nav, before Contact and License:

```yaml
nav:
  # ... chapters, FAQ, glossary ...
  - About: about.md
  - Contact: contact.md
  - License: license.md
```

If the nav already has an About entry, leave it.

## Verify

1. Build with `mkdocs build --strict` and confirm every link resolves.
2. Confirm the license and copyright match the package's license file.
3. Re-check each behavioural claim against the source, and run code for any claim about runtime behaviour.
4. Scan the page for dashes, title-case headings and promotional adjectives.

## Related guides

- `home-page-template.md`: the landing page, which About complements.
