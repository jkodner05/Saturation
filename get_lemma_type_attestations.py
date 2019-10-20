import re, sys
from os import listdir, walk
from os.path import isfile, join
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from construct_featmap import *
import statistics

PATH = "../../data/ud-treebanks-v2.3"

languages = sys.argv[1:]

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
    items_by_pos = {}
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
                if "_" in lemma or "_" in form:
                    continue

                if pos not in items_by_pos:
                    items_by_pos[pos] = []
                items_by_pos[pos].append((lemma, form, feats))

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
    return items_by_pos, numtokens_by_feats, counts_by_feats, numtokens_by_lemma, forms_by_lemma_nofeats, counts_by_lemma_nofeats, forms_by_lemma, counts_by_lemma, pos_by_feats, numtokens


def get_pdgmsize_stats(counts_by_lemma, numtoks_by_lemma, pos):
    avgsize = 0
    maxsize = 0
    maxone = ""
    relevantcount = 1
    relevanttokens = 0
    for lemma, size in counts_by_lemma.items():
        if lemma[1] == pos:
            relevanttokens += numtoks_by_lemma[lemma]
            avgsize += size
            if size > maxsize:
                maxsize = size
                maxone = lemma
            relevantcount += 1
    avgsize /= relevantcount
#    print(maxone)
    return avgsize, maxsize, relevantcount-1, maxone, relevanttokens


def plot_only_infltypes_by_counts(num_by_feats, pos_by_feats, ylab, subtitle):
    fig, ax = plt.subplots(1, 1, figsize=(12,12))

    if len(num_by_feats) < 2:
        return
    maxtokens = max(num_by_feats.values())

    x = []
    h1 = set([])
    h2 = set([])
    numbins = 0
    num_by_feats = sorted(num_by_feats.items(), key=lambda kv: kv[1], reverse=True)
    for feats, count in num_by_feats:        
        if "verb" in pos_by_feats[feats]:
#            print(feats, count)
            if HIGHLIGHT1 in feats or HIGHLIGHT2 in feats:
                x.extend([numbins]*count)
                if HIGHLIGHT1 in feats:
                    h1.add(numbins)
                elif HIGHLIGHT2 in feats:
                    h2.add(numbins)
                numbins += 1

    n, bins, patches = ax.hist(x, numbins)

    for i, patch in enumerate(patches):
        if i in h2:
            patch.set_facecolor("goldenrod")

    ax.set_xlabel('Past Verb Form', fontsize=30)
    ax.set_ylabel(ylab, fontsize=30)
    ax.set_title("Gothic" + ": " + subtitle + ' by Past Verb Infl. Category', fontsize=36)
    plt.xticks(fontsize=24)  
    plt.yticks(fontsize=24)

    handles = [Rectangle((0,0),1,1,color=c) for c in [patches[0].get_facecolor(),"goldenrod"]]
    labels= ["Past 3sg and Past Part.", "Other"]
    plt.legend(handles, labels, fontsize = 30)

    plt.savefig("plots/" + "UD_Gothic_cleaned"  + "_verbs" + ".png")
    plt.close(fig)


    exit()
    return




def plot_infltypes_by_counts(ax, num_by_feats, pos_by_feats, language, pos, subtitle):
    if len(num_by_feats) < 2:
        return
    maxtokens = max(num_by_feats.values())

    x = []
    numbins = 0
    sorted_num_by_feats = sorted(num_by_feats.items(), key=lambda kv: kv[1], reverse=True)
    freqs = set([])
    maxfreq = 0
    maxfeats = ""
    for feats, count in sorted_num_by_feats:        
        if pos in pos_by_feats[feats]:
            if pos == "verb":
                if count > maxfreq:
                    maxfreq = count
                    maxfeats = feats
                freqs.add(count)
#                print(feats, count)
            x.extend([numbins]*count)
            numbins += 1

    if(freqs):
        print(maxfeats)
        print("Max num type:", max(freqs))
        print("Mean num type:", statistics.mean(freqs))
        print("Median num type:", statistics.median(freqs))


    n, bins, patches = ax.hist(x, numbins)

    for i, patch in enumerate(patches):
        if HIGHLIGHT1 in sorted_num_by_feats[i][0]:
            patch.set_facecolor("r")
        elif HIGHLIGHT2 in sorted_num_by_feats[i][0]:
            patch.set_facecolor("goldenrod")

    fontsize=40
    ax.set_xlabel('Inflectional Category',fontsize=fontsize)
    ax.set_ylabel(subtitle + " Count",fontsize=fontsize)
    ax.set_title(language + ": " + subtitle + ' by Infl. Category: ' + pos,fontsize=fontsize)
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
    freqs = []
    for lemma, numtypes in numtypes_by_lemma:
        if lemma[1] == pos:
            if numtypes > 0:
                freqs.append(numtypes)
                x.extend([numbins]*numtypes)
                numbins += 1
            if cutoff and numbins >= cutoff:
                break

    print("Max 10 num type:", [lemma for lemma in numtypes_by_lemma if lemma[0][1] == pos][0:20])
    print("Max num type:", max(freqs))
    print("Mean num type:", statistics.mean(freqs))
    print("Median num type:", statistics.median(freqs))

    if numbins < 2:
        return

    n, bins, patches = ax.hist(x, numbins)
#    for i, patch in enumerate(patches):
#        patch.set_facecolor("grey")

    fontsize = 40
    ax.tick_params(labelsize=20)
    ax.set_xlabel('Ranked Lemmas', fontsize=fontsize)
    ax.set_ylabel('Infl Form Type Count', fontsize=fontsize)
#    ax.set_title('Infl Form Type Counts by Lemma', fontsize=fontsize)
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
#        if feats not in numtoks_by_feats_ranked:
#            print(feats)
        ypts.append(numtoks_by_feats_ranked[feats])

    ax.plot(xpts, ypts, "o")
        
    ax.set_xlabel('Type Rank')
    ax.set_ylabel('Token Rank')
    ax.set_title('Type vs Token Rank for ' + pos + " " + title)
    return



def make_inflplots(numtokens_by_feats, numtypes_by_feats, pos_by_feats, language, poss):
#    fig, axarr = plt.subplots(2, 2, figsize=(12,12))
#    fig.suptitle(language + " Inflectional Category Frequencies")
#    for i, pos in enumerate(poss):
#        plot_infltypes_by_counts(axarr[0,i], numtokens_by_feats, pos_by_feats, language, pos, "Tokens")
#        plot_infltypes_by_counts(axarr[1,i], numtypes_by_feats, pos_by_feats, language, pos, "Types")

#    plt.savefig("plots/" + language + "_infl" + ".png")
#    plt.close(fig)

    fig, axarr = plt.subplots(figsize=(12,12))
    fig.suptitle("UDT " + language.split("_")[1], fontsize=40)
    plot_infltypes_by_counts(axarr, numtypes_by_feats, pos_by_feats, language, poss[0], "Types")
    plt.savefig("plots/" + language + "_infl_" + poss[0] + ".png")
    plt.close(fig)


def make_lemmaplots(numtokens_by_lemma, numtypes_by_lemma, language, pos, cutoff=0):
#    fig, axarr = plt.subplots(2, 2, figsize=(12,12))
#    fig.suptitle(language + " POS: " + pos)

#    plot_lemmas_by_numtokens(axarr[0,0], numtokens_by_lemma, pos, cutoff=cutoff)
#    plot_lemmas_by_numtypes(axarr[0,1], numtypes_by_lemma, pos, cutoff=cutoff)
#    plot_numtokens_by_lemmas(axarr[1,0], numtokens_by_lemma, pos)
#    plot_numtypes_by_lemmas(axarr[1,1], numtypes_by_lemma, pos)
    
#    plt.savefig("plots/" + language + "_" + pos + ".png")
#    plt.close(fig)

    fig, axarr = plt.subplots(figsize=(12,12))
    fig.suptitle("UDT " + language.split("_")[1], fontsize=40)
    plot_lemmas_by_numtypes(axarr, numtypes_by_lemma, pos, cutoff=cutoff)
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


def get_mapdict(pos_by_feats, language):
    mapdict = {}
    if language == "UD_Arabic":
        mapdict = construct_UD_Arabic(pos_by_feats)
    elif language == "UD_Armenian":
        mapdict = construct_UD_Armenian(pos_by_feats)
    elif language == "UD_Czech":
        mapdict = construct_UD_Czech(pos_by_feats)
    elif language == "UD_English":
        mapdict = construct_UD_English(pos_by_feats)
    elif language == "UD_Finnish":
        mapdict = construct_UD_Finnish(pos_by_feats)
    elif language == "UD_German":
        mapdict = construct_UD_German(pos_by_feats)
    elif language == "UD_Gothic":
        mapdict = construct_UD_Gothic(pos_by_feats)
    elif language == "UD_Hungarian":
        mapdict = construct_UD_Hungarian(pos_by_feats)
    elif language == "UD_Latin":
        mapdict = construct_UD_Latin(pos_by_feats)
    elif language == "UD_Portuguese":
        mapdict = construct_UD_Portuguese(pos_by_feats)
    elif language == "UD_Russian":
        mapdict = construct_UD_Russian(pos_by_feats)
    elif language == "UD_Spanish":
        mapdict = construct_UD_Spanish(pos_by_feats)
    elif language == "UD_Tagalog":
        mapdict = construct_UD_Tagalog(pos_by_feats)
    elif language == "UD_Turkish":
        mapdict = construct_UD_Turkish(pos_by_feats)
    else:
        print("Cannot map " + language)
    return mapdict

def map_feats_by_lemma(forms_by_lemma, pos_by_feats, language):
    mapdict = get_mapdict(pos_by_feats, language)
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
            if DELETE in mappedfeats:
                continue
            featset.add(mappedfeats)
            forms_by_lemma_mapped[lemmapos].add((form,mappedfeats))

    counts_by_lemma_mapped = {lemma:len(forms) for lemma, forms in forms_by_lemma_mapped.items()}
    return counts_by_lemma_mapped, forms_by_lemma_mapped
    

def map_numfeats(counts_by_feats, pos_by_feats, language):
    mapdict = get_mapdict(pos_by_feats, language)
    counts_by_feats_mapped = {}
    for feats, count in counts_by_feats.items():
        if feats not in mapdict:
            continue
        mappedfeats = mapdict[feats]
        if DELETE in mappedfeats:
            continue
        if mappedfeats not in counts_by_feats_mapped:
            counts_by_feats_mapped[mappedfeats] = 0
        counts_by_feats_mapped[mappedfeats] += counts_by_feats[feats]
    return counts_by_feats_mapped


def map_posfeats(counts_by_feats, pos_by_feats, language):
    mapdict = get_mapdict(pos_by_feats, language)
    pos_by_feats_mapped = {}
    for feats, pos in counts_by_feats.items():
        if feats not in mapdict:
            continue
        mappedfeats = mapdict[feats]
        if DELETE in mappedfeats:
            continue
        pos_by_feats_mapped[mappedfeats] = pos_by_feats[feats]
    return pos_by_feats_mapped


def map_itemspos(items_by_pos, pos_by_feats, language):
    mapdict = get_mapdict(pos_by_feats, language)
    items_by_pos_mapped = {}
    for pos, items in items_by_pos.items():
        if pos not in items_by_pos_mapped:
            items_by_pos_mapped[pos] = []
        for item in items:
            feats = item[2]
            if feats not in mapdict:
                continue
            mappedfeats = mapdict[feats]
            if DELETE in mappedfeats:
                continue
            items_by_pos_mapped[pos].append((item[0], item[1], mappedfeats))
    return items_by_pos_mapped


def writeout(items_by_pos, forms_by_lemma, counts_by_lemma, counts_by_feats, numtokens_by_lemma, numtokens_by_feats, pos_by_feats, language, pos):
    with open("outputdata/" + language + "_" + pos + "_tokenlist.txt", "w") as fout:
        fout.write("LEMMA\tFORMS\tFEATURES\n")
        for item in items_by_pos[pos]:
            fout.write("%s\t%s\t%s\n" % item)
    with open("outputdata/" + language + "_" + pos + "_lemmastats.txt", "w") as fout:
        fout.write("LEMMA\tTOKENS\tRAW_PS\tFORM_FEAT_PAIRS\n")
        for lemmapos, formfeatss in forms_by_lemma.items():
            lemma = lemmapos[0]
            thispos = lemmapos[1]
            if pos == thispos:
                pairs = []
                for formfeats in formfeatss:
                    form = formfeats[0]
                    feats = formfeats[1]
                    if pos in pos_by_feats[feats]:
                        pairs.append(formfeats)
                fout.write("%s\t%s\t%s\t%s\n" % (lemma, numtokens_by_lemma[lemmapos], counts_by_lemma[lemmapos], ",".join([" ".join(pair) for pair in pairs])))
    with open("outputdata/" + language + "_" + pos + "_inflstats.txt", "w") as fout:
        fout.write("FEATURES\tTOKENS\tRAW_IPS\n")
        for feats, fpos in pos_by_feats.items():
            if pos in fpos:
                fout.write("%s\t%s\t%s\n" % (feats, numtokens_by_feats[feats], counts_by_feats[feats]))
            



def main():
    fnames_by_dirname = get_fnames()
    for language, fnames in fnames_by_dirname.items():
        is_testlang = False
        for testlang in languages:
            if testlang in language:
                is_testlang = True
        if not is_testlang:
            continue

        items_by_pos, numtokens_by_feats, counts_by_feats, numtokens_by_lemma, forms_by_lemma_nofeats, counts_by_lemma_nofeats, forms_by_lemma, counts_by_lemma, pos_by_feats, numtokens = get_counts(fnames)
        counts_by_lemma_mapped, forms_by_lemma_mapped = map_feats_by_lemma(forms_by_lemma, pos_by_feats, language)
        counts_by_feats_mapped = map_numfeats(counts_by_feats,  pos_by_feats, language)
        numtokens_by_feats_mapped = map_numfeats(numtokens_by_feats,  pos_by_feats, language)
        pos_by_feats_mapped = map_posfeats(pos_by_feats,  pos_by_feats, language)
        items_by_pos_mapped = map_itemspos(items_by_pos, pos_by_feats, language)

        print("\n\n")
        print(language)
        print(numtokens, len(counts_by_lemma))
#        for i, form in enumerate(forms_by_lemma_mapped[("et","verb")]):
#            if "=vnoun" in form:
#                print(i, form)


        #bybee
    #    for verb in bybee1985strong:
    #        if (verb, "verb") in counts_by_lemma_mapped:
    #            print(verb, counts_by_lemma_mapped[(verb, "verb")], forms_by_lemma_mapped[(verb,"verb")])
    #        else:
    #            print(verb, 0)

#        print(len(forms_by_lemma[("tener","verb")]))
#        for f in sorted(forms_by_lemma[("tener","verb")], key = lambda kv: kv[0]):
#            print(f)
#        print(len(forms_by_lemma_mapped[("tener","verb")]))
#        for f in sorted(forms_by_lemma_mapped[("tener","verb")], key = lambda kv: kv[0]):
#            print(f)
#        print(len(forms_by_lemma_nofeats[("tener","verb")]))
#        for f in sorted(forms_by_lemma_nofeats[("tener","verb")], key = lambda kv: kv):
#            print(f)



    ##########################
    # Token Type Plots
        #    make_tokentypeplots(numtokens_by_feats_mapped, counts_by_feats_mapped, numtokens_by_lemma, counts_by_lemma_mapped, pos_by_feats_mapped, language+"_cleaned", ("noun", "verb"))
    #    make_tokentypeplots(numtokens_by_feats, counts_by_feats, numtokens_by_lemma, counts_by_lemma, pos_by_feats, language, ("noun", "verb"))



    ##########################
    # writeout raw UDT
        writeout(items_by_pos, forms_by_lemma, counts_by_lemma, counts_by_feats, numtokens_by_lemma, numtokens_by_feats, pos_by_feats, language, "verb")

    ##########################
    # writeout cleaned UDT
        writeout(items_by_pos_mapped, forms_by_lemma_mapped, counts_by_lemma_mapped, counts_by_feats_mapped, numtokens_by_lemma, numtokens_by_feats_mapped, pos_by_feats_mapped, language+"_cleaned", "verb")



    ##########################
    # Raw UDT features
        print("\nRaw UDT")
        avgverb, maxverb, numverb, maxverbval, verbtokens = get_pdgmsize_stats(counts_by_lemma, numtokens_by_lemma, "verb")
#        print("N: ", avgnoun, maxnoun, numnoun, nountokens, nountokens/numnoun)
        print("V: ", avgverb, maxverb, numverb, verbtokens, verbtokens/numverb)
        make_lemmaplots(numtokens_by_lemma, counts_by_lemma, language, "verb", cutoff=100000)

    ##########################
    # Cleaned UDT features
        print("\nCleaned UDT")
        avgverb, maxverb, numverb, maxverbval, verbtokens = get_pdgmsize_stats(counts_by_lemma_mapped, numtokens_by_lemma, "verb")
#        print("N: ", avgnoun, maxnoun, numnoun, nountokens, nountokens/numnoun)
        print("V: ", avgverb, maxverb, numverb, verbtokens, verbtokens/numverb)
#        print(forms_by_lemma[("folear","verb")])
#        print(forms_by_lemma_mapped[("_","verb")])
#        exit()
        for lemma, formfeats in forms_by_lemma_mapped.items():
            if lemma[1] == "verb":
                feats_by_form = {}
                for form, feat in formfeats:
                    if "_" in form:
                        print(lemma)
                    if form not in feats_by_form:
                        feats_by_form[form] = []
                    feats_by_form[form].append(feat)
                    if len(feats_by_form[form]) > 1:
                        print(form)
                        for feat in feats_by_form[form]:
                            print("\t", feat)

#        for feats in forms_by_lemma[("ասել","verb")]:
#            print(feats)
        make_lemmaplots(numtokens_by_lemma, counts_by_lemma_mapped, language+"_cleaned", "verb", cutoff=100000)

    ##########################
    # Unique surface forms only
        print("\nSurface UDT")
        avgverb, maxverb, numverb, maxverbval, verbtokens = get_pdgmsize_stats(counts_by_lemma_nofeats, numtokens_by_lemma, "verb")
#        print("N: ", avgnoun, maxnoun, numnoun, nountokens, nountokens/numnoun)
        print("V: ", avgverb, maxverb, numverb, verbtokens, verbtokens/numverb)
        make_lemmaplots(numtokens_by_lemma, counts_by_lemma_nofeats, language+"_surfaceforms", "verb", cutoff=100000)


    ##########################
    # Raw UDT Infl
        print("\nRaw UDT Infl")
        make_inflplots(numtokens_by_feats, counts_by_feats, pos_by_feats, language, ("verb",))

    ##########################
    # Cleaned UDT Infl
        print("\nCleaned UDT Infl")
        make_inflplots(numtokens_by_feats_mapped, counts_by_feats_mapped, pos_by_feats_mapped, language+"_cleaned", ("verb",))

    ############
    #    plot_only_infltypes_by_counts(counts_by_feats_mapped, pos_by_feats_mapped, "# Lemmas Attested", "Types")
    #    plot_only_infltypes_by_counts(numtokens_by_feats_mapped, pos_by_feats_mapped, "# Tokens", "Tokens")




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

if __name__=="__main__":
    main()
