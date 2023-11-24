import pygame
import random
import math


class Game:
    def __init__(self):

        # <editor-fold desc="Cores">
        # Inicialize as variáveis do jogo
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.hex1043B = (16, 64, 59)
        self.hex8AA6A3 = (138, 166, 163)
        self.hex127369 = (18, 115, 105)
        self.hexBFBFBF = (191, 191, 191)
        # </editor-fold>

        # <editor-fold desc="Screen">
        self.screen_width, self.screen_height = 760, 480
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Breakout Game")
        self.background_color = self.hex1043B
        # </editor-fold>

        # <editor-fold desc="Scores">
        self.score = 0
        self.font = pygame.font.Font(None, 36)
        self.score_text = self.font.render("Score: 0", False, self.hexBFBFBF)
        # </editor-fold>

        # <editor-fold desc="Bricks">
        self.bricks = []
        self.brick_width = 79
        self.brick_height = 20

        for row in range(5):
            for col in range(10):
                brick_x = col * (self.brick_width + 8)
                brick_y = row * (self.brick_height + 8) + 50
                brick_color = self.hex127369
                self.bricks.append((brick_x, brick_y, self.brick_width, self.brick_height, brick_color))
        # </editor-fold>

        # <editor-fold desc="Platform">
        self.platform_width, self.platform_height = 120, 10
        self.platform_x = (self.screen_width - self.platform_width) // 2
        self.platform_y = self.screen_height - 20
        self.platform_speed = 12
        # </editor-fold>

        # <editor-fold desc="Ball">
        self.ball_radius = 10
        self.ball_x = self.screen_width // 2
        self.ball_y = self.screen_height // 2
        self.ball_speed_x = 6
        self.ball_speed_y = -6
        # </editor-fold>

    def start_gameloop(self, center_card_x: int):

        # <editor-fold desc="Scores">
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", False, self.hexBFBFBF)
        self.screen.blit(score_text, (self.screen_width - 100, 10))

        # Apague o texto anterior
        self.screen.fill(self.background_color)

        # Renderize o novo texto do placar
        score_text = font.render(f"Score: {self.score}", True, self.hexBFBFBF)
        self.screen.blit(score_text, (self.screen_width - 150, 10))
        # </editor-fold>

        # <editor-fold desc="Bricks">
        for brick in self.bricks:
            brick_x, brick_y, brick_width, brick_height, brick_color = brick
            pygame.draw.rect(self.screen, brick_color, (brick_x, brick_y, brick_width, brick_height))

        # Verifique colisão da bola com os tijolos
        ball_rect = pygame.Rect(self.ball_x - self.ball_radius, self.ball_y - self.ball_radius, self.ball_radius * 2,
                                self.ball_radius * 2)
        bricks_to_remove = []
        for brick in self.bricks:
            brick_rect = pygame.Rect(brick[0], brick[1], brick[2], brick[3])
            if ball_rect.colliderect(brick_rect):
                bricks_to_remove.append(brick)

        for brick in bricks_to_remove:
            self.ball_speed_y = -self.ball_speed_y
            self.bricks.remove(brick)
            self.score += 1
        # </editor-fold>

        # <editor-fold desc="Platform">
        # Apague a posição anterior da plataforma preenchendo com a cor de fundo
        pygame.draw.rect(self.screen, self.background_color, (self.platform_x, self.platform_y, self.platform_width, self.platform_height))

        # Comandos que atualizam a posição da plataforma
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.platform_x -= self.platform_speed
        if keys[pygame.K_RIGHT]:
            self.platform_x += self.platform_speed

        # Verifique se a nova posição ultrapassa os limites da tela
        if self.platform_x < 0:
            self.platform_x = 0  # Impede que a plataforma vá além do limite esquerdo
        elif self.platform_x + self.platform_width > self.screen_width:
            self.platform_x = self.screen_width - self.platform_width  # Impede que a plataforma vá além do limite direito
        elif center_card_x is not None:
            if 0 <= center_card_x <= self.screen.get_width():
                self.platform_x = center_card_x
        else:
            self.platform_x = self.platform_x

        # Desenhe a plataforma na nova posição
        pygame.draw.rect(self.screen, self.hex8AA6A3, (self.platform_x, self.platform_y, self.platform_width, self.platform_height))
        # </editor-fold>

        # <editor-fold desc="Ball">

        pygame.draw.circle(self.screen, self.background_color, (int(self.ball_x), int(self.ball_y)), self.ball_radius)

        # Atualize a posição da bola
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y

        # Verifique colisão com a plataforma encima
        if self.ball_y + self.ball_radius >= self.platform_y and self.platform_x <= self.ball_x <= self.platform_x + self.platform_width:
            self.ball_speed_y = -self.ball_speed_y
        elif self.ball_x < self.platform_x and math.sqrt(
                (self.ball_x - self.platform_x) ** 2 + (self.ball_y - self.platform_y) ** 2) <= self.ball_radius:
            self.ball_speed_x = -self.ball_speed_x  # Inverta a direção horizontal da bola
        elif self.ball_x > self.platform_x + self.platform_width and math.sqrt(
                (self.ball_x - (self.platform_x + self.platform_width)) ** 2 + (
                        self.ball_y - self.platform_y) ** 2) <= self.ball_radius:
            self.ball_speed_x = -self.ball_speed_x  # Inverta a direção horizontal da bola

        # Verifique colisões com as bordas da tela
        if self.ball_x - self.ball_radius < 0 or self.ball_x + self.ball_radius > self.screen_width:
            self.ball_speed_x = -self.ball_speed_x  # Inverte a direção horizontal da bola se atingir as bordas

        if self.ball_y - self.ball_radius < 0:
            self.ball_speed_y = -self.ball_speed_y  # Inverte a direção vertical da bola se atingir a parte superior

        # Verifique se a bola caiu abaixo da tela
        if self.ball_y + self.ball_radius > self.screen_height:
            # Redefina a posição da bola
            self.ball_x = self.screen_width // 2
            self.ball_y = self.screen_height // 2
            self.ball_speed_x = random.choice(
                [-self.ball_speed_x, self.ball_speed_x])  # Escolha uma velocidade aleatória (-5 ou 5)
            self.ball_speed_y = self.ball_speed_y

        # Desenhe a bola
        pygame.draw.circle(self.screen, self.hex8AA6A3, (int(self.ball_x), int(self.ball_y)), self.ball_radius)
        pygame.display.flip()
        # </editor-fold>
