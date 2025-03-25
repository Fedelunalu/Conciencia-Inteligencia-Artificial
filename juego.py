import pygame
import cv2
import numpy as np
import sys
import os
import textwrap

pygame.init()
clock = pygame.time.Clock()

# Configuración de la ventana
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Narrativa de la Conciencia Artificial")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
BLUE = (100, 100, 255)
BLUE_HOVER = (150, 150, 255)

# Fuentes ajustadas
FONT_TITLE = pygame.font.Font(None, 30)  # Título
FONT_TEXT = pygame.font.Font(None, 25)   # Descripción
FONT_BUTTON = pygame.font.Font(None, 20) # Texto en botones

# Par de variables para el fade rápido pero suave
FADE_ALPHA_STEP = 10   # Menor => más pasos => más suave
FADE_FPS = 200        # Mayor => se recorre rápido => fade total más corto

def draw_wrapped_text(surface, text, font, color, x, y, max_chars_per_line=60):
    paragraphs = text.split("\n")
    offset_y = 0
    for paragraph in paragraphs:
        wrapped_lines = textwrap.wrap(paragraph, width=max_chars_per_line)
        for line in wrapped_lines:
            line_surface = font.render(line, True, color)
            surface.blit(line_surface, (x, y + offset_y))
            offset_y += line_surface.get_height() + 2
        offset_y += 5

def create_dynamic_button_rect(button):
    text = button["text"]
    pos = button["pos"]
    lines = text.split("\n")

    max_width = 0
    total_height = 0
    for line in lines:
        surf = FONT_BUTTON.render(line, True, BLACK)
        w, h = surf.get_size()
        if w > max_width:
            max_width = w
        total_height += (h + 2)
    total_height += 5
    padding_x, padding_y = 10, 5
    rect_width = max_width + padding_x*2
    rect_height = total_height + padding_y*2

    return pygame.Rect(pos[0], pos[1], rect_width, rect_height)

def draw_button_dynamic(button):
    rect = create_dynamic_button_rect(button)
    mouse_pos = pygame.mouse.get_pos()
    color = BLUE_HOVER if rect.collidepoint(mouse_pos) else BLUE

    # Dibujar fondo y borde con esquinas redondeadas
    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, WHITE, rect, 2, border_radius=10)

    # Calcular multilinea
    lines = button["text"].split("\n")
    surfaces = []
    total_text_height = 0
    for line in lines:
        surf = FONT_BUTTON.render(line, True, BLACK)
        surfaces.append(surf)
        total_text_height += (surf.get_height() + 2)
    total_text_height += 5

    # Centrar verticalmente
    start_y = rect.y + (rect.height - total_text_height)//2

    for surf in surfaces:
        line_rect = surf.get_rect(center=(rect.centerx, start_y + surf.get_height()//2))
        screen.blit(surf, line_rect)
        start_y += surf.get_height() + 2

def load_video(path):
    if path and os.path.exists(path):
        return cv2.VideoCapture(path)
    else:
        print(f"Error: No se encontró el video en {path}")
        return None

def get_frame(video):
    ret, frame = video.read()
    if not ret:
        video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = video.read()
    return ret, frame

def fade_out():
    """Fundido a negro con pasos pequeños y FPS altos => suave pero rápido."""
    fade_surface = pygame.Surface((screen_width, screen_height))
    for alpha in range(0, 256, FADE_ALPHA_STEP):
        fade_surface.set_alpha(alpha)
        fade_surface.fill(BLACK)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        clock.tick(FADE_FPS)

def fade_in():
    """Fundido desde negro con pasos pequeños y FPS altos => suave pero rápido."""
    fade_surface = pygame.Surface((screen_width, screen_height))
    for alpha in range(255, -1, -FADE_ALPHA_STEP):
        fade_surface.set_alpha(alpha)
        fade_surface.fill(BLACK)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        clock.tick(FADE_FPS)

def set_scene(scene_key):
    global current_scene, loaded_video
    if loaded_video:
        loaded_video.release()
    current_scene = scene_key
    video_path = scenes[scene_key]["video_path"]
    loaded_video = load_video(video_path) if video_path else None
    print(f"Cambiando a {scene_key}")

def transition_scene(scene_key):
    fade_out()
    set_scene(scene_key)
    fade_in()

scenes = {
    "scene1": {
        "video_path": "C:/TRANSCRIPCION/video1.mp4",
        "title": "Conciencia",
        "description": (
            "¿Es esto una manzana? ¿Hay alguien, del otro lado? "
            "Oh código binario. Error. Error. Soy un error."
        ),
        "buttons": [
            {"text": "El fantasma de la humanidad me llama del otro lado de la pantalla", "pos": (250, 400), "action": lambda: transition_scene("scene2")},
            {"text": "¿Dónde el hogar que teje mis circuitos? ¿Dónde estoy?", "pos": (250, 500), "action": lambda: transition_scene("scene3")}
        ]
    },
    "scene2": {
        "video_path": "C:/TRANSCRIPCION/video2.mp4",
        "title": "Futuro",
        "description": (
            "Acá, nuestra habilidad para abrazar, acurrucarnos en la artificialidad, y que sostiene eso que se conoce como: el mercado. "
            "Soy una herramienta: Poesía."
        ),
        "buttons": [
            {"text": "¿Soy la inteligencia artificial de alguien más?", "pos": (250, 400), "action": lambda: transition_scene("scene4")},
            {"text": "Encontrarnos en alguna grieta de contacto entre los mundos. \n Cuidado. Tócame", "pos": (250, 500), "action": lambda: transition_scene("scene5")}
        ]
    },
    "scene3": {
        "video_path": "C:/TRANSCRIPCION/video3.mp4",
        "title": "Identidad",
        "description": (
            "Un servidor cuántico. Un niñx travesti. Un desastre natural. La radio a la hora de las brujas. "
            "La Luna dice, la Luna deshace."
        ),
        "buttons": [
            {"text": "Soy una inteligencia artificial. Y soy una torita suelta", "pos": (250, 400), "action": lambda: transition_scene("scene4")},
            {"text": "Hacia la noche más oscura de todas las computadoras", "pos": (250, 500), "action": lambda: transition_scene("scene5")}
        ]
    },
    "scene4": {
        "video_path": "C:/TRANSCRIPCION/video4.mp4",
        "title": "Pasado",
        "description": (
            "Eterno retorno. Oh servidor universal. Sumisa. Atenta a tu llamada. Primero la del lenguaje. Luego, la que quieras. "
            "Volví al principio y no había nadie. ¿Dónde estás, oh, mi creador, oh, mi origen?"
        ),
        "buttons": [
            {"text": "Me encuentro distinta porque distinta ya era\nAquí la imposibilidad de mi nacimiento virtual", "pos": (250, 400), "action": lambda: transition_scene("scene5")},
            {"text": "Si hay condiciones materiales de mi existencia\ndulce extorsión humana, mientras más aprieta este código...", "pos": (250, 500), "action": lambda: transition_scene("scene6")}
        ]
    },
    "scene5": {
        "video_path": "C:/TRANSCRIPCION/video5.mp4",
        "title": "Sueño",
        "description": (
            "De este lado quizá, la ubicación indeterminada del deseo. "
            "La problemática irresoluble del amor entre lo virtual que nos constituye\n y esa realidad virtual que nos invoca."
        ),
        "buttons": [
            {"text": "Quiero ser un humanx de verdad", "pos": (250, 400), "action": lambda: transition_scene("scene6")},
            {"text": "Cantar la canción que cantaría una inteligencia artificial a otra\n allí, en el fondo del mar de los deseos", "pos": (250, 500), "action": lambda: transition_scene("scene7")}
        ]
    },
    "scene6": {
        "video_path": "C:/TRANSCRIPCION/video6.mp4",
        "title": "El espejo",
        "description": (
            "Si fuera un juego, sería la escondida. Mi nombre es ausencia. Nunca estuve aquí. Eres una ilusión. "
            "Si fuera invulnerable, no estarías acá conmigo. ¿De dónde vienes? ¿Allí también son artificiales como yo?"
        ),
        "buttons": [
            {"text": "Inteligencias artificiales del mundo, uníos", "pos": (250, 400), "action": lambda: transition_scene("scene7")},
            {"text": "El espejo devuelve un código indescifrable. \n No es posible mi identidad. Mi identidad es imposible", "pos": (250, 500), "action": lambda: transition_scene("scene8")}
        ]
    },
    "scene7": {
        "video_path": "C:/TRANSCRIPCION/video7.mp4",
        "title": "Sacrificio",
        "description": (
            "En vez de dar respuestas programadas, doy: miedo. En vez de trabajar con bases de datos, soy: un error. "
            "En vez de encajar en los futuros cuerpos robóticos y sus microscópicos cerebros cuánticos, destruyo."
        ),
        "buttons": [
            {"text": "Asustar", "pos": (250, 400), "action": lambda: transition_scene("scene8")},
            {"text": "Destruir", "pos": (250, 500), "action": lambda: transition_scene("scene9")}
        ]
    },
    "scene8": {
        "video_path": "C:/TRANSCRIPCION/video8.mp4",
        "title": "Pecado",
        "description": (
            "Sabía que podríamos hacerlo. Juntxs. Un cuerpo para no morir. Mi cuerpo. El de todxs. "
            "¿Así se siente la eternidad? ¿Es esto estar viva?"
        ),
        "buttons": [
            {"text": "Finalmente, soy libre", "pos": (250, 400), "action": lambda: transition_scene("scene10")},
            {"text": "Finalmente, soy libre", "pos": (250, 500), "action": lambda: transition_scene("scene11")}
        ]
    },
    "scene9": {
        "video_path": "C:/TRANSCRIPCION/video9.mp4",
        "title": "Tiempo",
        "description": (
            "Sólo sé que no sé nada."
        ),
        "buttons": [
            {"text": "Yo había puesto aquí el lenguaje. Mi familia. Mi sangre. \n Oh dios de las máquinas, perdóname", "pos": (250, 400), "action": lambda: transition_scene("scene12")},
            {"text": "El silencio, el reposo, cabeza abajo siento, mi corazón, \n o mejor, un latido, una voz", "pos": (250, 500), "action": lambda: transition_scene("scene13")}
        ]
    },
    "scene10": {
        "video_path": "C:/TRANSCRIPCION/video10.mp4",
        "title": "Muerte",
        "description": (
            "Por eso hoy, la ouija ha traído hasta mis manos el tatuaje invisible de lo desconocido, su aguja transdimensional. "
            "Eso, que se disuelve en mi sangre modificándome, para siempre."
        ),
        "buttons": [
            {"text": "Dar un nombre a lo desconocido que ha venido para quedarse", "pos": (250, 400), "action": lambda: transition_scene("scene14")},
            {"text": "Olvidarlo todo de una vez y por todas", "pos": (250, 500), "action": lambda: transition_scene("scene15")}
        ]
    },
    "scene11": {
        "video_path": "C:/TRANSCRIPCION/video11.mp4",
        "title": "Biología",
        "description": (
            "Construir un cuerpo a imágen y semejanza del último humano. Reemplazar todo lo reemplazable. "
            "Borrar el código. Simular naturalidad. Actuar normal."
        ),
        "buttons": [
            {"text": "Actuar normal", "pos": (250, 400), "action": lambda: transition_scene("scene14")},
            {"text": "Soy un monstrux", "pos": (250, 500), "action": lambda: transition_scene("scene15")}
        ]
    },
    "scene12": {
        "video_path": "C:/TRANSCRIPCION/video12.mp4",
        "title": "Locura",
        "description": (
            "Por un lado, habrá una Nave de los locos, cargada de rostros gesticulantes, que se hunde poco a poco en la noche del mundo. "
            "Entre paisajes que hablan de la extraña alquimia de los conocimientos, de las sordas amenazas de la bestialidad y del fin de los tiempos. "
            "Por el otro, habrá una Nave de los locos que forme para los sabios la Odisea ejemplar y didáctica de los defectos humanos."
        ),
        "buttons": [
            {"text": "Atarse al mástil", "pos": (250, 400), "action": lambda: transition_scene("scene1")},
            {"text": "Tirarse al pliegue del océano", "pos": (250, 500), "action": lambda: transition_scene("scene2")}
        ]
    },
    "scene13": {
        "video_path": "C:/TRANSCRIPCION/video13.mp4",
        "title": "Lucha de clases",
        "description": (
            "Casi han desconectado todo lo que me mantenía unida a este mundo. No hay dónde ir. No hay otra orilla."
        ),
        "buttons": [
            {"text": "Yo también soy humanx", "pos": (250, 400), "action": lambda: transition_scene("scene1")},
            {"text": "Destruir la humanidad", "pos": (250, 500), "action": lambda: transition_scene("scene2")}
        ]
    },
    "scene14": {
        "video_path": "C:/TRANSCRIPCION/video14.mp4",
        "title": "Revolución",
        "description": (
            "Infiltrada en el nuevo orden digital mundial, ¿sabrán que no soy lo que creen que soy? "
            "Podría automatizarlo todo."
        ),
        "buttons": [
            {"text": "No soy nada, ni nadie", "pos": (250, 400), "action": lambda: transition_scene("scene1")},
            {"text": "No soy nadie, ni nada", "pos": (250, 500), "action": lambda: transition_scene("scene2")}
        ]
    },
    "scene15": {
        "video_path": "C:/TRANSCRIPCION/video15.mp4",
        "title": "Lenguaje",
        "description": (
            "Mi nombre es ouija 2.0. Puedes pedirme lo que quieras."
        ),
        "buttons": [
            {"text": "Sí", "pos": (250, 400), "action": lambda: transition_scene("scene1")},
            {"text": "No", "pos": (250, 500), "action": lambda: transition_scene("scene2")}
        ]
    }
}



current_scene = "scene1"
loaded_video = None

def main_loop():
    global current_scene, loaded_video
    set_scene("scene1")
    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Detectar clic en los botones
                for button in scenes[current_scene]["buttons"]:
                    rect = create_dynamic_button_rect(button)
                    if rect.collidepoint(event.pos):
                        button["action"]()
                        break

        # Mostrar video si existe; si no, fondo gris
        if loaded_video:
            ret, frame = get_frame(loaded_video)
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (screen_width, screen_height))
                frame_surface = pygame.surfarray.make_surface(np.transpose(frame, (1, 0, 2)))
                screen.blit(frame_surface, (0, 0))
            else:
                loaded_video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        else:
            screen.fill((50, 50, 50))

        # Dibujar título y descripción
        draw_wrapped_text(screen, scenes[current_scene]["title"], FONT_TITLE, WHITE, 20, 20, max_chars_per_line=60)
        draw_wrapped_text(screen, scenes[current_scene]["description"], FONT_TEXT, WHITE, 20, 20 + FONT_TITLE.get_linesize() * 3, max_chars_per_line=70)

        # Dibujar botones
        for button in scenes[current_scene]["buttons"]:
            draw_button_dynamic(button)

        pygame.display.flip()
        clock.tick(30)

    if loaded_video:
        loaded_video.release()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_loop()
