"""
Build script for the Nexcon site.

Instead of copy-pasting the header and footer into every page by hand,
this script keeps ONE copy of each (in partial/header.html and
partial/footer.html) and stitches them into your actual page files,
in place.

Folder layout it expects (matches your project):

  styles.css
  partial/
    header.html      <- shared <header> (with {{HOME}} / {{ABOUT_ACTIVE}} tokens)
    footer.html       <- shared <footer> + the nav-toggle/year script
  home/
    index.html        <- home page. Should contain <!-- HEADER --> and
                          <!-- FOOTER --> where those pieces belong.
  about/
    index.html         <- about page. Same deal.

How the tokens work:
  <!-- HEADER -->   in a page gets replaced with partial/header.html
  <!-- FOOTER -->   in a page gets replaced with partial/footer.html
  {{HOME}}          inside header/footer becomes "" on the home page itself
                    (so links stay instant same-page anchors like "#services"),
                    and "../home/" on every other page (so the link actually
                    navigates back to the homepage's section).
  {{ABOUT_ACTIVE}}  becomes ' class="is-active"' on the About page's own nav
                    link, and "" everywhere else.

Safe to run more than once: if a page has already been built (no
<!-- HEADER --> / <!-- FOOTER --> left in it), running this again just
leaves it unchanged.

To add a new page later (e.g. "contact"):
  1. Create contact/index.html with <!-- HEADER --> / <!-- FOOTER --> in it.
  2. Add an entry to the PAGES list below.
  3. Run this script again.

Usage:
    python3 build.py
"""

from pathlib import Path

ROOT = Path(__file__).parent
PARTIALS = ROOT / "partial"

# Each page: (path to its index.html, is this the homepage?)
PAGES = [
    ("home/index.html", True),
    ("about/index.html", False),
]


def build_page(page_path: str, is_home: bool) -> None:
    path = ROOT / page_path
    page_html = path.read_text(encoding="utf-8")
    header_html = (PARTIALS / "header.html").read_text(encoding="utf-8")
    footer_html = (PARTIALS / "footer.html").read_text(encoding="utf-8")

    home_prefix = "" if is_home else "../home/"
    about_active = "" if is_home else ' class="is-active"'

    header_html = header_html.replace("{{HOME}}", home_prefix)
    header_html = header_html.replace("{{ABOUT_ACTIVE}}", about_active)
    footer_html = footer_html.replace("{{HOME}}", home_prefix)

    final_html = page_html.replace("<!-- HEADER -->", header_html)
    final_html = final_html.replace("<!-- FOOTER -->", footer_html)

    path.write_text(final_html, encoding="utf-8")
    print(f"Built {page_path}")


if __name__ == "__main__":
    for page_path, is_home in PAGES:
        build_page(page_path, is_home)
    print("Done. Upload styles.css, the images at the site root, and the home/ and about/ folders.")