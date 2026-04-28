#!/usr/bin/env python3

# This file is managed by `git_helper`. Don't edit it directly

# stdlib
import os
import re
import sys
import warnings

# 3rd party
from sphinx.locale import _

# Suppress warnings from sphinx_autodoc_typehints
# TODO: Remove once the following issues is resolved:
# https://github.com/agronholm/sphinx-autodoc-typehints/issues/133
warnings.filterwarnings('ignore', message=r'sphinx.util.inspect.Signature\(\) is deprecated')

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('..'))




github_url = f"https://github.com/domdfcoding/domdfcoding"

rst_prolog = f""".. |pkgname| replace:: domdfcoding
.. |pkgname2| replace:: ``domdfcoding``
.. |browse_github| replace:: `Browse the GitHub Repository <{github_url}>`__
"""

author = "Dominic Davis-Foster"
project = "domdfcoding"
slug = re.sub(r'\W+', '-', project.lower())
copyright = "2020 Dominic Davis-Foster"  # pylint: disable=redefined-builtin
language = 'en'
package_root = "/"

extensions = [
		'sphinx.ext.intersphinx',
		'sphinx.ext.autodoc',
		'sphinx.ext.mathjax',
		'sphinx.ext.viewcode',
		'sphinxcontrib.httpdomain',
		"sphinxcontrib.extras_require",
		"sphinx.ext.todo",
		"sphinxemoji.sphinxemoji",
		"sphinx_tabs.tabs",
		"sphinx-prompt",
		"sphinx_autodoc_typehints",
		"sphinx.ext.autosummary",
		'asset_role',
		"sphinxcontrib.youtube",
		]

sphinxemoji_style = 'twemoji'
todo_include_todos = bool(os.environ.get("SHOW_TODOS", False))

templates_path = ['_templates']
html_static_path = ['_static', "_assets"]
source_suffix = '.rst'
exclude_patterns = []

master_doc = 'index'
suppress_warnings = ['image.nonlocal_uri']
pygments_style = 'default'

intersphinx_mapping = {
		'rtd': ('https://docs.readthedocs.io/en/latest/', None),
		'sphinx': ('https://www.sphinx-doc.org/en/stable/', None),
		'python': ('https://docs.python.org/3/', None),
		"NumPy": ('https://numpy.org/doc/stable/', None),
		"SciPy": ('https://docs.scipy.org/doc/scipy/reference', None),
		"matplotlib": ('https://matplotlib.org', None),
		"h5py": ('https://docs.h5py.org/en/latest/', None),
		"Sphinx": ('https://www.sphinx-doc.org/en/stable/', None),
		"Django": ('https://docs.djangoproject.com/en/dev/', 'https://docs.djangoproject.com/en/dev/_objects/'),
		"sarge": ('https://sarge.readthedocs.io/en/latest/', None),
		"attrs": ('https://www.attrs.org/en/stable/', None),
		'domdf_python_tools': ('https://domdf-python-tools.readthedocs.io/en/latest/', None),
		}

html_theme = 'sphinx_typo3_theme'
html_theme_options = {
		'logo_only': False,
		}
html_theme_path = ["../.."]
html_logo = "profile_pic.jpeg"
html_show_sourcelink = False  # True will show link to source

html_context = {
		# Github Settings
		"display_github": False,  # Integrate GitHub
		"github_user": "domdfcoding",  # Username
		"github_repo": "domdfcoding.github.io",  # Repo name
		"github_version": "master",  # Version
		"conf_py_path": "/",  # Path in the checkout to the docs root
		"theme_docstypo3org": True,
		"theme_project_home": "https://www.github.com/domdfcoding",
		"logo_width": 500,
		"logo_height": 500,
		}

htmlhelp_basename = slug

latex_documents = [
		('index', f'{slug}.tex', project, author, 'manual'),
		]

man_pages = [
		('index', slug, project, [author], 1)
		]

texinfo_documents = [
		('index', slug, project, author, slug, project, 'Miscellaneous'),
		]


# Extensions to theme docs
def setup(app):
	from sphinx.domains.python import PyField
	from sphinx.util.docfields import Field

	app.add_object_type(
			'confval',
			'confval',
			objname='configuration value',
			indextemplate='pair: %s; configuration value',
			doc_field_types=[
					PyField(
							'type',
							label=_('Type'),
							has_arg=False,
							names=('type',),
							bodyrolename='class'
							),
					Field(
							'default',
							label=_('Default'),
							has_arg=False,
							names=('default',),
							),
					]
			)
