# Cyberline website strategy: static HTML vs Hugo vs Zola

**Decision (November 14, 2026): keep the existing static GitHub Pages
website, with an isolated Hugo proof-of-concept. No migration of the production site.**

Cyberline is an MIT-licensed CSS library; its user-facing demo gallery already
works without runtime JavaScript. The current site consists of original
standalone HTML demos, a component gallery, and Markdown engineering guides.
Its value is the styling and copyable source, not a content-management system.

## Decision matrix

| Variable | Current static HTML | Hugo | Zola |
| --- | --- | --- | --- |
| Generator required to deploy | None | Single build-time binary | Single build-time binary |
| Runtime JavaScript | None | None, unless intentionally added | None, unless intentionally added |
| Docs authored in Markdown | GitHub renders files, not an integrated site | Native: templates, menus, taxonomies, render hooks | Native: sections, templates, taxonomies |
| Templates | Direct HTML | Go templates | Tera (Jinja-like) |
| Theme and module ecosystem | Own CSS only | Mature site themes and modules; optional Go-based modules | Smaller/simple theme model |
| Deployment on existing Pages main / | Native | Build output must be deployed instead | Build output must be deployed instead |
| URL/stylesheet migration risk | None | Real, needs parity tests | Real, needs parity tests |
| Maintenance overhead now | Lowest | Additional pinned tool + templates + CI | Additional pinned tool + templates + CI |
| Relevance to Cyberline | Best now | Best later for extensive documentation | Good lightweight alternative |

Official primary references:
- https://gohugo.io/about/features/
- https://gohugo.io/templates/types/
- https://gohugo.io/configuration/module/
- https://gohugo.io/host-and-deploy/deploy-to-github-pages/
- https://www.getzola.org/documentation/getting-started/
- https://www.getzola.org/documentation/content/overview/
- https://www.getzola.org/documentation/deployment/github-pages/

Both options are permissively licensed and generate static files. Zola is
Rust-based with Tera templates and a self-contained executable. Hugo is Go-
based with rich Markdown processing, output formats, template reuse, and a
well-developed documentation/content ecosystem. Neither is a replacement for
Vertigo: Vertigo handles stateful application logic; these tools only build
content pages ahead of time.

## Why Hugo wins if content becomes complex

Cyberline has growing engineering documentation (API conventions, tokens,
accessibility, recipes, CLI, integration guides) and may eventually need
versioned documentation, multilingual landing pages, release notes and
taxonomy navigation. Hugo is the better long-term fit for these requirements,
particularly because the related Vertigo ecosystem uses Go. It supports
modern native template layouts and content-mount workflows.

Zola would be preferable if the site stayed small and a developer valued
Tera's simpler templating experience more than Hugo's content features.
Neither generator's final asset size is intrinsically smaller; delivered CSS
is still defined by Cyberline itself, not by the SSG.

## Direct cost and hidden costs

A migration would require:
- moving/copying roughly ten carefully crafted HTML showcase/demo pages;
- testing every old GitHub Pages URL, relative asset reference and filename;
- changing Pages deployment (currently main /) to a generated artifact;
- pinning and regularly updating a new binary and template API;
- avoiding duplicated documentation sources and broken relative Markdown links;
- retaining the same zero-JavaScript runtime and MIT source availability.

It is not worth it today because a generator does not fix a demonstrated
customer problem yet. The isolated Hugo experiment uses existing Markdown and
CSS to test actual templates without changing the public site.

## Proposed trigger to revisit

Reevaluate after roughly **20–30 regularly maintained documentation pages**,
a genuine versioned documentation requirement, or recurring manual
navigation/link-editing pain. These are heuristic triggers, not a framework
performance threshold.

If migration is approved, use Hugo for the **documentation section first**,
not the component gallery and live CSS demos. Build locally or in CI, prove
output parity including the /docs/ and /examples/ paths, then cut over with
a rollback plan. Existing MIT stylesheet artifacts remain independent of
whatever generates the website.

## Vertigo boundary

Use Cyberline to style Vertigo's Go admin pages via an **opt-in CSS adapter**.
Keep static marketing, docs and free downloads publicly accessible. Add
Vertigo to Cyberline's customer portal only if buyers need retained
entitlements, team licenses, or authenticated download management.
One-time hosted checkout and private delivery should be validated before
adding a persistent application stack.

## Verified Hugo preview result

Using official Hugo **v0.170.0**, the isolated build rendered **11 HTML
pages** directly from the existing Cyberline Markdown guides and its two
preview landing/section pages. The verification script checked **67 local
links** and rejected browser JavaScript and unintended copied Python files.
The input uses the live repository CSS and example HTML through native Hugo
module mounts. The preview is not a public Pages deployment.

Repeat the check with a pinned Hugo binary:

~~~sh
python3 scripts/verify_hugo_preview.py --hugo /path/to/hugo
~~~

This establishes feasibility, not a benefit large enough to justify migrating
the current live site or its existing permalink structure.
