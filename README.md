# Simulation de Comportement de Foule avec Intelligence Artificielle en Python

Ce programme est une simulation 2D de comportement de foule (crowd simulation) implémentée en Python avec la bibliothèque Pygame. Il met en scène des agents intelligents qui interagissent entre eux, avec leur environnement, et avec un prédateur. Les agents sont capables de se déplacer de manière autonome en suivant des règles simples basées sur l'intelligence artificielle (IA), comme éviter les collisions, se regrouper, fuir un danger, et atteindre une cible.

---

## Sujet du Programme

Le programme simule un environnement 2D dans lequel :

- **Des agents** (représentés par des cercles bleus) se déplacent de manière autonome.
- **Un prédateur** (représenté par un cercle rouge) poursuit les agents, qui fuient s'ils sont trop proches.
- **Des obstacles** (statiques ou dynamiques) bloquent le chemin des agents, qui doivent les éviter.
- **Une cible** (représentée par un cercle vert) attire les agents, qui tentent de l'atteindre tout en respectant les règles de comportement.

Les agents utilisent des règles d'IA simples pour :

- **Éviter les collisions** entre eux et avec les obstacles.
- **Se regrouper** pour former des clusters tout en gardant une distance raisonnable.
- **Fuir le prédateur** s'il est trop proche.
- **Atteindre la cible** en se déplaçant de manière fluide et naturelle.

---

## Fonctionnalités Principales

### Agents Intelligents
- Chaque agent a une position, une direction, et une vitesse.
- Les agents évitent les collisions avec les autres agents et les obstacles.
- Ils se dirigent vers la cible tout en maintenant une cohésion de groupe.

### Prédateur
- Le prédateur se déplace aléatoirement dans l'environnement.
- Les agents fuient le prédateur s'ils sont dans son rayon de danger.

### Obstacles
- **Statiques** : Des obstacles fixes bloquent le chemin des agents.
- **Dynamiques** : Des obstacles mobiles se déplacent dans l'environnement.

### Cible
- Les agents tentent d'atteindre la cible, qui peut être déplacée par l'utilisateur.

### Interface Utilisateur
- L'utilisateur peut déplacer la cible en cliquant avec la souris.
- L'utilisateur peut ajouter des obstacles statiques en appuyant sur la barre d'espace.

---

## Structure du Code

Le programme est structuré en plusieurs classes et fonctions :

### Classe `Agent`
- Représente un agent intelligent.
- Gère le mouvement, l'évitement des collisions, la cohésion de groupe, la fuite du prédateur, et l'évitement des obstacles.

### Classe `Predator`
- Représente le prédateur qui poursuit les agents.
- Se déplace aléatoirement dans l'environnement.

### Classe `DynamicObstacle`
- Représente un obstacle mobile.
- Se déplace aléatoirement et rebondit sur les bords de l'écran.

### Fonctions Principales
- `initialize_agents()` : Initialise les agents avec des positions et directions aléatoires.
- `initialize_grid()` : Initialise la grille d'affichage.
- `update_agents()` : Met à jour la position des agents en fonction des règles d'IA.
- `render_grid()` : Affiche les agents, les obstacles, le prédateur, et la cible.

### Boucle Principale
- Gère les événements (clavier, souris).
- Met à jour les positions des agents, du prédateur, et des obstacles.
- Affiche l'environnement en temps réel.

---

## Comment Utiliser le Programme

### Exécution
1. Assurez-vous d'avoir Python et Pygame installés.
2. Exécutez le script Python pour lancer la simulation.

### Contrôles
- **Clic gauche** : Déplace la cible à l'emplacement de la souris.
- **Barre d'espace** : Ajoute un obstacle statique à l'emplacement de la souris.

### Paramètres
Vous pouvez ajuster les paramètres suivants dans le code :
- `AGENT_COUNT` : Nombre d'agents.
- `MAX_SPEED` : Vitesse maximale des agents.
- `DANGER_RADIUS` : Distance à laquelle les agents fuient le prédateur.
- `GROUP_RADIUS` : Distance à laquelle les agents forment des groupes.
- `repulsion_strength`, `cohesion_strength`, `target_strength` : Forces relatives des comportements.

---

## Exemples de Comportements

### Regroupement
- Les agents se rapprochent les uns des autres tout en évitant les collisions.

### Fuite
- Si le prédateur s'approche, les agents fuient dans la direction opposée.

### Évitement d'Obstacles
- Les agents contournent les obstacles statiques et dynamiques.

### Déplacement vers la Cible
- Les agents se dirigent vers la cible tout en respectant les autres règles.

---

## Conclusion

Ce programme est une démonstration simple mais puissante de la simulation de comportements complexes à partir de règles d'IA basiques. Il peut être utilisé comme base pour des projets plus avancés, comme des simulations de foule, des jeux vidéo, ou des modèles de trafic.

N'hésitez pas à explorer et à modifier le code pour l'adapter à vos besoins !

---

### Requirements
- Python 3.x
- Pygame (`pip install pygame`)

### Execution
```bash
python agent_ia.py
python -m unittest test_agent_ia.py