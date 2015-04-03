from osgrep import env
import os
import unittest


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.dot = os.path.dirname(os.path.abspath(__file__))
        self.fixtures_dir = os.path.join(self.dot, 'fixtures')

    def test_config_sample(self):
        c = env.Config(os.path.join(self.dot, '..', '..',
                                    'config.sample.yaml'))
        (hosts, services) = c.build_env()
        self.assertEqual(list(hosts.keys()), ['example.com'])
