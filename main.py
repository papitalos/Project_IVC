import cv2
import pygame
import game
import segmentation
import cam

# Inicializa o game
pygame.init()
# Inicializa as variaveis
game = game.Game()

metodo = 1
# Inicializa loops
running = True
while running:
    center_card_x = cam.start_camloop(metodo)
    game.start_gameloop(center_card_x)
    # Verifica se alguma tecla foi pressionada
    key = cv2.waitKey(1) & 0xFF
    if key == ord('1'):
        metodo = 1
        cv2.destroyAllWindows()
    elif key == ord('2'):
        metodo = 2
        cv2.destroyAllWindows()
    elif key == ord('3'):
        metodo = 3
        cv2.destroyAllWindows()
    elif key == ord('4'):
        metodo = 4
        cv2.destroyAllWindows()

    # Se a tecla 'q' for pressionada, encerra o loop
    if key == ord('q'):
        running = False

# Libera as memorias, fecha o jogo e destroi as janelas
running = False
pygame.quit()
cam.get_cap().release()
cv2.destroyAllWindows()
