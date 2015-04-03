from osgrep.templates import load as load_template

from osgrep.tests.mockssh import ExecHandler
from osgrep.runner import Runner


import unittest
import sshim


#TODO: Move this to a fixture
class FakeServer(object):
    hostname = "127.0.0.1"
    username = "ubuntu"
    password = "ubuntu"
    port = "1025"


class FakeService(object):
    name = "fake-service"
    log_files = [
        "/var/log/**.log"
    ]

    
class TestRunner(unittest.TestCase):

    def setUp(self):
        service = FakeService()
        service.server = FakeServer()
        self.services = {
            'fake-service': [service],
        }

        self.template = load_template("grep", {
            'path': FakeService.log_files[0],
            'expression': FakeService.name,
        })
        
    def test_grep(self):
        """Check if basic runner grep functionality works"""
        r = Runner(self.services)
                    
        def grep_response(script):
            script.writeline(self.template)
        
        with sshim.Server(grep_response, port=1025,
                          handler=ExecHandler):
            
            for response in r.grep("foo"):
                self.assertEqual(
                    (FakeService.name, FakeServer.hostname, self.template),
                    response,
                )
