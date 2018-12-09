import re
from feats_maps import *

def construct_UD_generic(pos_by_feats):
    findnumber = re.compile(r"(number=\w+)")
    featmap = {}
    for feats, poss in pos_by_feats.items():
        newfeats = ""
        if "noun" in poss:# or "verb" in poss:
            featmap[feats] = newfeats
        elif "verb" in poss:
            featmap[feats] = newfeats

    print(len(set(featmap.values())),set(featmap.values()))
    for feat, newfeat in featmap.items():
        if feat.count("|") != newfeat.count("|"):
            print(feat)
            print("\t", newfeat)
    exit()


def construct_UD_Czech(pos_by_feats):
    findnumber = re.compile(r"(number=\w+)")
    findcase = re.compile(r"(case=\w+)")
    findprontype = re.compile(r"(prontype=\w+)")
    findverbform = re.compile(r"(verbform=(\w+))")
    findvoice = re.compile(r"(voice=\w+)")
    findperson = re.compile(r"(person=\d)")
    findmood = re.compile(r"(mood=\w+)")
    findtense = re.compile(r"(tense=\w+)")
    findaspect = re.compile(r"(aspect=\w+)")
    findpolarity = re.compile(r"(polarity=\w+)")
    featmap = {}
    for feats, poss in pos_by_feats.items():
        newfeats = ""
        if "noun" in poss:# or "verb" in poss:
            number = findnumber.search(feats)
            case = findcase.search(feats)
            if number and case:
                newfeats = number.group(0) + "|" + case.group(0)
            else:
                newfeats=DELETE
            featmap[feats] = newfeats
        elif "verb" in poss:
            number = findnumber.search(feats)
            case = findcase.search(feats)
            verbform = findverbform.search(feats)
            voice = findvoice.search(feats)
            prontype = findprontype.search(feats)
            person = findperson.search(feats)
            mood = findmood.search(feats)
            tense = findtense.search(feats)
            aspect = findaspect.search(feats)
            polarity = findpolarity.search(feats)
            if verbform:
                newfeats += "|" + verbform.group(0)
            if voice:
                newfeats += "|" + voice.group(0)
            if person:
                newfeats += "|" + person.group(0)
            if tense:
                newfeats += "|" + tense.group(0)
            if mood:
                newfeats += "|" + mood.group(0)
            if aspect:
                newfeats += "|" + aspect.group(0)
            if polarity:
                newfeats += "|" + polarity.group(0)
            if not case:
                if number:
                    newfeats += "|" + number.group(0)
                if not number and verbform and verbform.group(2) == "fin":
                    newfeats = DELETE
            if prontype:
                newfeats = DELETE
        
            if newfeats[0] == "|":
                newfeats = newfeats[1:]
            featmap[feats] = newfeats
            
#    print(len(set(featmap.values())),set(featmap.values()))
#    for feat, newfeat in featmap.items():
#        if feat.count("|") != newfeat.count("|"):
#            print("CZ", feat)
#            print("\t", newfeat)
#    exit()
    return(featmap)


def construct_UD_German(pos_by_feats):
    findnumber = re.compile(r"(number=\w+)")
    findcase = re.compile(r"(case=\w+)")
    findprontype = re.compile(r"(prontype=\w+)")
    findverbform = re.compile(r"(verbform=(\w+))")
    findvoice = re.compile(r"(voice=\w+)")
    findperson = re.compile(r"(person=\d)")
    findmood = re.compile(r"(mood=\w+)")
    findtense = re.compile(r"(tense=\w+)")
    featmap = {}
    for feats, poss in pos_by_feats.items():
        newfeats = ""
        if "noun" in poss:# or "verb" in poss:
            number = findnumber.search(feats)
            case = findcase.search(feats)
            if number and case:
                newfeats = number.group(0) + "|" + case.group(0)
            else:
                newfeats=DELETE
            featmap[feats] = newfeats
        elif "verb" in poss:
            number = findnumber.search(feats)
            case = findcase.search(feats)
            verbform = findverbform.search(feats)
            voice = findvoice.search(feats)
            prontype = findprontype.search(feats)
            person = findperson.search(feats)
            mood = findmood.search(feats)
            tense = findtense.search(feats)
            if verbform:
                newfeats += "|" + verbform.group(0)
            if voice:
                newfeats += "|" + voice.group(0)
            if person:
                newfeats += "|" + person.group(0)
            if tense:
                newfeats += "|" + tense.group(0)
            if mood:
                newfeats += "|" + mood.group(0)
            if not case:
                if number:
                    newfeats += "|" + number.group(0)
                if not number and verbform and verbform.group(2) == "fin":
                    newfeats = DELETE
            if prontype:
                newfeats = DELETE
        
            if newfeats[0] == "|":
                newfeats = newfeats[1:]
            featmap[feats] = newfeats

#    print(len(set(featmap.values())),set(featmap.values()))
#    for feat, newfeat in featmap.items():
#        if feat.count("|") != newfeat.count("|"):
#            print(feat)
#            print("\t", newfeat)
    return(featmap)


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
    findtense = re.compile(r"(tense=\w+)")
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
            tense = findtense.search(feats)
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
                if tense:
                    newfeats += "|" + tense.group(0)
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

#    print(len(set(featmap.values())),set(featmap.values()))
#    for feat, newfeat in featmap.items():
#        if feat.count("|") != newfeat.count("|"):
#            print(feat)
#            print("\t", newfeat)

    return featmap


def construct_UD_Latin(pos_by_feats):
    findnumber = re.compile(r"(number=(plur|sing))")
    findcase = re.compile(r"(case=\w+)")
    findverbform = re.compile(r"(verbform=(\w+))")
    findperson = re.compile(r"(person=\d)")
    findmood = re.compile(r"(mood=\w+)")
    findgender = re.compile(r"(gender=\d)")
    findtense = re.compile(r"(tense=\w+)")
    findvoice = re.compile(r"(voice=\w+)")
    findaspect = re.compile(r"(aspect=\w+)")
    featmap = {}
    for feats, poss in pos_by_feats.items():
        newfeats = ""
        if "noun" in poss:# or "verb" in poss:
            number = findnumber.search(feats)
            case = findcase.search(feats)
            if number and case:
                newfeats = number.group(0) + "|" + case.group(0)
            else:
                newfeats=DELETE
            featmap[feats] = newfeats
        elif "verb" in poss:
            number = findnumber.search(feats)
            verbform = findverbform.search(feats)
            person = findperson.search(feats)
            mood = findmood.search(feats)
            gender = findgender.search(feats)
            tense = findtense.search(feats)
            voice = findvoice.search(feats)
            aspect = findaspect.search(feats)
            if verbform:
                newfeats = verbform.group(0)
                if not gender and not verbform.group(2) == "part" and not verbform.group(2) == "gdv" and not verbform.group(2) == "ger" and not verbform.group(2) == "sup":
                    if number:
                        newfeats += "|" + number.group(0)
                if person:
                    newfeats += "|" + person.group(0)
                if mood:
                    newfeats += "|" + mood.group(0)
                if tense:
                    newfeats += "|" + tense.group(0)
                if voice:
                    newfeats += "|" + voice.group(0)
                if aspect:
                    newfeats += "|" + aspect.group(0)
                if verbform.group(2) == "fin":
                    if not person or not number or not mood or not voice:
                        print(feats)
                        newfeats = DELETE
            else:
                newfeats = DELETE    
            featmap[feats] = newfeats

#    print(len(set(featmap.values())),set(featmap.values()))
#    for feat, newfeat in featmap.items():
#        if feat.count("|") != newfeat.count("|"):
#            print(feat)
#            print("\t", newfeat)
    return featmap
    exit()


def construct_UD_Spanish(pos_by_feats):
    findnumber = re.compile(r"(number=(plur|sing))")
    findverbform = re.compile(r"(verbform=(\w+))")
    findperson = re.compile(r"(person=\d)")
    findmood = re.compile(r"(mood=\w+)")
    findgender = re.compile(r"(gender=\d)")
    findtense = re.compile(r"(tense=\w+)")

    featmap = {}
    for feats, poss in pos_by_feats.items():
        newfeats = ""
        if "noun" in poss:# or "verb" in poss:
            number = findnumber.search(feats)
            if not number:
                newfeats = DELETE
            else:
                newfeats = number.group(0)
            featmap[feats] = newfeats
        elif "verb" in poss:
            number = findnumber.search(feats)
            verbform = findverbform.search(feats)
            person = findperson.search(feats)
            mood = findmood.search(feats)
            gender = findgender.search(feats)
            tense = findtense.search(feats)
            if verbform:
                newfeats = verbform.group(0)
                if not gender and not verbform.group(2) == "part":
                    if number:
                        newfeats += "|" + number.group(0)
                if person:
                    newfeats += "|" + person.group(0)
                if mood:
                    newfeats += "|" + mood.group(0)
                if tense:
                    newfeats += "|" + tense.group(0)
                if verbform.group(2) == "fin":
                    if not person or not number or not mood:
                        newfeats = DELETE
            else:
                newfeats = DELETE    

#            print(feats, "\t", newfeats, verbform.group(2))
            featmap[feats] = newfeats
#    print(len(set(featmap.values())),set(featmap.values()))    
    for feat, newfeat in featmap.items():
        if feat.count("|") != newfeat.count("|"):
            print(feat)
            print("\t", newfeat)
    return featmap


def construct_UD_Turkish(pos_by_feats):
    findnumber = re.compile(r"(number=(plur|sing))")
    findcase = re.compile(r"(case=\w+)")
    findverbform = re.compile(r"(verbform=\w+)")
    findvoice = re.compile(r"(voice=\w+)")
    findpartform = re.compile(r"(partform=\w+)")
    findperson = re.compile(r"(person=\d)")
    findpolarity = re.compile(r"(polarity=\w+)")
    findmood = re.compile(r"(mood=\w+)")
    findaspect = re.compile(r"(aspect=\w+)")
    findevident = re.compile(r"(evident=\w+)")
    findtense = re.compile(r"(tense=\w+)")
    featmap = {}
    for feats, poss in pos_by_feats.items():
        newfeats = ""
        if "noun" in poss:# or "verb" in poss:
            number = findnumber.search(feats)
            case = findcase.search(feats)
            if number and case:
                newfeats = number.group(0) + "|" + case.group(0)
            else:
                newfeats=DELETE
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
            aspect = findaspect.search(feats)
            evident = findevident.search(feats)
            tense = findtense.search(feats)
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
            if tense:
                newfeats += "|" + tense.group(0)
            if evident:
                newfeats += "|" + evident.group(0)
            if aspect:
                newfeats += "|" + aspect.group(0)
            if not case:
                if number:
                    newfeats += "|" + number.group(0)

            if newfeats[0] == "|":
                newfeats = newfeats[1:]
            featmap[feats] = newfeats

    print(len(set(featmap.keys())),len(set(featmap.values())),set(featmap.values()))
#    for feat, newfeat in featmap.items():
#        if feat.count("|") != newfeat.count("|"):
#            print(feat)
#            print("\t", newfeat)
    return featmap
