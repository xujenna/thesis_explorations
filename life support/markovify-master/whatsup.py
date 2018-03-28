import markovify
import nltk
import random
import re


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence


with open("../corpuses/ggia.txt") as f:
    ggia = f.read()
with open("../corpuses/horoscope.txt") as f:
    horoscope = f.read()
with open("../corpuses/oprah.txt") as f:
    oprah = f.read()

ggiaNLTK = POSifiedText(ggia)
horoscopeNLTK = POSifiedText(horoscope)
oprahNLTK = POSifiedText(oprah)

comb_model = markovify.combine([ggiaNLTK, horoscopeNLTK, oprahNLTK], [2, 1.5, 1])



# with open("../corpuses/eatinghealthy.txt") as f:
#     eating = f.read()
with open("../corpuses/food.txt") as f:
    food = f.read()

foodModel = markovify.NewlineText(food)
# eatingModel = markovify.NewLineText(eating)

# sentence = comb_model.make_sentence()

def respond(user_input):
    if "hungry" in user_input:
        foodsentence = foodModel.make_short_sentence(150)
        print("\n" + foodsentence + "\n")
        user_input = ""
    elif "feel" in user_input:
        feelsentence = comb_model.make_short_sentence(150)
        print("\n" + feelsentence + "\n")
        user_input = ""



while True:
    user_input = input("What's up? \n \n")
    if user_input == "x":
        break
    # inp_tokens = nltk.word_tokenize(user_input)
    # inp_tags = nltk.pos_tag(inp_tokens)
    # inp_pos = {}
    # for tag in inp_tags:
    #     if tag[1].startswith('V'):
    #         if not tag[1] in inp_pos:
    #             inp_pos[tag[1]] = []
    #         inp_pos[tag[1]] += [tag[0]]
    respond(user_input)




    # print (sentence)
    # print (inp_pos)

    # tokens = nltk.word_tokenize(sentence)
    # tags = nltk.pos_tag(tokens)
    #
    # new_sentence = ""
    #
    # for tag in tags:
    #     # looks at tags of generated sentence
    #     if tag[1].startswith('V'):
    #         print(inp_pos)
    #         if tag[1] in inp_pos:
    #             # there is a 1/(n+1) chance that an item in inp_pos[tag[1]] will replace the item in the sentence.
    #             # where n = len(inp_pos[tag[1]])
    #             # that leads to a 1 / (n+1) chance that it wont get replaced
    #
    #             rand = random.random()
    #             part = 1.0 / (len(inp_pos[tag[1]]) + 1)
    #             segment = int(rand / part)
    #             if segment < len(inp_pos[tag[1]]):
    #                 new_sentence += " " + inp_pos[tag[1]][segment]
    #                 print ("Replacing %s with %s, rand was %f" % (tag[0], inp_pos[tag[1]][segment], rand))
    #                 continue
    #             # print ("Not replacing %s with %s, rand was %f" % (tag[0], inp_pos[tag[1]], rand))
    #
    #     new_sentence += " " + tag[0]
    #
    # print ("\n" + new_sentence + "\n")
