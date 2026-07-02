import pygame
import random
import sys

# 1. ตั้งค่าเริ่มต้นให้กับ Pygame
pygame.init()

# 2. กำหนดขนาดหน้าจอและขนาดบล็อก
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 20
GRID_COUNT = SCREEN_WIDTH // GRID_SIZE

# 3. กำหนดคู่สีที่ดูสบายตา (สไตล์มินิมอล)
COLOR_BG = (240, 244, 248)       # สีพื้นหลังเทาอมฟ้าอ่อน
COLOR_SNAKE_HEAD = (46, 117, 89) # สีหัวงูเขียวเข้ม
COLOR_SNAKE_BODY = (67, 160, 71) # สีตัวงูเขียวสว่าง
COLOR_FOOD = (229, 57, 53)       # สีไข่สีแดง
COLOR_TEXT = (33, 33, 33)        # สีข้อความตัวหนังสือ

# 4. ตั้งค่าทิศทางการเคลื่อนที่
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Classic Snake Game 🐍")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Segoe UI", 24, bold=True)
        self.reset_game()

    def reset_game(self):
        # จุดเริ่มต้นของงู (กลางหน้าจอ) และทิศทางเริ่มต้น
        self.snake = [(GRID_COUNT // 2, GRID_COUNT // 2)]
        self.direction = RIGHT
        self.score = 0
        self.spawn_food()
        self.game_over = False

    def spawn_food(self):
        # สุ่มตำแหน่งไข่ใหม่ โดยไม่ให้ทับกับตัวงู
        while True:
            self.food = (random.randint(0, GRID_COUNT - 1), random.randint(0, GRID_COUNT - 1))
            if self.food not in self.snake:
                break

    def handle_events(self):
        # ตรวจจับการกดคีย์บอร์ดเพื่อเปลี่ยนทิศทาง
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if self.game_over:
                    if event.key == pygame.K_SPACE: # กด Spacebar เพื่อเล่นใหม่
                        self.reset_game()
                else:
                    if event.key == pygame.K_UP and self.direction != DOWN:
                        self.direction = UP
                    elif event.key == pygame.K_DOWN and self.direction != UP:
                        self.direction = DOWN
                    elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                        self.direction = LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                        self.direction = RIGHT

    def update(self):
        if self.game_over:
            return

        # คำนวณตำแหน่งหัวงูตัวใหม่
        cur_head = self.snake[0]
        new_head = (cur_head[0] + self.direction[0], cur_head[1] + self.direction[1])

        # ตรวจสอบว่าชนกำแพงหรือชนตัวเองหรือไม่
        if (new_head[0] < 0 or new_head[0] >= GRID_COUNT or
            new_head[1] < 0 or new_head[1] >= GRID_COUNT or
            new_head in self.snake):
            self.game_over = True
            return

        # เพิิ่มหัวงูไปที่ตำแหน่งใหม่
        self.snake.insert(0, new_head)

        # ตรวจสอบว่ากินไข่สำเร็จไหม
        if new_head == self.food:
            self.score += 1
            self.spawn_food()
        else:
            # ถ้าไม่ได้กินไข่ ให้ตัดหางงูออกเพื่อให้ความยาวเท่าเดิม
            self.snake.pop()

    def draw(self):
        # วาดพื้นหลัง
        self.screen.fill(COLOR_BG)

        # วาดตัวงู (แยกหัวและตัวคนละสีเพื่อให้ดูง่าย)
        for i, segment in enumerate(self.snake):
            rect = pygame.Rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2)
            color = COLOR_SNAKE_HEAD if i == 0 else COLOR_SNAKE_BODY
            pygame.draw.rect(self.screen, color, rect, border_radius=4)

        # วาดไข่ (ทรงกลมมน)
        food_rect = pygame.Rect(self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2)
        pygame.draw.rect(self.screen, COLOR_FOOD, food_rect, border_radius=10)

        # วาดคะแนนปัจจุบันบนมุมซ้าย
        score_text = self.font.render(f"Score: {self.score}", True, COLOR_TEXT)
        self.screen.blit(score_text, (15, 15))

        # หน้าจอ Game Over
        if self.game_over:
            # วาดแผงข้อความโปร่งแสงทับตรงกลาง
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 200)) 
            self.screen.blit(overlay, (0, 0))

            go_text = self.font.render("GAME OVER", True, COLOR_FOOD)
            restart_text = self.font.render("Press SPACE to Restart", True, COLOR_TEXT)
            
            self.screen.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
            self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            # ความเร็วของงู (10 เฟรมต่อวินาที - ยิ่งตัวเลขเยอะงูยิ่งวิ่งไว)
            self.clock.tick(10)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()

