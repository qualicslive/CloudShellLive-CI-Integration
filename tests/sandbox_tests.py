from unittest import TestCase
import requests
import json
from HTMLParser import HTMLParser
import os

class SandboxTests(TestCase):

    def example_test(self):
        serverString = os.environ["SERVERSTRING"]
        blueprintID = os.environ["BLUEPRINTID"]
        authUn = os.environ["AUTHUN"]
        authPw = os.environ["AUTHPW"]
        authDom = os.environ["AUTHDOM"]
        webServerName = os.environ["WEBSERVERNAME"]
        
        pass