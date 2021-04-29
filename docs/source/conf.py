# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../../tools/build/'))

from builders import buildExamples as be
from builders import buildFeatures as bf
from builders import buildModules as bm
from builders import buildTools as bt
from builders import buildTests as btst

import build_all_source

import subprocess as sp

# -- Project information -----------------------------------------------------
project = 'korali'
copyright = 'ETH Zurich'
author = 'CSELab'

# Build generated code
build_all_source.buildAllSource('../../source/','../generated_code/')

# Build rst files
be.build_examples('../../examples/', './examples/')
bf.build_features('../../examples/features/', './features/')
bm.build_modules('../../source/modules/', './modules/')
bt.build_tools('../../python/korali/', './using/tools/')
btst.build_tests('../../tests/', './dev/')

# Run doxygen
sp.run('(cd .. && doxygen)', shell=True) # compile the xml source

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
  'sphinx.ext.todo',
  'sphinx.ext.mathjax',
  'sphinx_rtd_theme',
  'breathe',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# breathe extension
breathe_default_project = "korali"
breathe_projects = {
        "korali": "../doxygen/xml"
}
breathe_domain_by_extension = { "h" : "cpp", "cu" : "cpp" }

# Tell sphinx what the primary language being documented is
primary_domain = 'cpp'

# Tell sphinx what the pygments highlight language should be
highlight_language = 'cpp'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If false, no module index is generated.
html_domain_indices = True

# If false, no index is generated.
html_use_index = True

# If true, the index is split into individual pages for each letter.
html_split_index = False

# If true, links to the reST sources are added to the pages.
html_show_sourcelink = False

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = False

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
html_show_copyright = True


