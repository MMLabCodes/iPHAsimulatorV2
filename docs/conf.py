"""Sphinx configuration. Read source files only; never import simulation code."""

from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[1]
package = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
project = "iPHASimulator v2"
author = "iPHASimulator contributors"
copyright = "2026, iPHASimulator contributors"
release = package["version"]
version = release

extensions = [
    "myst_parser",
    "autoapi.extension",
    "sphinx.ext.napoleon",
    "sphinx.ext.githubpages",
]
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
root_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "**/.ipynb_checkpoints"]
myst_enable_extensions = ["colon_fence", "deflist"]
myst_heading_anchors = 3

# Static parsing avoids importing RDKit, OpenMM, Open Babel or MDAnalysis.
# There is deliberately no nbsphinx, myst-nb, doctest or notebook execution hook.
autoapi_dirs = [str(ROOT / "src" / "iphasimulator")]
autoapi_root = "autoapi"
autoapi_options = ["members", "undoc-members", "show-module-summary"]
autoapi_member_order = "bysource"
autoapi_keep_files = True
autoapi_add_toctree_entry = False
autoapi_python_use_implicit_namespaces = True
napoleon_google_docstring = True
napoleon_numpy_docstring = True

html_theme = "sphinx_rtd_theme"
html_logo = "logo.png"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_title = "iPHASimulator v2 documentation"
html_theme_options = {
    "logo_only": False,
    "navigation_depth": 3,
    "collapse_navigation": True,
    "style_nav_header_background": "#163b46",
}
html_context = {
    "display_github": True,
    "github_user": "MMLabCodes",
    "github_repo": "iPHAsimulatorV2",
    "github_version": "main",
    "conf_py_path": "/docs/",
}
html_last_updated_fmt = None

# External links are checked separately: network availability must not decide
# whether pull requests can build the documentation.
linkcheck_timeout = 20
linkcheck_retries = 2
linkcheck_anchors = False


def format_existing_docstrings(app, what, name, obj, options, lines):
    """Repair two presentation-only RST defects without editing package sources."""
    # AutoAPI emits local names (rather than fully qualified names) in this event.
    text = "\n".join(lines)
    if name.endswith("get_platform") and "Select the OpenMM platform." in text:
        # This source docstring has an under-indented NumPy section underline.
        lines[:] = [line[4:] if line.startswith("    ") else line for line in lines]
    elif name.endswith("build_PHA_copolymer") and "existing PHA monomer-unit prepins" in text:
        # Mark the already-indented examples/output names as literal blocks.
        labels = {"Patterned AB copolymer:", "Random copolymer:", "Patterned:", "Random:"}
        lines[:] = [line + ":" if line.strip() in labels else line for line in lines]


def configure_page_links(app, pagename, templatename, context, doctree):
    """Generated API pages have no corresponding tracked file on GitHub."""
    if pagename.startswith("autoapi/"):
        context["display_github"] = False


def setup(app):
    # Run before Napoleon's NumPy/Google conversion (default priority 500).
    app.connect("autodoc-process-docstring", format_existing_docstrings, priority=100)
    app.connect("html-page-context", configure_page_links)
