from unittest import TestCase
import requests
import json
from HTMLParser import HTMLParser
import os

class SandboxTests(TestCase):

    def example_test(self):
        print os.environ["TRAVIS"]
        print os.environ["blueprintID"]
        pass