import pygame
import sys
import random
import os
import time

# 初始化pygame
pygame.init()

# 屏幕尺寸
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('植物大战僵尸')

# 颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

# 帧率控制
clock = pygame.time.Clock()
FPS = 30

# 游戏资源路径
RESOURCE_DIR = os.path.join(os.path.dirname(__file__), "resources")
if not os.path.exists(RESOURCE_DIR):
    os.makedirs(RESOURCE_DIR)

# 游戏参数
GRID_SIZE = 80  # 格子大小
GRID_ROWS = 5  # 网格行数
GRID_COLS = 9  # 网格列数
GRID_OFFSET_X = 50  # 网格X偏移
GRID_OFFSET_Y = 100  # 网格Y偏移
SUN_FALL_SPEED = 2  # 阳光下落速度
SUN_GENERATION_TIME = 5  # 阳光生成时间间隔(秒)
ZOMBIE_GENERATION_TIME = 10  # 僵尸生成初始时间间隔(秒)

# 植物类
class Plant:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = GRID_OFFSET_X + col * GRID_SIZE
        self.y = GRID_OFFSET_Y + row * GRID_SIZE
        self.health = 100
        self.cooldown = 0
        self.last_attack = 0
        self.attack_interval = 2  # 攻击间隔(秒)
        self.image = None
    
    def update(self, current_time):
        pass
    
    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (self.x, self.y))
        else:
            # 默认植物绘制
            pygame.draw.rect(surface, GREEN, (self.x, self.y, GRID_SIZE, GRID_SIZE), 0)
            pygame.draw.rect(surface, BLACK, (self.x, self.y, GRID_SIZE, GRID_SIZE), 2)
        
        # 健康条
        health_width = (GRID_SIZE - 10) * (self.health / 100)
        pygame.draw.rect(surface, RED, (self.x + 5, self.y + 5, health_width, 5))

# 向日葵类
class Sunflower(Plant):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.name = "向日葵"
        self.cost = 50
        self.health = 80
        self.sun_generation_time = 10  # 生成阳光的时间间隔(秒)
        self.last_generation = time.time()
    
    def update(self, current_time, suns):
        if current_time - self.last_generation >= self.sun_generation_time:
            self.last_generation = current_time
            suns.append(Sun(self.x + GRID_SIZE//4, self.y, is_falling=False))
    
    def draw(self, surface):
        # 绘制向日葵
        pygame.draw.rect(surface, (255, 255, 0), (self.x, self.y, GRID_SIZE, GRID_SIZE), 0)
        pygame.draw.rect(surface, BLACK, (self.x, self.y, GRID_SIZE, GRID_SIZE), 2)
        
        # 绘制脸
        face_center = (self.x + GRID_SIZE//2, self.y + GRID_SIZE//2)
        pygame.draw.circle(surface, (139, 69, 19), face_center, GRID_SIZE//3)
        
        # 绘制花瓣
        petal_radius = GRID_SIZE//4
        pygame.draw.circle(surface, (255, 255, 0), (face_center[0], face_center[1] - petal_radius), petal_radius)
        pygame.draw.circle(surface, (255, 255, 0), (face_center[0] + petal_radius, face_center[1]), petal_radius)
        pygame.draw.circle(surface, (255, 255, 0), (face_center[0], face_center[1] + petal_radius), petal_radius)
        pygame.draw.circle(surface, (255, 255, 0), (face_center[0] - petal_radius, face_center[1]), petal_radius)
        
        # 健康条
        health_width = (GRID_SIZE - 10) * (self.health / 80)
        pygame.draw.rect(surface, RED, (self.x + 5, self.y + 5, health_width, 5))

# 豌豆射手类
class Peashooter(Plant):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.name = "豌豆射手"
        self.cost = 100
        self.health = 100
        self.attack_power = 20
        self.attack_interval = 1.5  # 攻击间隔(秒)
        self.last_attack = time.time()
    
    def update(self, current_time, bullets, zombies):
        # 检查这一行是否有僵尸
        zombies_in_row = [z for z in zombies if z.row == self.row]
        if zombies_in_row and current_time - self.last_attack >= self.attack_interval:
            self.last_attack = current_time
            bullets.append(Bullet(self.x + GRID_SIZE, self.y + GRID_SIZE//2, self.row, self.attack_power))
    
    def draw(self, surface):
        # 绘制豌豆射手
        pygame.draw.rect(surface, (0, 200, 0), (self.x, self.y, GRID_SIZE, GRID_SIZE), 0)
        pygame.draw.rect(surface, BLACK, (self.x, self.y, GRID_SIZE, GRID_SIZE), 2)
        
        # 绘制头部
        head_center = (self.x + GRID_SIZE*2//3, self.y + GRID_SIZE//2)
        pygame.draw.circle(surface, (0, 100, 0), head_center, GRID_SIZE//3)
        
        # 绘制嘴巴(发射口)
        pygame.draw.circle(surface, BLACK, (head_center[0] + GRID_SIZE//4, head_center[1]), GRID_SIZE//8)
        
        # 健康条
        health_width = (GRID_SIZE - 10) * (self.health / 100)
        pygame.draw.rect(surface, RED, (self.x + 5, self.y + 5, health_width, 5))

# 坚果墙类
class WallNut(Plant):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.name = "坚果墙"
        self.cost = 50
        self.health = 400  # 较高的生命值
    
    def draw(self, surface):
        # 绘制坚果墙
        pygame.draw.rect(surface, BROWN, (self.x, self.y, GRID_SIZE, GRID_SIZE), 0)
        pygame.draw.rect(surface, BLACK, (self.x, self.y, GRID_SIZE, GRID_SIZE), 2)
        
        # 绘制面部特征
        face_center = (self.x + GRID_SIZE//2, self.y + GRID_SIZE//2)
        
        # 眼睛
        pygame.draw.circle(surface, BLACK, (face_center[0] - 10, face_center[1] - 10), 5)
        pygame.draw.circle(surface, BLACK, (face_center[0] + 10, face_center[1] - 10), 5)
        
        # 根据健康程度绘制不同表情
        if self.health > 266:
            # 微笑
            pygame.draw.arc(surface, BLACK, (face_center[0] - 15, face_center[1], 30, 20), 0, 3.14, 2)
        elif self.health > 133:
            # 平淡
            pygame.draw.line(surface, BLACK, (face_center[0] - 15, face_center[1] + 10), 
                             (face_center[0] + 15, face_center[1] + 10), 2)
        else:
            # 忧虑
            pygame.draw.arc(surface, BLACK, (face_center[0] - 15, face_center[1] + 10, 30, 20), 3.14, 6.28, 2)
        
        # 健康条
        health_width = (GRID_SIZE - 10) * (self.health / 400)
        pygame.draw.rect(surface, RED, (self.x + 5, self.y + 5, health_width, 5))

# 子弹类
class Bullet:
    def __init__(self, x, y, row, damage):
        self.x = x
        self.y = y
        self.row = row
        self.damage = damage
        self.speed = 10
        self.active = True
    
    def update(self):
        self.x += self.speed
        if self.x > SCREEN_WIDTH:
            self.active = False
    
    def draw(self, surface):
        pygame.draw.circle(surface, (0, 255, 0), (int(self.x), int(self.y)), 5)

# 阳光类
class Sun:
    def __init__(self, x, y, is_falling=True):
        self.x = x
        self.y = y
        self.is_falling = is_falling
        self.collected = False
        self.fall_speed = SUN_FALL_SPEED
        self.target_y = random.randint(150, 450) if is_falling else y
        self.radius = 20
        self.creation_time = time.time()
        self.lifespan = 10  # 10秒后消失
    
    def update(self):
        if self.is_falling and self.y < self.target_y:
            self.y += self.fall_speed
    
    def is_expired(self, current_time):
        return current_time - self.creation_time > self.lifespan
    
    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 0), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, (255, 200, 0), (int(self.x), int(self.y)), self.radius - 5)

# 僵尸类
class Zombie:
    def __init__(self, row):
        self.row = row
        self.x = SCREEN_WIDTH - 50
        self.y = GRID_OFFSET_Y + row * GRID_SIZE
        self.speed = random.uniform(0.3, 0.7)
        self.health = 100
        self.attack_power = 0.5  # 每帧造成的伤害
        self.attacking = False
        self.target_plant = None
        self.active = True
    
    def update(self, plants):
        if self.attacking and self.target_plant:
            self.target_plant.health -= self.attack_power
            if self.target_plant.health <= 0:
                # 添加检查确保目标植物仍在列表中
                if self.target_plant in plants:
                    plants.remove(self.target_plant)
                self.attacking = False
                self.target_plant = None
        else:
            self.x -= self.speed
            
            # 检查是否有植物在同一行且在接触范围内
            for plant in plants:
                if plant.row == self.row and self.x - (plant.x + GRID_SIZE) < 10 and self.x > plant.x:
                    self.attacking = True
                    self.target_plant = plant
                    break
        
        # 检查是否已到达最左侧
        if self.x <= GRID_OFFSET_X:
            return True  # 游戏结束标志
        
        # 检查是否死亡
        if self.health <= 0:
            self.active = False
        
        return False
    
    def draw(self, surface):
        # 绘制僵尸
        zombie_color = (150, 150, 150)
        pygame.draw.rect(surface, zombie_color, (self.x - 30, self.y, 30, GRID_SIZE), 0)
        
        # 头部
        head_y = self.y + 10
        pygame.draw.circle(surface, zombie_color, (int(self.x - 15), int(head_y)), 20)
        
        # 眼睛
        eye_offset = 5 if self.attacking else 0
        pygame.draw.circle(surface, RED, (int(self.x - 20 + eye_offset), int(head_y - 5)), 5)
        pygame.draw.circle(surface, RED, (int(self.x - 5 + eye_offset), int(head_y - 5)), 5)
        
        # 嘴巴
        mouth_y = head_y + 10
        pygame.draw.rect(surface, (100, 0, 0), (int(self.x - 25), int(mouth_y), 20, 5))
        
        # 健康条
        health_width = 30 * (self.health / 100)
        pygame.draw.rect(surface, RED, (self.x - 30, self.y - 10, health_width, 5))

# 游戏类
class PlantsVsZombies:
    def __init__(self):
        self.sun_count = 100
        self.plants = []
        self.zombies = []
        self.bullets = []
        self.suns = []
        self.game_over = False
        self.game_win = False
        self.wave_count = 0
        self.max_waves = 5
        self.last_sun_generation = time.time()
        self.last_zombie_generation = time.time()
        self.zombie_interval = ZOMBIE_GENERATION_TIME
        self.selected_plant = None
        self.plant_types = {
            "sunflower": {"name": "向日葵", "cost": 50, "class": Sunflower},
            "peashooter": {"name": "豌豆射手", "cost": 100, "class": Peashooter},
            "wallnut": {"name": "坚果墙", "cost": 50, "class": WallNut}
        }
        self.font = pygame.font.SysFont('SimHei', 24)
        self.large_font = pygame.font.SysFont('SimHei', 48)
        self.bg_color = (220, 255, 220)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_r and (self.game_over or self.game_win):
                    self.__init__()  # 重置游戏
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                
                # 如果游戏结束，忽略点击
                if self.game_over or self.game_win:
                    return True
                    
                # 检查是否点击了选择植物按钮
                if y < GRID_OFFSET_Y:
                    self.handle_plant_selection(x, y)
                # 检查是否点击了网格放置植物
                elif (GRID_OFFSET_X <= x <= GRID_OFFSET_X + GRID_COLS * GRID_SIZE and
                      GRID_OFFSET_Y <= y <= GRID_OFFSET_Y + GRID_ROWS * GRID_SIZE):
                    self.handle_grid_click(x, y)
                
                # 检查是否收集阳光
                self.collect_suns(x, y)
        
        return True
    
    def handle_plant_selection(self, x, y):
        button_width = 100
        button_height = 60
        button_y = 20
        
        # 向日葵按钮
        sunflower_button_x = 50
        if (sunflower_button_x <= x <= sunflower_button_x + button_width and
            button_y <= y <= button_y + button_height):
            if self.sun_count >= self.plant_types["sunflower"]["cost"]:
                self.selected_plant = "sunflower"
        
        # 豌豆射手按钮
        peashooter_button_x = 170
        if (peashooter_button_x <= x <= peashooter_button_x + button_width and
            button_y <= y <= button_y + button_height):
            if self.sun_count >= self.plant_types["peashooter"]["cost"]:
                self.selected_plant = "peashooter"
        
        # 坚果墙按钮
        wallnut_button_x = 290
        if (wallnut_button_x <= x <= wallnut_button_x + button_width and
            button_y <= y <= button_y + button_height):
            if self.sun_count >= self.plant_types["wallnut"]["cost"]:
                self.selected_plant = "wallnut"
    
    def handle_grid_click(self, x, y):
        if self.selected_plant:
            col = (x - GRID_OFFSET_X) // GRID_SIZE
            row = (y - GRID_OFFSET_Y) // GRID_SIZE
            
            # 检查该位置是否已有植物
            for plant in self.plants:
                if plant.row == row and plant.col == col:
                    return
            
            # 放置选定的植物
            plant_info = self.plant_types[self.selected_plant]
            if self.sun_count >= plant_info["cost"]:
                self.sun_count -= plant_info["cost"]
                self.plants.append(plant_info["class"](row, col))
            
            self.selected_plant = None
    
    def collect_suns(self, x, y):
        for sun in self.suns[:]:
            if not sun.collected and ((x - sun.x)**2 + (y - sun.y)**2) <= sun.radius**2:
                sun.collected = True
                self.sun_count += 25
                self.suns.remove(sun)
    
    def generate_sun(self, current_time):
        if current_time - self.last_sun_generation >= SUN_GENERATION_TIME:
            self.last_sun_generation = current_time
            self.suns.append(Sun(random.randint(100, SCREEN_WIDTH - 100), -20))
    
    def generate_zombie(self, current_time):
        # 随着波数增加，生成僵尸的频率增加
        if current_time - self.last_zombie_generation >= self.zombie_interval:
            self.last_zombie_generation = current_time
            
            # 计算当前应该生成多少僵尸
            zombies_to_spawn = min(self.wave_count + 1, 3)
            
            for _ in range(zombies_to_spawn):
                row = random.randint(0, GRID_ROWS - 1)
                self.zombies.append(Zombie(row))
            
            self.wave_count += 1
            
            # 减少生成间隔，增加难度
            self.zombie_interval = max(3, ZOMBIE_GENERATION_TIME - self.wave_count)
            
            # 检查是否达到最大波数
            if self.wave_count >= self.max_waves and len(self.zombies) == 0:
                self.game_win = True
    
    def update(self):
        current_time = time.time()
        
        if not self.game_over and not self.game_win:
            # 生成阳光
            self.generate_sun(current_time)
            
            # 更新阳光
            for sun in self.suns[:]:
                sun.update()
                if sun.is_expired(current_time):
                    self.suns.remove(sun)
            
            # 生成僵尸
            if self.wave_count < self.max_waves or len(self.zombies) > 0:
                self.generate_zombie(current_time)
            
            # 更新植物
            for plant in self.plants:
                if isinstance(plant, Sunflower):
                    plant.update(current_time, self.suns)
                elif isinstance(plant, Peashooter):
                    plant.update(current_time, self.bullets, self.zombies)
            
            # 更新子弹
            for bullet in self.bullets[:]:
                bullet.update()
                if not bullet.active:
                    self.bullets.remove(bullet)
                else:
                    # 检查子弹是否击中僵尸
                    for zombie in self.zombies:
                        if (zombie.row == bullet.row and 
                            zombie.x - 30 <= bullet.x <= zombie.x + 10):
                            zombie.health -= bullet.damage
                            self.bullets.remove(bullet)
                            break
            
            # 更新僵尸
            for zombie in self.zombies[:]:
                game_over = zombie.update(self.plants)
                if game_over:
                    self.game_over = True
                    break
                if not zombie.active:
                    self.zombies.remove(zombie)
            
            # 检查胜利条件
            if self.wave_count >= self.max_waves and len(self.zombies) == 0:
                self.game_win = True
    
    def draw(self, surface):
        # 清屏
        surface.fill(self.bg_color)
        
        # 绘制草坪网格背景
        for row in range(GRID_ROWS):
            for col in range(GRID_COLS):
                rect = pygame.Rect(
                    GRID_OFFSET_X + col * GRID_SIZE,
                    GRID_OFFSET_Y + row * GRID_SIZE,
                    GRID_SIZE, GRID_SIZE
                )
                if (row + col) % 2 == 0:
                    pygame.draw.rect(surface, (200, 255, 200), rect)
                else:
                    pygame.draw.rect(surface, (180, 255, 180), rect)
                pygame.draw.rect(surface, (100, 200, 100), rect, 1)
        
        # 绘制植物
        for plant in self.plants:
            plant.draw(surface)
        
        # 绘制子弹
        for bullet in self.bullets:
            bullet.draw(surface)
        
        # 绘制阳光
        for sun in self.suns:
            if not sun.collected:
                sun.draw(surface)
        
        # 绘制僵尸
        for zombie in self.zombies:
            zombie.draw(surface)
        
        # 绘制UI
        self.draw_ui(surface)
        
        # 如果游戏结束，显示结束画面
        if self.game_over:
            self.draw_game_over(surface)
        elif self.game_win:
            self.draw_game_win(surface)
        
        pygame.display.flip()
    
    def draw_ui(self, surface):
        # 绘制阳光数量
        sun_text = self.font.render(f"阳光: {self.sun_count}", True, BLACK)
        surface.blit(sun_text, (10, 10))
        
        # 绘制波数
        wave_text = self.font.render(f"波数: {self.wave_count}/{self.max_waves}", True, BLACK)
        surface.blit(wave_text, (SCREEN_WIDTH - 150, 10))
        
        # 绘制植物选择按钮
        button_width = 100
        button_height = 60
        button_y = 20
        
        # 向日葵按钮
        sunflower_button_x = 50
        pygame.draw.rect(surface, (255, 255, 0) if self.selected_plant == "sunflower" else (220, 220, 0), 
                         (sunflower_button_x, button_y, button_width, button_height))
        pygame.draw.rect(surface, BLACK, (sunflower_button_x, button_y, button_width, button_height), 2)
        plant_text = self.font.render(f"向日葵", True, BLACK)
        cost_text = self.font.render(f"{self.plant_types['sunflower']['cost']}", True, BLACK)
        surface.blit(plant_text, (sunflower_button_x + 10, button_y + 10))
        surface.blit(cost_text, (sunflower_button_x + 10, button_y + 35))
        
        # 豌豆射手按钮
        peashooter_button_x = 170
        pygame.draw.rect(surface, (0, 200, 0) if self.selected_plant == "peashooter" else (0, 150, 0), 
                         (peashooter_button_x, button_y, button_width, button_height))
        pygame.draw.rect(surface, BLACK, (peashooter_button_x, button_y, button_width, button_height), 2)
        plant_text = self.font.render(f"豌豆射手", True, BLACK)
        cost_text = self.font.render(f"{self.plant_types['peashooter']['cost']}", True, BLACK)
        surface.blit(plant_text, (peashooter_button_x + 10, button_y + 10))
        surface.blit(cost_text, (peashooter_button_x + 10, button_y + 35))
        
        # 坚果墙按钮
        wallnut_button_x = 290
        pygame.draw.rect(surface, BROWN if self.selected_plant == "wallnut" else (100, 50, 0), 
                         (wallnut_button_x, button_y, button_width, button_height))
        pygame.draw.rect(surface, BLACK, (wallnut_button_x, button_y, button_width, button_height), 2)
        plant_text = self.font.render(f"坚果墙", True, BLACK)
        cost_text = self.font.render(f"{self.plant_types['wallnut']['cost']}", True, BLACK)
        surface.blit(plant_text, (wallnut_button_x + 10, button_y + 10))
        surface.blit(cost_text, (wallnut_button_x + 10, button_y + 35))
    
    def draw_game_over(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        game_over_text = self.large_font.render("游戏结束!", True, RED)
        restart_text = self.font.render("按 R 键重新开始", True, WHITE)
        
        surface.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 
                                     SCREEN_HEIGHT//2 - game_over_text.get_height()//2))
        surface.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 
                                   SCREEN_HEIGHT//2 + 50))
    
    def draw_game_win(self, surface):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLUE)
        surface.blit(overlay, (0, 0))
        
        win_text = self.large_font.render("胜利!", True, WHITE)
        restart_text = self.font.render("按 R 键重新开始", True, WHITE)
        
        surface.blit(win_text, (SCREEN_WIDTH//2 - win_text.get_width()//2, 
                               SCREEN_HEIGHT//2 - win_text.get_height()//2))
        surface.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 
                                   SCREEN_HEIGHT//2 + 50))

# 主函数
def main():
    game = PlantsVsZombies()
    running = True
    
    while running:
        running = game.handle_events()
        game.update()
        game.draw(screen)
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
