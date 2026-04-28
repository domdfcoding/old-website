# stdlib
import pathlib
import re

# 3rd party
import repo_helper.readme
from jinja2 import BaseLoader, Environment
from repo_helper import readme
from repo_helper.core import GitHelper

# this package
from project_list import project_list

# TODO: get from github
repos_dir = pathlib.Path("~/Python/01 GitHub Repos").absolute()
projects_file = pathlib.Path("./source/projects.rst")

links_block_template = Environment(loader=BaseLoader).from_string(
		"""\
.. start links {{ unique_name.lstrip("_") }}

View the project on `GitHub <https://github.com/{{ username }}/{{ repo_name }}>`__.
Read the `documentation <https://{{ repo_name.lower() }}.rtfd.io>`__.

.. end links
"""
		)


def create_links_block(username: str, repo_name: str, unique_name: str = ''):
	if unique_name:
		unique_name = f"_{unique_name}"
	return links_block_template.render(
			username=username,
			repo_name=repo_name,
			unique_name=unique_name,
			)


def create_short_desc_block(short_desc: str, unique_name: str) -> str:
	if unique_name:
		unique_name = f"_{unique_name}"

	return f"""\
.. start short_desc{unique_name}

**{short_desc}**

.. end short_desc"""


def populate_projects(templates):
	"""

	:param templates:
	:type templates: jinja2.Environment
	"""

	shields_block = repo_helper.readme.create_shields_block(
			username="domdfcoding",
			repo_name=templates.globals["repo_name"],
			version=templates.globals["version"],
			conda=templates.globals["enable_conda"],
			tests=templates.globals["enable_tests"],
			docs=templates.globals["enable_docs"],
			travis_site=templates.globals["travis_site"],
			pypi_name=templates.globals["pypi_name"],
			docker_shields=templates.globals["docker_shields"],
			docker_name=templates.globals["docker_name"],
			platforms=templates.globals["platforms"],
			unique_name=templates.globals["import_name"],
			)

	if templates.globals["license"] == "GNU General Public License v2 (GPLv2)":
		shields_block.replace(
				f"https://img.shields.io/github/license/domdfcoding/{templates.globals['repo_name']}",
				"https://img.shields.io/badge/license-GPLv2-orange",
				)

	links_block = create_links_block(
			"domdfcoding", templates.globals["repo_name"], templates.globals["import_name"]
			)
	short_desc_block = create_short_desc_block(templates.globals["short_desc"], templates.globals["import_name"])

	projects = projects_file.read_text()

	if f"""\
{templates.globals["modname"]}
-----""" not in projects:
		projects += f"""
.. _{templates.globals["modname"]}:

{templates.globals["modname"]}
{'-' * (len(templates.globals["modname"]) + 5)}

.. description goes here

.. start short_desc_{templates.globals["import_name"]}
.. end short_desc_{templates.globals["import_name"]}

.. start links_{templates.globals["import_name"]}
.. end links_{templates.globals["import_name"]}

.. start shields {templates.globals["import_name"]}
.. end shields {templates.globals["import_name"]}

"""

	unique_name = templates.globals["import_name"].replace('_', "\\_")

	print(f'.. start short_desc_{unique_name}')

	projects = re.sub(
			fr'(?s)(\.\. start short_desc_{unique_name})\n(.*?)(\.\. end short_desc)',
			short_desc_block,
			projects,
			)

	projects = re.sub(
			fr'(?s)(\.\. start shields {unique_name})\n(.*?)(\.\. end shields)',
			shields_block,
			projects,
			)

	projects = re.sub(
			fr'(?s)(\.\. start links_{unique_name})\n(.*?)(\.\. end links)',
			links_block,
			projects,
			)

	with projects_file.open('w') as fp:
		fp.write(projects)


def depopulate_projects(templates):
	"""

	:param templates:
	:type templates: jinja2.Environment
	"""

	unique_name = templates.globals["import_name"].replace('_', "\\_")
	projects = projects_file.read_text()

	projects = re.sub(
			fr'(?s)(\.\. start shields_{unique_name})(.*?)(\.\. end shields)',
			f".. start shields {templates.globals['import_name']}\n.. end shields",
			projects,
			)

	projects = re.sub(
			fr'(?s)(\.\. start links_{unique_name})(.*?)(\.\. end links)',
			f".. start links {templates.globals['import_name']}\n.. end links",
			projects,
			)

	with projects_file.open('w') as fp:
		fp.write(projects)


if __name__ == "__main__":
	# stdlib
	import argparse

	parser = argparse.ArgumentParser(description='')
	parser.add_argument(
			"--populate",
			action="store_true",
			default=False,
			help="Populate the `projects.rst` file.",
			)
	parser.add_argument(
			"--depopulate",
			action="store_true",
			default=False,
			help="Depopulate the `projects.rst` file to make for easier editing.",
			)

	args = parser.parse_args()

	for repo in project_list:
		repo_path = repos_dir / repo
		gh = GitHelper(repo_path)

		if args.depopulate:
			depopulate_projects(gh.templates)
		else:
			populate_projects(gh.templates)
