# giovannibriglia.github.io

Personal academic website of Giovanni Briglia, live at **https://giovannibriglia.github.io**.

It is a [Jekyll](https://jekyllrb.com/) site built on the [al-folio](https://github.com/alshedivat/al-folio) theme (MIT licence). The homepage is a custom one-page layout; blog posts and the other pages still use al-folio's layouts.

## Homepage layout

The homepage (`/`) is rendered by [`_layouts/onepage.liquid`](_layouts/onepage.liquid) and has these sections, in order:

1. **Hero**: name, role, headline, intro, supervisors line and the animated causal-graph figure
2. **Highlights**: four short cards (award, oral, and so on)
3. **Research**: the three research questions, each linking to related papers
4. **Publications**: filterable list (Selected, All, Causal RL, Multi-agent, Earlier work) with BibTeX
5. **News and Talks**: the newest news items, with older ones folded away
6. **Contact**: email, profile links and CV

## Where to edit content

| To change | Edit |
| --- | --- |
| Headline, intro, role line, supervisors line, highlights | [`_pages/about.md`](_pages/about.md) (front matter; the body is the supervisors line) |
| Publications | [`_data/publications.yml`](_data/publications.yml) |
| Research questions | [`_data/research.yml`](_data/research.yml) |
| Talks | [`_data/talks.yml`](_data/talks.yml) |
| News | one file per item in [`_news/`](_news/) |
| CV | replace [`assets/pdf/cv.pdf`](assets/pdf/cv.pdf) |
| Email, Scholar, ORCID, GitHub, LinkedIn | [`_config.yml`](_config.yml) (`email`, `scholar_userid`, `orcid_id`, `github_username`, `linkedin_username`) |
| Colours and fonts | the `:root` block at the top of [`assets/onepage/site.css`](assets/onepage/site.css) |
| Hero figure | the inline `<svg>` in [`_layouts/onepage.liquid`](_layouts/onepage.liquid) |

### Add a publication

Add an entry to `items` in `_data/publications.yml`. The list is shown in file order, so put new papers at the top.

```yaml
- id: neurips2026                # unique; used for the #pub-neurips2026 anchor
  title: My New Paper
  authors: [G. Briglia, S. Mariani, F. Zambonelli]   # "G. Briglia" is shown in bold
  venue: NeurIPS 2026
  year: 2026
  image: /assets/img/home/my_new_paper.png           # optional thumbnail
  image_alt: Short description of the thumbnail
  badge: Spotlight               # optional
  badge_kind: oral               # oral (accent colour) or award (amber)
  tags: [selected, causal, multi]
  links:
    - { label: arXiv, url: "https://arxiv.org/abs/xxxx.xxxxx" }
    - { label: Code, url: "https://github.com/Giovannibriglia/..." }
  bibtex: |
    @inproceedings{briglia2026new,
      title={My New Paper},
      ...
    }
```

Tags decide which filter shows the paper: `selected` (shown by default), `causal`, `multi` and `earlier`. Keep thumbnails small, about 480 px wide, in `assets/img/home/`.

To link a paper from a research question, add its `id` under that question's `papers` in `_data/research.yml`.

### Add a news item

Create `_news/announcement_N.md`:

```markdown
---
layout: post
date: 2026-11-15
inline: true
related_posts: false
---

Our paper [My New Paper](https://arxiv.org/abs/xxxx.xxxxx) was accepted at **NeurIPS 2026**!
```

The homepage shows the 6 newest items (set by `news_limit` in `_pages/about.md`). The rest go under "Older news".

### Add a talk

Add an entry at the top of `_data/talks.yml`. `url` is optional and can point to slides:

```yaml
- when: Nov 2026
  title: Title of the talk
  where: Seminar name, Institution
  url: "/assets/pdf/my_slides.pdf"
```

## Run locally

You need Ruby 3.x and Bundler:

```bash
bundle install
bundle exec jekyll serve
```

Then open http://localhost:4000. With Docker, `docker compose up` does the same.

## Deploy and checks

Pushing to `master` runs these GitHub Actions:

| Workflow | What it does |
| --- | --- |
| **Deploy site** (`deploy.yml`) | Builds the site and publishes it to the `gh-pages` branch. If the build fails, the live site stays as it was. Pull requests are built but not deployed. |
| **Check content** (`content-check.yml`) | Validates the homepage data with `bin/check_content.py` (required fields, tags, unique ids, research links, local files, news dates) and checks the external links in the content files. Also runs every Monday to catch links that stop working. |
| **Check for broken links on site** (`broken-links-site.yml`) | After a deploy, checks the internal links in the built site. |

Run the content check locally before pushing:

```bash
python3 bin/check_content.py
```

It needs PyYAML (`pip install pyyaml`) and lists any problem with the file it is in. If a check fails on GitHub, open the run in the Actions tab to see the error.

The theme's own documentation is in [`INSTALL.md`](INSTALL.md), [`CUSTOMIZE.md`](CUSTOMIZE.md) and [`FAQ.md`](FAQ.md).
