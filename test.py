import pygame
import random

# Inicializar o pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman - Jogo da Forca")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fonte
font = pygame.font.Font(None, 50)

# Palavras do jogo
palavras = ["DEPIA"]

# Escolher palavra aleatória
palavra = random.choice(palavras)
palavra_oculta = ["_" for _ in palavra]
letras_erradas = []
max_erros = 6


def draw_hangman(errors):
    base_x, base_y = 700, 200  # Ajustando a posição do boneco para ficar abaixo da forca
    if errors >= 1:
        pygame.draw.circle(screen, BLACK, (base_x, base_y), 50, 5)  # Cabeça
    if errors >= 2:
        pygame.draw.line(screen, BLACK, (base_x, base_y + 50), (base_x, base_y + 150), 5)  # Corpo
    if errors >= 3:
        pygame.draw.line(screen, BLACK, (base_x, base_y + 70), (base_x - 50, base_y + 100), 5)  # Braço esquerdo
    if errors >= 4:
        pygame.draw.line(screen, BLACK, (base_x, base_y + 70), (base_x + 50, base_y + 100), 5)  # Braço direito
    if errors >= 5:
        pygame.draw.line(screen, BLACK, (base_x, base_y + 150), (base_x - 50, base_y + 200), 5)  # Perna esquerda
    if errors >= 6:
        pygame.draw.line(screen, BLACK, (base_x, base_y + 150), (base_x + 50, base_y + 200), 5)  # Perna direita


# Loop do jogo
running = True
while running:
    screen.fill(WHITE)

    # Desenhar forca
    pygame.draw.line(screen, BLACK, (450, 500), (750, 500), 5)  # Base
    pygame.draw.line(screen, BLACK, (600, 500), (600, 100), 5)  # Poste
    pygame.draw.line(screen, BLACK, (600, 100), (700, 100), 5)  # Suporte superior
    pygame.draw.line(screen, BLACK, (700, 100), (700, 150), 5)  # Corda

    # Exibir palavra oculta
    texto_palavra = font.render(" ".join(palavra_oculta), True, BLACK)
    screen.blit(texto_palavra, (50, 200))

    # Exibir letras erradas
    texto_erros = font.render("Erros: " + " ".join(letras_erradas), True, RED)
    screen.blit(texto_erros, (50, 300))

    # Desenhar boneco conforme erros
    draw_hangman(len(letras_erradas))

    # Verificar vitória ou derrota
    if "_" not in palavra_oculta:
        texto_vitoria = font.render("Você venceu!", True, BLACK)
        screen.blit(texto_vitoria, (50, 400))
        pygame.display.flip()
        pygame.time.delay(2000)
        break

    if len(letras_erradas) >= max_erros:
        texto_derrota = font.render(f"Você perdeu! A palavra era {palavra}", True, BLACK)
        screen.blit(texto_derrota, (50, 400))
        pygame.display.flip()
        pygame.time.delay(2000)
        break

    # Atualizar tela
    pygame.display.flip()

    # Capturar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            letra = pygame.key.name(event.key).upper()
            if letra in palavra and letra not in palavra_oculta:
                for i in range(len(palavra)):
                    if palavra[i] == letra:
                        palavra_oculta[i] = letra
            elif letra not in palavra and letra not in letras_erradas and letra.isalpha():
                letras_erradas.append(letra)

# Sair do pygame
pygame.quit()