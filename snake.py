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

    # Coordonées aléatoire de la pomme 
    def random_position(self):
        self.apple_x = random.randint(self.rect_x, self.rect_x + self.rect_width - self.rect_size)
        self.apple_y = random.randint(self.rect_y, self.rect_y + self.rect_height - self.rect_size)
        
        self.apple_x = (self.apple_x // self.rect_size) * self.rect_size
        self.apple_y = (self.apple_y // self.rect_size) * self.rect_size
        return self.apple_x, self.apple_y

    # Update la position de la pomme
    def update_position(self):
        self.apple_position_x, self.apple_position_y = self.random_position()

    def draw_apple(self):
        apple_radius = self.rect_size // 2  # Calculating radius of the circle
        apple_center = (self.apple_position_x + apple_radius, self.apple_position_y + apple_radius)  # Center of the circle
        pygame.draw.circle(self.screen, self.border_color, apple_center, apple_radius)


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
        self.segments = [{
            "x": self.player_position_x,
            "y": self.player_position_y
        }]
        self.direction = None  # Direction initially set to None (immobile)
        self.score = 0
        self.speed = 10

    def random_position_init(self):
        self.player_x = random.randint(self.rect_x, self.rect_x + self.rect_width - self.rect_size)
        self.player_y = random.randint(self.rect_y, self.rect_y + self.rect_height - self.rect_size)
        
        self.player_x = (self.player_x // self.rect_size) * self.rect_size
        self.player_y = (self.player_y // self.rect_size) * self.rect_size
        return self.player_x, self.player_y

    def draw_player(self):
        for segment in self.segments:
            pygame.draw.rect(self.screen, self.border_color, pygame.Rect(segment["x"], segment["y"], self.rect_size, self.rect_size))
    
    def handle_keys(self):
        keys = pygame.key.get_pressed()
        new_direction = self.direction

        if (keys[pygame.K_LEFT] or keys[pygame.K_q]) and self.direction != "RIGHT":
            new_direction = "LEFT"
        elif (keys[pygame.K_RIGHT] or keys[pygame.K_f]) and self.direction != "LEFT":
            new_direction = "RIGHT"
        elif (keys[pygame.K_UP] or keys[pygame.K_z]) and self.direction != "DOWN":
            new_direction = "UP"
        elif (keys[pygame.K_DOWN] or keys[pygame.K_e]) and self.direction != "UP":
            new_direction = "DOWN"

        if new_direction != self.direction:
            self.direction = new_direction

    def move_player(self):
        if self.direction is None:
            return
        
        # Move segments from back to front
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i]["x"] = self.segments[i - 1]["x"]
            self.segments[i]["y"] = self.segments[i - 1]["y"]

        # Move the head segment
        if self.direction == "LEFT":
            self.segments[0]["x"] -= self.rect_size
        elif self.direction == "RIGHT":
            self.segments[0]["x"] += self.rect_size
        elif self.direction == "UP":
            self.segments[0]["y"] -= self.rect_size
        elif self.direction == "DOWN":
            self.segments[0]["y"] += self.rect_size

    def grow(self):
        last_segment = self.segments[-1]
        new_segment = {
            "x": last_segment["x"],
            "y": last_segment["y"]
        }
        self.segments.append(new_segment)
                                    
class Jeu:
    def __init__(self, screen, rect_x, rect_y, rect_width, rect_height):
        self.screen = screen
        self.rect_x = rect_x
        self.rect_y = rect_y
        self.rect_width = rect_width
        self.rect_height = rect_height

        self.player = SnakePlayer(screen, rect_x, rect_y, rect_width, rect_height)
        self.apple = Apple(screen, rect_x, rect_y, rect_width, rect_height)

        self.font = pygame.font.Font(None, 24)  # Initialize font with smaller size

    def check_collision(self):
        # Check collision with walls
        if (self.player.segments[0]["x"] < self.rect_x or 
            self.player.segments[0]["x"] >= self.rect_x + self.rect_width or
            self.player.segments[0]["y"] < self.rect_y or
            self.player.segments[0]["y"] >= self.rect_y + self.rect_height):
            print("Game Over")
            pygame.quit()  # Quitter le jeu lorsque le joueur sort

        # Check collision with self
        for segment in self.player.segments[1:]:
            if self.player.segments[0]["x"] == segment["x"] and self.player.segments[0]["y"] == segment["y"]:
                print("Game Over")
                pygame.quit()  # Quitter le jeu lorsque le joueur touche son propre corps

        # Check collision with apple
        if self.player.segments[0]["x"] == self.apple.apple_position_x and self.player.segments[0]["y"] == self.apple.apple_position_y:
            self.apple.update_position()  # Mettre à jour la position de l'apple
            self.player.grow()  # Add a new segment
            self.player.score += 1  # Increment score by 1
            self.player.speed += 2  # Increment speed by 2
            print(f"Score: {self.player.score}, Speed: {self.player.speed}")

    def draw(self):
        self.screen.fill((0, 0, 0))
        pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(self.rect_x, self.rect_y, self.rect_width, self.rect_height), 1)
        self.player.draw_player()
        self.apple.draw_apple()

        # Draw score, speed, and length
        score_text = self.font.render(f"Score: {self.player.score}", True, (255, 255, 255))
        speed_text = self.font.render(f"Speed: {self.player.speed}", True, (255, 255, 255))
        length_text = self.font.render(f"Length: {len(self.player.segments)}", True, (255, 255, 255))

        self.screen.blit(score_text, (self.rect_x , self.rect_y - 40))
        self.screen.blit(speed_text, (self.rect_x + 150 , self.rect_y - 40))
        self.screen.blit(length_text, (self.rect_x + 300, self.rect_y - 40))

        pygame.display.flip()

    def run_game(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if running:
                self.player.handle_keys()
                self.player.move_player()
                self.check_collision()
                self.draw()
                
            clock.tick(self.player.speed)  # Control the speed of the game

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
