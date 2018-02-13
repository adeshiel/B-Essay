# Main functions
#Python 2.7

#!/usr/bin/env python2

import json
import unirest # only runs python 2.7
from collections import Counter
#import numpy as np
from StringIO import StringIO
from flask import Flask, render_template, jsonify, request
from key import MASH_KEY

app = Flask(__name__)

#if __name__ == '__main__':
#    app.run(
#        debug=True,
#    )

@app.route("/")
def homepage():
    return render_template("index.html")
# TODO: fully implement Flask

@app.route("/essay", methods=['GET', 'POST'])
def get_essay():
    text = request.form['essay']
    wrd_cnt = request.form['word_count']
    rare = request.form['rare']
    retu = makeNewEssay(text, wrd_cnt, rare)
    return render_template("essay.html", essay=retu)


name = open('names.txt', 'r')
n = name.read()
names = n.splitlines()

grammar = {
'persons': ["I", "me", "we", "us", "he", "she", "it", "they", "them", "you", "you all"]
,'punctuation': ["!", "?", ".", "!?", "?!", ",", ":", "(", ")", "&", "'", "\"", ";"]
,'end_punct': ["!", "?", "."]
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

@app.route("/<essay>")
class makeNewEssay(object):
    """makes a really silly essay"""
    def __init__(self, essay, word_target, rarity):
    #def __init__(self):
        self.essay = essay.split()
        self.new_essay = ""
        self.def_holder = ""
        self.final_essay = ""
        self.word_target = int(word_target)
        self.rarity = int(rarity)
        self.return_essay = ""
        # TODO: Maybe move the API call so that it doesn't run too many times, or add more checks before the call
        # TODO: Use a book or novel as a comparison, or something that would help it measure how legible it is
                # i.e. check that nouns are next to verbs, or adverbs next to verbs - just basic grammar rules
                # We can do this by looking in the partOfSpeech portion of the chosen definition
        # TODO: Double check that it's comparing the lowercase of words(i.e. "the" == "The")
        # TODO: ACTIVATE BABY MODE

    def __repr__(self):
#        print("Please input your essay:")
#        self.essay = raw_input().split()
#        print("Your essay is: ", self.essay)

#        print("How long does your essay need to be?")
#        self.word_target = int(input())

#        print("On a scale of 1 to 5, 5 being the most common, how rare should the changed words be?")
#        self.rarity = int(input())
#        assert((self.rarity >= 1) and (self.rarity <= 5)), "Outside of range!"

#        print("Okay! One moment please.")
        #self.essay = self.essay.split()

        return self.createEssay()




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
            #print("x is: ", x)
            if(x in grammar['punctuation'] or x in grammar['persons'] or x in names or x in grammar['indef_def_articles']):
                self.new_essay = self.new_essay[:-1] + x + " "
                continue

            else:
                ret = unirest.get("https://wordsapiv1.p.mashape.com/words/" +str(x) +"/synonyms",
                    headers={
                        "X-Mashape-Key": MASH_KEY,
                        "Accept": "application/json"
                    }
                )

                try:
                    response = json.loads(ret._raw_body)
                except ValueError:
                    continue

                if(('synonyms' in response.keys()) and len(response['synonyms']) != 0):
                    new_word = response['synonyms'][0]
                    if(len(response['synonyms']) > 1):
                        longest = new_word
                        if((max(response['synonyms'], key=len) > longest)):
                            longest = max(list(response['synonyms']), key=len)

                        self.new_essay = self.new_essay + longest + " "

                    else:
                        self.new_essay = self.new_essay + new_word + " "
                else:
                    self.new_essay = self.new_essay + x + " "

        self.essay = self.new_essay.split() #split it so it can be worked on


    def extendByDefinition(self):
        """ extends the word count of the essay by finding a rare-enough word and adding the definition """
        temp, pun = "", ""
        ignore = []

        for x in range(len(self.essay)):
            if(self.essay[x] not in grammar['punctuation'] and self.essay[x] not in ignore and self.essay[x][:-1] not in ignore and self.essay[x].title() not in names and self.essay[x] not in grammar['indef_def_articles']):
                if(x != (len(self.essay)-1) and self.essay[x+1] in grammar['punctuation']):
                    pun = self.essay[x+1]
                    self.essay.remove(self.essay[x+1])
                    #self.essay[x] = self.essay[x][:-1]

                ret1 = unirest.get("https://wordsapiv1.p.mashape.com/words/" +str(self.essay[x]) + "/frequency",
                    headers={
                        "X-Mashape-Key": MASH_KEY,
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
                            "X-Mashape-Key": MASH_KEY,
                            "Accept": "application/json"
                        }
                    )

                    defin = json.loads(ret2._raw_body)
                    if('results' in defin.keys() and 'definition' in defin['results'][0].keys()):
                        longest = ""
                        if(len(defin['results']) == 1):
                            longest = defin['results'][0]['definition']
                        else:
                            #longest = (max(list(defin['results']['definition']), key=len))
                            for y in defin['results']:
                                if(len(y['definition']) >= len(longest)):
                                    longest = y['definition']

                        if(pun != ""):
                            temp = longest # Correct
                            pun = ""
                        else:
                            temp = longest + ","

                        ignore.append(temp)

                        self.essay[x] += ", or"
                        check = temp.split()
                        self.essay[x+1:x+1] = check


                        #self.essay.insert(x+1, temp)
                        #TODO: here we go boys we just need to get this to be inserted as a split list since
                                #it goes in as one long string and counts it as one
                else:
                    self.essay[x] += pun
                    pun = ""
                        #self.essay.remove(self.essay[x+2])
                        #self.essay[x+2] += pun

    # TODO: implement grammar rules
    def grammarCheck(self):
        for w in range(len(self.essay)):
                if self.essay[w] == "a" and w != (len(self.essay) - 1):
                    if self.essay[w+1][0] in ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]:
                        self.essay[w] = "an"
                if self.essay[w] == "an" and w != (len(self.essay) - 1):
                    if self.essay[w+1][0] not in ["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]:
                        self.essay[w] = "a"
                if w == 0 or (w > 0 and self.essay[w - 1] in grammar['end_punct']):
                    self.essay[w] = self.essay[w].title()

    def joinEssay(self): #Do i need this?
        self.final_essay = ""
        for y in self.essay:
            if y[-1] in grammar['punctuation']:
                self.final_essay = self.final_essay[:-1] + y + " "
            else:
                self.final_essay += y + " "

    @app.route("/<essay>/new")
    def createEssay(self):
        # TODO: Fix inconsistency with using final_essay and normal essay
        #self.separatePunct()

        pun_length = len(list((Counter(grammar['punctuation']) & Counter(self.essay)).elements()))
        loopnum = 0
        while ((((len(self.final_essay)) - pun_length) < self.word_target) and (((len(self.essay)) - pun_length) < self.word_target)):
            loopnum +=1
            print("Start loop " + str(loopnum) + ": [final essay length]: " + str(len(self.final_essay)) + " [essay length]: " + str(len(self.essay)))

            pun_length = len(list((Counter(grammar['punctuation']) & Counter(self.essay)).elements()))
            print("(P1) " + str(self.essay))
            self.pickLongestSynonym()
            pun_length = len(list((Counter(grammar['punctuation']) & Counter(self.essay)).elements()))
            print("Current length [1]: ", (len(self.essay) - pun_length), " Word Target: ", self.word_target)
            self.separatePunct()

            self.grammarCheck()
            #self.joinEssay()
            print("(P2) " + str(self.final_essay))

            if(((len(self.final_essay)-pun_length) >= self.word_target) or (len(self.essay)-pun_length) >= self.word_target) :
                break

            self.extendByDefinition()
            pun_length = len(list((Counter(grammar['punctuation']) & Counter(self.essay)).elements()))
            print("Current length [2]: ", (len(self.final_essay) - pun_length))
            self.grammarCheck()
            self.separatePunct()
            #self.joinEssay()
            print("(P3) " + str(self.final_essay))


        self.joinEssay()
        return_essay = self.final_essay
        return return_essay

#!!! End of class !!!


#test = makeNewEssay("Agustin hurt his pee pee! Please, take him to the doctor. Tell me what they say.", 25, 3)
#test = makeNewEssay()
#print(test)
#print(test.testingKey())
