import re

DELETE = "--DELETE--"
HIGHLIGHT1 = "--HIGHLIGHT1--"
HIGHLIGHT2 = "--HIGHLIGHT2--"

def construct_UD_generic(pos_by_feats):
    findnumber = re.compile(r"(number=\w+)")
    featmap = {}
    for feats, poss in pos_by_feats.items():
        newfeats = ""
        if "noun" in poss and "verb" not in poss:
            featmap[feats] = newfeats
        elif "verb" in poss and "noun" not in poss:
            featmap[feats] = newfeats

    print(len(set(featmap.values())),set(featmap.values()))
    for feat, newfeat in featmap.items():
        if feat.count("|") != newfeat.count("|"):
            print(feat)
            print("\t", newfeat)
    exit()


def construct_UD_Arabic(pos_by_feats):
    findnumber = re.compile(r"(number=\w+)")
    findcase = re.compile(r"(case=\w+)")
    findgender = re.compile(r"(gender=\w+)")
    findverbform = re.compile(r"(verbform=(\w+))")
    findprontype = re.compile(r"(prontype=\w+)")
    findverbform = re.compile(r"(verbform=(\w+))")
    findvoice = re.compile(r"(voice=\w+)")
    findperson = re.compile(r"(person=\d)")
    findmood = re.compile(r"(mood=\w+)")
    findtense = re.compile(r"(tense=\w+)")
    findaspect = re.compile(r"(aspect=\w+)")
    findsubcat = re.compile(r"(subcat=\w+)")
    findpolarity = re.compile(r"(polarity=\w+)")
    finddefinite = re.compile(r"(definite=\w+)")
#    findstyle = re.compile(r"(style=\w+)")
#    findtypo = re.compile(r"(typo=\w+)")
#    findabbr = re.compile(r"(abbr=\w+)")
    featmap = {}
    for feats, poss in pos_by_feats.items():
        newfeats = ""
        if "noun" in poss and "verb" not in poss:
            featmap[feats] = newfeats
        elif "verb" in poss and "noun" not in poss:
            number = findnumber.search(feats)
            verbform = findverbform.search(feats)
            voice = findvoice.search(feats)
            case = findcase.search(feats)
            gender = findgender.search(feats)
            prontype = findprontype.search(feats)
            person = findperson.search(feats)
            mood = findmood.search(feats)
            tense = findtense.search(feats)
            aspect = findaspect.search(feats)
            polarity = findpolarity.search(feats)
            definite = finddefinite.search(feats)
#            style = findstyle.search(feats)
#            typo = findtypo.search(feats)
#            abbr = findabbr.search(feats)
            if number:
                newfeats += "|" + number.group(0)
            if gender:
                newfeats += "|" + gender.group(0)
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
            
            if verbform and "=fin" in verbform.group(0):
                if not number:
                    newfeats = "NO NUMBER!!!!!!!!!!!!!!!!!"
#                    newfeats = DELETE
                if not voice:
                    if mood and "=imp" not in mood.group(0):
#                        newfeats = "NO VOICE!!!!!!!!!!!!!!!!!"
                        newfeats = DELETE
                if not person:
                    if mood and "=imp" not in mood.group(0):
#                    newfeats = "NO PERSON!!!!!!!!!!!!!!!!!"
                        newfeats = DELETE
                if not tense and not aspect:
                    if mood and "=imp" not in mood.group(0):
#                    newfeats = "NO TENSE OR ASPECT!!!!!!!!!!!!!!!!!"
                        newfeats = DELETE
                if not mood:
                    newfeats = "NO MOOD!!!!!!!!!!!!!!!!!"
#                    newfeats = DELETE
#                    newfeats = DELETE
#                if not polarity:
#                    newfeats = "NO POLARITY!!!!!!!!!!!!!!!!!"
#                    newfeats = DELETE

            if case:
                newfeats = DELETE
            if definite:
                newfeats = DELETE
#            if style:
#                newfeats = DELETE
#            if typo:
#                newfeats = DELETE
#            if abbr:
#                newfeats = DELETE
#            if connegative:
#                newfeats = DELETE

            if newfeats[0] == "|":
                newfeats = newfeats[1:]
            featmap[feats] = newfeats

#    print(len(set(featmap.values())),set(featmap.values()))
#    for feat, newfeat in featmap.items():
#        if newfeat:
#            if feat.count("|") != newfeat.count("|") and newfeat != DELETE:
#                print(feat.strip())
#                print("\t", newfeat.strip())
#    exit()
    return featmap




def construct_UD_Armenian(pos_by_feats):
    findnumber = re.compile(r"(number=\w+)")
    findcase = re.compile(r"(case=\w+)")
    findverbform = re.compile(r"(verbform=(\w+))")
    findprontype = re.compile(r"(prontype=\w+)")
    findverbform = re.compile(r"(verbform=(\w+))")
    findvoice = re.compile(r"(voice=\w+)")
    findperson = re.compile(r"(person=\d)")
    findmood = re.compile(r"(mood=\w+)")
    findtense = re.compile(r"(tense=\w+)")
    findaspect = re.compile(r"(aspect=\w+)")
    findsubcat = re.compile(r"(subcat=\w+)")
    findpolarity = re.compile(r"(polarity=\w+)")
    findstyle = re.compile(r"(style=\w+)")
    findtypo = re.compile(r"(typo=\w+)")
    findabbr = re.compile(r"(abbr=\w+)")
    findconnegative = re.compile(r"(connegative=\w+)")
    featmap = {}
    for feats, poss in pos_by_feats.items():
        newfeats = ""
        if "noun" in poss and "verb" not in poss:
            featmap[feats] = newfeats
        elif "verb" in poss and "noun" not in poss:
            number = findnumber.search(feats)
            verbform = findverbform.search(feats)
            voice = findvoice.search(feats)
            case = findcase.search(feats)
            prontype = findprontype.search(feats)
            person = findperson.search(feats)
            mood = findmood.search(feats)
            tense = findtense.search(feats)
            aspect = findaspect.search(feats)
            subcat = findsubcat.search(feats)
            polarity = findpolarity.search(feats)
            style = findstyle.search(feats)
            typo = findtypo.search(feats)
            abbr = findabbr.search(feats)
            connegative = findconnegative.search(feats)
            if number:
                newfeats += "|" + number.group(0)
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
            if subcat:
                newfeats += "|" + subcat.group(0)
            if polarity:
                newfeats += "|" + polarity.group(0)
            
            if verbform and "=fin" in verbform.group(0):
                if not number:
                    newfeats = "NO NUMBER!!!!!!!!!!!!!!!!!"
                    newfeats = DELETE
                if not voice:
                    newfeats = "NO VOICE!!!!!!!!!!!!!!!!!"
                    newfeats = DELETE
                if not person:
                    newfeats = "NO PERSON!!!!!!!!!!!!!!!!!"
                    newfeats = DELETE
                if not tense or not aspect:
                    if voice.group(0) != "=mid":
                        newfeats = "NO TENSE OR ASPECT!!!!!!!!!!!!!!!!!"
                        newfeats = DELETE
                if not mood:
                    newfeats = "NO MOOD!!!!!!!!!!!!!!!!!"
                    newfeats = DELETE
                if not subcat:
                    newfeats = "NO SUBCAT!!!!!!!!!!!!!!!!!"
                    newfeats = DELETE
                if not polarity:
                    newfeats = "NO POLARITY!!!!!!!!!!!!!!!!!"
                    newfeats = DELETE
 
            if case:
                newfeats = DELETE
            if style:
                newfeats = DELETE
            if typo:
                newfeats = DELETE
            if abbr:
                newfeats = DELETE
            if connegative:
                newfeats = DELETE

            if newfeats[0] == "|":
                newfeats = newfeats[1:]
            featmap[feats] = newfeats

#    print(len(set(featmap.values())),set(featmap.values()))
#    for feat, newfeat in featmap.items():
#        if newfeat:
#            if feat.count("|") != newfeat.count("|") and newfeat != DELETE:
#                print(feat.strip())
#                print("\t", newfeat.strip())
    return(featmap)



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
        if "noun" in poss and "verb" not in poss:
            number = findnumber.search(feats)
            case = findcase.search(feats)
            if number and case:
                newfeats = number.group(0) + "|" + case.group(0)
            else:
                newfeats=DELETE
            featmap[feats] = newfeats
        elif "verb" in poss and "noun" not in poss:
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
        if "noun" in poss and "verb" not in poss:
            number = findnumber.search(feats)
            case = findcase.search(feats)
            if number and case:
                newfeats = number.group(0) + "|" + case.group(0)
            else:
                newfeats=DELETE
            featmap[feats] = newfeats
        elif "verb" in poss and "noun" not in poss:
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
                if not verbform and not number:
                    newfeats = DELETE
            if mood:
                newfeats += "|" + mood.group(0)
            if not case:
                if number:
                    newfeats += "|" + number.group(0)
                if not number and verbform and verbform.group(2) == "fin":
                    newfeats = DELETE
            if prontype:
                newfeats = DELETE
        
            if "person=3" in newfeats and "number=sing" in newfeats and ("tense=past" in newfeats) and "mood=ind" in feats and "voice=pass" not in feats:
#                print("HIGHLIGHT", newfeats)
                newfeats += "|" + HIGHLIGHT1
            elif "verbform=part" in feats and "tense=past" in feats and "voice=act" not in feats:
                newfeats += "|" + HIGHLIGHT1
            elif "tense=past" in newfeats:
                newfeats += "|" + HIGHLIGHT2


            if newfeats[0] == "|":
                newfeats = newfeats[1:]
            featmap[feats] = newfeats

#    print(len(set(featmap.values())),set(featmap.values()))
#    for feat, newfeat in featmap.items():
#        if feat.count("|") != newfeat.count("|"):
#            print(feat)
#            print("\t", newfeat)
    return(featmap)


def construct_UD_Gothic(pos_by_feats):
    findnumber = re.compile(r"(number=\w+)")
    findcase = re.compile(r"(case=\w+)")
    findprontype = re.compile(r"(prontype=\w+)")
    findverbform = re.compile(r"(verbform=(\w+))")
    findvoice = re.compile(r"(voice=\w+)")
    findperson = re.compile(r"(person=\d)")
    findaspect = re.compile(r"(aspect=\w+)")
    findmood = re.compile(r"(mood=\w+)")
    findtense = re.compile(r"(tense=\w+)")
    featmap = {}
    for feats, poss in pos_by_feats.items():
        newfeats = ""
        if "noun" in poss and "verb" not in poss:
            number = findnumber.search(feats)
            case = findcase.search(feats)
            if number and case:
                newfeats = number.group(0) + "|" + case.group(0)
            else:
                newfeats=DELETE
            featmap[feats] = newfeats
        elif "verb" in poss and "noun" not in poss:
            number = findnumber.search(feats)
            case = findcase.search(feats)
            verbform = findverbform.search(feats)
            voice = findvoice.search(feats)
            prontype = findprontype.search(feats)
            person = findperson.search(feats)
            aspect = findaspect.search(feats)
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
#            if aspect:
#                newfeats += "|" + aspect.group(0)
            if not case:
                if number:
                    newfeats += "|" + number.group(0)
                if not number and verbform and verbform.group(2) == "fin":
                    newfeats = DELETE
            if prontype:
                newfeats = DELETE
        
            if "person=3" in newfeats and "number=sing" in newfeats and ("tense=past" in newfeats) and "voice=act" in newfeats and "mood=sub" not in newfeats and "mood=imp" not in newfeats and "mood=opt" not in newfeats:
                newfeats += "|" + HIGHLIGHT1
            elif "verbform=part" in feats and "tense=past" in feats and "voice=act" not in feats:
                newfeats += "|" + HIGHLIGHT1
            elif "tense=past" in newfeats:
                newfeats += "|" + HIGHLIGHT2
                
            if newfeats[0] == "|":
                newfeats = newfeats[1:]
            featmap[feats] = newfeats

#    print(len(set(featmap.values())),set(featmap.values()))
#    for feat, newfeat in featmap.items():
#        if feat.count("|") != newfeat.count("|"):
#            print(feat)
#            print("\t", newfeat)
#    exit()
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
                if "verb" in poss:
                    newfeats = DELETE
            elif "number=plur" in feats and "tense=" not in feats and "verform=" not in feats:
                newfeats = "pl"
                if "verb" in poss:
                    newfeats = DELETE

            if newfeats == feats:
                newfeats = DELETE
            featmap[feats] = newfeats

#    print(len(set(featmap.keys())),len(set(featmap.values())),set(featmap.values()))
#    for feat, newfeat in featmap.items():
#        if feat.count("|") != newfeat.count("|"):
#            print(feat)
#            print("\t", newfeat)
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
        if "noun" in poss and "verb" not in poss:
            number = findnumber.search(feats)
            case = findcase.search(feats)
            if number and case:
                newfeats = number.group(0) + "|" + case.group(0)
            else:
                continue
            featmap[feats] = newfeats
        elif "verb" in poss and "noun" not in poss:
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


def construct_UD_Hungarian(pos_by_feats):
    findnumber = re.compile(r"(number=\w+)")
    findcase = re.compile(r"(case=\w+)")
    findverbform = re.compile(r"(verbform=(\w+))")
    findprontype = re.compile(r"(prontype=\w+)")
    findverbform = re.compile(r"(verbform=(\w+))")
    findvoice = re.compile(r"(voice=\w+)")
    findperson = re.compile(r"(person=\d)")
    findmood = re.compile(r"(mood=\w+)")
    findtense = re.compile(r"(tense=\w+)")
    findaspect = re.compile(r"(aspect=\w+)")
    findsubcat = re.compile(r"(subcat=\w+)")
    findpolarity = re.compile(r"(polarity=\w+)")
    findstyle = re.compile(r"(style=\w+)")
    findtypo = re.compile(r"(typo=\w+)")
    findabbr = re.compile(r"(abbr=\w+)")
    finddefinite = re.compile(r"(definite=\w+)")
    findconnegative = re.compile(r"(connegative=\w+)")
    featmap = {}
    for feats, poss in pos_by_feats.items():
        newfeats = ""
        if "noun" in poss and "verb" not in poss:
            featmap[feats] = newfeats
        elif "verb" in poss and "noun" not in poss:
            number = findnumber.search(feats)
            verbform = findverbform.search(feats)
            voice = findvoice.search(feats)
            case = findcase.search(feats)
            prontype = findprontype.search(feats)
            person = findperson.search(feats)
            mood = findmood.search(feats)
            tense = findtense.search(feats)
            aspect = findaspect.search(feats)
            subcat = findsubcat.search(feats)
            polarity = findpolarity.search(feats)
            style = findstyle.search(feats)
            typo = findtypo.search(feats)
            abbr = findabbr.search(feats)
            definite = finddefinite.search(feats)
            connegative = findconnegative.search(feats)
            if number:
                newfeats += "|" + number.group(0)
            if definite:
                newfeats += "|" + definite.group(0)
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
            if subcat:
                newfeats += "|" + subcat.group(0)
            if polarity:
                newfeats += "|" + polarity.group(0)
            
            if case:
                newfeats = DELETE
            if style:
                newfeats = DELETE
            if typo:
                newfeats = DELETE
            if abbr:
                newfeats = DELETE
            if connegative:
                newfeats = DELETE

            if newfeats[0] == "|":
                newfeats = newfeats[1:]
            featmap[feats] = newfeats

#    print(len(set(featmap.values())),set(featmap.values()))
#    for feat, newfeat in featmap.items():
#        if newfeat:
#            if feat.count("|") != newfeat.count("|"):
#                print(feat.strip())
#                print("\t", newfeat.strip())
#    exit()
    return(featmap)



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
        if "noun" in poss and "verb" not in poss:
            number = findnumber.search(feats)
            case = findcase.search(feats)
            if number and case:
                newfeats = number.group(0) + "|" + case.group(0)
            else:
                newfeats=DELETE
            featmap[feats] = newfeats
        elif "verb" in poss and "noun" not in poss:
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
#                        print(feats)
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


def construct_UD_Portuguese(pos_by_feats):
    findnumber = re.compile(r"(number=(plur|sing))")
    findverbform = re.compile(r"(verbform=(\w+))")
    findperson = re.compile(r"(person=\d)")
    findmood = re.compile(r"(mood=\w+)")
    findvoice = re.compile(r"(voice=\w+)")
    findgender = re.compile(r"(gender=\d)")
    findtense = re.compile(r"(tense=\w+)")

    featmap = {}
    for feats, poss in pos_by_feats.items():
        newfeats = ""
        if "_" in feats:
            print("EMPTY")
            newfeats = DELETE

        if "verb" in poss:
            number = findnumber.search(feats)
            verbform = findverbform.search(feats)
            person = findperson.search(feats)
            mood = findmood.search(feats)
            gender = findgender.search(feats)
            voice = findvoice.search(feats)
            tense = findtense.search(feats)
            if verbform:
                newfeats = verbform.group(0)
                if not gender and not verbform.group(2) == "part":
                    if number:
                        newfeats += "|" + number.group(0)
                if person:
                    newfeats += "|" + person.group(0)
                if voice:
                    newfeats += "|" + voice.group(0)
                if mood:
                    newfeats += "|" + mood.group(0)
                if tense:
                    newfeats += "|" + tense.group(0)
                if verbform.group(2) == "fin":
                    if not person or not number or not mood or not tense:
                        newfeats = DELETE
                    if gender:
                        newfeats = DELETE
                if verbform.group(2) != "fin":
                    newfeats = DELETE
            else:
                newfeats = DELETE    


#            print(feats, "\t", newfeats, verbform.group(2))
            featmap[feats] = newfeats
#    print(len(set(featmap.values())),set(featmap.values()))    
#    for feat, newfeat in featmap.items():
#        if feat.count("|") != newfeat.count("|"):
#            print(feat)
#            print("\t", newfeat)
#    exit()
    return featmap


def construct_UD_Russian(pos_by_feats):
    findnumber = re.compile(r"(number=\w+)")
    findcase = re.compile(r"(case=\w+)")
    findgender = re.compile(r"(gender=\w+)")
    findverbform = re.compile(r"(verbform=(\w+))")
    findprontype = re.compile(r"(prontype=\w+)")
    findverbform = re.compile(r"(verbform=(\w+))")
    findvoice = re.compile(r"(voice=\w+)")
    findperson = re.compile(r"(person=\d)")
    findmood = re.compile(r"(mood=\w+)")
    findtense = re.compile(r"(tense=\w+)")
    findaspect = re.compile(r"(aspect=\w+)")
    findstyle = re.compile(r"(style=\w+)")
    findtypo = re.compile(r"(typo=\w+)")
    findabbr = re.compile(r"(abbr=\w+)")
    finddegree = re.compile(r"(degree=\w+)")
    findvariant = re.compile(r"(variant=\w+)")
    featmap = {}
    for feats, poss in pos_by_feats.items():
        newfeats = ""
        if "noun" in poss and "verb" not in poss:
            featmap[feats] = newfeats
        elif "verb" in poss and "noun" not in poss:
            number = findnumber.search(feats)
            verbform = findverbform.search(feats)
            voice = findvoice.search(feats)
            case = findcase.search(feats)
            gender = findgender.search(feats)
            prontype = findprontype.search(feats)
            person = findperson.search(feats)
            mood = findmood.search(feats)
            tense = findtense.search(feats)
            aspect = findaspect.search(feats)
            style = findstyle.search(feats)
            typo = findtypo.search(feats)
            abbr = findabbr.search(feats)
            degree = finddegree.search(feats)
            variant = findvariant.search(feats)
            if number:
                newfeats += "|" + number.group(0)
            if verbform:
                newfeats += "|" + verbform.group(0)
            if gender:
                newfeats += "|" + gender.group(0)
            if person:
                newfeats += "|" + person.group(0)
            if tense:
                newfeats += "|" + tense.group(0)
            if mood:
                newfeats += "|" + mood.group(0)
                if "=ind" in mood.group(0):
                    if not voice:
                        newfeats += "|voice=act"
            if voice:
                if verbform and "=inf" not in verbform.group(0) and "=conv" not in verbform.group(0):
                    newfeats += "|" + voice.group(0)
            if aspect:
                if verbform and "=inf" not in verbform.group(0):
                    newfeats += "|" + aspect.group(0)
            
            if verbform and "=fin" in verbform.group(0):
                if not number:
                    newfeats = "NO NUMBER!!!!!!!!!!!!!!!!!"
                    #newfeats = DELETE
#                if not voice:
#                    newfeats = "NO VOICE!!!!!!!!!!!!!!!!!"
#                    #newfeats = DELETE
                if not person:
                    if "=imp" not in aspect.group(0):
                        newfeats = "NO PERSON!!!!!!!!!!!!!!!!!"
                        newfeats = DELETE
#                if not tense and not aspect:
#                    newfeats = "NO TENSE OR ASPECT!!!!!!!!!!!!!!!!!"
#                    #newfeats = DELETE
#                if not mood:
#                    newfeats = "NO MOOD!!!!!!!!!!!!!!!!!"
#                    #newfeats = DELETE
 
            if verbform and "=conv" in verbform.group(0) and not tense:
                newfeats = DELETE
            if not verbform:
                newfeats = DELETE
            if case:
                newfeats = DELETE
            if degree:
                newfeats = DELETE
            if variant:
                newfeats = DELETE
#            if style:
#                newfeats = DELETE
#            if typo:
#                newfeats = DELETE
#            if abbr:
#                newfeats = DELETE

#            print(feats, newfeats)
            if newfeats[0] == "|":
                newfeats = newfeats[1:]
            featmap[feats] = newfeats

#    print(len(set(featmap.values())),set(featmap.values()))
#    for feat, newfeat in featmap.items():
#        if newfeat:
#            if feat.count("|") != newfeat.count("|") and newfeat != DELETE:
#                print(feat.strip())
#                print("\t", newfeat.strip())
#    exit()
    return(featmap)



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
        if "noun" in poss and "verb" not in poss:
            number = findnumber.search(feats)
            if not number:
                newfeats = DELETE
            else:
                newfeats = number.group(0)
            featmap[feats] = newfeats
        elif "verb" in poss and "noun" not in poss:
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
                if verbform.group(2) != "fin":
                    newfeats = DELETE
            else:
                newfeats = DELETE    

#            print(feats, "\t", newfeats, verbform.group(2))
            featmap[feats] = newfeats
#    print(len(set(featmap.values())),set(featmap.values()))    
#    for feat, newfeat in featmap.items():
#        if feat.count("|") != newfeat.count("|"):
#            print(feat)
#            print("\t", newfeat)
    return featmap


def construct_UD_Tagalog(pos_by_feats):
    findnumber = re.compile(r"(number=\w+)")
    findforeign = re.compile(r"(foreign=\w+)")
    findaspect = re.compile(r"(aspect=\w+)")
    findtense = re.compile(r"(tense=\w+)")
    findverbform = re.compile(r"(verbform=\w+)")
    findmood = re.compile(r"(mood=\w+)")
    featmap = {}
    for feats, poss in pos_by_feats.items():
        newfeats = ""
        if "verb" in poss and "noun" not in poss:
            foreign = findforeign.search(feats)
            verbform = findverbform.search(feats)
            aspect = findaspect.search(feats)
            tense = findtense.search(feats)
            mood = findmood.search(feats)
            if tense:
                newfeats += "|" + tense.group(0)
            if verbform:
                newfeats += "|" + verbform.group(0)
            if aspect:
                newfeats += "|" + aspect.group(0)
            if mood:
                newfeats += "|" + mood.group(0)


            if foreign:
                newfeats = DELETE

            print(feats, newfeats)
            if newfeats[0] == "|":
                newfeats = newfeats[1:]
            featmap[feats] = newfeats


#    print(len(set(featmap.values())),set(featmap.values()))
#    for feat, newfeat in featmap.items():
#        if feat.count("|") != newfeat.count("|"):
#            print(feat)
#            print("\t", newfeat)
#    exit()
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
    findtense = re.compile(r"(tense=\w+)")
    featmap = {}
    for feats, poss in pos_by_feats.items():
        newfeats = ""
        if "noun" in poss and "verb" not in poss:
            number = findnumber.search(feats)
            case = findcase.search(feats)
            if number and case:
                newfeats = number.group(0) + "|" + case.group(0)
            else:
                newfeats=DELETE
            featmap[feats] = newfeats
        elif "verb" in poss and "noun" not in poss:
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
            tense = findtense.search(feats)
            if verbform:
                newfeats += verbform.group(0)
                if "vnoun" in verbform.group(0):
                    newfeats = DELETE
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
            if aspect:
                newfeats += "|" + aspect.group(0)
            if not case:
                if number:
                    newfeats += "|" + number.group(0)
            
            if newfeats[0] == "|":
                newfeats = newfeats[1:]
            featmap[feats] = newfeats

#    print(len(set(featmap.keys())),len(set(featmap.values())),set(featmap.values()))
#    for feat, newfeat in featmap.items():
#        if feat.count("|") != newfeat.count("|"):
#            print(feat)
#            print("\t", newfeat)
    return featmap
