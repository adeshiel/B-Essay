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
            array = unirest.get("https://wordsapiv1.p.mashape.com/words/{x}/synonyms",
                headers={
                    "X-Mashape-Key": "o4BB4YatyVmshNlvtMFsZNXCDPcmp1u8RNQjsnb2RscDXVMK0f",
                    "Accept": "application/json"
                }
            )
            response = json.loads(array)
            print(response)
            if(len(response.items()) != 0 & len(response.items()[1]) != 0):
                newmeanings = response.items()[1][1:]
                if(len(newmeanings) > 1):
                    longest = newmeanings[0]
                    for y in newmeanings:
                        if(len(newmeanings[y]) >= longest):
                            longest = newmeanings[y]
                    newEssay = newEssay + longest + " "
                else:
                    newEssay = newEssay + newmeanings[1] + " "
            else:
                newEssay = newEssay + x + " "

        return newEssay

    def testingKey(self):
        word = self.essay
        array = unirest.get("https://wordsapiv1.p.mashape.com/words/{word}/synonyms",
            headers={
                "X-Mashape-Key": "o4BB4YatyVmshNlvtMFsZNXCDPcmp1u8RNQjsnb2RscDXVMK0f",
                "Accept": "application/json"
            }
        )
        return array.body()


#response = unirest.get("https://wordsapiv1.p.mashape.com/words/{x}/synonyms",
#    headers={
#        "X-Mashape-Key": "o4BB4YatyVmshNlvtMFsZNXCDPcmp1u8RNQjsnb2RscDXVMK0f",
#        "Accept": "application/json"
#    }
#)

test = makeNewEssay("Help")
#print(test.pickLongestSynonym())
print(test.testingKey())
