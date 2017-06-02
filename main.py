# Main functions
#Python 2.7
import json
import unirest
from StringIO import StringIO
from flask import Flask
app = Flask(__name__)

@app.route('/')
class makeNewEssay(object):
    """makes a really silly essay"""
    def __init__(self, essay):
        self.essay = essay
        newEssay = ""

    def pickLongestSynonym(self):
        """ goes through each word in the essay to find a longer synonym and appends
        it to the new Essay """
        for x in self.essay:
            response = unirest.get("https://wordsapiv1.p.mashape.com/words/" +str(x) +"/synonyms",
                headers={
                    "X-Mashape-Key": "o4BB4YatyVmshNlvtMFsZNXCDPcmp1u8RNQjsnb2RscDXVMK0f",
                    "Accept": "application/json"
                }
            )
            new_essay = self.essay
            if(len(response["synonyms"]) != None): #& len(response.items()[1]) != 0):
                new_word = response["synonyms"][0]
                if(len(response["synonyms"] > 1):
                    longest = new_word
                    for y in response["synonyms"]:
                        if(len(y) >= longest):
                            longest = y
                    new_essay = new_essay + longest + " "
                else:
                    new_essay = new_essay + new_word + " "
            else:
                new_essay = new_essay + x + " "

        return new_essay

    def testingKey(self):
        word = self.essay
        array = unirest.get("https://wordsapiv1.p.mashape.com/words/" + str(word) + "/synonyms",
            headers={
                "X-Mashape-Key": "o4BB4YatyVmshNlvtMFsZNXCDPcmp1u8RNQjsnb2RscDXVMK0f",
                "Accept": "application/json"
            }
        )
        return array._raw_body


#response = unirest.get("https://wordsapiv1.p.mashape.com/words/{x}/synonyms",
#    headers={
#        "X-Mashape-Key": "o4BB4YatyVmshNlvtMFsZNXCDPcmp1u8RNQjsnb2RscDXVMK0f",
#        "Accept": "application/json"
#    }
#)

test = makeNewEssay("Help")
#print(test.pickLongestSynonym())
print(test.testingKey())
