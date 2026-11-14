# portwally.github.io

Static GitHub Pages site (plain HTML/CSS/JS, no build). Every app has its own folder with an `index.html`. The start page is `index.html`; `cat.html` is a plain list of all pages; `sitemap.xml` lists every URL.

## Footer cross-links: always check them (standing job)

The GitHub Action "Check cross-links" (`.github/workflows/check-cross-links.yml`) fails when the footer links of the sub-app pages drift from the apps listed on the start page. **Keeping it green is Claude's job.** Whenever a page or app is added, renamed, removed, or listed on the start page, and before any push that touches `index.html`, `Retro Computing/`, a footer, or a new folder:

1. Run `.github/check-footers.sh` from the repo root. It runs the same shell code as the workflow, so what it prints is what CI will say.
2. Fix every drift it reports, then run it again until it prints `ALL FOOTER CHECKS PASS`.
3. After pushing, confirm the run on that commit is green (`gh run list --workflow check-cross-links.yml --limit 1`).

Do this unasked, also when the user only asks to "add a page" or "list it on the home page". Never push with a failing check without saying so.

### The two kinds of footer

**Normal pages** (all Mac, iOS, Portugal and other pages): the footer must link to **every** app that the start page links as `href="X/"`, except the page itself. So a new app listed on the start page needs a link in the footer of every normal page.

**Apple II pages** keep the **shorter footer**: it links only to the other Apple IIgs programs and the macOS retro apps, exactly the set the 1977 page (`Retro Computing/index.html`) links with `../X/`, plus a link to `Retro Computing` itself, minus the page itself. These pages are listed in `RETRO_REGEX` in the workflow:
`TileTown`, `TileTown 2`, `Conquer-GS`, `Conquer3`, `GSCommander`, `GSLauncher`, `MegaconvertGS`, `EmuBuddy`, `Hyperhaul`, `GTApple`.

Adding a new Apple IIgs program or retro Mac app therefore means all of this:
- add the folder name to `RETRO_REGEX` in the workflow;
- add a menu entry (`<li class="l6">`, with `data-img`, `data-name`, `data-desc`) to `Retro Computing/index.html`;
- link it from the footer of every other Apple II page, in that page's own footer style;
- link it from the footer of every normal page too (it is on the start page);
- give the new page itself a footer that links to all the other Apple II / retro pages.

### Rules the check enforces

- Footer links are `../Folder/`. Folders with a space are written `%20` (`../Wallys%20Manager/`, `../TileTown%202/`); the audit decodes `%20` for normal pages, but **Fire's check compares the raw text**, so Fire must use `%20` exactly as the start page does.
- Only pages with at least 3 `../X/` links are audited (a body link counts as a link, so a link in the page text also satisfies the check).
- Skipped folders: `.github`, `casalilli`, `node_modules`, `assets`, `Fire` (own job), `The Holy War`, and any folder not linked from the start page.
- **IIgs Demos** (`Demos/`) is a normal page for the start-page rule. It is also listed on the 1977 page and linked from the Apple II footers.
- Footer styles differ per page (inline `<p>` lists, `<li>` lists, one link per line, grouped paragraphs). Insert the new link in the same style as its neighbours.

## Adding a page: the full list

New app/page = folder with `index.html`, then: start-page entry in `index.html` (number, icon in `assets/icons/`, tag text in all 12 languages in the `T` table, app counts), `cat.html` button (and a colour rule if the grid has more entries than colour rules), `sitemap.xml` entry, footers (see above), and the 1977 page if it is an Apple II / retro page.

## Demos page

`Demos/` is only for Apple IIgs **demos** (no software, no games, no counts in the wording). Each demo is one block in `Demos/index.html` with a still image, a compressed video and the `.po` disk image.

## Commits

Do not commit other people's or other sessions' uncommitted work; stage only the files you changed. End commit messages with the Co-Authored-By line required by the session.
