# stdlib
import pathlib
import re
from typing import Dict

# 3rd party
from docutils import nodes


class blogpost_node(nodes.Structural, nodes.Element):
	pass


def asset_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
	"""Link to an asset.

	Returns 2 part tuple containing list of nodes to insert into the
	document and a list of system messages.  Both are allowed to be
	empty.

	:param name: The role name used in the document.
	:param rawtext: The entire markup snippet, with role.
	:param text: The text marked with the role.
	:param lineno: The line number where rawtext appears in the input.
	:param inliner: The inliner instance that called us.
	:param options: Directive options for customization.
	:param content: The directive content for customization.
	"""

	ref = re.findall(r"<.*>", text)
	if ref:
		ref = ref[0].lstrip('<').rstrip('>')
		link_text = re.split(r"<.*>", text)[0]
	else:
		if text.startswith('~'):
			ref = text[1:]
			link_text = pathlib.Path(text[1:]).name
		else:
			ref = text
			link_text = text

	# try:
	# 	issue_num = int(text)
	# 	if issue_num <= 0:
	# 		raise ValueError
	# except ValueError:
	# 	msg = inliner.reporter.error(
	# 		'BitBucket issue number must be a number greater than or equal to 1; '
	# 		'"%s" is invalid.' % text, line=lineno)
	# 	prb = inliner.problematic(rawtext, rawtext, msg)
	# 	return [prb], [msg]
	app = inliner.document.settings.env.app
	node = make_link_node(rawtext, app, ref, link_text, options)
	return [node], []


def make_link_node(rawtext, app, ref, link_text: str, options: Dict):
	"""Create a link to an asset.

	:param rawtext: Text being replaced with link node.
	:param app: Sphinx application context
	:param ref:
	:param link_text:
	:param options: Options dictionary passed to role func.
	"""

	try:
		base = app.config.assets_base
		if not base:
			raise AttributeError
	except AttributeError as err:
		raise ValueError(f'assets_base configuration value is not set ({str(err)})')
	# #
	# slash = '/' if base[-1] != '/' else ''
	# ref = base + slash + type + '/' + slug + '/'
	# set_classes(options)
	node = nodes.reference(rawtext, link_text, refuri=f"{base}/{ref}", **options)
	return node


def setup(app):
	app.add_role("asset", asset_role)
	app.add_config_value("assets_base", "/notebook/_static", "env")
	return
