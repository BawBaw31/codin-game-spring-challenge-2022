import sys
import math

# CONSTANTS
base = [int(i) for i in input().split()]
other_base = [17630, 9000] if base == [0, 0] else [0, 0]
heroes_per_player = int(input())
roles = ["def", "def", "attk"]
zones = ([(3000, 4500), (5000, 2000), (13000, 5000)] 
    if base == [0, 0] else [(15000, 4000), (12000, 7000), (5000, 4000)])
speed = [800, 400]
shield_duration = 12
spell_ranges = [1280, 2200]
spell_cost = 10
zone_radius = 9000
danger_health = 15
danger = 6000
mana_goal = 150
mana_minimum = 50

possible_path = ([(2000, 2000), (7500, 1000), (2000, 7000)] 
    if base != [0, 0] else [(17630 - 2000, 9000 - 2000), (17630 - 7500, 9000 - 1000), (17630 - 2000, 9000 - 7000)])
path = possible_path[1]

# VARIABLES
targets = {}
attk_phase = False

# FUNCTIONS
def order(args, order="MOVE", comment=""):
    print(order, " ".join([str(arg) for arg in args]), comment , file=sys.stderr, flush=True)
    print(order, " ".join([str(arg) for arg in args]), comment)

def is_closer_to(foo, bar, chi):
    return math.dist(foo, chi) < math.dist(bar, chi)

def is_targeted(enemy):
    return True if enemy["id"] in targets.values() else False

def is_dangerous(enemy):
    return True if math.dist(enemy["xy"], base) <= danger else False

def shield_myself(hero, mana):
    if not hero["shield"] and mana >= mana_minimum:
        order([hero["id"]], "SPELL SHIELD", "shield me")
        mana -= spell_cost
        return True
    return False

def mess_with_spiders(spider, hero, mana, i):
    if (math.dist(spider["xy+vxy"], hero["xy"]) <= spell_ranges[1] 
    and mana >= mana_minimum and not spider["controlled"]):
        if spider["threat"] != 2:
            order([spider["id"], other_base[0], other_base[1]], "SPELL CONTROL", "go go go")
            mana -= spell_cost
            return True
        elif (math.dist(spider["xy+vxy"], other_base) <= speed[1] * shield_duration
        and not spider["shield"]):
            order([spider["id"]], "SPELL SHIELD", "go go go")
            mana -= spell_cost
            del targets[i]
            return True
    return False

def attk_opps(opps, hero, mana, defend=False):
    direction = base if not defend else other_base
    for opp in opps:
        if (math.dist(opp["xy"], hero["xy"]) < spell_ranges[1] 
        and not opp["controlled"] and mana >= mana_minimum):
            order([opp["id"], direction[0], direction[1]], "SPELL CONTROL", "nashav")
            mana -= spell_cost
            return True
    return False

def find_any_target(enemies, i):
    if i in targets.keys():
        if (targets[i] not in enemies.keys()
        or math.dist(enemies[targets[i]]["xy+vxy"], other_base) > zone_radius):
            del targets[i]
    for enemy in enemies.values():
        if (math.dist(enemy["xy+vxy"], other_base) < zone_radius and not enemy["shield"] 
        and (enemy["threat"] != 2 or enemy["health"] < danger_health)):
            if i in targets.keys():
                if i in targets.keys():
                    actual_target = enemies.get(targets[i])
                    if is_closer_to(enemy["xy+vxy"], actual_target["xy+vxy"], hero["xy"]):
                        targets[i] = enemy["id"]
                else:
                    targets[i] = enemy["id"]
            else:
                targets[i] = enemy["id"]

def find_target(enemies, i):
    if i in targets.keys():
        if (targets[i] not in enemies.keys()
        or math.dist(enemies[targets[i]]["xy+vxy"], base) > zone_radius):
            del targets[i]
    for enemy in enemies.values():
        if (math.dist(enemy["xy"], base) < zone_radius 
        and (not is_targeted(enemy) or is_dangerous(enemy))):
            if i in targets.keys():
                    actual_target = enemies.get(targets[i])

                    if actual_target['in_base'] == 1:
                        if enemy["in_base"] == 1 and is_closer_to(enemy["xy+vxy"], actual_target["xy+vxy"], base):
                            targets[i] = enemy["id"]
                    elif actual_target['threat'] == 1:
                        if (enemy["in_base"] == 1 or (enemy["threat"] == 1
                        and is_closer_to(enemy["xy+vxy"], actual_target["xy+vxy"], base))):
                            targets[i] = enemy["id"]
                    else:
                        if enemy["threat"] == 1 or enemy["in_base"] == 1:
                            targets[i] = enemy["id"]
            else:
                targets[i] = enemy["id"]



# TOUR
while True:
    bros = []
    opps = []
    spiders = {}

    for i in range(2):
        if not i:
            health, mana = [int(j) for j in input().split()]
        else:
            opp_health, opp_mana = [int(j) for j in input().split()]

    entity_count = int(input())
    for i in range(entity_count):
        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]
        stats = {
            "id": _id,
            "xy": (x, y),
            "shield": shield_life,
            "controlled": is_controlled,
            "health": health,
            "vxy": (vx, vy),
            "in_base": near_base,
            "threat": threat_for,
            "xy+vxy": (vx + x, vy + y)
        }

        if _type == 0:
            spiders[_id] = stats
        elif _type == 1:
            bros.append(stats)
        elif _type == 2:
            opps.append(stats)
        
    for i in range(heroes_per_player):
        hero = bros[i]
        # DEF
        if roles[i] == "def":
            # REPOSITION
            if math.dist(base, hero["xy"]) > zone_radius:
                order(zones[i], comment="deep")
            else:
                # if attk_opps(opps, hero, mana, True):
                #     pass
                # else:
                if shield_myself(hero, mana):
                        pass
                else:
                    find_target(spiders, i)
                    if i in targets.keys():
                        target = spiders[targets[i]]
                        if (is_dangerous(target) and not target['shield'] and target["health"] >= danger_health
                        and math.dist(target["xy"], hero["xy"]) < spell_ranges[0]):
                            order(other_base, "SPELL WIND", "nashav")
                            mana -= spell_cost
                        else:
                            order(spiders.get(targets[i])["xy+vxy"], comment="chase")
                    else:
                        order(zones[i], comment="chill")


        # ATTK
        elif roles[i] == "attk":
            # REPOSITION
            if math.dist(other_base, hero["xy"]) > zone_radius:
                order(zones[i], comment="deep")
            else:
                if not attk_phase:
                    find_any_target(spiders, i)
                    if i in targets.keys():
                        order(spiders.get(targets[i])["xy+vxy"], comment="chase")
                    else:
                        order(path, comment="path")
                        for key, p in enumerate(possible_path):
                            print(path, p, key , file=sys.stderr, flush=True)
                            if hero["xy"] == p:
                                print(path, p, key , file=sys.stderr, flush=True)
                                path = possible_path[key + 1] if key != 2 else possible_path[0]
                                break                    
                    if mana >= mana_goal:
                        attk_phase = True
                else:
                    if shield_myself(hero, mana):
                        pass
                    elif attk_opps(opps, hero, mana):
                        pass
                    else:
                        order(possible_path[0], comment="path")

                    if mana <= mana_minimum:
                        attk_phase = False

        # NEVER ???
        else:
            order([], "WAIT", "???")


# print("" , file=sys.stderr, flush=True)