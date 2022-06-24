import argparse, re, os
from os.path import basename
from collections import defaultdict
import statistics
import numpy as np
from get_rankstats import write_lemmatokentype_by_rank, write_infltokentype_by_rank, psizes

exclude_speakers = set(["CHI", "ROS", "DAV", "ARR", "DAN", "JEN"])
exclude_lemmas = set(["be","not","me","us","you","dog","house","eye","bowl","nose","finger","boot","boat","bicycle","toy","station","zipper","channel","lunch","case","arm","clock","key","spoon","crayon","sock","glove","chicken","shadow","powder","pot","head","market","diaper","toast"])

posmap = {"n":"noun", "v":"verb", "aux":"verb", "part":"verb", "inf":"verb"}


def map_pos(pos):
    return posmap[pos]


def parse_file(fname, freqsbymorph, morphsbytype, freqsbyfeat, lemmasbyfeat, posbyfeat, POSset, language):

    textlineregex = re.compile(r"^\*[A-Z][A-Z][A-Z]:")
    morphlineregex = re.compile(r"^%mor:")

    poses = set([])

    with open(fname, "r") as f:
        speaker = ""
        for line in f:
            if textlineregex.match(line.strip()):
                textline = line.strip()
                speaker = textline[0:4]
            for excl in exclude_speakers:
                if excl in speaker:
                    continue
            if morphlineregex.match(line.strip()):
                rawwords = line.strip()[6:].split(" ")
                for word in rawwords:
                    parts = word.split("~")
                    for part in parts:
                        lemma = part.split("|")[-1].split("&")[0].split("-")[0]
                        POS = part.split("|")[0].split("#")[-1] #handles german participles
                        if not POSset or POS in POSset:
                            feats = "."
                            try:
                                feats = word.split("|")[-1].split("-")[1]
                                if "=" in feats:
                                    feats = feats.split("=")[0]
                            except:
#                                print(word)
                                pass
                            if feats in ("PL","Y") and "english" in language.lower(): #these exist on English verbs for some reason
                                continue
                            if lemma in exclude_lemmas:
                                continue
#                            if (lemma,map_pos(POS)) not in morphsbytype:
#                                print(POS, "\t", word, "\t", part, "\t", lemma)


#                            if "english" in language.lower() and "pl" in feats.lower():
#                                continue
#                                print(part, lemma, feats)

#                            print lemma, POS, POSset
                            freqsbymorph[part] += 1
                            freqsbyfeat[feats] += 1
                            morphsbytype[(lemma,map_pos(POS))].add(part)
                            lemmasbyfeat[feats].add((lemma,map_pos(POS)))
                            posbyfeat[feats].add(map_pos(POS))
#                            morphsbytype[lemma+"_"+POS].add(part)


def count_types(basedir, POSset, language):

    freqsbymorph = defaultdict(int)
    freqsbyfeat = defaultdict(int)
    morphsbytype = defaultdict(lambda : set([]))
    lemmasbyfeat = defaultdict(lambda : set([]))
    posbyfeat = defaultdict(lambda : set([]))

    for subdir, dirs, files in os.walk(basedir):
        for fname in files:
            if ".cha" in fname:
                parse_file(os.path.join(subdir, fname), freqsbymorph, morphsbytype, freqsbyfeat, lemmasbyfeat, posbyfeat, POSset, language)
                
    return dict(freqsbymorph), dict(morphsbytype), dict(freqsbyfeat), dict(lemmasbyfeat), dict(posbyfeat)


def combine_freqs_bytype(freqsbymorph, morphsbytype, infl):
    freqsbytype = {}
    for word, morphs in morphsbytype.items():
        freqsbytype[word] = 0
        for morph in morphs:
            freqsbytype[word] += freqsbymorph[morph]

    freqsbytypefiltered = {}
    if infl:
        for word, morphs in morphsbytype.items():
            hasinfl = False
            for morph in morphs:
                if infl in morph.lower():
                    hasinfl = True
            if hasinfl:
                freqsbytypefiltered[word] = freqsbytype[word]
    else:
        freqsbytypefiltered = freqsbytype            
                
    return freqsbytypefiltered


def sort_types(freqsbymorph, minfreq):

    filtered_types = {}
    for word, freq in freqsbymorph.items():
        if freq >= minfreq:
            filtered_types[word] = freq

    return sorted(filtered_types.items(), key=lambda kv: kv[1], reverse=True)
    

def writeout(outfname, sortedtypes):
    with open(outfname, "w") as f:
        for word, freq in sortedtypes:
            f.write("%s\t%s\n" % (word, freq))


def invert(morphsbytype):
    numbyinfl = {}
    for lemma, morphs in morphsbytype.items():
        for morph in morphs:
            infl = "-".join(morph.split("=")[0].split("-")[1:])
            if infl not in numbyinfl:
                numbyinfl[infl] = 0
            numbyinfl[infl] += 1
    return numbyinfl

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Get type frequencies from Brown Corpus")

    parser.add_argument("inputdir", nargs="+", help="Brown base directory or subdirectory")
    parser.add_argument("outfile", nargs="?", help="file to write output to")
    parser.add_argument("--pos", nargs="+", help="pos list", type=str)
    parser.add_argument("--minfreq", nargs="?", help="min frquency", type=int, default=0)
    parser.add_argument("--rankcutoff", nargs="?", help="rank cutoff", type=int, default=1000000)
    parser.add_argument("--infl", nargs="?", help="all lemmas must attest this inflectional category", type=str, default="")
    parser.add_argument("--languages", nargs="+", type=str, default ="")
    
    args = parser.parse_args()

        
    POSset = [{"n"},{"v","part","inf"}]
    if args.pos:
        POSset = set(args.pos)

    with open("lemmasCDS.csv", "w") as flemma:
        flemma.write("corpustype,language,maxsize,pos,lemma,tokfreq,typfreq,tokrank,typrank,tokrank_notie,typrank_notie\n")
        with open("inflCDS.csv", "w") as finfl:
            finfl.write("corpustype,language,maxsize,pos,feats,tokfreq,typfreq,tokrank,typrank,tokrank_notie,typrank_notie\n")
            for i, language in enumerate(args.languages):
                inputdir = args.inputdir[i]
                for pos in POSset:

                    freqsbymorph, morphsbytype, freqsbyfeat, lemmasbyfeat, posbyfeat, = count_types(inputdir, pos, language)
                    freqsbytype = combine_freqs_bytype(freqsbymorph, morphsbytype, args.infl.lower())

                    mappedpos = map_pos(list(pos)[0])

                    freqsbytype = {typ:freq for typ, freq in freqsbytype.items() if typ[1]==mappedpos}

                    sortedtypes = sort_types(freqsbytype, args.minfreq)
                    sortedtypes = sortedtypes[0:min(len(sortedtypes),args.rankcutoff)]

                #    writeout(args.outfile, sortedtypes)

                    print(language, pos)
                    print(morphsbytype.keys())
                    print("# Tokens", sum(freqsbymorph.values()))
                    print("# Types", len(sortedtypes))
                    morphsbytype_noPOS = {lemma:set([morph.split("|")[1].replace("&","-") for morph in morphs]) for lemma, morphs in morphsbytype.items()}
                #    numbyinfl = invert(morphsbytype_noPOS)
                    nummorphsbytype = {lemma:len(morphs) for lemma, morphs in morphsbytype_noPOS.items()}

                    write_lemmatokentype_by_rank(freqsbytype, nummorphsbytype, "CHILDES_"+language, mappedpos, flemma)

                    for typ, ps in nummorphsbytype.items():
                        if ps==6:
                            print(typ, morphsbytype[typ])
                    print("Max PS", max(nummorphsbytype.values()))
                    print("Mean PS", statistics.mean(nummorphsbytype.values()))
                    print("Median PS", statistics.median(nummorphsbytype.values()))
                #    plot_lemmas_by_numtypes(nummorphsbytype,basename(args.outfile).replace(".txt",".pdf"), args.language)



                    print("# Feats", len(lemmasbyfeat))
                    numlemmasbyfeat = {feat:len(lemmas) for feat, lemmas in lemmasbyfeat.items()}
#                    numlemmasbyfeat = {feat:len(lemmas) for feat, lemmas in lemmasbyfeat.items()}
                    
#                    print(numlemmasbyfeat)
#                    print(numtoksbyfeat)
#                    print(posbyfeat)
                    write_infltokentype_by_rank(freqsbyfeat, numlemmasbyfeat, posbyfeat, "CHILDES_"+language, mappedpos, finfl)
                #    print( {feat:lemmas for feat, lemmas in lemmasbyfeat.items()})
                    print("Num lemmas", len(nummorphsbytype))
                    print("Max IPS", max(numlemmasbyfeat.values()), max(numlemmasbyfeat.values())/len(nummorphsbytype))
                    print("Mean IPS", statistics.mean(numlemmasbyfeat.values())/len(nummorphsbytype))
                    print("Median IPS", statistics.median(numlemmasbyfeat.values())/len(nummorphsbytype))
                #    plot_infls_by_numlemmas(numlemmasbyfeat,basename(args.outfile).replace(".txt","_IPS.pdf"), args.language)



