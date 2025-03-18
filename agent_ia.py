import pygame
import random
import math

# Constantes
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
AGENT_COUNT = 20
AGENT_RADIUS = 5
MAX_SPEED = 2
FPS = 120
DANGER_RADIUS = 100  # Distance à laquelle les agents fuient le prédateur
TARGET_RADIUS = 10   # Rayon du point cible
OBSTACLE_RADIUS = 20  # Rayon des obstacles
GROUP_RADIUS = 50    # Distance à laquelle les agents forment des groupes

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Classe Agent
class Agent:
    agents = []
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(-1, 1)
        self.speed = MAX_SPEED
        # Nouveaux paramètres
        self.repulsion_radius = AGENT_RADIUS * 3  # Zone de répulsion
        self.repulsion_strength = 0.5  # Force de répulsion
        self.cohesion_strength = 0.1   # Force de groupe
        self.target_strength = 0.2     # Force vers la cible
        # Ajouter l'agent à la liste des agents
        Agent.agents.append(self)

    def move(self, target, predator, obstacles):
        # Initialiser les forces
        fx, fy = 0, 0
        
        # 1. Force vers la cible (prioritaire)
        target_vector = self.calculate_target_force(target)
        fx += target_vector[0] * self.target_strength
        fy += target_vector[1] * self.target_strength

        # 2. Force de répulsion entre agents
        avoidance_vector = self.calculate_avoidance_force()
        fx += avoidance_vector[0] * self.repulsion_strength
        fy += avoidance_vector[1] * self.repulsion_strength

        # 3. Force de cohésion (groupe)
        cohesion_vector = self.calculate_cohesion_force()
        fx += cohesion_vector[0] * self.cohesion_strength
        fy += cohesion_vector[1] * self.cohesion_strength

        # 4. Fuite du prédateur
        predator_vector = self.calculate_predator_force(predator)
        fx += predator_vector[0]
        fy += predator_vector[1]

        # 5. Évitement des obstacles
        obstacle_vector = self.calculate_obstacle_force(obstacles)
        fx += obstacle_vector[0]
        fy += obstacle_vector[1]

        # Normaliser et appliquer la direction
        length = math.hypot(fx, fy)
        if length > 0:
            self.dx = fx / length
            self.dy = fy / length

        # Appliquer le mouvement
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        # Contraintes aux bords
        self.x = max(AGENT_RADIUS, min(WINDOW_WIDTH - AGENT_RADIUS, self.x))
        self.y = max(AGENT_RADIUS, min(WINDOW_HEIGHT - AGENT_RADIUS, self.y))

    def calculate_target_force(self, target):
        dx = target[0] - self.x
        dy = target[1] - self.y
        distance = math.hypot(dx, dy)
        if distance > 0:
            return (dx / distance, dy / distance)
        return (0, 0)

    def calculate_avoidance_force(self):
        fx, fy = 0, 0
        for other in Agent.agents:
            if other != self:
                dx = self.x - other.x
                dy = self.y - other.y
                distance = math.hypot(dx, dy)
                
                # Éviter la division par zéro
                if distance < 1e-6:  # Si la distance est très petite (presque nulle)
                    continue  # Ignorer cet agent
                
                if distance < self.repulsion_radius:
                    weight = 1 - (distance / self.repulsion_radius)
                    fx += (dx / distance) * weight
                    fy += (dy / distance) * weight
        return (fx, fy)

    def calculate_cohesion_force(self):
        avg_x, avg_y, count = 0, 0, 0
        for other in Agent.agents:  # Utiliser la variable de classe
            if other != self:
                distance = math.hypot(self.x - other.x, self.y - other.y)
                if distance < GROUP_RADIUS:
                    avg_x += other.x
                    avg_y += other.y
                    count += 1
        if count > 0:
            avg_x /= count
            avg_y /= count
            dx = avg_x - self.x
            dy = avg_y - self.y
            distance = math.hypot(dx, dy)
            if distance > 0:
                return (dx / distance, dy / distance)
        return (0, 0)

    def calculate_predator_force(self, predator):
        dx = self.x - predator.x
        dy = self.y - predator.y
        distance = math.hypot(dx, dy)
        if distance < DANGER_RADIUS:
            strength = 1.5 * (1 - distance / DANGER_RADIUS)
            return (dx / distance * strength, dy / distance * strength)
        return (0, 0)

    def calculate_obstacle_force(self, obstacles):
        fx, fy = 0, 0
        for obstacle in obstacles:
            if isinstance(obstacle, tuple):
                ox, oy = obstacle
            else:
                ox, oy = obstacle.x, obstacle.y
            
            dx = self.x - ox
            dy = self.y - oy
            distance = math.hypot(dx, dy)
            if distance < OBSTACLE_RADIUS + AGENT_RADIUS:
                weight = 1 - (distance / (OBSTACLE_RADIUS + AGENT_RADIUS))
                fx += (dx / distance) * weight
                fy += (dy / distance) * weight
        return (fx, fy)

    def draw(self, screen):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), AGENT_RADIUS)

# Classe Predator (prédateur)
class Predator:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(-1, 1)
        self.speed = MAX_SPEED * 1.5  # Le prédateur est plus rapide

    def move(self):
        # Mettre à jour la position
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        # Rebondir sur les bords de la fenêtre
        if self.x < 0 or self.x > WINDOW_WIDTH:
            self.dx *= -1
        if self.y < 0 or self.y > WINDOW_HEIGHT:
            self.dy *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), AGENT_RADIUS)

# Classe Obstacle dynamique
class DynamicObstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(-1, 1)
        self.speed = MAX_SPEED * 0.5  # Les obstacles se déplacent plus lentement

    def move(self):
        # Mettre à jour la position
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed

        # Rebondir sur les bords de la fenêtre
        if self.x < 0 or self.x > WINDOW_WIDTH:
            self.dx *= -1
        if self.y < 0 or self.y > WINDOW_HEIGHT:
            self.dy *= -1

    def draw(self, screen):
        pygame.draw.circle(screen, ORANGE, (int(self.x), int(self.y)), OBSTACLE_RADIUS)

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Crowd Simulation with Pygame")
clock = pygame.time.Clock()

# Créer les agents
agents = [Agent(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for _ in range(AGENT_COUNT)]

# Créer le prédateur
predator = Predator(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))

# Créer des obstacles statiques et dynamiques
static_obstacles = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for _ in range(5)]
dynamic_obstacles = [DynamicObstacle(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT)) for _ in range(3)]
obstacles = static_obstacles + dynamic_obstacles

# Définir la cible initiale
target = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

# Boucle principale
running = True
while running:
    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Déplacer la cible avec la souris
            target = pygame.mouse.get_pos()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Ajouter un nouvel obstacle statique
                obstacles.append(pygame.mouse.get_pos())

    # Mettre à jour les agents
    for agent in agents:
        agent.move(target, predator, obstacles)

    # Mettre à jour le prédateur
    predator.move()

    # Mettre à jour les obstacles dynamiques
    for obstacle in dynamic_obstacles:
        obstacle.move()

    # Dessiner l'arrière-plan
    screen.fill(WHITE)

    # Dessiner les obstacles
    for obstacle in obstacles:
        if isinstance(obstacle, DynamicObstacle):
            obstacle.draw(screen)
        else:
            pygame.draw.circle(screen, BLACK, obstacle, OBSTACLE_RADIUS)

    # Dessiner la cible
    pygame.draw.circle(screen, GREEN, target, TARGET_RADIUS)

    # Dessiner les agents
    for agent in agents:
        agent.draw(screen)

    # Dessiner le prédateur
    predator.draw(screen)

    # Mettre à jour l'affichage
    pygame.display.flip()
    clock.tick(FPS)

# Quitter Pygame
pygame.quit()

