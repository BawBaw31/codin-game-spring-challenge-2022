## Règles

- tour par tour
- 3 vies : si un monstre arrive à la base il en enlève une
- 3 héros par joueur :
    - 800 unités max par tour
    - infligent à tous les tours des dégats aux ennemis proches
    - stack du mana en infligeant des dégats aux monstres
    - ont un cercle de vision autour d'eux
- monstres :
    - 400 unités
- chaque tour --> donner un ordre à chaque héros :
    - aller à un endroit
    - attendre
    - cast un spell
        - shield un ennemi/allié pendant 12 tours qui rend insensible aux sorts
        - controller le prochain déplacement d'un ennemi
        - repousser les ennemis autour de soi

## Inputs
- vie et mana de ma team
- list d'"entités" : 
    - id
    - type : 0 monstre / 1 allié / 2 adversaire
    - x, y
    - shield_life : 0-12
    - is_controlled : son prochain mouvement est controllé
    ________
    - health
    - vx, vy : vecteur vitesse
    - near_base : a pris la base pour cible
    - threat_for : va cibler la base un jour 0/1/2

## Conditions de lose
    - perdre ses trois <3
    - avoir moins de <3 que l'ennemi au bout de 220tours
    - avoir autant de <3 et stacké moins de mana que l'ennemi
    - ne pas donner d'ordre aux trois héros pendant un tour