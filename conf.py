# Configuration file for the Sphinx documentation builder.

#### SET THIS TO True TO TURN ON THE WORKAROUND FOR THE BUG
_shorten_class_names = False

# -- Imports -----------------------------------------------------------------

import os
import re
import sys
from sphinx.ext import apidoc

# -- Path setup --------------------------------------------------------------

sys.path.insert(0, os.path.abspath('.'))
_output_dir = os.path.abspath(".")
_unfiltered_files = os.path.abspath("unfiltered-files.txt")

# -- Project information -----------------------------------------------------

project = 'Example'
copyright = '2021, Donal Fellows'
author = 'Donal Fellows'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc'
]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = 'bizstyle'
html_static_path = ['_static']

# -- Customisation code ------------------------------------------------------

def setup(app):
    """
    Connects (if enabled) a handler that rewrites objects to have the right
    (public) module names.
    """
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

# We want to run apidoc every time; that's how the real project rolls
# It's important when the project moves internal class structure around
apidoc.main(['-q', '-o', _output_dir, "foo", 'foo/bar/grill.py'])
