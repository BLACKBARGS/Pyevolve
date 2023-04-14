import random
import pygame
from pygame.locals import *

# parametros
WIDTH = 1000
HEIGHT = 600
NUM_CREATURES = 100
NUM_FOOD = 1200  # Aumentar a quantidade de comida
CREATURE_SIZE = 7
FOOD_SIZE = 3
SPEED = 2
GENERATION_TICKS = 600
REPRODUCTION_RATE = 2.5
MUTATION_RATE = 2.5
MUTATION_AMOUNT = 2
INITIAL_ENERGY = 2000  # Aumentar a energia inicial das criaturas
ENERGY_CONSUMPTION_RATE = 0.2
MIN_CREATURES = 4
FOOD_ENERGY = 650
COLORS = [(0, 255, 0), (0, 0, 255), (255, 255, 0)]

# inicializar pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulação Auto-evolutiva")
clock = pygame.time.Clock()

# indicacao de geracao, tamanho da fonte e cor
font = pygame.font.Font(None, 36)
font_color = (255, 255, 255)

def update_font_color():
    global font_color
    r, g, b = font_color
    r = (r + random.randint(0, 50)) % 256
    g = (g + random.randint(0, 50)) % 256
    b = (b + random.randint(0, 50)) % 256
    font_color = (r, g, b)

def update_font_size():
    global font
    new_size = random.randint(32, 48)
    font = pygame.font.Font(None, new_size)

def create_creature(speed=None, size=None, color=None):
    return {
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "color": color if color else (0, 255, 0),
        "food": 0,
        "speed": speed if speed is not None else random.randint(1, SPEED),
        "size": size if size is not None else random.randint(3, CREATURE_SIZE),
        "energy": INITIAL_ENERGY,
    }

def move_creature(creature, creatures, food):
    # Buscar comida em vez de perseguir outras criaturas
    closest_food = None
    closest_distance = float("inf")
    for f in food:
        distance = ((creature["x"] - f["x"]) ** 2 + (creature["y"] - f["y"]) ** 2) ** 0.5
        if distance < closest_distance:
            closest_food = f
            closest_distance = distance

    if closest_food:
        dx = closest_food["x"] - creature["x"]
        dy = closest_food["y"] - creature["y"]
        length = (dx ** 2 + dy ** 2) ** 0.5
        if length > 0:
            dx /= length
            dy /= length
        creature["x"] += creature["speed"] * dx
        creature["y"] += creature["speed"] * dy

# recoloca as criaturas e tbm tem um numero minimo 
def replenish_creatures(creatures):
    while len(creatures) < MIN_CREATURES:
        creature = create_creature()
        creatures.append(creature)
    return creatures

# cria as criaturas 
creatures = [create_creature(color=color) for i, color in enumerate(COLORS) for _ in range(NUM_CREATURES // len(COLORS))]

# cria as comidas
food = [
    {
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "color": (255, 0, 0),
    }
    for _ in range(NUM_FOOD)
]

def reproduce(parent1, parent2):
    child_speed = random.choice([parent1["speed"], parent2["speed"]])
    child_size = random.choice([parent1["size"], parent2["size"]])

    # adiciona as mutacoes
    if random.random() < MUTATION_RATE:
        child_speed += random.randint(-MUTATION_AMOUNT, MUTATION_AMOUNT)
        child_speed = max(1, child_speed)

    if random.random() < MUTATION_RATE:
        child_size += random.randint(-MUTATION_AMOUNT, MUTATION_AMOUNT)
        child_size = max(1, child_size)

    child = create_creature(speed=child_speed, size=child_size, color=parent1["color"])

    # restaura a energia dos pais
    parent1["energy"] += FOOD_ENERGY
    parent2["energy"] += FOOD_ENERGY

    return child

def create_new_generation(creatures):
    creatures = sorted(creatures, key=lambda c: c["food"], reverse=True)
    new_generation = []
    for i in range(len(creatures) // 2):
        parent1, parent2 = creatures[i], creatures[len(creatures) - 1 - i]
        if random.random() < REPRODUCTION_RATE:
            child = reproduce(parent1, parent2)
            new_generation.append(child)

    return new_generation


def replenish_food(food):
    while len(food) < NUM_FOOD:
        food.append({
            "x": random.randint(0, WIDTH),
            "y": random.randint(0, HEIGHT),
            "color": (255, 0, 0),
        })
    return food




generation = 0
ticks = 0
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    if ticks % GENERATION_TICKS == 0:
        creatures = create_new_generation(creatures)
        creatures = replenish_creatures(creatures)
        food = replenish_food(food)  # repõe a comida a cada nova geração
        generation += 1
        update_font_color()
        update_font_size()

    # move as criaturas
    for creature in creatures:
        move_creature(creature, creatures, food)

    # verifica se a criatura comeu a comida
    for creature in creatures:
        for f in food:
            distance = ((creature["x"] - f["x"]) ** 2 + (creature["y"] - f["y"]) ** 2) ** 0.5
            if distance < creature["size"]:
                creature["food"] += 1
                creature["energy"] += FOOD_ENERGY
                food.remove(f)

    # remove as criaturas sem energia
    creatures = [c for c in creatures if c["energy"] > 0]

    # desenha criaturas e comidas
    for creature in creatures:
        pygame.draw.circle(screen, creature["color"], (int(creature["x"]), int(creature["y"])), creature["size"])
    for f in food:
        pygame.draw.circle(screen, f["color"], (int(f["x"]), int(f["y"])), FOOD_SIZE)

    # desenha texto da geracao
    text = font.render("Geração: {}".format(generation), True, font_color)
    screen.blit(text, (10, 10))

    ticks += 1
    pygame.display.flip()
    clock.tick(60)

pygame.quit()


