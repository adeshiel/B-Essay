# B-Essay

### Have you ever needed to meet a word count for a paper, but after a certain point you don't know what else to write? Then B-Essay is the app for you!
###### ...kinda

I make no guaruntees that this will get you a B in your class ~~or even a C but for the pun's sake)~~ but this silly little app works to extend your essay/input to meet that given word count by putting in the filler for you!


## Inputs

#### Target Word Count

How many words do you need? Currently has a pitiful limit of 1000 words for the API's ~~and my wallet's~~ sake.

#### Word Frequency

Is set on a range of 1 through 5, with 5 meaning that the word is commonly used. This tells the app which words to target for extension. So setting it to 1 will target the words that quite a few people actually won't know the definition to, making it seem more believable. Meanwhile setting it to 5 will seem like an April Fools joke to the poor soul you ask to decode it.

#### The Essay

Self explanatory. Copy-paste the essay into the textarea shown. Planning to implement an Upload File component eventually.


## Resources Used

- Python 2.7
- [Flask](http://flask.pocoo.org/)
- [Words API](https://www.wordsapi.com/)
- HTML
- CSS
