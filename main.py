# Main functions
#Python 2.7
import json
import unirest
from StringIO import StringIO
from flask import Flask
app = Flask(__name__)


name = open('names.txt', 'r')
n = name.read()
names = n.splitlines()
punctuation = ["!", "?", ".", "!?", "?!", ","]

@app.route('/')
class makeNewEssay(object):
    """makes a really silly essay"""
    def __init__(self, essay, word_target):
        self.essay = essay.split()
        self.new_essay = ""
        self.final_essay = ""
        self.word_target = word_target
        # TODO: fully implement word target
        # TODO: Maybe move the API call so that it doesn't run too many times, dunno if it'll make much difference though

        placeholder = []
        for z in self.essay:
            if(z[-1] in punctuation):
                placeholder.append(z[:-1])
                placeholder.append(z[-1])
            else:
                placeholder.append(z)
        self.essay = placeholder
    #KEEP IN MIND THAT "?!" AND "!?" ARE MORE THAN THE INDEX OF -1; NEED TO MAKE ANOTHER CASE FOR THIS

    def separatePunct(self):
        """ Separates the punctuation from the string and places it next in the list,
            can probably be optimized with insert or list comprehension """
        placeholder = []
        for z in self.essay:
            if(z[-1] in punctuation):
                placeholder.append(z[:-1])
                placeholder.append(z[-1])
            else:
                placeholder.append(z)
        self.essay = placeholder

    def pickLongestSynonym(self):
        """ goes through each word in the essay to find a longer synonym and appends
        it to the new Essay """
        self.essay.separatePunct()
        for x in self.essay:

            if(x in punctuation):
                self.new_essay = self.new_essay[:-1] + x + " "
                self.essay.remove(x)
                continue

            elif(x not in names):
                ret = unirest.get("https://wordsapiv1.p.mashape.com/words/" +str(x) +"/synonyms",
                    headers={
                        "X-Mashape-Key": "o4BB4YatyVmshNlvtMFsZNXCDPcmp1u8RNQjsnb2RscDXVMK0f",
                        "Accept": "application/json"
                    }
                )
                try:
                    response = json.loads(ret._raw_body)
                except ValueError:
                    continue

                if(len(response['synonyms']) != 0):
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

        self.essay = self.new_essay.split()

    def extendByDefinition(self):
        """ extends the word count of the essay by finding a rare-enough word and adding the definition """
        temp = ""
        ignore = []

        for x in range(len(self.essay)):

            if(self.essay[x] in punctuation):
                self.essay[x-1] += self.essay[x]
                self.essay[x] = ''
                continue

            pun = ""

            if(self.essay[x][:-1] not in ignore or self.essay[x] not in names):
                if(self.essay[x][-1] in punctuation):
                    pun = self.essay[x][-1]
                    self.essay[x] = self.essay[x][:-1]

                ret1 = unirest.get("https://wordsapiv1.p.mashape.com/words/" +str(self.essay[x]) + "/frequency",
                    headers={
                        "X-Mashape-Key": "o4BB4YatyVmshNlvtMFsZNXCDPcmp1u8RNQjsnb2RscDXVMK0f",
                        "Accept": "application/json"
                    }
                )

                try:
                    freq = json.loads(ret1._raw_body)
                except ValueError:
                    continue

                if('frequency' in freq.keys() and freq['frequency']['zipf'] <= 2.5):
                    ret2 = unirest.get("https://wordsapiv1.p.mashape.com/words/" +str(self.essay[x]),
                        headers={
                            "X-Mashape-Key": "o4BB4YatyVmshNlvtMFsZNXCDPcmp1u8RNQjsnb2RscDXVMK0f",
                            "Accept": "application/json"
                        }
                    )

                    defin = json.loads(ret2._raw_body)

                    if('definition' in defin.keys()):
                        longest = ""
                        for y in defin['results']:
                            if(len(y['definition']) >= len(longest)):
                                longest = y['definition']

                        if(self.essay[x+1] in punctuation):
                            temp = longest + self.essay[x+1]
                        else:
                            temp = longest +", "

                        ignore.append(longest)

                        self.essay[x] += ", or"
                        self.essay.insert(x+1, temp)
                        self.essay.remove(self.essay[x+2])


        #print(self.essay)

    def joinEssay(self):
        for y in self.essay:
            if y in punctuation:
                self.final_essay = self.final_essay[:-1] + y + " "
            else:
                self.final_essay += y + " "

    def createEssay(self):
        while((len(self.essay)-self.essay.count(punctuation)) < self.word_target):
            self.pickLongestSynonym()
            print(self.essay)
            self.extendByDefinition()
            #print(self.essay)
        #return_essay = ' '.join(self.essay)
        self.joinEssay()
        return_essay = self.final_essay
        return return_essay



#test = makeNewEssay("King Henry won the throne when his force defeated King Richard III at the Battle of Bosworth Field, the culmination of the Wars of Roses.", 50)
test = makeNewEssay("Abby is superbly kind.", 6)
print(test.createEssay())
#print(test.testingKey())
