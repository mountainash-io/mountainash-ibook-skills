---
name: faq-generator
description: Generate or refresh the confirmed FAQ appendix from completed source-backed chapters, preserving curated entries and existing unsupported FAQ data.
license: Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)
metadata:
  ibook.version: "2.0.0"
  ibook.preferred-model: "sonnet"
---

# FAQ appendix

Resolve the explicit source repository/worktree. Read its confirmed `docs-site/editorial-brief.md`, approved `docs-site/chapter-plan.md`, relevant profiles/all available audience facets, internal graph and completed chapters. FAQ inclusion is default-on but must be confirmed in the brief. Do not substitute course-quality scores, word counts or a percentage of drafted chapters for that gate.

Write `docs-site/site/docs/faq.md` and present it under Appendices in navigation. Do not publish internal graph reports or a graph directory to carry the FAQ. The glossary is a useful terminology input when included; its deliberate exclusion does not prevent a confirmed FAQ.

## Content

- Use `# FAQ`, `##` category headings and `###` question headings. Categories follow reader needs, not compulsory Bloom-level quotas.
- Cover actual conceptual confusion, getting started, usage, failure modes, boundaries, extension points and internals at the depths chosen by the brief. Consider each selected facet rather than hardcoding a single audience.
- Answer from current source and completed chapters. Do not invent guarantees, commands, examples or troubleshooting fixes. A genuine knowledge gap belongs in the internal review report, not a fabricated answer.
- Preserve useful curated questions, order and untouched answers during refresh. Reuse existing accurate explanations selectively. Resolve duplicates and contradictory answers explicitly.
- Link answers to actual relevant chapters or sections. Anchor links are allowed when verified against built destinations; otherwise use stable chapter links. Prefer a short answer plus a link over repeating the whole explanation.
- Do not generate quizzes or mandatory interactive elements. A Mermaid diagram can explain an answer where useful.

## FAQ format safety

Content migration and machine export are different operations. Inventory any existing `docs-site/learning-graph/faq.md`, `faq-chatbot-training.json`, published copy and the appendix before editing. Keep unsupported existing JSON untouched. Never replace heading-based FAQ data with an empty marker export.

`ibook refresh faq-export --faq FAQ` and `faq-verify --faq FAQ --json JSON` support **paired-marker format only**. Use them only when the FAQ already satisfies that format and the output shape is appropriate. Capture export to a separate candidate; never redirect over existing JSON. Confirm question IDs, ordering, categories, answers and concept associations before adopting it. Do not introduce a converter as an implicit part of prose refresh.

For heading-based legacy FAQs, compare ordered question/category headings and complete answers with the existing JSON, trimming only surrounding whitespace. Preserve internal Markdown and untouched entries. An empty projection of a nonempty FAQ is a refusal even if a command exits successfully. Ambiguous formats or unexplained differences require review; do not write successful state hashes.

## Completion

Finish every agreed category and verify source accuracy, useful coverage and chapter/section links. Build and inspect appendix navigation and representative destinations. Report actual changes and preserved artifacts, not a guessed quality score. Update refresh state only after verification; keep history truthful. Routine changes use the persisted brief; editorial changes require focused confirmation. Accepted books remain unchanged until reviewed PR acceptance; Actions publish prepared content only.
