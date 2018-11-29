import re, sys
from os import listdir, walk
from os.path import isfile, join
import matplotlib.pyplot as plt

PATH = "../../data/ud-treebanks-v2.3"

def get_fnames():
    fnames_by_language = {}
    for root, dirs, files in walk(PATH):
        for fname in files:
            if fname.endswith(".conllu"):
                language = root.split("/")[-1].split("-")[0]
#                print(fname,root,language)
                if language not in fnames_by_language:
                    fnames_by_language[language] = []
                fnames_by_language[language].append(join(root,fname))
#                print(join(language, fname))

    return fnames_by_language
        
def get_counts(fnames):
    forms_by_lemma = {}
    forms_by_lemma_nofeats = {}
    numtokens = 0
    numtokens_by_feats = {}
    lemmas_by_feats = {}
    numtokens_by_lemma = {}
    pos_by_feats = {}
    for fname in fnames:
        print("\t", fname)
        with open(fname, "r") as f:
            for line in f:
                if line[0] == "#" or not line.strip():
                    continue
                components = line.lower().split("\t")
                form = components[1]
                lemma = components[2]
                pos = components[3]
                feats = components[4]
                if lemma == "_":
                    continue
                if feats not in pos_by_feats:
                    pos_by_feats[feats] = set([])
                pos_by_feats[feats].add(pos)
                if feats not in numtokens_by_feats:
                    numtokens_by_feats[feats] = 0
                numtokens_by_feats[feats] += 1
                if (lemma,pos) not in numtokens_by_lemma:
                    numtokens_by_lemma[(lemma,pos)] = 0
                numtokens_by_lemma[(lemma,pos)] += 1
                if feats not in lemmas_by_feats:
                    lemmas_by_feats[feats] = set([])
                lemmas_by_feats[feats].add((lemma, pos))
                if (lemma,pos) not in forms_by_lemma:
                    forms_by_lemma[(lemma,pos)] = set([])
                if (lemma,pos) not in forms_by_lemma_nofeats:
                    forms_by_lemma_nofeats[(lemma,pos)] = set([])
                forms_by_lemma_nofeats[(lemma,pos)].add(form)
                forms_by_lemma[(lemma,pos)].add((form,feats))
                numtokens += 1

        
    counts_by_feats = {feats:len(lemmas) for feats, lemmas in lemmas_by_feats.items()}
    counts_by_lemma = {lemma:len(forms) for lemma, forms in forms_by_lemma.items()}
    counts_by_lemma_nofeats = {lemma:len(forms) for lemma, forms in forms_by_lemma_nofeats.items()}
    return numtokens_by_feats, counts_by_feats, numtokens_by_lemma, forms_by_lemma_nofeats, counts_by_lemma_nofeats, forms_by_lemma, counts_by_lemma, pos_by_feats, numtokens


def get_pdgmsize_stats(counts_by_lemma, pos):
    avgsize = 0
    maxsize = 0
    maxone = ""
    relevantcount = 1
    for lemma, size in counts_by_lemma.items():
        if lemma[1] == pos:
            avgsize += size
            if size > maxsize:
                maxsize = size
                maxone = lemma
            relevantcount += 1
    avgsize /= relevantcount
    print(maxone)
    return avgsize, maxsize, relevantcount


def plot_infltypes_by_numtoken(numtokens_by_feats, pos_by_feats, language, pos):
    if len(numtokens_by_feats) < 2:
        return
    maxtokens = max(numtokens_by_feats.values())
    numtokens_by_feats = sorted(numtokens_by_feats.items(), key=lambda kv: kv[1], reverse=True)

    x = []
#    print(numtokens_by_feats)
#    print(pos_by_feats)
    numbins = 0
    for feats, numtokens in numtokens_by_feats:
        if pos in pos_by_feats[feats]:
            x.extend([numbins]*numtokens)
            numbins += 1

    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(x, numbins)
#    plt.ylim(0, maxtokens)
    ax.set_xlabel('Inflectional Category')
    ax.set_ylabel('Token Count')
    ax.set_title(language + ': Token Count by Inflectional Category for ' + pos)
    fig.tight_layout()
    plt.show()
    return

def plot_infltypes_by_numtoken(numtypes_by_feats, pos_by_feats, language, pos):
    if len(numtypes_by_feats) < 2:
        return
    maxtypes = max(numtypes_by_feats.values())
    numtypes_by_feats = sorted(numtypes_by_feats.items(), key=lambda kv: kv[1], reverse=True)

    x = []
#    print(numtypes_by_feats)
#    print(pos_by_feats)
    numbins = 0
    for feats, numtypes in numtypes_by_feats:
        if pos in pos_by_feats[feats]:
            x.extend([numbins]*numtypes)
            numbins += 1

    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(x, numbins)
#    plt.ylim(0, maxtypes)
    ax.set_xlabel('Inflectional Category')
    ax.set_ylabel('Attested Type Count')
    ax.set_title(language + ': Type Count by Inflectional Category for ' + pos)
    fig.tight_layout()
    plt.show()
    return

def plot_lemmas_by_numtokens(ax, numtokens_by_lemma, pos, cutoff=0):
    numtokens_by_lemma = sorted(numtokens_by_lemma.items(), key=lambda kv: kv[1], reverse=True)

    x = []
#    print(numtokens_by_lemma)
#    print(pos_by_feats)
    numbins = 0
    for lemma, numtokens in numtokens_by_lemma:
        if lemma[1] == pos:
            x.extend([numbins]*numtokens)
            numbins += 1
            if cutoff and numbins >= cutoff:
                break

    if numbins < 2:
        return

    n, bins, patches = ax.hist(x, numbins)
    ax.set_xlabel('Lemma')
    ax.set_ylabel('Attested Inflected Form Token Count')
    ax.set_title('Infl Form Token Count by Lemma')
    return


def plot_lemmas_by_numtypes(ax, numtypes_by_lemma, pos, cutoff=0):
    numtypes_by_lemma = sorted(numtypes_by_lemma.items(), key=lambda kv: kv[1], reverse=True)

    x = []
    numbins = 0
    for lemma, numtypes in numtypes_by_lemma:
        if lemma[1] == pos:
            x.extend([numbins]*numtypes)
            numbins += 1
            if cutoff and numbins >= cutoff:
                break

    if numbins < 2:
        return

    n, bins, patches = ax.hist(x, numbins)
    ax.set_xlabel('Lemma')
    ax.set_ylabel('Attested Inflected Form Type Count')
    ax.set_title('Infl Form Type Count by Lemma')
    return


def plot_numtypes_by_lemmas(ax, numtypes_by_lemma, pos):
    lemmas_by_numtypes = {}
    for lemma, numtypes in numtypes_by_lemma.items():
        if lemma[1] == pos:
            if numtypes not in lemmas_by_numtypes:
                lemmas_by_numtypes[numtypes] = set([])
            lemmas_by_numtypes[numtypes].add(lemma)

    lemmas_by_numtypes = sorted(lemmas_by_numtypes.items(), key=lambda kv: len(kv[1]), reverse=True)

    x = []
    numbins = 0
    for numtypes, lemmas in lemmas_by_numtypes:
        x.extend([numbins]*len(lemmas))
        numbins += 1

    if numbins < 2:
        return

    n, bins, patches = ax.hist(x, numbins)
    ax.set_xlabel('Attested Paradigm Size')
    ax.set_ylabel('Number of Lemmas with Attested Form Type Count')
    ax.set_title('Lemma by Infl Form Type Count')
    return


def plot_numtokens_by_lemmas(ax, numtokens_by_lemma,pos):
    lemmas_by_numtokens = {}

    for lemma, numtokens in numtokens_by_lemma.items():
        if lemma[1] == pos:
            if numtokens not in lemmas_by_numtokens:
                lemmas_by_numtokens[numtokens] = set([])
            lemmas_by_numtokens[numtokens].add(lemma)

    lemmas_by_numtokens = sorted(lemmas_by_numtokens.items(), key=lambda kv: len(kv[1]), reverse=True)

    x = []
    numbins = 0
    for numtokens, lemmas in lemmas_by_numtokens:
        x.extend([numbins]*len(lemmas))
        numbins += 1

#    if numbins > 20:
#        numbins /= 10

    if numbins < 2:
        return

    n, bins, patches = ax.hist(x, int(numbins))
    ax.set_xlabel('Attested Paradigm Size')
    ax.set_ylabel('Number of Lemmas with Token Count')
    ax.set_title('# of Lemmas by Token Count')
    return



def make_lemmaplots(numtokens_by_lemma, numtypes_by_lemma, language, pos, cutoff=0):
    fig, axarr = plt.subplots(2, 2, figsize=(12,12))
    fig.suptitle(language + " POS: " + pos)

    plot_lemmas_by_numtokens(axarr[0,0], numtokens_by_lemma, pos, cutoff=cutoff)
    plot_lemmas_by_numtypes(axarr[0,1], numtypes_by_lemma, pos, cutoff=cutoff)
    plot_numtokens_by_lemmas(axarr[1,0], numtokens_by_lemma, pos)
    plot_numtypes_by_lemmas(axarr[1,1], numtypes_by_lemma, pos)
    
    plt.savefig("plots/" + language + "_" + pos + ".png")
#    fig.tight_layout()
#    plt.show()


fnames_by_dirname = get_fnames()
for language, fnames in fnames_by_dirname.items():
    numtokens_by_feats, counts_by_feats, numtokens_by_lemma, forms_by_lemma_nofeats, counts_by_lemma_nofeats, forms_by_lemma, counts_by_lemma, pos_by_feats, numtokens = get_counts(fnames)
    print(language)
    print(numtokens, len(counts_by_lemma))
    avgnoun, maxnoun, numnoun = get_pdgmsize_stats(counts_by_lemma_nofeats, "noun")
    avgverb, maxverb, numverb = get_pdgmsize_stats(counts_by_lemma_nofeats, "verb")
    print("N: ", avgnoun, maxnoun, numnoun)
    print("V: ", avgverb, maxverb, numverb)
    avgnoun, maxnoun, numnoun = get_pdgmsize_stats(counts_by_lemma, "noun")
    avgverb, maxverb, numverb = get_pdgmsize_stats(counts_by_lemma, "verb")
    print("N: ", avgnoun, maxnoun, numnoun)
    print("V: ", avgverb, maxverb, numverb)

#    plot_infltypes_by_numtoken(numtokens_by_feats, pos_by_feats, language, "noun")
#    plot_infltypes_by_numtoken(numtokens_by_feats, pos_by_feats, language, "verb")
#    plot_infltypes_by_numtoken(counts_by_feats, pos_by_feats, language, "noun")
#    plot_infltypes_by_numtoken(counts_by_feats, pos_by_feats, language, "verb")

    make_lemmaplots(numtokens_by_lemma, counts_by_lemma, language, "noun", cutoff=1000)
    make_lemmaplots(numtokens_by_lemma, counts_by_lemma, language, "verb", cutoff=1000)
    make_lemmaplots(numtokens_by_lemma, counts_by_lemma_nofeats, language+"_surfaceforms", "noun", cutoff=1000)
    make_lemmaplots(numtokens_by_lemma, counts_by_lemma_nofeats, language+"_surfaceforms", "verb", cutoff=1000)

#    plot_lemmas_by_numtokens(numtokens_by_lemma, language, "noun", cutoff=1000)
#    plot_lemmas_by_numtokens(numtokens_by_lemma, language, "verb", cutoff=1000)
#    plot_lemmas_by_numtypes(counts_by_lemma_nofeats, language+"_nofeats", "noun", cutoff=1000)
#    plot_lemmas_by_numtypes(counts_by_lemma_nofeats, language+"_nofeats", "verb", cutoff=1000)
#    plot_lemmas_by_numtypes(counts_by_lemma, language, "noun", cutoff=1000)
#    plot_lemmas_by_numtypes(counts_by_lemma, language, "verb", cutoff=1000)

#    plot_numtypes_by_lemmas(counts_by_lemma_nofeats, language+"_nofeats", "noun")
#    plot_numtypes_by_lemmas(counts_by_lemma_nofeats, language+"_nofeats", "verb")
#    plot_numtypes_by_lemmas(counts_by_lemma, language, "noun")
#    plot_numtypes_by_lemmas(counts_by_lemma, language, "verb")
