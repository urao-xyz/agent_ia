import unittest
import math
from agent_ia import Agent, Predator, DynamicObstacle

class TestAgent(unittest.TestCase):
    def setUp(self):
        # Réinitialiser la liste des agents
        Agent.agents = []

        # Créez un agent pour les tests
        self.agent = Agent(100, 100)
        self.predator = Predator(200, 200)
        self.obstacle = DynamicObstacle(150, 150)

        # Ajouter d'autres agents proches avec des positions différentes
        positions = [(110, 110), (120, 120), (130, 130), (140, 140), (150, 150)]  # Positions différentes
        for pos in positions:
            Agent(pos[0], pos[1])  # Créer des agents avec des positions uniques

    def test_calculate_target_force(self):
        target = (300, 300)
        force = self.agent.calculate_target_force(target)
        expected_force = ((target[0] - self.agent.x) / math.hypot(target[0] - self.agent.x, target[1] - self.agent.y),
                          (target[1] - self.agent.y) / math.hypot(target[0] - self.agent.x, target[1] - self.agent.y))
        self.assertAlmostEqual(force[0], expected_force[0], places=5)
        self.assertAlmostEqual(force[1], expected_force[1], places=5)

    def test_calculate_avoidance_force(self):
        force = self.agent.calculate_avoidance_force()
        self.assertNotEqual(force, (0, 0))  # La force ne devrait pas être nulle

    def test_calculate_cohesion_force(self):
        force = self.agent.calculate_cohesion_force()
        self.assertNotEqual(force, (0, 0))  # La force ne devrait pas être nulle

    def test_calculate_predator_force(self):
        force = self.agent.calculate_predator_force(self.predator)
        distance = math.hypot(self.agent.x - self.predator.x, self.agent.y - self.predator.y)
        if distance < 100:  # DANGER_RADIUS
            self.assertNotEqual(force, (0, 0))  # La force ne devrait pas être nulle
        else:
            self.assertEqual(force, (0, 0))  # La force devrait être nulle

    def test_calculate_obstacle_force(self):
        force = self.agent.calculate_obstacle_force([self.obstacle])
        distance = math.hypot(self.agent.x - self.obstacle.x, self.agent.y - self.obstacle.y)
        if distance < 25:  # OBSTACLE_RADIUS + AGENT_RADIUS
            self.assertNotEqual(force, (0, 0))  # La force ne devrait pas être nulle
        else:
            self.assertEqual(force, (0, 0))  # La force devrait être nulle

if __name__ == '__main__':
    unittest.main()