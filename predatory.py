import random
import pygame
from pygame.locals import *

# parametros
WIDTH = 1000
HEIGHT = 600
NUM_CREATURES = 125
NUM_FOOD = 1000
CREATURE_SIZE = 7
FOOD_SIZE = 3
SPEED = 3
GENERATION_TICKS = 800
REPRODUCTION_RATE = 2.5
MUTATION_RATE = 2.5
MUTATION_AMOUNT = 2
INITIAL_ENERGY = 1000
ENERGY_CONSUMPTION_RATE = 0.2
MIN_CREATURES = 4
FOOD_ENERGY = 600
STRENGTH_GAIN_PER_FOOD = 5
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

def create_creature(speed=None, size=None, color=None, predator=False):
    return {
        "x": random.randint(0, WIDTH),
        "y": random.randint(0, HEIGHT),
        "color": color if color else (0, 255, 0),
        "food": 0,
        "speed": speed if speed is not None else random.randint(1, SPEED),
        "size": size if size is not None else random.randint(3, CREATURE_SIZE),
        "energy": INITIAL_ENERGY,
        "predator": predator,
        "strength": 0,
    }

def move_creature(creature, creatures):
    if creature["predator"]:
        # Predador se move em direção à presa mais próxima
        closest_prey = None
        closest_distance = float("inf")
        for other in creatures:
            if other["predator"]:
                continue
            distance = ((creature["x"] - other["x"]) ** 2 + (creature["y"] - other["y"]) ** 2) ** 0.5
            if distance < closest_distance:
                closest_prey = other
                closest_distance = distance

        if closest_prey:
            dx = closest_prey["x"] - creature["x"]
            dy = closest_prey["y"] - creature["y"]
            length = (dx ** 2 + dy ** 2) ** 0.5
            if length > 0:
                dx /= length
                dy /= length
            creature["x"] += creature["speed"] * dx
            creature["y"] += creature["speed"] * dy
    else:
        # Presa tenta evitar predadores próximos
        dx = 0
        dy = 0
        for other in creatures:
            if not other["predator"]:
                continue
            distance = ((creature["x"] - other["x"]) ** 2 + (creature["y"] - other["y"]) ** 2) ** 0.5
            if distance > 0 and distance < creature["size"] * 5:
                dx += (creature["x"] - other["x"]) / distance
                dy += (creature["y"] - other["y"]) / distance

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
creatures = [create_creature(color=color, predator=i % 2 == 0) for i, color in enumerate(COLORS) for _ in range(NUM_CREATURES // len(COLORS))]

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

    child = create_creature(speed=child_speed, size=child_size, color=parent1["color"], predator=parent1["predator"])

    # restaura a energia dos pais
    parent1["energy"] += FOOD_ENERGY
    parent2["energy"] += FOOD_ENERGY

    return child

def create_new_generation(creatures):
    creatures = sorted(creatures, key=lambda c: c["food"], reverse=True)
    new_generation = creatures[: len(creatures) // 2]
    for _ in range(len(creatures) // 2):
        parent1 = random.choice(new_generation)
        parent2 = random.choice(new_generation)
        if random.random() < REPRODUCTION_RATE:
            child = reproduce(parent1, parent2)
            new_generation.append(child)
    return new_generation

ticks = 0
generation = 0
running = True
while running:
    screen.fill((000, 000, 000))

    # atualiza as criaturas
    for creature in creatures:
        move_creature(creature, creatures)

        # limite do tamanho da tela
        creature["x"] = max(0, min(WIDTH - creature["size"], creature["x"]))
        creature["y"] = max(0, min(HEIGHT - creature["size"], creature["y"]))
        
        # verifica se a criatura achou comida
        for f in food:
            if (
                abs(creature["x"] - f["x"]) < creature["size"]
                and abs(creature["y"] - f["y"]) < creature["size"]
            ):
                creature["food"] += 1
                creature["energy"] += FOOD_ENERGY
                f["x"] = random.randint(0, WIDTH)
                f["y"] = random.randint(0, HEIGHT)

        # reduz a energia da criatura
        creature["energy"] -= ENERGY_CONSUMPTION_RATE

    # remove criaturas sem energia
    creatures = [creature for creature in creatures if creature["energy"] > 0]

    ticks += 1

    if ticks >= GENERATION_TICKS:
        creatures = create_new_generation(creatures)
        creatures = replenish_creatures(creatures)
        ticks = 0
        generation += 1
        update_font_color()
        update_font_size()
        REPRODUCTION_RATE += 0.1
        MUTATION_RATE += 0.01

    # desenha o contador de geracoes
    generation_text = font.render(f"Geração: {generation}", True, font_color)
    screen.blit(generation_text, (10, 10))

    # desenha as criaturas e comida 
    for creature in creatures:
        pygame.draw.rect(
            screen,
            creature["color"],
            (creature["x"], creature["y"], creature["size"], creature["size"]),
        )
    for f in food:
        pygame.draw.rect(
            screen,
            f["color"],
            (f["x"], f["y"], FOOD_SIZE, FOOD_SIZE),
        )

    # verifica eventos
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # atualiza a tela e espera
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

