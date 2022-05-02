import sys
import math

base_x, base_y = [int(i) for i in input().split()]
heroes_per_player = int(input())

# SET BASE AND STRATEGIC POINTS
# TODO : REDUCE CODE
if base_x != 0:
    moves = {
        0: "12000 8000",
        1: "16000 7000",
        2: "16000 3000",
    }
    other_base_x = 200
    other_base_y = 200
else:
    moves = {
        0: "6000 900",
        1: "2000 2000",
        2: "2000 5500",
    }
    other_base_x = 17630
    other_base_y = 9000

spell_ranges = [1280, 2200]
spell_cost = 10
danger_dist = 3000
dangerous_monster_health = 20
# TODO : MAYBE USE ARRAYS INSTEAD OF DICTS
targets = {}

# TOUR
while True:

    # SET ENTITIES + TEAM STATS
    # TODO : MAYBE USE ARRAYS INSTEAD OF DICTS
    team_infos = {}
    opp_team_infos = {}
    heroes = {}
    monsters = {}
    opponents = {}
    for i in range(2):
        health, mana = [int(j) for j in input().split()]
        stats = {
                'health': health,
                'mana': mana
            }
        if i == 0: team_infos = stats
        else: opp_team_infos = stats

    entity_count = int(input())
    for i in range(entity_count):
        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in input().split()]
        stats = {
                "id": _id,
                "type": _type,
                "x": x,
                "y": y,
                "shield_life": shield_life,
                "is_controlled": is_controlled,
                "health": health,
                "vx": vx,
                "vy": vy,
                "near_base": near_base,
                "threat_for": threat_for
            }
        # TODO : REDUCE CODE
        if (_type == 1):
            if base_x != 0:
                heroes[_id - 3] = stats
            else:
                heroes[_id] = stats
        if (_type == 0):
            monsters[_id] = stats
        if (_type == 2):
            opponents[_id] = stats

    for i in range(heroes_per_player):
        hero = heroes[i]

        # HERO HAS A TARGET
        if i in targets:

            # TARGET STILL ALIVE
            if targets[i] in monsters and monsters[targets[i]]['threat_for'] == 1:
                monster = monsters[targets[i]]

                # SHIELD
                if monster["threat_for"] != 1 and math.dist([hero["x"], hero["y"]],[monster["x"], monster["y"]]) <= spell_ranges[1] and not monster["shield_life"]:
                    print("SPELL SHIELD " + str(monster["id"]) + " shield")
                    del targets[i]

                # USE OFFENSIVE SPELL
                elif team_infos["mana"] >= spell_cost and not monster["shield_life"]:
                    # WIND
                    if math.dist([monster["x"], monster["y"]], [base_x, base_y]) <= danger_dist and math.dist([hero["x"], hero["y"]],[monster["x"], monster["y"]]) <= spell_ranges[0]:
                        print("SPELL WIND " + str(other_base_x) + " " + str(other_base_y) + " wind")
                        team_infos["mana"] -= spell_cost
                    # CONTROL
                    elif team_infos["mana"] >= 4*spell_cost and math.dist([hero["x"], hero["y"]],[monster["x"], monster["y"]]) <= spell_ranges[1] and monster["near_base"] == 0:
                        print("SPELL CONTROL " + str(monster["id"]) + " " + str(other_base_x) + " " + str(other_base_y) + " control")
                        team_infos["mana"] -= spell_cost
                    # CHASE
                    else: print("MOVE " + str(monster["x"] + monster["vx"]) + " " + str(monster["y"] + monster["vy"]) + " chasing")

                # CHASE
                else: print("MOVE " + str(monster["x"] + monster["vx"]) + " " + str(monster["y"] + monster["vy"]) + " chasing")

            # TARGET IS DEAD
            else:
                del targets[i]
                if str(hero["x"]) + " " + str(hero["y"]) != moves[i]:
                    print("MOVE " + moves[i] + " replacing")
                else: print("WAIT waiting")

        # HERO DOESN'T HAVE TARGET
        else:

            # NO MONSTERS IN RANGE
            if not monsters:
                print("MOVE " + moves[i] + " starting")

            # MONSTERS ARE IN RANGE
            else:
                target_is_set = False

                # STILL WITHOUT TARGET
                if not target_is_set:
                    for n in monsters:
                        if monsters[n]["threat_for"] == 1:
                            monster_x = monsters[n]["x"]
                            monster_y = monsters[n]["y"]
                            monster_x_target = monsters[n]["x"] + monsters[n]["vx"]
                            monster_y_target = monsters[n]["y"] + monsters[n]["vy"]

                            if not target_is_set:
                                targets[i] = n
                                target_is_set = True

                            else:
                                # MONSTER ISN'T DANGEROUS
                                #if monsters[n]["health"] < dangerous_monster_health:
                                #    if n not in targets.values():
                                #        if math.dist([base_x, base_y], [monster_x, monster_y]) < math.dist([base_x, base_y], [monsters[targets[i]]["x"], monsters[targets[i]]["y"]]):
                                #            targets[i] = n

                                # MONSTER IS DANGEROUS
                                # else:
                                if math.dist([base_x, base_y], [monster_x, monster_y]) < math.dist([base_x, base_y], [monsters[targets[i]]["x"], monsters[targets[i]]["y"]]):
                                        targets[i] = n

                # HAVE TARGET
                if target_is_set:
                    print("MOVE " + str(monsters[targets[i]]["x"]) + " " + str(monsters[targets[i]]["y"]) + " starting to chase")
                # STILL WITHOUT TARGET
                else:
                    print("MOVE " + moves[i] + " default")





# print("" , file=sys.stderr, flush=True)