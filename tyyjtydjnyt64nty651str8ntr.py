import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
GROUND_HEIGHT = 100
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10
TIMER_LIMIT = 60  # Таймер в секундах
PLATFORM_WIDTH = 50  # Ширина платформы
PLATFORM_HEIGHT = 50  # Высота платформы

# Цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)  # Цвет картошки

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.velocity_y = 0
        self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False

    def update(self, platforms):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Проверка коллизий с платформами
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y >= 0:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True
                break

        # Проверка выхода за пределы экрана
        if self.rect.y >= SCREEN_HEIGHT - GROUND_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.rect.height
            self.velocity_y = 0
            self.on_ground = True
            
    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)


class Potato:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 30)
        self.color = ORANGE  # Цвет картошки

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class Platform:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.rect)


def load_level(filename):
    platforms = []
    player_pos = None
    potato_pos = None

    with open(filename, 'r') as file:
        for y, line in enumerate(file):
            for x, char in enumerate(line.strip()):
                if char == '#':
                    platforms.append(Platform(x * PLATFORM_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT - (y * PLATFORM_HEIGHT)))
                elif char == '&':
                    player_pos = (x * 50, SCREEN_HEIGHT - GROUND_HEIGHT - (y * 50))
                elif char == '@':
                    potato_pos = (x * 50, SCREEN_HEIGHT - GROUND_HEIGHT - (y * 50))
    
    return platforms, player_pos, potato_pos


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Спасение картошки")
    clock = pygame.time.Clock()

    # Загрузка уровня из текстового файла
    platforms, player_pos, potato_pos = load_level('level.txt')

    player = Player(*player_pos)
    potato = Potato(*potato_pos)

    game_over = False
    potato_saved = False
    start_time = pygame.time.get_ticks()  # Запоминаем время начала игры

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and game_over:
                mouse_x, mouse_y = event.pos
                if restart_button.collidepoint(mouse_x, mouse_y):
                    main()  # Перезапуск игры

        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_LEFT]:
                player.rect.x -= 5
            if keys[pygame.K_RIGHT]:
                player.rect.x += 5
            if keys[pygame.K_SPACE]:
                player.jump()

            player.update(platforms)

            # Проверка столкновения с картошкой
            if player.rect.colliderect(potato.rect):
                potato_saved = True
                game_over = True

            # Проверка выхода за пределы экрана
            if player.rect.y > SCREEN_HEIGHT or player.rect.x < 0 or player.rect.x > SCREEN_WIDTH:
                game_over = True

            # Проверка времени
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Время в секундах
            if elapsed_time > TIMER_LIMIT and not potato_saved:
                game_over = True

        # Отрисовка
        screen.fill(WHITE)
        player.draw(screen)
        potato.draw(screen)  # Отрисовка картошки
        for platform in platforms:
            platform.draw(screen)  # Отрисовка платформ

        if game_over:
            font = pygame.font.Font(None, 74)
            if potato_saved:
                text = font.render("Картоха спасена!", True, GREEN)
            else:
                text = font.render("Ааа я стал пюрешкой!", True, RED)

            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

            # Кнопка перезапуска
            restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50)
            pygame.draw.rect(screen, GREEN, restart_button)
            button_font = pygame.font.Font(None, 36)
            button_text = button_font.render("Перезапуск", True, WHITE)
            screen.blit(button_text, (restart_button.x + restart_button.width // 2 - button_text.get_width() // 2,
                                       restart_button.y + restart_button.height // 2 - button_text.get_height() // 2))

        # Отрисовка земли
        pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT))
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
