import math
import webbrowser
from pathlib import Path
import cv2
import numpy as np
import pygame
from ultralytics import YOLO
import requests

pygame.init()
cap = cv2.VideoCapture(0)
current_dir = Path(__file__).parent

selected_color_NoPPE = (220, 20, 60)
selected_color_PPE = (20, 220, 60)

glasses_model = YOLO(current_dir / "best11.pt")
glasses_model.overrides['verbose'] = False
glasses_model.model.names = {0: "Sem EPI", 1: "Óculos EPI"}

d_info = pygame.display.Info()
screen_width, screen_height = d_info.current_w, d_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Argus IA")

# Variáveis Infinitas
start_time = None
fps_bool = True
audio_bool = True
audio_clicked = False
fps_clicked = False
infoApertado = False
info_clicked = False
IniciarApertado = False
ConfigApertado = False
running = True
fullscreen = False

prev_frame_time = pygame.time.get_ticks()
new_frame_time = 0

icone = pygame.image.load(current_dir / "PixelLogo.png")
pygame.display.set_icon(icone)

# menu informações
info_menu = pygame.image.load(current_dir / "Informações.png")
info_menu = pygame.transform.scale(info_menu, (screen_width, screen_height))

# Página Inicial
background0 = pygame.image.load(current_dir / "1.png")
background0 = pygame.transform.scale(background0, (screen_width, screen_height))

# Botão Iniciar
background1 = pygame.image.load(current_dir / "2.png")
background1 = pygame.transform.scale(background1, (screen_width, screen_height))

# Botão Configurar
background2 = pygame.image.load(current_dir / "3.png")
background2 = pygame.transform.scale(background2, (screen_width, screen_height))

# Botão Sair
background3 = pygame.image.load(current_dir / "4.png")
background3 = pygame.transform.scale(background3, (screen_width, screen_height))

icon = pygame.image.load(current_dir / "Info_Icon.png")
InfoIcon = pygame.transform.scale(icon, (33, 33))

# Configuração ON/ON
config = pygame.image.load(current_dir / "9.png")
config = pygame.transform.scale(config, (screen_width, screen_height))

# Configuração OFF/ON
config2 = pygame.image.load(current_dir / "10.png")
config2 = pygame.transform.scale(config2, (screen_width, screen_height))

# Configuração ON/OFF
config3 = pygame.image.load(current_dir / "11.png")
config3 = pygame.transform.scale(config3, (screen_width, screen_height))

# Configuração OFF/OFF
config4 = pygame.image.load(current_dir / "12.png")
config4 = pygame.transform.scale(config4, (screen_width, screen_height))

alert_sound = pygame.mixer.Sound("alerta_epi.mp3")
alert_sound2 = pygame.mixer.Sound("alerta_epi2.mp3")

WLED_IP = "http://hydraws.local"

def draw_circle(surface, center, radius):
    for angle in range(360):
        color = hsl2rgb(angle / 360.0, 1.0, 0.5)
        x = center[0] + int(radius * math.cos(math.radians(angle)))
        y = center[1] + int(radius * math.sin(math.radians(angle)))
        pygame.draw.line(surface, color, center, (x, y), 2)


def hsl2rgb(h, s, l):
    if s == 0:
        r = g = b = int(l * 255)
    else:
        def hue_to_rgb(p, q, t):
            if t < 0:
                t += 1
            if t > 1:
                t -= 1
            if t < 1 / 6:
                return p + (q - p) * 6 * t
            if t < 1 / 2:
                return q
            if t < 2 / 3:
                return p + (q - p) * (2 / 3 - t) * 6
            return p

        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1 / 3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1 / 3)

        r, g, b = int(r * 255), int(g * 255), int(b * 255)

    return r, g, b


def chromatic_circles():
    global selected_color_NoPPE, selected_color_PPE

    # Posições dos círculos de cores (proporcionais à tela)
    color_circle_center1 = (screen_width * (540.5 / 960), screen_height * (356 / 540))
    color_circle_center2 = (screen_width * (247.5 / 960), screen_height * (356 / 540))

    # Desenha os círculos de cores
    draw_circle(screen, color_circle_center1, screen_width * (47 / 960))
    draw_circle(screen, color_circle_center2, screen_width * (47 / 960))

    # Detecta o clique do mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_button = pygame.mouse.get_pressed()

    # Circulo Cromático No PPE
    distance1 = math.sqrt((mouse_x - color_circle_center1[0]) ** 2 + (mouse_y - color_circle_center1[1]) ** 2)
    if mouse_button[0] and distance1 <= screen_width * (48 / 960):
        angle = math.degrees(math.atan2(mouse_y - color_circle_center1[1], mouse_x - color_circle_center1[0]))
        if angle < 0:
            angle += 360
        selected_color_NoPPE = hsl2rgb(angle / 360.0, 1.0, 0.5)  # Salva a cor selecionada

    # Exibe o texto e a cor selecionada para No PPE
    font = pygame.font.Font(current_dir / "PressStart2P-Regular.ttf", 12)
    color_text = font.render(f"{selected_color_NoPPE[0]}, {selected_color_NoPPE[1]}, {selected_color_NoPPE[2]}", True,
                             (255, 255, 255))
    color_text_rect = color_text.get_rect(
        center=(color_circle_center1[0] + screen_width * 0.13, color_circle_center1[1] + screen_height * 0.027))
    screen.blit(color_text, color_text_rect)
    pygame.draw.rect(screen, selected_color_NoPPE, (
    color_circle_center1[0] + screen_width * 0.132, color_circle_center1[1] - screen_height * 0.057,
    screen_width * 0.037, screen_height * 0.043))

    # Circulo Cromático PPE
    distance2 = math.sqrt((mouse_x - color_circle_center2[0]) ** 2 + (mouse_y - color_circle_center2[1]) ** 2)
    if mouse_button[0] and distance2 <= screen_width * (48 / 960):
        angle = math.degrees(math.atan2(mouse_y - color_circle_center2[1], mouse_x - color_circle_center2[0]))
        if angle < 0:
            angle += 360
        selected_color_PPE = hsl2rgb(angle / 360.0, 1.0, 0.5)  # Salva a cor selecionada

    # Exibe o texto e a cor selecionada para PPE
    color_text = font.render(f"{selected_color_PPE[0]}, {selected_color_PPE[1]}, {selected_color_PPE[2]}", True,
                             (255, 255, 255))
    color_text_rect = color_text.get_rect(
        center=(color_circle_center2[0] + screen_width * 0.13, color_circle_center2[1] + screen_height * 0.027))
    screen.blit(color_text, color_text_rect)
    pygame.draw.rect(screen, selected_color_PPE, (
    color_circle_center2[0] + screen_width * 0.132, color_circle_center2[1] - screen_height * 0.053,
    screen_width * 0.036, screen_height * 0.043))


while running:
    font = pygame.font.Font(current_dir / "PressStart2P-Regular.ttf", int(screen_height * 0.0179))

    class_colors = {
        0: selected_color_NoPPE,  # No PPE
        1: selected_color_PPE  # PPE Goggles
    }

    x, y = pygame.mouse.get_pos()

    if not ConfigApertado and not IniciarApertado:
        # Tela Principal - Botão Iniciar
        if screen_width * 0.36 <= x <= screen_width * 0.64 and screen_height * 0.25 <= y <= screen_height * 0.37:
            screen.blit(background1, (0, 0))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        # Tela Principal - Botão Configurações
        elif screen_width * 0.36 <= x <= screen_width * 0.64 and screen_height * 0.44 <= y <= screen_height * 0.56:
            screen.blit(background2, (0, 0))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        # Tela Principal - Botão Sair
        elif screen_width * 0.36 <= x <= screen_width * 0.64 and screen_height * 0.63 <= y <= screen_height * 0.76:
            screen.blit(background3, (0, 0))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        # Tela Principal - Hydra
        elif screen_width * 0.73 <= x <= screen_width * 0.90 and screen_height * 0.07 <= y <= screen_height * 0.17:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        # Tela Principal - FRC
        elif screen_width * 0.05 <= x <= screen_width * 0.30 and screen_height * 0.07 <= y <= screen_height * 0.18:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        # Tela Principal
        else:
            screen.blit(background0, (0, 0))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    # Verificando eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif not ConfigApertado and not IniciarApertado:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                # Tela Principal - Botão Iniciar
                if screen_width * 0.36 <= x <= screen_width * 0.64 and screen_height * 0.25 <= y <= screen_height * 0.37:
                    IniciarApertado = True

                # Tela Principal - Botão Configurações
                elif screen_width * 0.36 <= x <= screen_width * 0.64 and screen_height * 0.44 <= y <= screen_height * 0.56:
                    ConfigApertado = True

                # Tela Principal - Botão Sair
                elif screen_width * 0.36 <= x <= screen_width * 0.64 and screen_height * 0.63 <= y <= screen_height * 0.76:
                    running = False

                # Tela Principal - Hydra
                elif screen_width * 0.73 <= x <= screen_width * 0.90 and screen_height * 0.07 <= y <= screen_height * 0.17:
                    webbrowser.open("https://www.instagram.com/hydrafrc/")

                # Tela Principal - FRC
                elif screen_width * 0.05 <= x <= screen_width * 0.30 and screen_height * 0.07 <= y <= screen_height * 0.18:
                    webbrowser.open("https://www.firstinspires.org/robotics/frc/game-and-season")

    # Exibição da detecção YOLO
    if IniciarApertado:
        ret, frame = cap.read()

        if 15 <= x <= 35 and (screen_height - 35 <= y <= screen_height - 10):
            if infoApertado == False and info_clicked == False:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    IniciarApertado = False
                    alert_sound.fadeout(100)
                    alert_sound2.fadeout(100)

        elif 12 <= x <= 31 and 11 <= y <= 32:
            if info_clicked == False:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not info_clicked:
                    infoApertado = not infoApertado
                    info_clicked = True

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    info_clicked = False

        elif infoApertado and info_clicked:
            if screen_width * 0.19 <= x <= screen_width * 0.21 and screen_height * 0.05 <= y <= screen_height * 0.08:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    infoApertado = False
                    info_clicked = False

            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if ret:
            if screen_width / 4 - 20 <= x <= screen_width / 4 - 30 and y == 20:
                IniciarApertado = False

            # Redimensiona o frame
            frame_resized = cv2.resize(frame, (screen_width, screen_height))

            # Realiza a inferência
            results = glasses_model(frame_resized)
            detections = results[0].boxes

            # Contador de detecções
            class_counts = {}
            class_names = glasses_model.names

            # inicializa contador com zero para as classes
            for class_id in range(len(class_names)):
                class_counts[class_id] = 0

            # contar as detecções separadamente por classe
            for detection in detections:
                class_id = int(detection.cls)  # ID da classe detectada
                class_counts[class_id] += 1

            # Exibir as detecções, mesmo que sejam 0
            settings = [
                (f"Num. de detecções:", f"{class_counts[0] + class_counts[1]}"),
                (f"Detecções No PPE:", f"{class_counts[0]}"),
                (f"Detecções PPE:", f"{class_counts[1]}"),
            ]

            is_detecting_class_0 = False

            # Exibe as detecções no frame
            for detection in detections:

                x, y, w, h = detection.xywh[0].cpu().numpy()
                class_id = int(detection.cls)
                confidence = detection.conf
                label = f"{glasses_model.names[class_id]} ({confidence.item():.2f})"
                color = class_colors.get(int(class_id), (255, 255, 255))
                color = (color[2], color[1], color[0])

                x1, y1 = int(x - w / 2), int(y - h / 2)
                x2, y2 = int(x + w / 2), int(y + h / 2)
                cv2.rectangle(frame_resized, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame_resized, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # Verificar se a classe 0 foi detectada (No PPE)
                if class_id == 0:
                    is_detecting_class_0 = True

                # Gerenciar o cronômetro
            if is_detecting_class_0:
                if start_time is None:
                    start_time = pygame.time.get_ticks()

                elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Converte milissegundos para segundos

                if elapsed_time > 0.5 and not pygame.mixer.get_busy() and audio_bool:
                    alert_sound.play()
                    alert_sound2.play()
                    start_time = None
            else:
                alert_sound.stop()
                alert_sound2.stop()
                start_time = None

            # Calcula o FPS usando pygame.time
            new_frame_time = pygame.time.get_ticks()
            fps = 1000 / (new_frame_time - prev_frame_time)  # Converte de milissegundos para FPS
            prev_frame_time = new_frame_time

            if fps_bool:
                cv2.putText(frame_resized, f"{int(fps)} FPS", (screen_width - 75, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            ((0, 255, 0)), 2)

            # Converte o frame para RGB
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            pygame_frame = pygame.surfarray.make_surface(np.transpose(frame_rgb, (1, 0, 2)))

            # Exibe o frame no Pygame
            screen.blit(pygame_frame, (0, 0))

            if infoApertado == False:
                screen.blit(InfoIcon, (5, 5))
                # Desenha o poligono
                pygame.draw.polygon(screen, (255, 204, 0), [
                    (25, screen_height - 20),
                    (35, screen_height - 10),
                    (35, screen_height - 30),
                    (25, screen_height - 20)
                ])
                pygame.draw.polygon(screen, (255, 204, 0), [
                    (15, screen_height - 20),
                    (25, screen_height - 10),
                    (25, screen_height - 30),
                    (15, screen_height - 20)
                ])

                # Desenha a borda do poligono
                pygame.draw.polygon(screen, (0, 0, 0), [
                    (25, screen_height - 20),
                    (35, screen_height - 10),
                    (35, screen_height - 30),
                    (25, screen_height - 20)
                ], 1)

                pygame.draw.polygon(screen, (0, 0, 0), [
                    (15, screen_height - 20),
                    (25, screen_height - 10),
                    (25, screen_height - 30),
                    (15, screen_height - 20)
                ], 1)

            if infoApertado == True and info_clicked:
                screen.blit(info_menu, (0, 0))
                for i, (label, value) in enumerate(settings):
                    option_y = screen_height * 0.16 + i * (screen_height * 0.12)
                    text = font.render(f"{label}", True, (0, 0, 0))
                    values = font.render(f"{value}", True, (0, 0, 0))
                    screen.blit(text, ((screen_width * 0.04), option_y))
                    screen.blit(values, ((screen_width * 0.04), option_y + 28))

    elif ConfigApertado:
        if fps_bool == True and audio_bool == True:
            screen.blit(config, (0, 0))

        elif fps_bool == False and audio_bool == True:
            screen.blit(config2, (0, 0))

        elif fps_bool == True and audio_bool == False:
            screen.blit(config3, (0, 0))

        else:
            screen.blit(config4, (0, 0))

        # Botão do X
        if screen_width * 0.804 <= x <= screen_width * 0.837 and screen_height * 0.222 <= y <= screen_height * 0.276:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                ConfigApertado = False

        # Botão de Áudio
        elif screen_width * 0.660 <= x <= screen_width * 0.739 and screen_height * 0.354 <= y <= screen_height * 0.411:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not audio_clicked:
                audio_bool = not audio_bool
                audio_clicked = True  # Marca como clicado

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                audio_clicked = False  # Reseta o clique ao soltar

        # Botão de FPS
        elif screen_width * 0.400 <= x <= screen_width * 0.479 and screen_height * 0.354 <= y <= screen_height * 0.411:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not fps_clicked:
                fps_bool = not fps_bool
                fps_clicked = True  # Marca como clicado

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                fps_clicked = False  # Reseta o clique ao soltar

        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        chromatic_circles()

    # Atualiza a tela
    pygame.display.update()


cap.release()
cv2.destroyAllWindows()