# Main functions
#Python 2.7
import json
import unirest
from StringIO import StringIO
from flask import Flask
app = Flask(__name__)

f = open('female.txt', 'r')
f1 = f.read()
flist = f1.splitlines()
m = open('male.txt', 'r')
m1 = m.read()
mlist = m1.splitlines()
names = flist + mlist

print(names)

@app.route('/')
class makeNewEssay(object):
    """makes a really silly essay"""
    def __init__(self, essay, word_target):
        self.essay = essay.split()
        new_essay = ""
        self.new_essay = new_essay
        self.word_target = word_target

    def pickLongestSynonym(self):
        """ goes through each word in the essay to find a longer synonym and appends
        it to the new Essay """
        for x in self.essay:
            ret = unirest.get("https://wordsapiv1.p.mashape.com/words/" +str(x) +"/synonyms",
                headers={
                    "X-Mashape-Key": "o4BB4YatyVmshNlvtMFsZNXCDPcmp1u8RNQjsnb2RscDXVMK0f",
                    "Accept": "application/json"
                }
            )
            response = json.loads(ret._raw_body)
            #synonym = json.loads(response)
            #return
            if(x not in names):
                if(len(response['synonyms']) != 0): #& len(response.items()[1]) != 0):
                    new_word = response['synonyms'][0]
                    if(len(response['synonyms']) > 1):
                        longest = new_word
                        for y in response['synonyms']:
                            if(len(y) >= longest):
                                longest = y
                        self.new_essay = self.new_essay + longest + " "
                    else:
                        self.new_essay = self.new_essay + new_word + " "
                else:
                    self.new_essay = self.new_essay + x + " "
            else:
                self.new_essay = self.new_essay + x + " "

        print(self.new_essay)


#test = makeNewEssay("Please excuse my dear Aunt Sally", 6)
#print(test.pickLongestSynonym())
#print(test.testingKey())
