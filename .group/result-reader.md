# Human-readable strategy result

`result.html` is a derived view of the product's current native Markdown, generated after final checks. It does not replace any document, change its contract, accept a decision, execute an action or upgrade an evidence state.

## Required properties

- The reader supplies product-specific reading paths, search, progressive detail, local record/document navigation, complete source downloads and visible source status.
- Every consumed document's exact text, relative source identity and SHA256 remain embedded. A short visible excerpt is identified by the document it opens; full text stays available.
- Brand embeds explicitly referenced supported native media within the current state, where supplied, and makes their files available. Evidence directories and external source assets are not silently imported. Missing or external material remains a source condition, never a fabricated asset.
- The HTML contains its data, CSS, scripts, required fonts and available displayed material. It reads and interacts from a local file without a server or network. Product code bundles its own assets and font licences.
- The generator reads current top-level state and supported native subdirectories (audience messages, product value models and strategy reviews); it never silently overlays candidates or scans unrelated evidence, requests or owner source material.
- `python3 {product-root}/.group/tools/result_html.py {state-directory} [--out FILE] [--open]` writes only derived HTML. Omit `--open` for intermediate checks; final delivery opens once. Failure to open is reported with the retained complete path.

## Acceptance

Check source byte fidelity, actual record/status meaning, local navigation and its missing/empty states, keyboard/focus, phone/desktop and asset resolution. Verify generation and reading from a clean isolated product copy with the original repository unavailable and network disabled. Producing-agent clarity self-review and owner review are distinct from executable rendering checks.

For a final delivery that combines current documents and proposed revisions, pass `--candidate` explicitly to overlay matching files from `STATE_DIRECTORY/candidate/`. The HTML records those exact candidate source paths and statuses; generation grants no acceptance. Without this flag the current source set is exported. Point `STATE_DIRECTORY` directly at a standalone final/candidate document directory when that is the complete delivered result. Never substitute older current documents for the version actually delivered.

## Tool view and compatible result commands

The tool guide describes this product's mechanics and is generated from definitions with the same product-local shell/assets as the result reader. It does not replace or accept native state. Established state-view commands delegate to the result reader; candidate overlays, explicit current/proposed comparison and scoped record links retain their meanings. Shared references and product-local SIT/MCH/CASE references remain distinct. Native material remains available as contained downloads. `--compare-candidates` shows both revisions without accepting either.
