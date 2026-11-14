# Cyberline Console Kit — 10-interview design-partner pilot

**Status: recruiting infrastructure prepared; no prospects contacted yet.**
A [public invitation is posted](https://github.com/dporkka/cyberline-css/issues/3), but no actual participants have been recruited. This is a zero-budget qualitative validation experiment, not a marketing
automation or a promise to ship premium assets. Core CSS, Grid and Noir themes,
the full component library, and the free examples remain MIT-licensed.

## Hypothesis and decision

An independent developer building server-rendered dashboards (Go/templ,
HTMX, Rails/Hotwire, Django, Astro, Rust templates) will pay **$59 one time**
for *complete polished and accessible application screens*, instead of
needing a new JavaScript component framework. The current two example screens
are already free. Only **future**, separately authored screen compositions
could be sold under a commercial license.

Qualifying participants must have shipped or be currently building a
commercial/internal web application and be able to critique *actual code*
rather than screenshots. Upvotes, GitHub stars, and generic compliments are
not purchase evidence.

## Recruitment scope

Public review issue: https://github.com/dporkka/cyberline-css/issues/3


Use the ten **uncontacted** slots in
[design-partner-pilot.csv](design-partner-pilot.csv). They are target segments,
not fabricated identities or sales leads. Recruit only through opt-in responses
or respectful, permitted community posts; **consent** and community rules
matter. Do not scrape or mass-DM members.

Good first channels:

- **Go/templ:** the official templ guide lists Gopher Slack's `#templ`
  channel and GitHub Discussions at https://templ.guide/help-and-community/.
- **HTMX:** the official community page lists Discord and GitHub Discussions:
  https://htmx.org/talk/. Ask moderators before sharing project links.
- **Astro:** reach an Astro-focused developer already discussing open-source
  website themes in opt-in spaces; prioritize use case over follower count.
- **Independent SaaS developers:** ask for one-to-one critique from existing
  contacts who use server rendering and actively buy design templates.

## Public research prompt (adapt to rules of each community)

> I'm testing a tiny, MIT-licensed, zero-runtime-JS CSS design system for
> dashboards with Grid/Noir themes. Two original HTML screens are free:
> https://dporkka.github.io/cyberline-css/examples/console.html and
> https://dporkka.github.io/cyberline-css/examples/resources.html.
> I'm looking for 10 developers building real SaaS or internal tools to review
> the markup and tell me which *complete screens* are genuinely time-consuming.
> I'm also testing whether a separately authored eight-screen kit might be
> worth $59 once built. It is not on sale. Interested in giving a 15-minute
> critique? You can reply via
> https://github.com/dporkka/cyberline-css/issues .

## One-to-one message, only for an appropriate existing relationship

> Would you review two free, framework-independent HTML/CSS SaaS screens?
> I want feedback on accessibility, integration friction, and which complete
> layouts would save development time. This isn't a sales pitch; the existing
> library is MIT and the proposed $59 Console Kit has a private prototype,
> but it is not yet for sale or publicly distributed.
> A quick code-level critique would be more useful than a general opinion.

## Five questions, 15 minutes

1. What framework/backend do you actually use, and what did you ship recently?
2. Have you personally bought UI template kits? What triggered the purchase?
3. Review the two live demos, copy HTML into your app if relevant, and identify
   the first piece that creates integration or accessibility friction.
4. Which three *finished screens* are missing, and what functionality is
   expected to be included versus left to your backend?
5. After seeing this actual scope, would you commit $59 when delivered? Ask
   what budget line or comparable purchase supports that answer; mark **paid
   intent**, not actual revenue.

## Logging and thresholds

- Update each slot's status `not_contacted` → `invited` → `accepted` →
  `interviewed` or `declined`. Store personally identifying respondent
  details only with permission, and preferably in a **private** tracker rather
  than in this public source repository.
- Log explicit outcomes separately: `would_buy`, `maybe`, `would_not_buy`,
  plus any actual **paid** commitments (only after selling is legally ready).
- Do not count hypothetical "yes" responses as sales. Sample of 10 qualitative
  interviews cannot establish a statistically reliable conversion rate.
- Before expanding the premium catalog, seek 10 interviews plus independent
  evidence of purchase intent (real preorder when legally ready, signed
  design-partner commitment, or clear willingness backed by prior purchases).
- Reject requests to move essential accessibility improvements or existing
  MIT functionality into paid bundles. Keep delivery/refund/license terms
  documented before accepting money.

**Current outcomes:** 0 invited, 0 interviewed, 0 paid commitments. The
Console Kit private prototype exists, but it is **not available for purchase** and no checkout exists.
