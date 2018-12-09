import re, sys
from os import listdir, walk
from os.path import isfile, join
import matplotlib.pyplot as plt
from feats_maps import *
from construct_featmap import *

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
    feats_by_pos = {}
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
                feats = components[5]
                if lemma == "_":
                    continue

                if pos not in feats_by_pos:
                    feats_by_pos[pos] = {}
                if feats not in feats_by_pos[pos]:
                    feats_by_pos[pos][feats] = set([])
                if len(feats_by_pos[pos][feats]) < 20:
                    feats_by_pos[pos][feats].add(form)

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

        
#    print("Noun:", len(feats_by_pos["noun"]),feats_by_pos["noun"])
#    print("Verb:", len(feats_by_pos["verb"]),feats_by_pos["verb"])
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
    return avgsize, maxsize, relevantcount, maxone


def plot_infltypes_by_counts(ax, num_by_feats, pos_by_feats, language, pos, subtitle):
    if len(num_by_feats) < 2:
        return
    maxtokens = max(num_by_feats.values())

    x = []
#    print(count_by_feats)
#    print(pos_by_feats)
    numbins = 0
    num_by_feats = sorted(num_by_feats.items(), key=lambda kv: kv[1], reverse=True)
    for feats, count in num_by_feats:        
#        print(feats, count)
        if pos in pos_by_feats[feats]:
            x.extend([numbins]*count)
            numbins += 1

    n, bins, patches = ax.hist(x, numbins)
#    plt.ylim(0, maxtokens)
    ax.set_xlabel('Inflectional Category')
    ax.set_ylabel(subtitle + " Count")
    ax.set_title(language + ": " + subtitle + ' by Infl. Category: ' + pos)
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
            if numtypes > 0:
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

#    print(lemmas_by_numtypes.keys())
#    exit()
    lemmas_by_numtypes = sorted(lemmas_by_numtypes.items(), key=lambda kv: len(kv[1]), reverse=True)
    
    x = []
    numbins = 0
    for numtypes, lemmas in lemmas_by_numtypes:
        x.extend([numbins]*len(lemmas))
        numbins += 1


    import statistics
    print(x)
    print(statistics.mean(x))
    print(statistics.median(x))
    exit()

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


def plot_lemmatokentype_by_rank(ax, numtoks_by_lemma, numtypes_by_lemma, language, pos, title):

    def rank(num_by_lemma_sorted):
        num_by_lemma_ranked = {}
        numrank = 0
        prevnum = 0
        for lemma, num in num_by_lemma_sorted:
            if len(lemma) < 2 or lemma[1] != pos:
                continue
            if num < prevnum:
                numrank += 1
            prevnum = num
            num_by_lemma_ranked[lemma] = numrank
        return num_by_lemma_ranked

    numtoks_by_lemma_sorted = sorted(numtoks_by_lemma.items(), key=lambda kv: kv[1], reverse=True)
    numtypes_by_lemma_sorted = sorted(numtypes_by_lemma.items(), key=lambda kv: kv[1], reverse=True)

    numtypes_by_lemma_ranked = rank(numtypes_by_lemma_sorted)
    numtoks_by_lemma_ranked = rank(numtoks_by_lemma_sorted)

    xpts = []
    ypts = []
 
#    print(len(numtypes_by_lemma_ranked))
#    print(len(numtoks_by_lemma_ranked))
#    print(numtypes_by_lemma_ranked)
#    print(numtoks_by_lemma_ranked)
#    exit()
    for lemma, numtypes in numtypes_by_lemma_ranked.items():
        xpts.append(numtypes)
        if lemma not in numtoks_by_lemma_ranked:
            print(lemma)
        ypts.append(numtoks_by_lemma_ranked[lemma])

    ax.plot(xpts, ypts, "o")
        
    ax.set_xlabel('Type Rank')
    ax.set_ylabel('Token Rank')
    ax.set_title('Type vs Token Rank for ' + pos + " " + title)
    return


def plot_infltokentype_by_rank(ax, numtoks_by_feats, numtypes_by_feats, POS_by_feats, language, pos, title):

    def rank(num_by_feats_sorted):
        num_by_feats_ranked = {}
        numrank = 0
        prevnum = 0
        for feats, num in num_by_feats_sorted:
            if len(feats) < 2 or pos not in POS_by_feats[feats]:
                continue
            if num < prevnum:
                numrank += 1
            prevnum = num
            num_by_feats_ranked[feats] = numrank
        return num_by_feats_ranked

    numtoks_by_feats_sorted = sorted(numtoks_by_feats.items(), key=lambda kv: kv[1], reverse=True)
    numtypes_by_feats_sorted = sorted(numtypes_by_feats.items(), key=lambda kv: kv[1], reverse=True)

#    for feats, numtypes in numtypes_by_feats_sorted:
#        print(numtypes, "\t", feats)
#    exit()

    numtypes_by_feats_ranked = rank(numtypes_by_feats_sorted)
    numtoks_by_feats_ranked = rank(numtoks_by_feats_sorted)

    xpts = []
    ypts = []
 
    for feats, numtypes in numtypes_by_feats_ranked.items():
        xpts.append(numtypes)
        if feats not in numtoks_by_feats_ranked:
            print(feats)
        ypts.append(numtoks_by_feats_ranked[feats])

    ax.plot(xpts, ypts, "o")
        
    ax.set_xlabel('Type Rank')
    ax.set_ylabel('Token Rank')
    ax.set_title('Type vs Token Rank for ' + pos + " " + title)
    return



def make_inflplots(numtokens_by_feats, numtypes_by_feats, pos_by_feats, language, poss):
    fig, axarr = plt.subplots(2, 2, figsize=(12,12))
    fig.suptitle(language + " Inflectional Category Frequencies")
    for i, pos in enumerate(poss):
        plot_infltypes_by_counts(axarr[0,i], numtokens_by_feats, pos_by_feats, language, pos, "Tokens")
        plot_infltypes_by_counts(axarr[1,i], numtypes_by_feats, pos_by_feats, language, pos, "Types")

    plt.savefig("plots/" + language + "_infl" + ".png")
    plt.close(fig)


def make_lemmaplots(numtokens_by_lemma, numtypes_by_lemma, language, pos, cutoff=0):
    fig, axarr = plt.subplots(2, 2, figsize=(12,12))
    fig.suptitle(language + " POS: " + pos)

    plot_lemmas_by_numtokens(axarr[0,0], numtokens_by_lemma, pos, cutoff=cutoff)
    plot_lemmas_by_numtypes(axarr[0,1], numtypes_by_lemma, pos, cutoff=cutoff)
    plot_numtokens_by_lemmas(axarr[1,0], numtokens_by_lemma, pos)
    plot_numtypes_by_lemmas(axarr[1,1], numtypes_by_lemma, pos)
    
    plt.savefig("plots/" + language + "_" + pos + ".png")
    plt.close(fig)
#    fig.tight_layout()
#    plt.show()


def make_tokentypeplots(numtoks_by_feats, numtypes_by_feats, numtoks_by_lemma, numtypes_by_lemma, POS_by_feats, language, poss):
    fig, axarr = plt.subplots(2, 2, figsize=(12,12))
    fig.suptitle(language + " Token vs Type Ranks")
    for i, pos in enumerate(poss):
        plot_lemmatokentype_by_rank(axarr[0,i], numtoks_by_lemma, numtypes_by_lemma, language, pos, "Lemma")
        plot_infltokentype_by_rank(axarr[1,i], numtoks_by_feats, numtypes_by_feats, POS_by_feats, language, pos, "Infl Category")

    plt.savefig("plots/" + language + "_typetoken" + ".png")
    plt.close(fig)


def get_mapdict(language):
    mapdict = {}
    if language == "UD_Arabicxxxx":
        mapdict = construct_UD_Arabic(pos_by_feats)
    elif language == "UD_Czech":
        mapdict = construct_UD_Czech(pos_by_feats)
    elif language == "UD_English":
        mapdict = construct_UD_English(pos_by_feats)
    elif language == "UD_Finnish":
        mapdict = construct_UD_Finnish(pos_by_feats)
    elif language == "UD_German":
        mapdict = construct_UD_German(pos_by_feats)
    elif language == "UD_Latin":
        mapdict = construct_UD_Latin(pos_by_feats)
    elif language == "UD_Spanish":
        mapdict = construct_UD_Spanish(pos_by_feats)
    elif language == "UD_Turkish":
        mapdict = construct_UD_Turkish(pos_by_feats)
    else:
        print("Cannot map " + language)
    return mapdict

def map_feats_by_lemma(forms_by_lemma, language):
    mapdict = get_mapdict(language)
    forms_by_lemma_mapped = {}
    featset = set([])
    for lemmapos, formfeatss in forms_by_lemma.items():
        if lemmapos not in forms_by_lemma_mapped:
            forms_by_lemma_mapped[lemmapos] = set([])
        for formfeats in formfeatss:
            form = formfeats[0]
            feats = formfeats[1]
            if feats not in mapdict:
                continue
            mappedfeats = mapdict[feats]
            if mappedfeats == DELETE:
                continue
            featset.add(mappedfeats)
            forms_by_lemma_mapped[lemmapos].add((mappedfeats))

    counts_by_lemma_mapped = {lemma:len(forms) for lemma, forms in forms_by_lemma_mapped.items()}
    return counts_by_lemma_mapped, forms_by_lemma_mapped
    

def map_numfeats(counts_by_feats, language):
    mapdict = get_mapdict(language)
    counts_by_feats_mapped = {}
    for feats, count in counts_by_feats.items():
        if feats not in mapdict:
            continue
        mappedfeats = mapdict[feats]
        if mappedfeats == DELETE:
            continue
        if mappedfeats not in counts_by_feats_mapped:
            counts_by_feats_mapped[mappedfeats] = 0
        counts_by_feats_mapped[mappedfeats] += counts_by_feats[feats]
    return counts_by_feats_mapped


def map_posfeats(counts_by_feats, language):
    mapdict = get_mapdict(language)
    pos_by_feats_mapped = {}
    for feats, pos in counts_by_feats.items():
        if feats not in mapdict:
            continue
        mappedfeats = mapdict[feats]
        if mappedfeats == DELETE:
            continue
        pos_by_feats_mapped[mappedfeats] = pos_by_feats[feats]
    return pos_by_feats_mapped


fnames_by_dirname = get_fnames()
for language, fnames in fnames_by_dirname.items():
    if "UD_Spanish" not in language:
        continue
#    if "UD_Spanish" not in language and "UD_Turkish" not in language and "UD_Czech" not in language and "UD_English" not in language and "UD_Finnish" not in language:
        continue
    print("\n\n")
    numtokens_by_feats, counts_by_feats, numtokens_by_lemma, forms_by_lemma_nofeats, counts_by_lemma_nofeats, forms_by_lemma, counts_by_lemma, pos_by_feats, numtokens = get_counts(fnames)
    counts_by_lemma_mapped, forms_by_lemma_mapped = map_feats_by_lemma(forms_by_lemma, language)
    counts_by_feats_mapped = map_numfeats(counts_by_feats, language)
    numtokens_by_feats_mapped = map_numfeats(numtokens_by_feats, language)
    pos_by_feats_mapped = map_posfeats(pos_by_feats, language)




    print(language)
    print(numtokens, len(counts_by_lemma))

    #bybee
#    for verb in bybee1985strong:
#        if (verb, "verb") in counts_by_lemma_mapped:
#            print(verb, counts_by_lemma_mapped[(verb, "verb")], forms_by_lemma_mapped[(verb,"verb")])
#        else:
#            print(verb, 0)


    avgnoun, maxnoun, numnoun, maxnounval = get_pdgmsize_stats(counts_by_lemma_mapped, "noun")
    avgverb, maxverb, numverb, maxverbval = get_pdgmsize_stats(counts_by_lemma_mapped, "verb")
    print("N: ", avgnoun, maxnoun, numnoun)
    print("V: ", avgverb, maxverb, numverb)
    avgnoun, maxnoun, numnoun, maxnounval = get_pdgmsize_stats(counts_by_lemma_nofeats, "noun")
    avgverb, maxverb, numverb, maxverbval = get_pdgmsize_stats(counts_by_lemma_nofeats, "verb")
    print("N: ", avgnoun, maxnoun, numnoun)
    print("V: ", avgverb, maxverb, numverb)
    avgnoun, maxnoun, numnoun, maxnounval = get_pdgmsize_stats(counts_by_lemma, "noun")
    avgverb, maxverb, numverb, maxverbval = get_pdgmsize_stats(counts_by_lemma, "verb")
    print("N: ", avgnoun, maxnoun, numnoun)
    print("V: ", avgverb, maxverb, numverb)

#    make_tokentypeplots(numtokens_by_feats_mapped, counts_by_feats_mapped, numtokens_by_lemma, counts_by_lemma_mapped, pos_by_feats_mapped, language+"_cleaned", ("noun", "verb"))
#    make_tokentypeplots(numtokens_by_feats, counts_by_feats, numtokens_by_lemma, counts_by_lemma, pos_by_feats, language, ("noun", "verb"))

#    make_inflplots(numtokens_by_feats_mapped, counts_by_feats_mapped, pos_by_feats_mapped, language+"_cleaned", ("noun", "verb"))

#    make_lemmaplots(numtokens_by_lemma, counts_by_lemma, language, "noun", cutoff=100000)
#    make_lemmaplots(numtokens_by_lemma, counts_by_lemma, language, "verb", cutoff=100000)
#    make_lemmaplots(numtokens_by_lemma, counts_by_lemma_nofeats, language+"_surfaceforms", "noun", cutoff=100000)
#    make_lemmaplots(numtokens_by_lemma, counts_by_lemma_nofeats, language+"_surfaceforms", "verb", cutoff=100000)
#    make_lemmaplots(numtokens_by_lemma, counts_by_lemma_mapped, language+"_cleaned", "noun", cutoff=100000)
    make_lemmaplots(numtokens_by_lemma, counts_by_lemma_mapped, language+"_cleaned", "verb", cutoff=100000)




#############3
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
