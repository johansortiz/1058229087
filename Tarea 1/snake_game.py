import pygame
import sys
import random
import cv2
import numpy as np

# Inicializa Pygame y la cámara de OpenCV.
pygame.init()
cap = cv2.VideoCapture(0)  # Abre la cámara predeterminada para capturar video.

# Configuración de la ventana de juego y la superficie de juego, incluyendo un área extra para mostrar el puntaje.
screen_width, screen_height = 800, 600  # Dimensiones de la pantalla del juego.
score_height = 40  # Altura de la zona donde se muestra el puntaje.
playSurface = pygame.display.set_mode((screen_width, screen_height + score_height))  # Superficie de juego.
pygame.display.set_caption("Snake Game")  # Título de la ventana del juego.

# Definición de colores para el juego.
yellow = pygame.Color(255, 255, 0)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)

# Controlador de FPS para manejar la velocidad de actualización de la pantalla.
fpsController = pygame.time.Clock()

# Configuración de parámetros iniciales del juego.
delta = 20  # Tamaño de los segmentos de la serpiente.
initial_speed = 5  # Velocidad inicial de la serpiente.
snake_speed = initial_speed  # Velocidad actual de la serpiente (puede aumentar durante el juego).
score = 0  # Puntaje inicial.

# Configuración del tamaño de la comida (el doble del tamaño de un segmento de la serpiente).
food_size = delta * 2

# Carga y escala de las imágenes de la serpiente y la comida.
snake_img = pygame.image.load('snake.png').convert_alpha()
food_img = pygame.image.load('food.png').convert_alpha()
snake_img = pygame.transform.scale(snake_img, (delta, delta))
food_img = pygame.transform.scale(food_img, (food_size, food_size))

# Función para mostrar la pantalla de inicio con opciones "Play" y "Quit".
def start_screen():
    """
    Esta función muestra la pantalla de inicio del juego, con botones para iniciar ("Play") o salir ("Quit").
    """
    title_img = pygame.image.load('inicio.jpg')  # Carga una imagen para el título.
    title_img = pygame.transform.scale(title_img, (400, 150))  # Escala la imagen.
    playSurface.fill((30, 30, 30))  # Rellena la pantalla con un color gris oscuro.

    # Centrando la imagen del título y agregando botones para iniciar o salir del juego.
    title_rect = title_img.get_rect(center=(screen_width // 2, 150))
    playSurface.blit(title_img, title_rect.topleft)

    font_options = pygame.font.SysFont('monaco', 50)
    play_rect = pygame.Rect((screen_width // 2 - 100, 300), (200, 60))  # Botón "Play".
    quit_rect = pygame.Rect((screen_width // 2 - 100, 400), (200, 60))  # Botón "Quit".

    # Dibuja los botones "Play" y "Quit" en la pantalla.
    draw_button(play_rect, "Play", font_options)
    draw_button(quit_rect, "Quit", font_options)
    pygame.display.flip()  # Actualiza la pantalla.

    # Espera la interacción del usuario para iniciar o salir del juego.
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si se cierra la ventana, termina el juego.
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Si se hace clic con el ratón.
                mouse_pos = pygame.mouse.get_pos()
                if play_rect.collidepoint(mouse_pos):  # Si se hace clic en "Play", inicia el juego.
                    waiting = False
                elif quit_rect.collidepoint(mouse_pos):  # Si se hace clic en "Quit", sale del juego.
                    pygame.quit()
                    sys.exit()
        # Cambia el color de los botones al pasar el mouse por encima.
        mouse_pos = pygame.mouse.get_pos()
        draw_button(play_rect, "Play", font_options, hover=play_rect.collidepoint(mouse_pos))
        draw_button(quit_rect, "Quit", font_options, hover=quit_rect.collidepoint(mouse_pos))
        pygame.display.flip()

# Función para dibujar botones con colores diferentes cuando hay hover.
def draw_button(rect, text, font, hover=False):
    """
    Esta función dibuja un botón en la pantalla, con cambios visuales cuando el usuario pasa el ratón por encima (hover).
    
    Args:
        rect (pygame.Rect): Área donde se dibuja el botón.
        text (str): Texto que se muestra en el botón.
        font (pygame.font.Font): Fuente a usar para el texto.
        hover (bool): Si el ratón está sobre el botón.
    """
    # Cambia los colores según si el botón está en hover o no.
    if hover:
        border_color = (255, 255, 255)  # Blanco.
        bg_color = (0, 255, 0)  # Verde para hover.
        text_color = (0, 0, 0)  # Negro para el texto.
    else:
        border_color = (255, 255, 255)  # Blanco.
        bg_color = (0, 0, 0)  # Negro para estado normal.
        text_color = (255, 255, 255)  # Blanco para el texto.

    # Dibuja el borde, fondo y texto del botón.
    pygame.draw.rect(playSurface, border_color, rect, border_radius=5)
    pygame.draw.rect(playSurface, bg_color, rect.inflate(-4, -4), border_radius=5)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    playSurface.blit(text_surface, text_rect)

# Función para mostrar la pantalla de "Game Over" y opciones de "Retry" y "Quit".
def game_over():
    """
    Esta función muestra la pantalla de "Game Over" cuando el jugador pierde, con botones para reiniciar o salir.
    """
    playSurface.fill((30, 30, 30))  # Rellena la pantalla con un color gris oscuro.
    font_title = pygame.font.SysFont('monaco', 72)
    font_options = pygame.font.SysFont('monaco', 50)
    font_score = pygame.font.SysFont('monaco', 40)

    # Muestra el texto "Game Over" y el puntaje alcanzado.
    game_over_text = font_title.render("Game Over", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 3))
    playSurface.blit(game_over_text, game_over_rect.topleft)

    score_text = font_score.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    playSurface.blit(score_text, score_rect.topleft)

    # Botones de "Retry" para reiniciar el juego y "Quit" para salir.
    retry_rect = pygame.Rect((screen_width // 2 - 125, screen_height // 2 + 50), (250, 60))
    quit_rect = pygame.Rect((screen_width // 2 - 125, screen_height // 2 + 150), (250, 60))

    # Dibuja los botones de "Retry" y "Quit".
    draw_button(retry_rect, "Retry", font_options)
    draw_button(quit_rect, "Quit", font_options)
    pygame.display.flip()  # Actualiza la pantalla.

    # Espera la interacción del usuario para reiniciar o salir.
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Si se cierra la ventana, termina el juego.
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:  # Si se hace clic con el ratón.
                mouse_pos = pygame.mouse.get_pos()
                if retry_rect.collidepoint(mouse_pos):  # Si selecciona "Retry", reinicia el juego.
                    return True
                elif quit_rect.collidepoint(mouse_pos):  # Si selecciona "Quit", sale del juego.
                    pygame.quit()
                    sys.exit()
        # Cambia el color de los botones con hover.
        mouse_pos = pygame.mouse.get_pos()
        draw_button(retry_rect, "Retry", font_options, hover=retry_rect.collidepoint(mouse_pos))
        draw_button(quit_rect, "Quit", font_options, hover=quit_rect.collidepoint(mouse_pos))
        pygame.display.flip()

# Función para mostrar el puntaje actual del jugador en la pantalla.
def show_score():
    """
    Esta función muestra el puntaje actual del jugador en la parte inferior de la pantalla.
    """
    font = pygame.font.SysFont('monaco', 32)
    playSurface.fill(black, (0, screen_height, screen_width, score_height))  # Limpia la zona del puntaje.
    score_surface = font.render(f"Score: {score}", True, white)  # Genera el texto del puntaje.
    playSurface.blit(score_surface, (10, screen_height + 10))  # Muestra el puntaje.

# Función para detectar el color amarillo en la imagen de la cámara.
def detect_color():
    """
    Esta función utiliza OpenCV para detectar el color amarillo en la imagen de la cámara.
    
    Returns:
        frame (np.array): El frame capturado de la cámara con el contorno amarillo dibujado si es detectado.
        (cx, cy) (tuple or None): Las coordenadas del centro del contorno amarillo más grande detectado, o None si no hay detección.
    """
    ret, frame = cap.read()  # Captura un frame de la cámara.
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # Convierte la imagen a espacio de color HSV.

    # Rango de color amarillo para la detección con OpenCV.
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)  # Crea una máscara para el color amarillo.
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # Encuentra contornos de la máscara.
    
    # Si hay contornos de color amarillo, encuentra el centro del contorno más grande.
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M['m00'] != 0:
            cx = int(M['m10'] / M['m00'])  # Coordenada x del centroide.
            cy = int(M['m01'] / M['m00'])  # Coordenada y del centroide.
            cv2.drawContours(frame, [largest_contour], -1, (0, 255, 0), 3)  # Dibuja el contorno.
            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)  # Dibuja un círculo en el centroide.
            return frame, (cx, cy)

    return frame, None  # Retorna el frame sin detección si no hay amarillo.

# Función para mover la serpiente según la dirección.
def move_snake(snakePos, changeto):
    """
    Esta función mueve la posición de la serpiente en la dirección especificada.
    
    Args:
        snakePos (list): Lista con la posición actual [x, y] de la cabeza de la serpiente.
        changeto (str): Dirección a la que se quiere mover la serpiente ("UP", "DOWN", "LEFT", "RIGHT").
    """
    if changeto == 'RIGHT':
        snakePos[0] += delta  # Mueve a la derecha.
    elif changeto == 'LEFT':
        snakePos[0] -= delta  # Mueve a la izquierda.
    elif changeto == 'DOWN':
        snakePos[1] += delta  # Mueve hacia abajo.
    elif changeto == 'UP':
        snakePos[1] -= delta  # Mueve hacia arriba.

# Lógica principal del juego.
def main_game():
    """
    Esta es la función principal que controla el flujo del juego. 
    Inicializa la posición de la serpiente y la comida, detecta colisiones y actualiza la pantalla.
    """
    global score, snake_speed

    # Configuración inicial de la posición de la serpiente y la comida.
    snakePos = [100, 50]  # Posición inicial de la cabeza de la serpiente.
    snakeBody = [[100, 50], [100 - delta, 50], [100 - 2 * delta, 50]]  # Segmentos iniciales de la serpiente.
    foodPos = [random.randrange(1, (screen_width - food_size) // delta) * delta,
               random.randrange(1, (screen_height - food_size) // delta) * delta]  # Posición aleatoria de la comida.
    foodSpawn = True  # Indicador para generar nueva comida.
    direction = 'RIGHT'  # Dirección inicial de movimiento.
    changeto = direction

    score = 0  # Puntaje inicial.
    snake_speed = initial_speed  # Velocidad inicial.

    # Bucle principal del juego.
    while True:
        frame, yellow_center = detect_color()  # Detecta el color amarillo en la cámara.
        
        # Cambia la dirección de la serpiente según la posición del color amarillo.
        if yellow_center:
            cx, cy = yellow_center
            # Decide la dirección dependiendo de la posición relativa del color amarillo.
            if abs(cx - screen_width // 2) > abs(cy - screen_height // 2):
                if cx < screen_width // 2:
                    changeto = 'RIGHT'
                else:
                    changeto = 'LEFT'
            else:
                if cy > screen_height // 2:
                    changeto = 'DOWN'
                else:
                    changeto = 'UP'

        move_snake(snakePos, changeto)  # Mueve la serpiente en la dirección indicada.

        # Si la serpiente come la comida, aumenta el puntaje y la velocidad.
        snakeBody.insert(0, list(snakePos))
        if (foodPos[0] <= snakePos[0] < foodPos[0] + food_size and
            foodPos[1] <= snakePos[1] < foodPos[1] + food_size):
            foodSpawn = False
            score += 1
            if score % 5 == 0:  # Aumenta la velocidad cada 5 puntos.
                snake_speed += 5
        else:
            snakeBody.pop()  # Si no come, elimina el último segmento (la serpiente no crece).

        # Genera nueva comida si es necesario.
        if not foodSpawn:
            foodPos = [random.randrange(1, (screen_width - food_size) // delta) * delta,
                       random.randrange(1, (screen_height - food_size) // delta) * delta]
            foodSpawn = True

        # Muestra el video de la cámara en el fondo del juego.
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(np.rot90(frame_rgb))
        playSurface.blit(pygame.transform.scale(frame_surface, (screen_width, screen_height)), (0, 0))
        
        # Dibuja la serpiente y la comida.
        for pos in snakeBody:
            playSurface.blit(snake_img, (pos[0], pos[1]))

        playSurface.blit(food_img, (foodPos[0], foodPos[1]))

        # Detecta colisiones con los bordes o consigo misma.
        if snakePos[0] >= screen_width or snakePos[0] < 0 or snakePos[1] >= screen_height or snakePos[1] < 0:
            if game_over():  # Si la serpiente choca con un borde, muestra "Game Over".
                return
        for block in snakeBody[1:]:
            if snakePos == block:  # Si la serpiente se come a sí misma, muestra "Game Over".
                if game_over():
                    return

        show_score()  # Muestra el puntaje actual.
        pygame.display.flip()  # Actualiza la pantalla.
        fpsController.tick(snake_speed)  # Controla la velocidad del juego.

# Bucle principal para iniciar el juego.
start_screen()
while True:
    main_game()

# Libera la cámara y cierra las ventanas de OpenCV al finalizar el juego.
cap.release()
cv2.destroyAllWindows()
