#! python3

'''
 * Date: 22-08-21
 * Desc: Booster Generator for V:TES.
 * Generates N boosters, with appropriate rarity distributions, from a given set.
 * Any preconstructed cards are processed as either V rarity for crypt or U rarity for library.
 * Author: H. Skjevling
'''

import sys, time, traceback, datetime
import threading, random

import parser

mutex = threading.Lock()

#Scary multithreaded test-code
class InputThread(threading.Thread):
    def __init__(self, parser):
        self.parser = parser
        threading.Thread.__init__(self, daemon=True)

    def run(self):
        try:
            while(1):
                card = input(">")
                if not card == "":
                    print("\nLoading test-card, " + card + ":\n")
                    self.loadCard(card)
                card = ""
        except KeyboardInterrupt:
            pass

    def loadCard(self, cardName): #Volatile test-code
        try:
            mutex.acquire()
            card = self.parser.getCard(cardName)
            if card == None:
                return
            if "Abbrev" in card.keys():
                return
            addDrawable(drawableCard)
        finally:
            mutex.release()

def getRandom(cards, rarity):
    if int(rarity) > len(cards):
        return None
    return random.choices(cards, k=int(rarity))

def main():
    try:
        t0 = time.localtime()
        random.seed()
        p = parser.CardListCsvParser()

        sets = p.parseSets()
        if len(sys.argv) != 3:
            print("Please pass a valid set as argv[1] and number of boosters as argv[2].\nValid sets are:\n")
            for set_name in sets.keys():
                print(set_name + " (" + sets[set_name]["Full Name"] + ")")
            return
        else:
            for set_name in sets.keys():
                if set_name.lower() == sys.argv[1].lower():
                    desired_set = sets[set_name]["Abbrev"]
            num_boosters = sys.argv[2]

        c_commons = list()
        c_vampires = list()
        c_uncommons = list()
        c_rares = list()
        c_preconstructed = list()

        crypt = p.parseCrypt()
        set_crypt = dict()
        for card_name in crypt.keys():
            card = crypt[card_name]
            card_sets = card["Set"].split(", ")
            for card_set in card_sets:
                set_split = card_set.split(":")
                if set_split[0].lower() == desired_set.lower():
                    set_crypt[card_name] = card
                    if len(set_split) > 1:
                        rarities = set_split[1].split("/")
                    else:
                        rarities = set_split[1][0]

                    for rarity in rarities:
                        if rarity[0] == "C":
                            c_commons.append(card_name)
                            break
                        elif rarity[0] == "V":
                            c_vampires.append(card_name)
                            break
                        elif rarity[0] == "U":
                            c_uncommons.append(card_name)
                            break
                        elif rarity[0] == "R":
                            c_rares.append(card_name)
                            break
                        elif rarity[0] == "X": # BSC
                            c_vampires.append(card_name)
                            break
                        elif rarity[0] == "P":
                            if not card_name in c_vampires + c_commons + c_uncommons + c_rares + c_preconstructed:
                                c_preconstructed.append(card_name)
                                break
                        else:
                            print(card_name + " was " + rarity + " (" + str(set_split) + ")")
                            if not card_name in c_vampires and not card_name in c_preconstructed:
                                c_preconstructed.append(card_name)
                    break

        l_commons = list()
        l_vampires = list()
        l_uncommons = list()
        l_rares = list()
        l_preconstructed = list()

        library = p.parseLibrary()
        set_library = dict()
        for card_name in library.keys():
            card = library[card_name]
            card_sets = card["Set"].split(", ")
            for card_set in card_sets:
                set_split = card_set.split(":")
                if set_split[0].lower() == desired_set.lower():
                    set_library[card_name] = card
                    if len(set_split) > 1:
                        rarities = set_split[1].split("/")
                    else:
                        rarities = set_split[1][0]
                    for rarity in rarities:
                        if rarity[0] == "C":
                            l_commons.append(card_name)
                            break
                        elif rarity[0] == "V":
                            l_vampires.append(card_name)
                            break
                        elif rarity[0] == "U":
                            l_uncommons.append(card_name)
                            break
                        elif rarity[0] == "R":
                            l_rares.append(card_name)
                            break
                        elif rarity[0] == "P":
                            l_preconstructed.append(card_name)
                            break
                        else:
                            print(card_name + " was " + rarity + " (" + str(set_split) + ")")
                            if card_name in l_commons + l_uncommons + l_rares + l_preconstructed:
                                break

                            while not rarity[0].isnumeric() and len(rarity) > 1:
                                rarity = rarity[1:]
                            if rarity == "1":
                                l_rares.append(card_name)
                            elif rarity == "2":
                                l_uncommons.append(card_name)
                            else:
                                l_commons.append(card_name)
                            break
                        # Note that some cards are "POD:DTC" rarity, but we ignore them
                    break

        print("Crypt cards from " + sets[desired_set]["Full Name"] + " (" + str(len(set_crypt)) + "):")
        print(str(len(c_vampires)) + " vampires")
        print(str(len(c_commons)) + " commons")
        print(str(len(c_uncommons)) + " uncommons")
        print(str(len(c_rares)) + " rares")
        print(str(len(c_preconstructed)) + " preconstructed only")
        print("Library cards from " + sets[desired_set]["Full Name"] + " (" + str(len(set_library)) + "):")
        print(str(len(l_vampires)) + " vampires")
        print(str(len(l_commons)) + " commons")
        print(str(len(l_uncommons)) + " uncommons")
        print(str(len(l_rares)) + " rares")
        print(str(len(l_preconstructed)) + " preconstructed only")
        print()

        all_vampires = c_vampires
        all_commons = c_commons + l_commons
        all_uncommons = c_uncommons + l_uncommons
        all_rares = c_rares + l_rares

        distributions = p.parseBoosterDistribution()

        if desired_set not in distributions:
            print("No booster distribution defined for this set.")
            return

        num_c = distributions[desired_set]["C"]
        num_v = distributions[desired_set]["V"]
        num_u = distributions[desired_set]["U"]
        num_r = distributions[desired_set]["R"]

        print("Boosters are: " + str(distributions[desired_set]))

        # We process Preconstructed library cards as U
        all_uncommons += l_preconstructed
        # We process Preconstructed library cards as V (or U if there is no V rarity in the set)
        if(num_v == 0):
            all_uncommons += c_preconstructed
        else:
            all_vampires += c_preconstructed

        all_cards = dict()

        for i in range(0, int(num_boosters)):
            print()
            booster_c = getRandom(all_commons, num_c)
            booster_v = getRandom(all_vampires, num_v)
            booster_u = getRandom(all_uncommons, num_u)
            booster_r = getRandom(all_rares, num_r)
            print("Booster #" + str(i+1) + ":")
            print("Vampires:\t" + str(booster_v))
            print("Commons:\t" + str(booster_c))
            print("Uncommons:\t" + str(booster_u))
            print("Rares:\t\t" + str(booster_r))

            for card in booster_c:
                current = 0
                if card in all_cards:
                    current = all_cards[card]
                all_cards.update({card : current + 1})
            for card in booster_v:
                current = 0
                if card in all_cards:
                    current = all_cards[card]
                all_cards.update({card : current + 1})
            for card in booster_u:
                current = 0
                if card in all_cards:
                    current = all_cards[card]
                all_cards.update({card : current + 1})
            for card in booster_r:
                current = 0
                if card in all_cards:
                    current = all_cards[card]
                all_cards.update({card : current + 1})

        file = open("import.txt", "w")
        print("\nAll cards:")
        for k in all_cards.keys():
            print(str(all_cards[k]) + "x " + k)
            file.write(str(all_cards[k]) + "x " + k + "\n")
        file.close()

    except KeyboardInterrupt:
        print("\n-- Ctrl^C ---")

    except:
        print()
        traceback.print_exc()

    finally:
        print("\nTime is now\t", time.strftime("%H:%M:%S"))
        totalTime = time.mktime(time.localtime()) - time.mktime(t0)
        print("Running since\t", time.strftime("%H:%M:%S", t0), "(", totalTime, "seconds )")

if __name__ == "__main__":
    exit(main())
