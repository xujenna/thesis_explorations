import markovify

# Get raw text as string.
with open("../corpuses/ggia.txt") as f:
    ggia = f.read()
with open("../corpuses/horoscope.txt") as f:
    horoscope = f.read()
with open("../corpuses/oprah.txt") as f:
    oprah = f.read()
with open("../corpuses/sugar.txt") as f:
    sugar = f.read()

# Build the model.
ggiaModel = markovify.Text(ggia)
horoscopeModel = markovify.Text(horoscope)
oprahModel = markovify.Text(oprah)
sugarModel = markovify.Text(sugar)
comboModel = markovify.combine([ggiaModel, horoscopeModel, oprahModel], [2, 1, 1])
#
# for i in range(2):
#     print("\n"+comboModel.make_sentence()+"\n")

# Print three randomly-generated sentences of no more than 140 characters
for i in range(1):
    print("\n"+comboModel.make_short_sentence(140)+"\n")
