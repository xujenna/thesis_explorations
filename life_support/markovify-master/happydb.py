import markovify
import nltk
import re

class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

# Get raw text as string.
with open("../corpuses/hm_only.txt") as f:
    happyDB = f.read()
# with open("../corpuses/horoscope.txt") as f:
#     horoscope = f.read()
# with open("../corpuses/oprah.txt") as f:
#     oprah = f.read()
# with open("../corpuses/sugar.txt") as f:
#     sugar = f.read()

# Build the model.
# ggiaModel = markovify.Text(ggia)
# horoscopeModel = markovify.Text(horoscope)
# oprahModel = markovify.Text(oprah)
# sugarModel = markovify.Text(sugar)

happyNLTK = POSifiedText(happyDB)
# horoscopeNLTK = POSifiedText(horoscope)
# oprahNLTK = POSifiedText(oprah)
# happyModel = markovify.Text(happyNLTK)
happyModel = markovify.combine([happyNLTK], [1])

# for i in range(2):
#     print("\n"+comboModel.make_sentence()+"\n")

# Print three randomly-generated sentences of no more than 140 characters
for i in range(20):
    print("\n"+happyModel.make_short_sentence(140)+"\n")
