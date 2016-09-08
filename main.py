from goose import Goose
import argparse


def proc_word(word, word_count):
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 0
    return word_count

parser = argparse.ArgumentParser()
parser.add_argument("nout", help = "Number of sentences in the summary")
parser.add_argument("url", help ="the link to the article you wish to summarize")
args = parser.parse_args()


gob = Goose()
article = gob.extract(url=args.url)
nout = int(args.nout)

word_count = {}

for word in article.cleaned_text.split():
   word_count = proc_word(word, word_count)
     
sentence_list = article.cleaned_text.split(".")
sentence_list = [(sentence.rstrip(" \n\"")).lstrip(" \n\"") for sentence in sentence_list ]
nsent = len(sentence_list)


sent_score = []
for i in range(nsent):
    sc = 0
    for word in sentence_list[i].split():
        if word in word_count:
            sc += word_count[word]
    sent_score.append( (i, sc) )
    
    
    
sorted_by_score = sorted(sent_score, key=lambda tup: tup[1], reverse=True)
relsent = sorted_by_score[:nout]
relsent_chrono = sorted(relsent, key=lambda tup: tup[0])

print "\n%s \n\nSUMMARY: \n" %(article.title)
for tup in relsent_chrono:
    print "%s %s.\n" % (u"\u2022", sentence_list[ tup[0] ] )
