import re
from feats_maps import *

def construct_UD_generic(rawfeats):
    featmap = {}
#    for feat in rawfeats:
#        featparts = feat.split(",")

#
# Do mapping here
#

#cleanfeat = feat
    featmap[feat] = cleanfeat
    print(len(set(featmap.values())),featmap)
    exit()

def construct_UD_English(pos_by_feats):
    featmap = {}
    for feats, poss in pos_by_feats.items():
        if "noun" in poss or "verb" in poss:
            newfeats = feats
            if "tense=pres" in feats and "person=3" in feats:
                if "number=plur" not in feats:
                    newfeats = "pres3sg"
                else:
                    newfeats = "pres"
            elif "tense=pres" in feats and "verbform=fin" in feats:
                newfeats = "pres"
            elif "verbform=inf" in feats:
                newfeats = "pres"
            elif "mood=imp" in feats:
                newfeats = "pres"
            elif "tense=past" in feats and "verbform=fin" in feats:
                newfeats = "past"
            elif "tense=pres" in feats and "verbform=part" in feats:
                newfeats = "ing"
            elif "tense=past" in feats and "verbform=part" in feats:
                newfeats = "ppart"
            elif "voice=pass" in feats and "verbform=part" in feats:
                newfeats = "ppart"
            elif "verbform=ger" in feats:
                newfeats = "ing"

            if "number=sing" in feats and "tense=" not in feats and "verform=" not in feats:
                newfeats = "sg"
            elif "number=plur" in feats and "tense=" not in feats and "verform=" not in feats:
                newfeats = "pl"

            if newfeats == feats:
                newfeats = DELETE
            featmap[feats] = newfeats

    return featmap



def construct_UD_Finnish(pos_by_feats):
    findnumber = re.compile(r"(number=(plur|sing))")
    findcase = re.compile(r"(case=...)")
    findverbform = re.compile(r"(verbform=\w+)")
    findvoice = re.compile(r"(voice=\w+)")
    findpartform = re.compile(r"(partform=\w+)")
    findperson = re.compile(r"(person=\d)")
    findpolarity = re.compile(r"(polarity=\w+)")
    findmood = re.compile(r"(mood=\w+)")
    findinfform = re.compile(r"(infform=\d)")
    featmap = {}
    for feats, poss in pos_by_feats.items():
        newfeats = ""
        if "noun" in poss:# or "verb" in poss:
            number = findnumber.search(feats)
            case = findcase.search(feats)
            if number and case:
                newfeats = number.group(0) + "|" + case.group(0)
            else:
                continue
            featmap[feats] = newfeats
        elif "verb" in poss:
            number = findnumber.search(feats)
            case = findcase.search(feats)
            verbform = findverbform.search(feats)
            voice = findvoice.search(feats)
            partform = findpartform.search(feats)
            person = findperson.search(feats)
            number = findnumber.search(feats)
            mood = findmood.search(feats)
            polarity = findpolarity.search(feats)
            infform = findinfform.search(feats)
            if verbform:
                newfeats += verbform.group(0)
                if voice:
                    newfeats += "|" + voice.group(0)
                if partform:
                    newfeats += "|" + partform.group(0)
                if person:
                    newfeats += "|" + person.group(0)
                if polarity:
                    newfeats += "|" + polarity.group(0)
                if mood:
                    newfeats += "|" + mood.group(0)
                if infform:
                    newfeats += "|" + infform.group(0)
            else:
                newfeats = DELETE
                continue
            if not case:
                if number:
                    newfeats += "|" + number.group(0)
                if not number:
                    newfeats = DELETE
                    continue

            featmap[feats] = newfeats

    return featmap
#    print(len(set(featmap.values())),featmap)


def construct_UD_Czech(rawfeats):
    featmap = {}
    for feat in rawfeats:
        featparts = feat.split(",")
#        if featparts[0] != "n" and featparts[0] != "v":
#            continue
#        if len(featparts) < 2:
#            continue

        cleanfeat = feat
        featmap[feat] = cleanfeat
    print(len(set(featmap.values())),featmap.values())
    exit()
