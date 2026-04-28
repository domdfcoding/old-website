# 3rd party
import tabulate
from git_helper import GitHelper
from git_helper.shields import make_rtfd_shield, make_travis_shield

# this package
from project_list import project_list, repos_dir

header = """\
======================
Build Status
======================


"""

corner = '+'
side = '|'
top = '-'


class Project:

	def __init__(
			self,
			name,
			*,
			travis=True,
			travis_name=None,
			travis_site="com",
			appveyor=False,
			appveyor_name=None,
			rtfd=True,
			rtfd_name=None,  # TODO: docker
			):
		self.name = str(name)
		self.travis = travis
		self.travis_site = travis_site
		self.appveyor = appveyor
		self.rtfd = rtfd

		if travis_name:
			self.travis_name = str(travis_name)
		else:
			self.travis_name = self.name

		if appveyor_name:
			self.appveyor_name = str(appveyor_name)
		else:
			self.appveyor_name = self.name

		if rtfd_name:
			self.rtfd_name = str(rtfd_name)
		else:
			self.rtfd_name = self.name

	def table_data(self):
		return [
				self.name,
				self.travis_badge if self.travis else '',
				self.rtfd_badge if self.rtfd else '',
				self.appveyor_badge if self.appveyor else '',
				]

	@property
	def appveyor_badge(self):
		return f"""
.. image:: https://img.shields.io/appveyor/build/domdfcoding/{self.appveyor_name}/master?logo=appveyor
    :target: https://ci.appveyor.com/project/domdfcoding/{self.appveyor_name}
    :alt: {self.name} build status (Appveyor)\
"""

	@property
	def travis_badge(self):
		return make_travis_shield(self.travis_name, "domdfcoding", self.travis_site)

	@property
	def rtfd_badge(self):
		return make_rtfd_shield(self.rtfd_name)


projects = []

for repo in project_list:
	gh = GitHelper(repos_dir / repo)
	projects.append(
			Project(
					gh.templates.globals["repo_name"],
					rtfd_name=gh.templates.globals["repo_name"],
					travis_site=gh.templates.globals["travis_site"],
					),
			)

projects += [
		Project("Cawdrey", travis_site="org", rtfd_name="cawdrey"),
		Project("PyMassSpec", travis_site="org", appveyor=True, rtfd_name="pymassspec"),
		Project("pyms-nist-search", travis=False, appveyor=True),
		Project("msp2lib", appveyor=True),
		]

table = tabulate.tabulate([project.table_data() for project in projects], tablefmt="rst")
print(table)

with open("source/build_status.rst", 'w') as fp:
	fp.write(header)
	fp.write(table)
