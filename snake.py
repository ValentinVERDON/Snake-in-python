import pygame
import random

class Apple:
    def __init__(self, screen, rect_x, rect_y, rect_width, rect_height):
        self.screen = screen
        self.rect_x = rect_x
        self.rect_y = rect_y
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.border_color = (255, 0, 0)
        self.rect_size = 10
        self.apple_position_x, self.apple_position_y = self.random_position()

    def random_position(self):
        self.apple_x = random.randint(self.rect_x, self.rect_x + self.rect_width - self.rect_size)
        self.apple_y = random.randint(self.rect_y, self.rect_y + self.rect_height - self.rect_size)
        
        self.apple_x = (self.apple_x // self.rect_size) * self.rect_size
        self.apple_y = (self.apple_y // self.rect_size) * self.rect_size
        return self.apple_x, self.apple_y

    def update_position(self):
        self.apple_position_x, self.apple_position_y = self.random_position()

    def draw_apple(self):
        pygame.draw.rect(self.screen, self.border_color, pygame.Rect(self.apple_position_x, self.apple_position_y, self.rect_size, self.rect_size))


class SnakePlayer:
    def __init__(self, screen, rect_x, rect_y, rect_width, rect_height):
        self.screen = screen
        self.rect_x = rect_x
        self.rect_y = rect_y
        self.rect_width = rect_width
        self.rect_height = rect_height
        self.border_color = (0, 128, 0)
        self.rect_size = 10
        self.player_position_x, self.player_position_y = self.random_position_init()
        self.can_move = True  # Indicateur pour autoriser le mouvement
        self.score = 0

    def random_position_init(self):
        self.player_x = random.randint(self.rect_x, self.rect_x + self.rect_width - self.rect_size)
        self.player_y = random.randint(self.rect_y, self.rect_y + self.rect_height - self.rect_size)
        
        self.player_x = (self.player_x // self.rect_size) * self.rect_size
        self.player_y = (self.player_y // self.rect_size) * self.rect_size
        return self.player_x, self.player_y

    def draw_player(self):
        pygame.draw.rect(self.screen, self.border_color, pygame.Rect(self.player_position_x, self.player_position_y, self.rect_size, self.rect_size))
    
    def move_player(self):
        keys = pygame.key.get_pressed()
        
        # Seulement autoriser le mouvement si la touche est pressée pour la première fois
        if self.can_move:
            if keys[pygame.K_LEFT] or keys[pygame.K_q]:
                self.player_position_x -= self.rect_size
                self.can_move = False
            elif keys[pygame.K_RIGHT] or keys[pygame.K_f]:
                self.player_position_x += self.rect_size
                self.can_move = False
            elif keys[pygame.K_UP] or keys[pygame.K_z]:
                self.player_position_y -= self.rect_size
                self.can_move = False
            elif keys[pygame.K_DOWN] or keys[pygame.K_e]:
                self.player_position_y += self.rect_size
                self.can_move = False
        
        # Vérifier si toutes les touches sont relâchées pour réactiver le mouvement
        if not any(keys):
            self.can_move = True


class Jeu:
    def __init__(self, screen, rect_x, rect_y, rect_width, rect_height):
        self.screen = screen
        self.rect_x = rect_x
        self.rect_y = rect_y
        self.rect_width = rect_width
        self.rect_height = rect_height

        self.player = SnakePlayer(screen, rect_x, rect_y, rect_width, rect_height)
        self.apple = Apple(screen, rect_x, rect_y, rect_width, rect_height)

    def check_collision(self):
        if (self.player.player_position_x < self.rect_x or 
            self.player.player_position_x >= self.rect_x + self.rect_width or
            self.player.player_position_y < self.rect_y or
            self.player.player_position_y >= self.rect_y + self.rect_height):
            print("Game Over")
            pygame.quit()  # Quitter le jeu lorsque le joueur sort
        if self.player.player_position_x == self.apple.apple_position_x and self.player.player_position_y == self.apple.apple_position_y:
            self.apple.update_position()  # Mettre à jour la position de l'apple
            self.player.score += 1
            print(f"Score: {self.player.score}")
            

    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(self.rect_x, self.rect_y, self.rect_width, self.rect_height), 1)
        self.player.draw_player()
        self.apple.draw_apple()
        pygame.display.flip()

    def run_game(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if running:
                self.player.move_player()
                self.check_collision()
                self.draw()

        pygame.quit()

# Exemple d'utilisation
if __name__ == "__main__":
    pygame.init()
    game_window = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Snake Game")

    rect_width, rect_height = 500, 300
    rect_size = 10
    rect_x = ((600 - rect_width) // 2) // rect_size * rect_size  # Position x multiple de 10
    rect_y = ((400 - rect_height) // 2) // rect_size * rect_size  # Position y multiple de 10
    rect_width = (rect_width // rect_size) * rect_size
    rect_height = (rect_height // rect_size) * rect_size

    jeu = Jeu(game_window, rect_x, rect_y, rect_width, rect_height)
    jeu.run_game()
