from goose import Goose
import argparse

def proc_word(word, word_score):
    if word in word_score:
        word_score[word] += 1
    else:
        word_score[word] = 0
    return word_score

parser = argparse.ArgumentParser()
parser.add_argument("nout", help = "Number of sentences in the summary")
parser.add_argument("url", help ="the link to the article you wish to summarize")
args = parser.parse_args()


gob = Goose()
article = gob.extract(url=args.url)
nout = int(args.nout)

word_score = {}

for word in article.title.split():
    word_score[word] = 2
    
for word in article.cleaned_text.split():
   word_score = proc_word(word, word_score)


uselessfile = open("useless_words.txt")
uselessfile_cont = uselessfile.read()

#this for loop will make score of useless words such as a, an, it etc 0
for word in uselessfile_cont.split():
    if word in word_score:
        word_score[word] = 0
        
uselessfile.close()        
        
sentence_list = article.cleaned_text.split(".")
sentence_list = [(sentence.rstrip(" \n\"")).lstrip(" \n\"") for sentence in sentence_list ]
nsent = len(sentence_list)


sent_score = []
for i in range(nsent):
    sc = 0
    for word in sentence_list[i].split():
        if word in word_score:
            sc += word_score[word]
    sent_score.append( (i, sc) )
    
    
    
sorted_by_score = sorted(sent_score, key=lambda tup: tup[1], reverse=True)
relsent = sorted_by_score[:nout]
relsent_chrono = sorted(relsent, key=lambda tup: tup[0])

print "\n%s \n\nSUMMARY: \n" %(article.title)
for tup in relsent_chrono:
    print "%s %s.\n" % (u"\u2022", sentence_list[ tup[0] ] )
