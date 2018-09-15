import markovify

with open("../corpuses/oakley.txt") as f:
    oakley = f.read()

oakleyModel = markovify.Text(oakley)


for i in range(2):
    print("\n"+oakleyModel.make_sentence()+"\n")
