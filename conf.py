# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import re
import sys
from sphinx.ext import apidoc

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Example'
copyright = '2021, Donal Fellows'
author = 'Donal Fellows'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

_output_dir = os.path.abspath(".")
_unfiltered_files = os.path.abspath("unfiltered-files.txt")
_shorten_class_names = False

# Automatically called by sphinx at startup
def setup(app):
    # NB: extra dot at end is deliberate!
    trim = ("foo.", )

    # Magic to shorten the names of our classes to their public versions
    def skip_handler(_app, what, name, obj, skip, _options):
        if not skip and what == 'module' and hasattr(obj, "__module__"):
            # Get parent module *and* check if our name is in it
            m = re.sub(r'\.[a-z0-9_]+$', '', obj.__module__)
            if any(m.startswith(prefix) for prefix in trim) and \
                    name in dir(sys.modules[m]):
                print("SHORTENING MODULE NAME FOR", obj, "TO", m)
                # It is, so update to say that's canonical location for
                # documentation purposes
                obj.__module__ = m
        return skip  # We don't care to change this

    if _shorten_class_names:
        # Connect the callback to the autodoc-skip-member event from apidoc
        app.connect('autodoc-skip-member', skip_handler)

def filtered_files(base, unfiltered_files_filename):
    with open(unfiltered_files_filename) as f:
        lines = [line.rstrip() for line in f]
    # Skip comments and empty lines to get list of files we DON'T want to
    # filter out; this is definitely complicated
    unfiltered = set(
        line for line in lines if not line.startswith("#") and line != "")
    for root, _dirs, files in os.walk(base):
        for filename in files:
            if filename.endswith(".py") and not filename.startswith("_"):
                full = root + "/" + filename
                if full not in unfiltered:
                    print("FILTERING FILE IN __init__:", full)
                    yield full

apidoc.main([
    '-q', '-o', _output_dir, "foo",
    *filtered_files("foo", _unfiltered_files)])
