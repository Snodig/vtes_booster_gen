'''
 * Date: 14-12-07
 * Desc: Utility-functions
 * Author: H. N. Skjevling
'''

import os, re, unicodedata

def removeAccents(string):
    nkfdForm = unicodedata.normalize('NFKD', string)
    return u"".join([c for c in nkfdForm if not unicodedata.combining(c)])

#Blood Shadowed Court images are missing!
def getImageFileName(cardDictEntry):
    try:
        retVal = None
        cardName = cardDictEntry["Name"]
        cardName = removeAccents(cardName)
        #Remove any non-word characters [A-Z, 0-9]
        alphaPattern = re.compile(r"\W+", re.UNICODE)
        cardName = re.sub(alphaPattern, "", cardName)

        #Advanced cards have "adv" appended to the image-name
        advanced = cardDictEntry.get("Adv") == "Advanced"
        if advanced:
            cardName += "adv"

        sets = cardDictEntry["Set"].split(", ")
        if(len(sets) > 1):
            sets.reverse()

        #Loop over all set-subfolders
        for setName in sets:

            #Remove annoying subset (":XXX") and promo number
            isolatedSetName = setName.split(":")[0]
            if "Promo" in isolatedSetName:
                isolatedSetName = "Promo"

            filePath = os.getcwd() + "\\Resources\\" + isolatedSetName + "\\" + cardName

            if os.path.exists(filePath + ".jpg"):
                retVal = filePath + ".jpg"
                break
            elif os.path.exists(filePath + ".jpeg"):
                retVal = filePath + ".jpeg"
                break

    except:
        print("Exception caught when handling card:\n" + str(cardDictEntry))
        raise

    finally:
        if retVal == None:
            print("Card image not found: " + str(sets) + "/" + cardName)

        return retVal
