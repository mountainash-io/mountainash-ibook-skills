---
name: glossary-generator
description: Generate or refresh the confirmed glossary appendix using internal concepts, package profiles and source-backed chapter definitions.
license:
metadata:
  ibook.version: "2.0.0"
  ibook.preferred-model: "sonnet"
---

# Glossary appendix

Resolve the explicit source repository/worktree. Read its confirmed `docs-site/editorial-brief.md`, approved `docs-site/chapter-plan.md`, internal graph and relevant module profiles, then the actual chapters. The glossary is included by default, but its inclusion must be confirmed in the brief. If excluded, report that decision without generating it. Do not require a course page, fixed concept count or numerical quality score.

Write `docs-site/site/docs/glossary.md`, presented under Appendices in navigation. Keep graph concepts and editorial reports outside the site. Preserve useful existing definitions, curated examples and manual entries; verify accuracy against current source before reusing them. Do not silently discard terms during refresh.

## Definition contract

Follow ISO 11179 guidance: precise, concise, distinct, non-circular definitions. Define the class and distinguishing characteristics rather than repeating the term. Do not hide implementation restrictions in a general definition; explain them separately in the package-specific discussion. Prefer a short definition (normally 20–50 words), then a source-backed example only where useful.

Use one `# Glossary` heading and consistent term headings, sorted alphabetically. Keep API spellings intact. Disambiguate identical labels using context rather than dropping entries. Define abbreviations, avoid undefined specialist vocabulary and link related terms where useful. Match the audiences/depths in the brief, not an assumed school grade.

Every entry should link to the real chapter or section containing its primary explanation. Section anchors are allowed after verification against the built page; use a chapter link when the heading is not stable. Reuse explanations through links rather than duplicating entire chapters. For existing paired-marker entries, retain IDs and concept associations so targeted refresh remains possible.

## Verification and refresh

Review definition accuracy, circular references, duplicate/ambiguous labels, alphabetic ordering and chapter/section destinations. Build the candidate and verify appendix navigation and a representative link in the browser. Do not claim generated term counts without measuring them.

Routine refresh reuses the confirmed brief and preserves untouched entries. Editorial scope changes require focused confirmation. Unsupported legacy artifact formats are not implicitly converted. Keep accepted content intact until reviewed PR acceptance. No automatic publishing, quiz generation or mandatory MicroSim step belongs here. Honor the user's inline/delegation preference; no forced subagent is required.
