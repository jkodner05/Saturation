import re, sys
from os import listdir, walk, mkdir
from os.path import isfile, join, exists
from construct_featmap import *
import statistics

#PATH = "../../data/ud-treebanks-v2.3"
PATH = sys.argv[1]
languages = sys.argv[2:]

earlystop = ""
#earlystop = int(sys.argv[3])

historical = set(["ud_gothic","ud_latin"])
dohighlight = set([])
psizes = {("UD_English_cleaned","verb"):5,("UD_German_cleaned","verb"):29,("UD_Gothic_cleaned","verb"):52,("UD_Finnish_cleaned","verb"):150,("UD_Latin_cleaned","verb"):113,("UD_Spanish_cleaned","verb"):67,("UD_Turkish_cleaned","verb"):120,("CHILDES_English","verb"):5,("CHILDES_German","verb"):29,("CHILDES_Spanish","verb"):67}

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
        
def get_counts(fnames, language, mapfeats):
    forms_by_lemma = {}
    forms_by_lemma_nofeats = {}
    numtokens = 0
    numtokens_by_feats = {}
    lemmas_by_feats = {}
    numtokens_by_lemma = {}
    pos_by_feats = {}
    feats_by_pos = {}
    items_by_pos = {}
    if mapfeats:
        print("Creating feature map",end="")
        pos_by_feats_mapping = {}
        for fname in fnames:
            with open(fname, "r") as f:
                for line in f:
                    if line[0] == "#" or not line.strip():
                        continue
                    components = line.lower().split("\t")
                    form = components[1]
                    lemma = components[2]
                    pos = components[3]
                    feats = components[5]
                    if feats not in pos_by_feats_mapping:
                        pos_by_feats_mapping[feats] = set([])
                    pos_by_feats_mapping[feats].add(pos)
                print(".", end="")
        mapdict = get_mapdict(pos_by_feats_mapping, language)
        print()
#        print(mapdict)

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
                if re.match(r"^\d+", lemma):
                    continue
                if not re.search(r"\w+", lemma):
                    continue
                if re.match(r"^\W", lemma) or re.match(r".*?\W$", lemma):
                    continue
                if lemma[-1] == ".":
                    continue
                if "#" in lemma:
                    continue

                if mapfeats:
                    if (feats,pos) not in mapdict:
#                        print("Feats not in mapdict", feats, lemma, pos)
                        continue
#                    print((feats, pos),)
                    feats = mapdict[(feats, pos)]
#                    print(feats)
                    if language == "UD_EnglisH":
                        lemmapos = (lemma, pos)
                    if language == "UD_English" and (lemma, pos) in forms_by_lemma and len(forms_by_lemma[(lemma,pos)]) > 5:
        #                print("Too may pos", lemmapos, forms_by_lemma_mapped[lemmapos])
                        continue
                    if DELETE in feats:
                        continue
                    if feats in lemmas_by_feats and (lemma,pos) in lemmas_by_feats[feats]:
                        # alternative form
                        if (form,feats) not in forms_by_lemma[(lemma,pos)]:
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
#                if numtokens == earlystop:
#                    break
#            if numtokens == earlystop:
#                break
#        if numtokens == earlystop:
#            break

#    print("Noun:", len(feats_by_pos["noun"]),feats_by_pos["noun"])
#    print("Verb:", len(feats_by_pos["verb"]),feats_by_pos["verb"])
    counts_by_feats = {feats:len(lemmas) for feats, lemmas in lemmas_by_feats.items()}
    counts_by_lemma = {lemma:len(forms) for lemma, forms in forms_by_lemma.items()}
    counts_by_lemma_nofeats = {lemma:len(forms) for lemma, forms in forms_by_lemma_nofeats.items()}
    print(numtokens)
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


def PAST_plot_only_infltypes_by_counts(num_by_feats, pos_by_feats, title, ylab, subtitle, language, suff):
    fig, ax = plt.subplots(figsize=(12,12))
    fig.set_dpi(300)
    if len(num_by_feats) < 2:
        return
    maxtokens = max(num_by_feats.values())

    x = []
    h1 = set([])
    h2 = set([])
    h3 = set([])
    numbins = 0
    num_by_feats = sorted(num_by_feats.items(), key=lambda kv: kv[1], reverse=True)
    sumcounts = 0
    relevantcounts = []
    for feats, count in num_by_feats:        
        if "verb" in pos_by_feats[feats]:
#            print(feats, count)
            if HIGHLIGHT1 in feats or HIGHLIGHT2 in feats or HIGHLIGHT3 in feats:
                x.extend([numbins]*count)
                if HIGHLIGHT1 in feats:
                    h1.add(numbins)
                    print(feats, count)
                elif HIGHLIGHT2 in feats:
                    h2.add(numbins)
                    print(feats, count)
                elif HIGHLIGHT3 in feats:
                    h3.add(numbins)
                    print(feats, count)
                numbins += 1
                sumcounts += count
                relevantcounts.append(count)
    print(sumcounts, relevantcounts[0], relevantcounts[1], relevantcounts[2])

#    print(numbins)
#    n, bins, patches = ax.hist(x, numbins)

#    for i, patch in enumerate(patches):
#        if i in h1:
#            patch.set_facecolor("silver")
#        if i in h2:
#            patch.set_facecolor("goldenrod")


    colors = []
    for i in range(0,numbins):
        if i in h1:
            colors.append("silver")
        elif i in h2:
            colors.append("goldenrod")
        else:
            colors.append("C0")
    ax.bar(range(0,len(relevantcounts)), relevantcounts, width=1.0, linewidth=1, color=colors, edgecolor=colors)

    fontsize=30
    ax.set_xlabel('Past Infl. Category', fontsize=fontsize)
    ax.set_ylabel(ylab, fontsize=fontsize)
    ax.set_title(language.replace("UD_","") + " " + title, fontsize=35)
    ax.tick_params(labelsize=25)
    plt.xticks(range(0, len(relevantcounts)+1, 3))
    
    handles = [Rectangle((0,0),1,1,color=c) for c in ["silver", "goldenrod", "C0"]]
    labels= ["Past Ptc", "Past 3sg", "Other Past"]
    plt.legend(handles, labels, fontsize=fontsize)

    plt.savefig("plots/" + language + "_pastinfl_"  + suff + ".pdf")
    plt.close(fig)

#    exit()
    return


def plot_only_infltypes_by_counts(num_by_feats, pos_by_feats, ylab, subtitle, language):
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
            if HIGHLIGHT1 in feats or HIGHLIGHT2 in feats or True:
                x.extend([numbins]*count)
                if HIGHLIGHT1 in feats:
                    h1.add(numbins)
                elif HIGHLIGHT2 in feats:
                    h2.add(numbins)
                numbins += 1
                

    print(numbins)
    n, bins, patches = ax.hist(x, numbins)

    for i, patch in enumerate(patches):
        if i in h2:
            patch.set_facecolor("goldenrod")

    ax.set_xlabel('Past Verb Form', fontsize=30)
    ax.set_ylabel(ylab, fontsize=30)
    ax.set_title(language + ": " + subtitle + ' by Past Verb Infl. Category', fontsize=36)
    plt.xticks(fontsize=24)  
    plt.yticks(fontsize=24)

    handles = [Rectangle((0,0),1,1,color=c) for c in [patches[0].get_facecolor(),"goldenrod"]]
    labels= ["Past 3sg and Past Part.", "Other"]
    plt.legend(handles, labels, fontsize = 30)

    plt.savefig("plots/" + language + "_cleaned"  + "_verbs" + ".png")
    plt.close(fig)

#    exit()
    return




def plot_infltypes_by_counts(ax, num_by_feats, pos_by_feats, language, pos, subtitle, begrey=False):
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


#    n, bins, patches = ax.hist(x, numbins)
#    if begrey:
#        for i, patch in enumerate(patches):
#            patch.set_facecolor("grey")
    if language in dohighlight:
        for i, patch in enumerate(patches):
            if HIGHLIGHT1 in sorted_num_by_feats[i][0]:
                patch.set_facecolor("r")
            elif HIGHLIGHT2 in sorted_num_by_feats[i][0]:
                patch.set_facecolor("goldenrod")


    y = [float(count) for feats, count in sorted_num_by_feats if (pos in pos_by_feats[feats])]
    if begrey:
        ax.bar(range(0,len(y)), y, width=1.0, color="grey", edgecolor="grey", linewidth=1)
    else:
        ax.bar(range(0,len(y)), y, width=1.0, linewidth=1)
        
    fontsize=40
    ax.tick_params(labelsize=25)
    ax.set_xlabel('Ranked Infl. Categories',fontsize=fontsize)
    ax.set_ylabel("Lemma Count",fontsize=fontsize)
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


def plot_lemmas_by_numtypes(ax, numtypes_by_lemma, pos, cutoff=0, begrey=False):
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

#    n, bins, patches = ax.hist(x, numbins)
#    if begrey:
#        for i, patch in enumerate(patches):
#            patch.set_facecolor("grey")

    numtypes_by_lemma_nozero = [(lemma, count) for lemma, count in numtypes_by_lemma if count]
    y = [float(count) for lemma, count in numtypes_by_lemma_nozero if lemma[1] == pos]
    if cutoff:
        ycut = y[0:min(len(y),cutoff)]
    if begrey:
        ax.bar(range(0,len(ycut)), ycut, width=1.0, color="grey", edgecolor="grey", linewidth=1)
    else:
        ax.bar(range(0,len(ycut)), ycut, width=1.0, linewidth=1)


    fontsize = 40
    ax.tick_params(labelsize=25)
    ax.set_xlabel('Ranked Lemmas', fontsize=fontsize)
    ax.set_ylabel('Infl. Form Type Count', fontsize=fontsize)
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


def write_lemmatokentype_by_rank(numtoks_by_lemma, numtypes_by_lemma, language, pos, flemma):

    def rank(num_by_lemma_sorted):
        num_by_lemma_ranked = {}
        num_by_lemma_ranked_nodup = {}
        numrank = 0
        numrank_nodup = -1
        prevnum = 0
        maxfreq = 0
        for lemma, num in num_by_lemma_sorted:
            if len(lemma) < 2 or lemma[1] != pos:
                continue
            numrank_nodup += 1
            if num < prevnum:
                numrank = numrank_nodup
            prevnum = num
            num_by_lemma_ranked[lemma] = numrank
            if numrank == 0:
                maxfreq = num
            num_by_lemma_ranked_nodup[lemma] = numrank_nodup
        return num_by_lemma_ranked, num_by_lemma_ranked_nodup, maxfreq

    numtoks_by_lemma_sorted = sorted(numtoks_by_lemma.items(), key=lambda kv: kv[1], reverse=True)
    numtypes_by_lemma_sorted = sorted(numtypes_by_lemma.items(), key=lambda kv: kv[1], reverse=True)

    numtypes_by_lemma_ranked, numtypes_by_lemma_ranked_nodup, maxsize = rank(numtypes_by_lemma_sorted)
    numtoks_by_lemma_ranked, numtoks_by_lemma_ranked_nodup, _ = rank(numtoks_by_lemma_sorted)

#    typrank_sorted = sorted(numtypes_by_lemma_ranked.items(), key=lambda kv:kv[1], reverse=True)
#    tokrank_sorted = sorted(numtoks_by_lemma_ranked.items(), key=lambda kv:kv[1], reverse=True)
#    for typ, rank in typrank_sorted:
#        print(typ, rank, numtypes_by_lemma[typ])
#    for tok, rank in tokrank_sorted:
#        print(tok, rank, numtoks_by_lemma[tok])
#    print(pos)
#    print("tok rank\ttok freq")
#    print(max(numtoks_by_lemma_ranked.values()),max(numtoks_by_lemma.values()))
#    print(min(numtoks_by_lemma_ranked.values()),min(numtoks_by_lemma.values()))
#    print("typ rank\ttyp freq")
#    print(max(numtypes_by_lemma_ranked.values()),max(numtypes_by_lemma.values()))
#    print(min(numtypes_by_lemma_ranked.values()),min(numtypes_by_lemma.values()))
#    exit()


    numtokss, numtypess, typeranks, tokranks = set(), set(), set(), set()
    print(len(numtoks_by_lemma_ranked), len(numtypes_by_lemma_ranked))
    corpustype = "UD Modern"
    if "Latin" in language or "Gothic" in language:
        corpustype = "UD Historical"
    elif "CHILDES" in language:
        corpustype = "CHILDES CDS"
    if (language,pos) in psizes:
        maxsize = psizes[(language,pos)]
    for lemmapos in numtoks_by_lemma_ranked:
        numtoks = numtoks_by_lemma[lemmapos]
        numtypes = numtypes_by_lemma[lemmapos]
        typerank = numtypes_by_lemma_ranked[lemmapos]
        tokrank = numtoks_by_lemma_ranked[lemmapos]
        typeranknd = numtypes_by_lemma_ranked_nodup[lemmapos]
        tokranknd = numtoks_by_lemma_ranked_nodup[lemmapos]
        numtokss.add(numtoks)
        tokranks.add(tokrank)
        numtypess.add(numtypes)
        typeranks.add(typerank)
#        if numtypes == 0:
#            continue
#        print(language, lemmapos[1], lemmapos[0], numtoks, numtypes, tokrank, typerank)
        flemma.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (corpustype,language.split("_")[1] +" "+ language.split("_")[0]+str(earlystop),maxsize,lemmapos[1],lemmapos[0],numtoks,numtypes,tokrank,typerank,tokranknd,typeranknd))
    print("Printing tok rank\ttok freq")
    print(min(tokranks),max(numtokss))
    print(max(tokranks),min(numtokss))
    print("Printing typ rank\ttyp freq")
    print(min(typeranks),max(numtypess))
    print(max(typeranks),min(numtypess))

    return


def write_infltokentype_by_rank(numtoks_by_feats, numtypes_by_feats, pos_by_feats, language, pos, finfl):

    def rank(num_by_feats_sorted):
        num_by_feats_ranked = {}
        num_by_feats_ranked_nodup = {}
        numrank = 0
        numrank_nodup = -1
        prevnum = 0
        maxfreq=0
        for feats, num in num_by_feats_sorted:
#            if len(feats) < 2 or pos not in pos_by_feats[feats]:
            if pos not in pos_by_feats[feats]:
                continue
            numrank_nodup += 1
            if num < prevnum:
                numrank = numrank_nodup
            prevnum = num
            if numrank == 0:
                maxfreq = num
            num_by_feats_ranked[feats] = numrank
            num_by_feats_ranked_nodup[feats] = numrank_nodup
        return num_by_feats_ranked, num_by_feats_ranked_nodup, maxfreq

    numtoks_by_feats_sorted = sorted(numtoks_by_feats.items(), key=lambda kv: kv[1], reverse=True)
    numtypes_by_feats_sorted = sorted(numtypes_by_feats.items(), key=lambda kv: kv[1], reverse=True)

    numtypes_by_feats_ranked, numtypes_by_feats_ranked_nodup, maxsize = rank(numtypes_by_feats_sorted)
    numtoks_by_feats_ranked, numtoks_by_feats_ranked_nodup, _ = rank(numtoks_by_feats_sorted)

    print(pos_by_feats)
    print(numtoks_by_feats_sorted, numtypes_by_feats_sorted)
    print(numtoks_by_feats_ranked, numtypes_by_feats_ranked)
    numtokss, numtypess, typeranks, tokranks = set(), set(), set(), set()
    print(len(numtoks_by_feats_ranked), len(numtypes_by_feats_ranked))
    corpustype = "UD Modern"
    if "Latin" in language or "Gothic" in language:
        corpustype = "UD Historical"
    elif "CHILDES" in language:
        corpustype = "CHILDES CDS"
    psize=maxsize
    if (language,pos) in psizes:
        psize = psizes[(language,pos)]
    for feats in numtoks_by_feats_ranked:
        numtoks = numtoks_by_feats[feats]
        numtypes = numtypes_by_feats[feats]
        typerank = numtypes_by_feats_ranked[feats]
        tokrank = numtoks_by_feats_ranked[feats]
        typeranknd = numtypes_by_feats_ranked_nodup[feats]
        tokranknd = numtoks_by_feats_ranked_nodup[feats]
        numtokss.add(numtoks)
        tokranks.add(tokrank)
        numtypess.add(numtypes)
        typeranks.add(typerank)
#        if numtypes == 0:
#            continue
#        print(language, lemmapos[1], lemmapos[0], numtoks, numtypes, tokrank, typerank)
        finfl.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (corpustype,language.split("_")[1] +" "+ language.split("_")[0]+str(earlystop),maxsize,pos,feats,numtoks,numtypes,tokrank,typerank,tokranknd,typeranknd,psize))


    return



def make_inflplots(numtokens_by_feats, numtypes_by_feats, pos_by_feats, language, poss, begrey=False):
#    fig, axarr = plt.subplots(2, 2, figsize=(12,12))
#    fig.suptitle(language + " Inflectional Category Frequencies")
#    for i, pos in enumerate(poss):
#        plot_infltypes_by_counts(axarr[0,i], numtokens_by_feats, pos_by_feats, language, pos, "Tokens")
#        plot_infltypes_by_counts(axarr[1,i], numtypes_by_feats, pos_by_feats, language, pos, "Types")

#    plt.savefig("plots/" + language + "_infl" + ".png")
#    plt.close(fig)

    fig, axarr = plt.subplots(figsize=(12,12))
    fig.set_dpi(300)
    fig.suptitle("UD " + language.split("_")[1] + " IPS", fontsize=50)
    plot_infltypes_by_counts(axarr, numtypes_by_feats, pos_by_feats, language, poss[0], "Types", begrey=begrey)
    plt.savefig("plots/" + language + "_infl_" + poss[0] + ".pdf")
    plt.close(fig)


def make_lemmaplots(numtokens_by_lemma, numtypes_by_lemma, language, pos, cutoff=0, begrey=False):
#    fig, axarr = plt.subplots(2, 2, figsize=(12,12))
#    fig.suptitle(language + " POS: " + pos)

#    plot_lemmas_by_numtokens(axarr[0,0], numtokens_by_lemma, pos, cutoff=cutoff)
#    plot_lemmas_by_numtypes(axarr[0,1], numtypes_by_lemma, pos, cutoff=cutoff)
#    plot_numtokens_by_lemmas(axarr[1,0], numtokens_by_lemma, pos)
#    plot_numtypes_by_lemmas(axarr[1,1], numtypes_by_lemma, pos)
    
#    plt.savefig("plots/" + language + "_" + pos + ".png")
#    plt.close(fig)

    fig, axarr = plt.subplots(figsize=(12,12))
    fig.set_dpi(300)
    fig.suptitle("UD " + language.split("_")[1] + " PS", fontsize=50)
    plot_lemmas_by_numtypes(axarr, numtypes_by_lemma, pos, cutoff=cutoff, begrey=begrey)
    plt.savefig("plots/" + language + "_" + pos + ".pdf")
    plt.close(fig)

#    fig.tight_layout()
#    plt.show()





def make_tokentypecsv(numtoks_by_feats, numtypes_by_feats, numtoks_by_lemma, numtypes_by_lemma, POS_by_feats, language, poss, flemma, finfl):

    for i, pos in enumerate(poss):
        print("WRITING", language, pos)
        print(len(numtoks_by_lemma))
        write_lemmatokentype_by_rank(numtoks_by_lemma, numtypes_by_lemma, language, pos, flemma)
        write_infltokentype_by_rank(numtoks_by_feats, numtypes_by_feats, POS_by_feats, language, pos, finfl)
#        plot_infltokentype_by_rank(axarr[1,i], numtoks_by_feats, numtypes_by_feats, POS_by_feats, language, pos, "Infl Category" finfl)


    

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
#    print(mapdict)
    forms_by_lemma_mapped = {}
    featset = set([])
    for lemmapos, formfeatss in forms_by_lemma.items():
        for formfeats in formfeatss:
            form = formfeats[0]
            feats = formfeats[1]
#            print(form, feats)
            if language == "UD_English" and lemmapos in forms_by_lemma_mapped and len(forms_by_lemma_mapped[lemmapos]) > 5:
#                print("Too may pos", lemmapos, forms_by_lemma_mapped[lemmapos])
                continue
#            print(form, feats)
            if feats not in mapdict:
#                print("Feats not in mapdict", formfeats, lemmapos)
                continue
#            print(form, feats)
            mappedfeats = mapdict[feats]
#            print(form, feats, mappedfeats)
            if DELETE in mappedfeats:
                continue
            featset.add(mappedfeats)
            if lemmapos not in forms_by_lemma_mapped:
                forms_by_lemma_mapped[lemmapos] = set([])
#            print((form,mappedfeats))
            forms_by_lemma_mapped[lemmapos].add((form,mappedfeats))

    counts_by_lemma_mapped = {lemma:len(forms) for lemma, forms in forms_by_lemma_mapped.items()}
    forms_by_lemma_mapped = {lemma:forms for lemma, forms in forms_by_lemma_mapped.items()}
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
    with open("lemmas.csv", "w") as flemma:
#    with open("lemmasEarly.csv", "a") as flemma:

#        flemma.write("%s,%s,%s,%s,%s,%s,%s\n" % (language,lemmapos[1],lemmapos[0],numtoks,numtypes,tokrank,typerank))
        flemma.write("corpustype,language,maxsize,pos,lemma,tokfreq,typfreq,tokrank,typrank,tokrank_notie,typrank_notie\n")
        with open("infls.csv", "w") as finfl:
#        with open("inflsEarly.csv", "a") as finfl:
            finfl.write("corpustype,language,maxsize,pos,feats,tokfreq,typfreq,tokrank,typrank,tokrank_notie,typrank_notie,psize\n")
            for language, fnames in fnames_by_dirname.items():
                is_testlang = False
                for testlang in languages:
                    if testlang in language:
                        is_testlang = True
                if not is_testlang:
                    continue

                items_by_pos, numtokens_by_feats, counts_by_feats, numtokens_by_lemma, forms_by_lemma_nofeats, counts_by_lemma_nofeats, forms_by_lemma, counts_by_lemma, pos_by_feats, numtokens = get_counts(fnames, language, mapfeats=False)
                items_by_pos_mapped, numtokens_by_feats_mapped, counts_by_feats_mapped, numtokens_by_lemma_mapped, forms_by_lemma_nofeats_mapped, counts_by_lemma_nofeats_mapped, forms_by_lemma_mapped, counts_by_lemma_mapped, pos_by_feats_mapped, numtokens_mapped = get_counts(fnames, language, mapfeats=True)


#                for lemmapos, feats in forms_by_lemma_mapped.items():
#                    if lemmapos[1] == "noun" and len(feats) > 2:
#                        print(lemmapos, feats)


#                counts_by_lemma_mapped, forms_by_lemma_mapped = map_feats_by_lemma(forms_by_lemma, pos_by_feats, language)
#                print(len(counts_by_lemma),len(counts_by_lemma_mapped))
#                exit()
#                counts_by_feats_mapped = map_numfeats(counts_by_feats,  pos_by_feats, language)
#                numtokens_by_feats_mapped = map_numfeats(numtokens_by_feats,  pos_by_feats, language)
#                pos_by_feats_mapped = map_posfeats(pos_by_feats,  pos_by_feats, language)
#                items_by_pos_mapped = map_itemspos(items_by_pos, pos_by_feats, language)

                print("\n\n")
                print(language)
                print(numtokens, len(counts_by_lemma))

            ##########################
            # Token Type Plots
                #    make_tokentypeplots(numtokens_by_feats_mapped, counts_by_feats_mapped, numtokens_by_lemma, counts_by_lemma_mapped, pos_by_feats_mapped, language+"_cleaned", ("noun", "verb"))
            #    make_tokentypeplots(numtokens_by_feats, counts_by_feats, numtokens_by_lemma, counts_by_lemma, pos_by_feats, language, ("noun", "verb"))



            ##########################
            # writeout raw UDT
#                writeout(items_by_pos, forms_by_lemma, counts_by_lemma, counts_by_feats, numtokens_by_lemma, numtokens_by_feats, pos_by_feats, language, "verb")

            ##########################
            # writeout cleaned UDT
#                writeout(items_by_pos_mapped, forms_by_lemma_mapped, counts_by_lemma_mapped, counts_by_feats_mapped, numtokens_by_lemma, numtokens_by_feats_mapped, pos_by_feats_mapped, language+"_cleaned", "verb")



            ##########################
            # Cleaned UDT features
                print("\nCleaned UDT")
                avgverb, maxverb, numverb, maxverbval, verbtokens = get_pdgmsize_stats(counts_by_lemma_mapped, numtokens_by_lemma_mapped, "verb")
#                print("N: ", avgnoun, maxnoun, numnoun, nountokens, nountokens)
                print("V: ", avgverb, maxverb, numverb, verbtokens, verbtokens, len(set([feat for feat in counts_by_feats_mapped if "verb" in pos_by_feats_mapped[feat]])))

                for lemma, formfeats in forms_by_lemma_mapped.items():
                    if lemma[1] == "verb":
                        feats_by_form = {}
                        for form, feat in formfeats:
        #                    if "_" in form:
        #                        print(lemma)
                            if form not in feats_by_form:
                                feats_by_form[form] = []
                            feats_by_form[form].append(feat)

                make_tokentypecsv(numtokens_by_feats_mapped, counts_by_feats_mapped, numtokens_by_lemma_mapped, counts_by_lemma_mapped, pos_by_feats_mapped, language+"_cleaned", ("noun", "verb"), flemma, finfl)







if __name__=="__main__":
    outdir = "outputdata"
    if not exists(outdir):
        mkdir(outdir)
    main()
