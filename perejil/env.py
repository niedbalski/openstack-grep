from collections import defaultdict

import logging
import os
import pprint
import yaml
from perejil import exc


class Server(object):
    def __init__(self, hostname):
        self.hostname = hostname
        self.username = None
        self.identity_file = None
        self.services = []
        self.log = logging.getLogger(self.__class__.__name__)


class Service(object):
    name = None

    def __init__(self, server=None, cfg=None):
        self.server = server
        self.cfg = cfg


class NovaCompute(Service):
    name = 'nova-compute'

    @property
    def log_files(self):
        return ["/var/log/nova/*.log*"]

    def __repr__(self):
        return "<NovaCompute %s>" % self.server.hostname


class NovaApi(Service):
    name = 'nova-api'


class NeutronApi(Service):
    name = 'neutron-api'


class NeutronServer(Service):
    name = 'neutron-server'


klasses = {
    'nova-compute': NovaCompute,
    'nova-api': NovaApi,
}

class Config(object):
    def __init__(self, fpath):
        self.fpath = fpath
        self._cfg = None
        self.log = logging.getLogger(self.__class__.__name__)

    @property
    def cfg(self):
        if self._cfg:
            return self._cfg

        if not os.path.isfile(self.fpath):
            raise exc.PerejilError("'%s' no such file or directory" % self.fpath)

        with open(self.fpath, 'rb') as f:
            self._cfg = yaml.safe_load(f.read())

        return self._cfg

    def build_env(self):
        hosts = {}
        services = defaultdict(list)
        for service_name, nodes in self.cfg['services'].items():
            for node in nodes:
                hostname = node.get('host', self.cfg['default-host'])
                if hostname in hosts:
                    server = hosts[hostname]
                else:
                    server = Server(hostname)
                    server.port = node.get('port', self.cfg['default-port'])
                    server.username = node.get('username',
                                               self.cfg['default-username'])
                    server.identity_file = node.get('identity-file',
                                                    self.cfg['default-identity-file'])
                    hosts[hostname] = server

                klass = klasses[service_name]
                service = klass(server=server, cfg=node)
                services[service_name].append(service)

        self.log.debug('Hosts defined: %s' % pprint.pformat(hosts))
        self.log.debug("Services defined: %s" % pprint.pformat(services))

        return (hosts, services)
