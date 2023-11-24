import cv2
import pygame
import game
import segmentation
import cam

# Inicializa o game
pygame.init()
# Inicializa as variaveis
game = game.Game()
segmentation.create_trackbar()

# Inicializa loops
running = True
while running:
    center_card_x = cam.start_camloop()
    game.start_gameloop(center_card_x)

    # Fim do loop
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera as memorias, fecha o jogo e destroi as janelas
running = False
pygame.quit()
cam.get_cap().release()
cv2.destroyAllWindows()
