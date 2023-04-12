# Simulação Auto-evolutiva

### Este programa é uma simulação de um ecossistema em que criaturas se reproduzem e evoluem ao longo do tempo. A simulação é executada usando o pygame, uma biblioteca de jogos para Python

#### Como usar

#### Para usar este programa, basta executar o código em um ambiente Python compatível com o pygame. Certifique-se de ter o pygame instalado antes de executar o programa. Depois de executar o programa, você verá uma janela com a simulação em execução.

Parâmetros

O programa possui vários parâmetros que podem ser ajustados para controlar a simulação. Esses parâmetros estão no início do código e incluem:

WIDTH: Largura da tela em pixels.
HEIGHT: Altura da tela em pixels.
NUM_CREATURES: Número inicial de criaturas na simulação.
NUM_FOOD: Número inicial de alimentos na simulação.
CREATURE_SIZE: Tamanho máximo das criaturas.
FOOD_SIZE: Tamanho dos alimentos.
SPEED: Velocidade máxima das criaturas.
GENERATION_TICKS: Número de ticks (atualizações) antes de criar uma nova geração de criaturas.
REPRODUCTION_RATE: Taxa de reprodução das criaturas.
MUTATION_RATE: Taxa de mutação das criaturas.
MUTATION_AMOUNT: Quantidade máxima de mutação permitida.
INITIAL_ENERGY: Energia inicial das criaturas.
ENERGY_CONSUMPTION_RATE: Taxa de consumo de energia das criaturas.
MIN_CREATURES: Número mínimo de criaturas necessárias para manter a simulação em execução.
FOOD_ENERGY: Quantidade de energia fornecida por cada comida.
COLORS: Lista de cores usadas para criar as criaturas.
Funcionamento:

A simulação começa com um número inicial de criaturas e alimentos na tela. As criaturas são representadas como retângulos coloridos, enquanto os alimentos são representados como pequenos quadrados vermelhos. As criaturas se movem aleatoriamente pela tela e consomem alimentos para ganhar energia. Quando uma criatura tem energia suficiente e encontra outra criatura, ela pode se reproduzir e criar uma nova criatura.

A cada "geração" da simulação, as criaturas com melhor desempenho (ou seja, as que conseguiram coletar mais alimentos) têm uma maior probabilidade de se reproduzir. As criaturas filhas herdam características de seus pais, mas também podem sofrer mutações aleatórias. A cada nova geração, o número total de criaturas na simulação é mantido constante, para evitar que a simulação cresça indefinidamente.

A simulação é interrompida quando o número de criaturas cai abaixo de um determinado limite mínimo, o que pode ocorrer se as criaturas não conseguirem coletar comida suficiente para sobreviver
