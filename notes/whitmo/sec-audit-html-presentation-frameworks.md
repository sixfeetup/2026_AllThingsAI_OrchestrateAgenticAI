# Security Audit: HTML Presentation Frameworks
**Date:** 2026-03-09
**Scope:** reveal.js, Slidev, impress.js, Marp

---

## 1. hakimel/reveal.js

**Version:** 5.2.1 (latest, published ~March 2025)
**License:** MIT
**Stars:** 70.7k | **Open Issues:** ~794 | **Contributors:** 325

### Known CVEs

| CVE | Severity | Description | Fix |
|-----|----------|-------------|-----|
| CVE-2022-0776 | MEDIUM (4.6) | XSS via missing postMessage origin verification in speaker-view.html | Upgrade to >= 4.3.0 |
| CVE-2020-8127 | CRITICAL (9.8) | XSS via postMessage API | Upgrade to >= 3.9.2 |

**[MEDIUM]** Two historical XSS vulnerabilities, both patched. The postMessage attack surface in the speaker notes/multiplexing feature is a recurring theme. No CVEs disclosed in 2023-2026.

### Security Policy
**[LOW]** No SECURITY.md or formal security policy published. No published GitHub security advisories. No visible Dependabot configuration.

### Dependency Profile
**[INFO]** Zero runtime dependencies. The core library is self-contained JavaScript with no npm production dependencies. DevDependencies include Rollup, Babel, Gulp, and testing tools (~20+ devDeps), but these do not ship to users. This is an excellent supply chain posture for a frontend library.

### External Resources
**[INFO]** Does NOT load external CDN resources (Google Fonts, analytics, tracking) by default. Fonts are bundled. The demo page references an S3-hosted logo (hakim-static.s3.amazonaws.com), but this is not part of the library itself. Plugin ecosystem (Markdown, highlight.js, MathJax) may introduce external loads if enabled.

### Maintenance Status
**[LOW]** Last npm release ~1 year ago (v5.2.1, ~March 2025). Repository pushed to as recently as 2026. The project is mature and stable but release cadence has slowed. The 794 open issues suggest a backlog, though many are feature requests. Single primary maintainer (Hakim El Hattab) is a bus-factor risk.

### Summary: reveal.js
| Category | Rating |
|----------|--------|
| Known CVEs | MEDIUM (historical, all patched) |
| Security Policy | LOW (none published) |
| Dependency Hygiene | INFO (excellent -- zero runtime deps) |
| External Resources | INFO (none by default) |
| Maintenance Posture | LOW (mature but slow cadence, single maintainer) |

---

## 2. slidevjs/slidev

**Version:** 52.14.1 (released 2026-03-03)
**License:** MIT
**Stars:** 44.7k | **Open Issues:** ~157 | **Contributors:** 335 | **Releases:** 419

### Known CVEs
**[INFO]** No known CVEs found in NVD, Snyk, or GitHub Advisory Database for Slidev specifically. One GitHub issue (#2211) was a false positive where antivirus flagged powershell.exe invocation during Vite dev server startup -- not an actual vulnerability.

### Security Policy
**[LOW]** No SECURITY.md or formal security policy published. No GitHub security advisories.

### Dependency Profile
**[HIGH]** Very large dependency tree. Slidev is built on Vue 3, Vite, UnoCSS, Shiki, Monaco Editor, VueUse, Iconify, KaTeX, Mermaid, and Drauu. A typical `npm install` of @slidev/cli pulls in hundreds of transitive dependencies. This represents a significant supply chain attack surface, especially given the September 2025 npm ecosystem compromise (CISA alert) which affected packages like chalk, debug, and ansi-styles that are common transitive dependencies of Vite/Vue toolchains.

### External Resources
**[MEDIUM]** Loads Google Fonts via CDN by default. Font provider is configurable, and local fonts can be specified, but out-of-the-box behavior makes network requests to Google. This has GDPR implications (EU court rulings have found Google Fonts loading without consent to be a GDPR violation). Iconify icons may also load via CDN.

### Maintenance Status
**[INFO]** Excellent maintenance posture. 419 releases, most recent 6 days ago. Led by Anthony Fu with a large contributor base. Active issue triage and responsive maintenance. Monorepo structure with well-organized packages.

### Architectural Consideration
**[MEDIUM]** Slidev runs a local Vite dev server that executes arbitrary Vue components from Markdown files. This is by design (it is a developer tool), but means opening an untrusted .md file in Slidev could execute arbitrary JavaScript. This is similar to VS Code's trust model -- the user should only open trusted content.

### Summary: Slidev
| Category | Rating |
|----------|--------|
| Known CVEs | INFO (none found) |
| Security Policy | LOW (none published) |
| Dependency Hygiene | HIGH (massive dep tree, large attack surface) |
| External Resources | MEDIUM (Google Fonts CDN by default, GDPR concern) |
| Maintenance Posture | INFO (excellent, very active) |
| Execution Model | MEDIUM (executes arbitrary code from slide content by design) |

---

## 3. impress/impress.js

**Version:** 2.0.0 (released July 2022)
**License:** MIT
**Stars:** 38.5k | **Open Issues:** ~51 | **Contributors:** 88

### Known CVEs
**[INFO]** No known CVEs found in NVD, Snyk, or GitHub Advisory Database for impress.js.

### Security Policy
**[LOW]** No SECURITY.md or formal security policy published. No GitHub security advisories.

### Dependency Profile
**[INFO]** Zero runtime dependencies. Like reveal.js, impress.js is a standalone JavaScript library that does not use jQuery or any other runtime library. Build/dev dependencies exist (buildify) but do not ship. Minimal supply chain attack surface.

### External Resources
**[INFO]** Does NOT load external CDN resources by default. No fonts, analytics, or tracking. Pure CSS3 transforms and transitions.

### Maintenance Status
**[CRITICAL]** Last tagged release: v2.0.0 in July 2022 -- nearly 4 years ago. The project appears effectively unmaintained. While 51 issues remain open and 8 PRs are pending, there is no evidence of active triage. The project went through a 4-year hiatus before the 2.0 release, and appears to have entered another dormant period. Any security issues discovered would likely go unpatched indefinitely.

### Summary: impress.js
| Category | Rating |
|----------|--------|
| Known CVEs | INFO (none found) |
| Security Policy | LOW (none published) |
| Dependency Hygiene | INFO (excellent -- zero runtime deps) |
| External Resources | INFO (none by default) |
| Maintenance Posture | CRITICAL (effectively unmaintained since July 2022) |

---

## 4. marp-team/marp

**Version:** marp-cli v4.2.3 (released ~August 2025), marp-core v4.x
**License:** MIT
**Stars:** 10.6k | **Open Issues:** varies by sub-repo | **Contributors:** 13

### Known CVEs
**[INFO]** No known CVEs found in NVD, Snyk, or GitHub Advisory Database for any Marp packages (marp-core, marp-cli, marpit).

### Security Policy
**[LOW]** No SECURITY.md or formal security policy published across the Marp organization.

### Dependency Profile
**[HIGH]** Marp CLI depends on Puppeteer/Chromium for PDF, PPTX, and image export. This is a very large dependency (~400MB+ for Chromium alone) with a significant attack surface. Chromium vulnerabilities are frequent and well-documented. Additionally, marp-core uses KaTeX for math rendering, which loads web fonts from jsDelivr CDN by default.

### External Resources
**[MEDIUM]** By default, Marp Core loads web-font resources through jsDelivr CDN. The helper script can be injected inline (default, works offline) or referenced through jsDelivr. The Marp team explicitly does NOT recommend importing external resources in CSS. Local font paths can be configured as an alternative.

### Puppeteer/Chromium Concern
**[MEDIUM]** Marp CLI's reliance on Puppeteer for rendering introduces a headless Chromium instance. Common deployment patterns (especially Docker) often run Chromium with --no-sandbox, which significantly increases risk if processing untrusted content. Chrome/Chromium RCE vulnerabilities are discovered regularly. The Marp team is small and cannot guarantee rapid Chromium version bumps.

### Maintenance Status
**[LOW]** Last CLI release ~7 months ago (v4.2.3, ~August 2025). The team acknowledges limited resources. The project is functional but development velocity is modest. The monorepo umbrella (marp-team/marp) was last updated July 2023, though sub-packages are more recent. Some sub-projects (Marp Web, Marp React, Marp Vue) are explicitly marked as outdated/archived.

### Summary: Marp
| Category | Rating |
|----------|--------|
| Known CVEs | INFO (none found) |
| Security Policy | LOW (none published) |
| Dependency Hygiene | HIGH (Puppeteer/Chromium is massive attack surface) |
| External Resources | MEDIUM (jsDelivr CDN for fonts by default) |
| Maintenance Posture | LOW (small team, modest cadence, some sub-projects archived) |
| Chromium Risk | MEDIUM (headless browser for export, sandbox concerns) |

---

## Comparative Summary

| | reveal.js | Slidev | impress.js | Marp |
|---|-----------|--------|------------|------|
| **Known CVEs** | 2 (patched) | 0 | 0 | 0 |
| **Security Policy** | None | None | None | None |
| **Runtime Deps** | 0 | Hundreds | 0 | Hundreds + Chromium |
| **External CDN Default** | No | Yes (Google Fonts) | No | Yes (jsDelivr) |
| **Last Release** | ~Mar 2025 | Mar 2026 | Jul 2022 | ~Aug 2025 |
| **Maintenance** | Stable/slow | Excellent | Unmaintained | Modest |
| **GDPR Concern** | No | Yes | No | Minor |
| **Highest Finding** | MEDIUM | HIGH | CRITICAL | HIGH |

## Recommendations

1. **For maximum security posture:** reveal.js offers the best profile -- zero runtime deps, no external resource loading, patched CVEs. The main risk is slower maintenance cadence.

2. **For active development:** Slidev has the best maintenance but the largest attack surface. Pin dependency versions, use lockfiles, audit regularly, and configure `fonts.local` to avoid Google Fonts CDN calls.

3. **Avoid for new projects:** impress.js is effectively unmaintained. Any future vulnerability would go unpatched.

4. **For Marp users:** Be aware of the Chromium dependency. Keep Puppeteer updated, never run with --no-sandbox in production, and configure local fonts to avoid CDN calls.

5. **Universal:** None of these projects publish a SECURITY.md. For any production use, establish your own vulnerability monitoring via Snyk, npm audit, or GitHub Dependabot on your consuming project.
