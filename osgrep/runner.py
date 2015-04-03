#!/usr/bin/env python

from fabric.api import settings, hide
from fabric.operations import sudo


from osgrep.templates import load as load_template


class Runner(object):

    def __init__(self, services):
        self.services = services

    def grep(self, expression):
        for name, service in self.services.items():
            for unit in service:
                
                kwargs = {
                    'user': unit.server.username,
                    'port': unit.server.port,
                    'host_string': unit.server.hostname,
                    'warn_only': True,
                }

                if hasattr(unit.server, 'identity_file'):
                    kwargs.update({
                        'key_filename': unit.server.identity_file
                    })
                    
                if hasattr(unit.server, 'password'):
                    kwargs.update({'password': unit.server.password})
                    
                with settings(hide("warnings", "user", "stdout", "stderr",
                                   "commands", "running"),
                              **kwargs):

                    for log in unit.log_files:
                        yield name, unit.server.hostname, sudo(
                            load_template('grep', {
                                'path': log,
                                'expression': expression,
                            }))
