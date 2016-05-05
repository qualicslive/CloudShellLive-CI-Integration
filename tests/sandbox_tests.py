from unittest import TestCase
import requests
import json
from HTMLParser import HTMLParser
import os

foundSearchString = False
needleNode = "h1"
needleCompare = "Hello World!"
needle = ""

# parse out what's in the source code
class TestDocParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global foundSearchString
        global needleNode
        global needle
    
        if tag.lower().strip() == needleNode:
            foundSearchString = True
        else:
            foundSearchString = False
    def handle_data(self, data):
        global foundSearchString
        global needleNode
        global needle
        
        if foundSearchString:
            foundSearchString = False
            needle = data

class SandboxTests(TestCase):
    def example_test(self):
        global foundSearchString
        global needleNode
        global needle
        
        ########################################
        # pull data from encrypted travis keys:
        ########################################
        serverString = os.environ["SERVERSTRING"]
        blueprintID = os.environ["BLUEPRINTID"]
        authUn = os.environ["AUTHUN"]
        authPw = os.environ["AUTHPW"]
        authDom = os.environ["AUTHDOM"]
        webServerName = os.environ["WEBSERVERNAME"]
        
        sandboxID = ""

        ########################################
        # two part request: get auth token, then reserve
        ########################################

        # authentication
        URI = serverString+"/login"
        auth = {"username":authUn,"password":authPw,"domain":authDom}
        headers = {"Content-Type":"application/json"}
        ar = requests.put(URI, data=json.dumps(auth), headers=headers)
        token = str(ar.content).replace('"','')

        # reserve sandbox
        body = {}
        body["duration"] = "PT30M"  # ISO 8601 for 30 minutes
        body["name"] = "Travis Test " + os.environ["TRAVIS_BUILD_ID"]  # Name of sandbox

        headers = {}
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Basic "+token

        URI = serverString+"/v1/blueprints/"+blueprintID+"/start"

        # sandbox start request
        sbsr = requests.post(URI, data=json.dumps(body), headers=headers)
        print sbsr.text
        
        quickMap = {}
        sbsrobj = json.loads(sbsr.text)

        for component in sbsrobj["components"]:
            quickMap[component["name"]] = component
            
            if (component["name"] == webServerName):
                for attr in component["attributes"]:
                    if (attr["name"] == "HTTP IP"):
                        testURL = attr["value"]

        sandboxID = sbsrobj["id"]

        ########################################
        # begin test
        ########################################
        # convert server name to IP since not in response?
        tr = requests.get(testURL)
        testHTML = tr.text

        parser = TestDocParser()
        parser.feed(testHTML)
            

        ########################################
        # end sandbox
        ########################################
        headers = {}
        headers["Content-Type"] = "application/json"
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Basic "+token

        URI = serverString+"/v1/sandboxes/"+sandboxID+"/stop"

        # sandbox stop request
        sbsr = requests.post(URI, headers=headers)

        ########################################
        # do pass fail
        ########################################
        # compare value we got back
        if (needle.strip() == needleCompare.strip()):
            # identical
            print "PASS! Expected '" + needleCompare.strip() +"' and got '"+needle.strip()+"'"
            pass
        elif (len(needle.strip()) == 0):
            # couldnt find node
            print "FAIL! Expected '" + needleCompare.strip() +"' and could not locate node '"+needleNode+"'"
            exit(1)
        else:
            # not identical
            print "FAIL! Expected '" + needleCompare.strip() +"' and got '"+needle.strip()+"'"
            exit(2)