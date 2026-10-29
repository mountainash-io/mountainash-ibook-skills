---
name: home-page-template
description: This skill creates a professional home page with cover image, social media metadata, and proper formatting for intelligent textbooks. It includes generating AI prompts for cover images with montage backgrounds and central titles, setting up Open Graph and Twitter card metadata, and configuring the index.md with proper frontmatter.
image: img/cover.png
og:image: img/cover.png
---

# Home Page Template

This skill creates a professional home page for intelligent textbooks with cover images optimized for social media sharing.

## What This Skill Creates

1. **docs/index.md** - Home page with proper frontmatter metadata
2. **docs/img/cover.png** - AI-generated cover image (user generates externally)
3. **Social media optimization** - Open Graph and Twitter Card metadata

## Prerequisites

- Existing MkDocs Material project (use `init-textbook.md` — feature 0 — first if needed)
- Access to an AI image generator (ChatGPT/DALL-E, Midjourney, or similar)
- Course/book description and key themes identified

## Workflow

### Step 1: Gather Book Information

Collect the following information from the user:

1. **Book Title** - The main title (e.g., "Automating Instructional Design")
2. **Subtitle** (optional) - A secondary tagline
3. **Description** - 1-2 sentence description for SEO and social sharing
4. **Key Themes** - 5-10 major topics/concepts covered in the book
5. **Target Audience** - Who the book is for
6. **Color Palette** - Primary colors for the book's branding
7. **Visual Style** - Modern, classic, technical, playful, etc.

### Step 2: Identify Montage Elements

Based on the book's themes, identify visual elements for the cover montage. These should be concrete, visually distinct items that represent the book's content.

#### Common Element Categories

**Technology/AI Themes:**
- Neural network patterns, circuit traces
- Chat bubbles, prompt interfaces
- Geometric AI iconography
- Data flow visualizations

**Education/Learning Themes:**
- Lightbulb icons (insight)
- Book or graduation cap silhouettes
- Ascending steps or pathways
- Connected nodes (knowledge graphs)

**Visualization/Data Themes:**
- Chart elements (bar, line, pie)
- Network graphs with nodes and edges
- Timeline bars with markers
- Map outlines with data points
- Flowchart arrows and shapes

**Process/Methodology Themes:**
- Gear mechanisms
- Puzzle pieces
- Circular workflow arrows
- Checklist elements

**Human/Interaction Themes:**
- Abstract human silhouettes
- Cursor/touch indicators
- Slider controls, buttons
- Interactive UI elements

### Step 3: Design the Cover Layout

Standard intelligent textbook cover layout:

```
+--------------------------------------------------------------+
|                                                              |
|     [Montage elements    [Montage elements                   |
|      distributed          distributed                        |
|      throughout]          throughout]                        |
|                                                              |
|               +------------------------+                     |
| Mascot        |                        |                     |
| Image         |    BOOK TITLE          |  (Semi-transparent  |
|               |    (White Text)        |   dark overlay)     |
|               |                        |                     |
|               +------------------------+                     |
|                                                              |
|  [More montage        [More montage                          |
|   elements]            elements]                             |
|                                                              |
+--------------------------------------------------------------+

Aspect Ratio: 1.91:1 (e.g., 1910x1000 pixels)
```

### Step 4: Generate the AI Image Prompt

Create a detailed prompt for the AI image generator. Follow this template:

```
A wide landscape book cover background (1.91:1 aspect ratio) for "[BOOK TITLE]".

[BACKGROUND DESCRIPTION]: Deep [PRIMARY COLOR]-to-[SECONDARY COLOR] gradient background.

[MONTAGE ELEMENTS]: A montage of [THEME] elements including:
- [Element 1 with visual description]
- [Element 2 with visual description]
- [Element 3 with visual description]
- [Continue for 6-10 elements]

[STYLE]: [VISUAL STYLE] design aesthetic with [ACCENT COLORS] accents.

[COMPOSITION]: Elements softly fade toward edges with subtle vignette, leaving center area darker/cleaner for white title text overlay.

[TECHNICAL]: Professional quality, high resolution. No text in image.
```

#### Example Prompts by Topic

**For Educational Technology Book:**
```
A wide landscape book cover background (1.91:1 aspect ratio) for an educational technology textbook. Deep blue (#1a237e) to teal (#00695c) gradient background with a montage of EdTech elements: glowing neural network patterns suggesting AI, network graph visualizations with interconnected nodes, timeline bars with milestone markers, small data charts and graphs, flowchart arrows, animated particle trails, a stylized 6-level pyramid in graduated colors (purple to blue), interactive UI elements like sliders and toggle buttons, lightbulb icons representing insight, interconnected gears showing process. Modern flat design aesthetic with warm orange (#ff7043) and electric purple (#7c4dff) accents. Elements softly fade toward edges, leaving center darker for white title text overlay. Professional, tech-forward, educational mood. No text in image.
```

**For Data Science Book:**
```
A wide landscape book cover background (1.91:1 aspect ratio) for a data science textbook. Dark navy (#0d1b2a) to deep purple (#1b0d2a) gradient background with a montage of data science elements: scatter plot visualizations, regression lines, decision tree branches, Python code snippets (stylized/blurred), Jupyter notebook cells, pandas dataframe grids, neural network layer diagrams, confusion matrix heatmaps, ROC curve shapes, bar and histogram silhouettes. Modern technical aesthetic with cyan (#00bcd4) and magenta (#e91e63) accent glows. Elements arranged as floating panels with subtle shadows, fading toward edges. Center area has darker overlay for white title text. Professional, analytical, modern mood. No text in image.
```

**For Business/Management Book:**
```
A wide landscape book cover background (1.91:1 aspect ratio) for a business management textbook. Deep charcoal (#263238) to dark blue (#1a237e) gradient background with a montage of business elements: organizational chart hierarchies, strategy matrix grids, upward trending arrows, pie chart segments, Gantt chart bars, handshake silhouettes, target/bullseye icons, ascending bar graphs, connected stakeholder nodes, briefcase icons, growth curve lines. Clean corporate aesthetic with gold (#ffc107) and teal (#009688) accents. Elements distributed evenly with professional spacing, subtle fade toward edges. Center reserved for white title text with semi-transparent overlay. Professional, strategic, authoritative mood. No text in image.
```

### Step 5: Generate the Cover Image

1. Copy the generated prompt
2. Use an AI image generator:
   - **ChatGPT/DALL-E**: Paste prompt directly
   - **Midjourney**: Add `--ar 191:100` for aspect ratio
   - **Stable Diffusion**: Use appropriate settings for 1910x1000
3. Generate 2-4 variations
4. Select the best result
5. Download at highest available resolution

### Step 6: Add Title Text Overlay (Optional)

If adding title text directly to the image:

1. Use image editing software (Canva, Figma, Photoshop, GIMP)
2. Add semi-transparent dark rectangle in center (opacity 40-60%)
3. Add title text in white
4. Recommended fonts: Inter, Montserrat, Source Sans Pro, or system sans-serif
5. Export as PNG at 1910x1000 pixels minimum

**Note:** Many users prefer to let the image stand alone without baked-in text, using HTML/CSS overlays instead for flexibility.

### Step 7: Save the Cover Image

Save the final image to the docs folder:

```
docs/img/cover.png
```

Recommended specifications:
- Format: PNG (for quality) or WebP (for size)
- Dimensions: 1910x1000 pixels minimum
- File size: Under 500KB for web performance

### Step 8: Create the Home Page (docs/index.md)

The home page is the package's landing page, and the one page that has to set the scene. A reader arriving from search or PyPI should see, before any code, what problem the package solves and that it is meant for them. It must not read like the middle of a chapter: no field-level mechanics up front. Build it from these sections, in order:

1. **Tagline.** One bold line under the H1 that says what the package is and the range it covers.
2. **Scene.** Two short paragraphs. First the everyday problem, told as the situation readers recognise (how it starts simple and then sprawls). Then what the package does about it, in plain terms. Name only what most users need; never internals.
3. **Who it's for.** One card per audience, up front, using Material grid cards (`<div class="grid cards" markdown>`). Draw the audiences and benefits from the package profile's facets (`docs-site/profile/facets/*.json`): each facet's `summary` and `documentation_plan`, and the `broader-hype` facet's before/after and "for free" points. Rename audiences to how readers describe themselves, skip internal-only audiences such as maintainers, and end each card with a link to the chapter that audience needs first. Check every claim against the source; the pitch comes from concrete benefits, not adjectives.
4. **See it work.** One short, runnable usage example of the public API that exercises the core use case end to end, including any input file the reader would write. Run it, show its real output in comments, and close with one sentence on what it showed. Follow the `## Code examples` rules in the chapter-content-generator skill.
5. **Where to go next.** The first chapter a new user should read, the package overview and About.

Put version or migration notices at the bottom as an admonition, not above the scene. Apply the humanizer pass from the chapter-content-generator skill: sentence-case headings, no dashes, no bold inline-header lists, no puffery. Card titles are the one place bold labels belong.

```markdown
---
title: {{PACKAGE_TITLE}}
description: {{PACKAGE_DESCRIPTION}}
image: /img/cover.png
og:image: /img/cover.png
twitter:image: /img/cover.png
---

# {{PACKAGE_TITLE}}

**{{TAGLINE}}**

{{THE_PROBLEM_AS_READERS_LIVE_IT}}

{{WHAT_THE_PACKAGE_DOES_ABOUT_IT}}

## Who it's for

<div class="grid cards" markdown>

-   **{{AUDIENCE_NAME}}**

    ---

    {{WHAT_THIS_AUDIENCE_GETS}}

    [{{FIRST_STEP_LABEL}}]({{CHAPTER_LINK}})

</div>

## See it work

{{INPUT_FILE_IF_ANY}}

{{RUNNABLE_USAGE_EXAMPLE_WITH_REAL_OUTPUT}}

{{ONE_SENTENCE_ON_WHAT_THE_EXAMPLE_SHOWED}}

## Where to go next

- {{FIRST_CHAPTER_POINTER}}
- The [package overview](course-description.md) covers scope and ecosystem context.
- [About](about.md) has authorship, the license and the link to the code repository.

!!! note "{{VERSION_NOTICE_TITLE_IF_ANY}}"
    {{VERSION_NOTICE}}
```

### Frontmatter Fields Explained

| Field | Purpose | Example |
|-------|---------|---------|
| `title` | Page title in browser tab and SEO | `Automating Instructional Design` |
| `description` | SEO meta description, social sharing | `Learn to create interactive educational simulations using AI` |
| `image` | Default social media image path | `/img/cover.png` |
| `og:image` | Open Graph image (Facebook, LinkedIn) | `/img/cover.png` |
| `twitter:image` | Twitter Card image | `/img/cover.png` |
| `hide: - toc` | Hides table of contents on home page | - |

### Step 9: Verify Social Media Preview

Test how the page appears when shared:

1. **Facebook Debugger**: https://developers.facebook.com/tools/debug/
2. **Twitter Card Validator**: https://cards-dev.twitter.com/validator
3. **LinkedIn Post Inspector**: https://www.linkedin.com/post-inspector/

Enter your deployed site URL to preview social cards.

### Step 10: Add Cover Image to Navigation (Optional)

To display the cover image prominently on the home page, add to `docs/index.md`:

```markdown
<figure markdown>
  ![{{BOOK_TITLE}}](./img/cover.png){ width="100%" }
</figure>
```

Or with a link wrapper:

```markdown
[![{{BOOK_TITLE}}](./img/cover.png){ width="100%" }](chapters/01/index.md)
```

## Complete example: docs/index.md

From the mountainash-settings book (abridged):

````markdown
# Mountainash Settings

**Typed configuration for Python, from a single script to a fleet of services.**

Configuration always starts small: a dictionary loaded from a YAML file. Then staging needs a different host. The deployment overrides a port through an environment variable. A database password turns up that must never be committed. Before long, three services parse the same file three different ways, and nobody is sure which value actually wins.

mountainash-settings is the one place all of that comes together. You describe your settings once, as a typed Pydantic class. Files, environment variables and your secret store all feed into it, in an order you can predict, and every part of your code gets the same validated answer.

## Who it's for

<div class="grid cards" markdown>

-   **Application developers**

    ---

    Replace hand-merged YAML, `os.environ` lookups and vault calls with one class that loads YAML, TOML, JSON and `.env` files and validates the result.

    [Define a settings class](chapters/02-mountainash-base-settings/index.md)

-   **Teams connecting to many systems**

    ---

    Declare a database's or SDK's parameters once as a connection profile, then render the exact keyword arguments its driver expects. Every registered profile gets a ready-made pytest suite.

    [Build connection profiles](chapters/06-connection-profiles/index.md)

</div>

## See it work

```python
settings = get_settings(
    settings_class=AppConfig,
    config_files="app.yaml",
    env_prefix="APP_",
    secret_store=store,
)
print(settings.DB_HOST, settings.DB_PORT)  # db.internal 6543
```

The host came from the file, the port from the environment and the password from the secret store.
````

## Troubleshooting

### Image Not Appearing in Social Previews

1. Ensure image path starts with `/` (absolute from site root)
2. Verify image exists at `docs/img/cover.png`
3. Check image dimensions (minimum 1200x630 for best compatibility)
4. Clear social platform caches using their debug tools
5. Wait 24 hours for caches to refresh

### Image Quality Issues

- Use PNG for sharp graphics and text
- Minimum 1910x1000 pixels
- If file size is too large, use WebP or optimize PNG

### Frontmatter Not Working

- Ensure `---` delimiters are on their own lines
- No spaces before first `---`
- YAML syntax must be valid (proper indentation, colons)

## Quick Reference

```yaml
# Minimal frontmatter for social sharing
---
title: Book Title
description: Brief description for search engines and social sharing
image: /img/cover.png
og:image: /img/cover.png
twitter:image: /img/cover.png
hide:
  - toc
---
```

## Related Skills

- `init-textbook.md` - Create new MkDocs project structure (feature 0)
- `learning-graph-viewer.md` - Add interactive learning graph
- `book-publisher` (linkedin-post route) - Create social media announcements
