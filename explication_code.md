**Etude de la classe Apple**

*Attribut* :
- screen
- rect_x / rect_y
- rect_width / rect_height
- border_color
- rect_size

- apple_position (x,y) : position de la pomme

*Fonctions* :
- random_position : retourne la position (x,y) de la pomme
- uptdate_position : maj la pos de la pomme en utilisant random_position
- draw_apple : affiche la pomme


**Etude de la classe SnakePlayer**

*Attribut* :
- screen
- rect_x / rect_y
- rect_width / rect_height
- border_color
- rect_size

- player_position (x,y) : position 
- segments[x,y]
- direction : next direction
- score : score of the player
- speed : speed of the snake

*Fonctions* :
- random_position : retourne la position (x,y) du joueur au début
- draw_player : dessine le serpent
- handle_keys : link between keys and direction 
- move_player : on avance tt les blocs d'un cran puis en fonction de direction, on avance le premier dans la direction souhaité
- grow : on ajoute un segment avec les même coordonnées que le dernier


**Etude classe Jeu**

*Attribut* :
- screen
- rect_x / rect_y
- rect_width / rect_height

- player
- apple

- font

*Fonctions* :
- ... pas besoin d'étudier
- run_game : fonction qui continuer tant que running est activé (si on perds pas en gros)
    Etapes : player.handle_keys => player.move_player => check_collision => draw
