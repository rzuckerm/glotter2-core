import sys
from pathlib import Path

# Ensure the project's `src` directory is on sys.path so Sphinx can import packages
ROOT = str(Path(__file__).parent.parent.resolve())
SYS_SRC = str(Path(ROOT) / "src")
if SYS_SRC not in sys.path:
    sys.path.insert(0, SYS_SRC)

project = "Glotter 2-Core"
copyright = ""
author = ""

html_show_copyright = False

version = ""
release = ""

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx_rtd_theme",
]

templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"

html_theme = "sphinx_rtd_theme"
html_static_path = []
html_favicon = "favicon.gif"
html_logo = "images/glotter2_small.png"
