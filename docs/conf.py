# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#


import glob
import importlib
import os
import subprocess
import sys

from sphinx.ext import apidoc


# for apidoc
sys.path.insert(0, os.path.abspath("../isshub"))

# default env var to be used by the doc builder, for example readthedocs
# os.environ.setdefault("XXX", "yyy")


# -- Project information -----------------------------------------------------

project = "IssHub"
copyright = '2019, Stéphane "Twidi" Angel'
author = 'Stéphane "Twidi" Angel'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinxprettysearchresults",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "navigation_depth": -1,
    "collapse_navigation": True,
    "sticky_navigation": True,
    "includehidden": True,
    "titles_only": False,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "isshubdoc"

# -- Extension configuration -------------------------------------------------

html_use_old_search_snippets = True

# -- Run apidoc when building the documentation-------------------------------


def run_apidoc(_):
    """Run apidoc on the marsha project and store source doc in ``source`` dir."""
    current_dir = os.path.dirname(__file__)
    source_path = os.path.join(current_dir, "source")
    output_path = os.path.normpath(os.path.join(current_dir, "..", "isshub"))
    exclude_paths = [
        os.path.join(output_path, exclude_path) for exclude_path in ["*/tests/*"]
    ]
    apidoc.main(
        [
            "--force",
            "--module-first",
            "--separate",
            "--output-dir",
            source_path,
            output_path,
        ]
        + exclude_paths
    )
    subprocess.run(
        ["sed", "-i", "-e", r"s/ \(module\|package\)$//"]
        + glob.glob(os.path.join(source_path, "*.rst"))
    )


def setup(app):
    # Run apidoc
    app.connect("builder-inited", run_apidoc)
    # Add custom css/js for rtd template
    app.add_css_file("css/custom.css")
    app.add_js_file("js/custom.js")
    # Add git content into doc
    current_dir = os.path.dirname(__file__)
    subprocess.run(
        [
            os.path.join(current_dir, "git_to_sphinx.py"),
            os.path.normpath(os.path.join(current_dir, "..")),
        ]
    )
