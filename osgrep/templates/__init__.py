#!/usr/bin/env python

from jinja2 import Environment, PackageLoader

env = Environment()
env.loader = PackageLoader('osgrep', 'templates')


def load(name, params):
    """
    Load a template from the osgrep.templates package
    :param name: template name
    :type name: string
    """
    return env.get_template(name + ".tpl").render(**params)
