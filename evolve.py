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
SPEED = 2
GENERATION_TICKS = 800
REPRODUCTION_RATE = 2.5
MUTATION_RATE = 2.5
MUTATION_AMOUNT = 2
INITIAL_ENERGY = 1000
ENERGY_CONSUMPTION_RATE = 0.2
MIN_CREATURES = 4
FOOD_ENERGY = 600
COLORS = [(0, 255, 0), (0, 0, 255), (255, 255, 0)]

# inicializar pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulação Auto-evolutiva")
clock = pygame.time.Clock()

# indicacao de geracao, tamanho da fonte e cor
font = pygame.font.Font(None, 36)

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


# recoloca as criaturas e tbm tem um numero minimo 
def replenish_creatures(creatures):
    while len(creatures) < MIN_CREATURES:
        creature = create_creature()
        creatures.append(creature)
    return creatures


# cria as criaturas 
creatures = [create_creature(color=color) for color in COLORS for _ in range(NUM_CREATURES // len(COLORS))]

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
        # movimento randomico
        dx = random.randint(-creature["speed"], creature["speed"])
        dy = random.randint(-creature["speed"], creature["speed"])
       
        
        creature["x"] += dx
        creature["y"] += dy
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

    # remove criatuaras sem energia
    creatures = [creature for creature in creatures if creature["energy"] > 0]

    ticks += 1

    if ticks >= GENERATION_TICKS:
        creatures = create_new_generation(creatures)
        creatures = replenish_creatures(creatures)
        ticks = 0
        generation += 1

    # desenha o contador de geracoes
    generation_text = font.render(f"Geração: {generation}", True, (255, 255, 255))
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