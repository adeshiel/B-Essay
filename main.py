# Main functions
#Python 2.7

import json
import unirest
#import numpy as np
from StringIO import StringIO
from flask import Flask
app = Flask(__name__)

# TODO: fully implement Flask

name = open('names.txt', 'r')
n = name.read()
names = n.splitlines()

grammar = {
'persons': ["I", "me", "we", "us", "he", "she", "it", "they", "them", "you", "you all"]
,'punctuation': ["!", "?", ".", "!?", "?!", ","]
,'indef_def_articles': ["the", "a", "an"]
,'coord_conjuctions': ["and", "but", "for", "nor", "or", "so", "yet"]
,'and': ["and","also", "besides", "furthermore", "likewise", "moreover"]
,'but': ["but","however", "nevertheless", "nonetheless", "still","conversely","instead","otherwise","rather"]
,'so': ["so","accordingly", "consequently", "hence", "meanwhile", "then","therefore","thus"]
,'time_conjunctions': ["after","as long as", "as soon as", "before", "by the time", "now that", "once", "since", "till", "until", "when", "whenever", "while"]
,'concession_conjunctions': ["though", "although", "even though", "while"]
,'condition_conjunctions': ["if", "only if", "unless", "until", "provided that", "assuming that", "even if", "in case", "in case that", "lest"]
,'comparison_conjunctions': ["than", "rather than", "whether", "as much as", "whereas"]
,'reason_conjunctions': ["because", "since", "so that", "in order to", "in order that", "why"]
,'manner_conjunctions': ["how","as though","as if"]
,'place_conjunctions': ["where","wherever"]
}



@app.route('/')
class makeNewEssay(object):
    """makes a really silly essay"""
    def __init__(self, essay, word_target, rarity):
        self.essay = essay.split()
        self.new_essay = ""
        self.final_essay = ""
        self.word_target = word_target
        self.rarity = rarity
        # TODO: Maybe move the API call so that it doesn't run too many times, or add more checks before the call
        # TODO: Use a book or novel as a comparison, or something that would help it measure how legible it is
                # i.e. check that nouns are next to verbs, or adverbs next to verbs - just basic grammar rules
                # We can do this by looking in the partOfSpeech portion of the chosen definition
        # TODO: Double check that it's comparing the lowercase of words(i.e. "the" == "The")
        self.separatePunct()
    #KEEP IN MIND THAT "?!" AND "!?" ARE MORE THAN THE INDEX OF -1; MAKE ANOTHER CASE FOR THIS

    def separatePunct(self):
        """ Separates the punctuation from the string and places it next in the list,
            can probably be optimized with insert or list comprehension """
        placeholder = []
        for z in self.essay:
            if(z[-1] in grammar['punctuation'] and len(z) >= 2):
                placeholder.append(z[:-1])
                placeholder.append(z[-1])
            else:
                placeholder.append(z)
        self.essay = placeholder


# TODO: Fix so that it doesn't make use of new_essay but just rebuilds essay - maybe
    def pickLongestSynonym(self):
        """ goes through each word in the essay to find a longer synonym and appends
        it to the new essay """
        self.separatePunct()
        for x in self.essay:
            if(x in grammar['persons']):
                continue
            if(x in grammar['punctuation']):
                self.new_essay = self.new_essay[:-1] + x + " "
                self.essay.remove(x)
                continue

            elif(x not in names and x not in grammar['indef_def_articles']):
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
        pun = ""
        for x in range(len(self.essay)):
            if(self.essay[x] not in ignore and self.essay[x][:-1] not in ignore and self.essay[x].title() not in names and x not in grammar['indef_def_articles']):
                if(self.essay[x][-1] in grammar['punctuation']):
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

                if('frequency' in freq.keys() and freq['frequency']['zipf'] <= self.rarity): # ranged 1-7, 1 being very rare and 7 being normal
                    ret2 = unirest.get("https://wordsapiv1.p.mashape.com/words/" +str(self.essay[x]),
                        headers={
                            "X-Mashape-Key": "o4BB4YatyVmshNlvtMFsZNXCDPcmp1u8RNQjsnb2RscDXVMK0f",
                            "Accept": "application/json"
                        }
                    )

                    defin = json.loads(ret2._raw_body)
                    if('definition' in defin['results'][0].keys()):
                        longest = ""
                        if(len(defin['results']) == 1):
                            longest = defin['results'][0]['definition']
                        else:
                            for y in defin['results']:
                                if(len(y['definition']) >= len(longest)):
                                    longest = y['definition']

                        if(pun != ""):
                            temp = longest + pun # Correct
                            pun = ""
                        else:
                            temp = longest +","

                        ignore.append(temp)

                        self.essay[x] += ", or"
                        self.essay.insert(x+1, temp)
                else:
                    self.essay[x] += pun
                        #self.essay.remove(self.essay[x+2])
                        #self.essay[x+2] += pun

    # TODO: implement grammar rules
    def grammarCheck(self):
        self.essay.separatePunct()


        print("")

    def joinEssay(self): #Do i need this?
        for y in self.essay:
            if y in grammar['punctuation']:
                self.final_essay = self.final_essay[:-1] + y + " "
            else:
                self.final_essay += y + " "

    def createEssay(self):
        true_length = 0
        for x in self.essay:
            splt = x.split()
            for y in splt:
                true_length += 1
        while((len(self.essay)-self.essay.count(grammar['punctuation'])) < self.word_target):
            self.pickLongestSynonym()
            test = " ".join(self.essay)
            self.essay = test.split()
            self.extendByDefinition()
            test = " ".join(self.essay)
            self.essay = test.split()

        self.joinEssay()
        return_essay = self.final_essay
        return return_essay

#!!! End of class !!!


#test = makeNewEssay("King Henry won the throne when his force defeated King Richard III at the Battle of Bosworth Field, the culmination of the Wars of Roses.", 50)
test = makeNewEssay("Adam has been a great friend.", 10, 4)
print(test.createEssay())
#print(test.testingKey())
