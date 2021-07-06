# -*- coding: utf-8 -*-
import os
import sys
import catkin_sphinx

sys.path.insert(0, os.path.abspath("../."))

project = "P3IV Documentation"
copyright = "2021, FZI Forschungszentrum Informatik"
author = "Ö. Şahin Taş"

release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "m2r2",
]

source_suffix = [".rst", ".md"]

templates_path = ["_templates"]

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"

html_static_path = ["_static"]

# todo configuration
todo_include_todos = True
