import markovify

# Get raw text as string.
with open("../corpuses/ggia.txt") as f:
    ggia = f.read()
with open("../corpuses/horoscope.txt") as f:
    horoscope = f.read()
with open("../corpuses/oprah.txt") as f:
    oprah = f.read()


# Build the model.
ggiaModel = markovify.Text(ggia)
horoscopeModel = markovify.Text(horoscope)
oprahModel = markovify.Text(oprah)
comboModel = markovify.combine([ggiaModel, horoscopeModel, oprahModel], [1.5, 1, 1])
#
# for i in range(2):
#     print("\n"+text_model.make_sentence()+"\n")

# Print three randomly-generated sentences of no more than 140 characters
for i in range(2):
    print("\n"+comboModel.make_short_sentence(140)+"\n")
