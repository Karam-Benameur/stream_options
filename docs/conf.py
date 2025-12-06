# Configuration file for the Sphinx documentation builder.

import os
import sys

# Ajoute la racine du projet au PYTHONPATH pour que Sphinx trouve core, pages, etc.
sys.path.insert(0, os.path.abspath('..'))

# -- Informations sur le projet -----------------------------------------------------

project = 'StreamOptions'
author = 'Groupe StreamOptions (M1 SSD)'
release = '0.1'

# -- Extensions Sphinx --------------------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',        # génère la doc à partir des docstrings
    'sphinx.ext.napoleon',       # support des docstrings style NumPy/Google
    'sphinx.ext.viewcode',       # lien vers le code source
    'sphinx.ext.autosummary',    # tableaux récapitulatifs
]

autosummary_generate = True
autodoc_typehints = 'description'

# -- Templates & patterns -----------------------------------------------------------

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Thème HTML ---------------------------------------------------------------------

html_theme = "sphinx_rtd_theme"

html_theme_options = {
    
}
   # thème simple par défaut
html_static_path = ['_static']
