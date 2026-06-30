import pygame
import sys
import os
import random

pygame.init()
pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PIC_DIR = os.path.join(BASE_DIR, "pic")
SOUND_DIR = os.path.join(BASE_DIR, "sou")

info = pygame.display.Info()
SCREEN_H = info.current_h - 60
SCREEN_W = int(SCREEN_H * 0.6)
WIDTH, HEIGHT = SCREEN_W, SCREEN_H

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("飞机大战")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
DARK_BLUE = (10, 20, 50)
NEON_BLUE = (0, 200, 255)
NEON_PINK = (255, 50, 150)
NEON_GREEN = (0, 255, 100)
ORANGE_GRADIENT = (255, 150, 50)
RED_ALERT = (255, 50, 50)

ENEMY_CONFIG = {
    "count": 3,
    "names": ["小飞机", "中型机", "大型机"],
    "sizes": [(45, 45), (60, 60), (75, 75)],
    "hp": [2, 5, 10],
    "scores": [10, 15, 20],
    "weights": [60, 30, 10],
    "fire_interval": 800,
}

PLANE_CONFIG = [
    {"name": "炽焰壹号", "ability": "能力：子弹伤害 1.5", "damage": 1.5, "fire_interval": 500, "bullet_speed_mul": 3, "hp": 100},
    {"name": "桃汐甜心", "ability": "能力：射速 0.2s", "damage": 1.0, "fire_interval": 200, "bullet_speed_mul": 3, "hp": 100},
    {"name": "云流零度", "ability": "能力：子弹速度 4x", "damage": 1.0, "fire_interval": 500, "bullet_speed_mul": 4, "hp": 100},
]

MODE_CONFIG = [
    {"name": "休 闲", "desc": "敌机不会发射子弹"},
    {"name": "激 战", "desc": "敌机持续发射子弹"},
]

class ResourceManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.channels = {}
        self.fonts = {}
        self._load_images()
        self._load_sounds()
        self._load_fonts()

    def _load_images(self):
        bg_img = pygame.image.load(os.path.abspath(os.path.join(PIC_DIR, "background.jpg")))
        bg_height = int(HEIGHT * 2)
        self.images["background"] = pygame.transform.scale(bg_img, (WIDTH, bg_height))

        bullet_img = pygame.image.load(os.path.abspath(os.path.join(PIC_DIR, "bullet.png")))
        self.images["bullet"] = pygame.transform.scale(bullet_img, (10, 30))

        enemy_bullet_img = pygame.image.load(os.path.abspath(os.path.join(PIC_DIR, "bullet1.png")))
        self.images["enemy_bullet"] = pygame.transform.scale(enemy_bullet_img, (10, 30))

        e_imgs = []
        for i in range(3):
            img = pygame.image.load(os.path.abspath(os.path.join(PIC_DIR, f"e{i+1}.png")))
            img = pygame.transform.scale(img, ENEMY_CONFIG["sizes"][i])
            if i == 1:
                img = pygame.transform.rotate(img, 180)
            e_imgs.append(img)
        self.images["enemies"] = e_imgs

        blowup_img = pygame.image.load(os.path.abspath(os.path.join(PIC_DIR, "blowup.png")))
        self.images["blowup"] = pygame.transform.scale(blowup_img, (80, 80))

        hp_pack_img = pygame.image.load(os.path.abspath(os.path.join(PIC_DIR, "血包.png")))
        self.images["hp_pack"] = pygame.transform.scale(hp_pack_img, (35, 35))

        shield_img = pygame.image.load(os.path.abspath(os.path.join(PIC_DIR, "护盾.png")))
        self.images["shield"] = pygame.transform.scale(shield_img, (35, 35))

        gameover_img = pygame.image.load(os.path.abspath(os.path.join(PIC_DIR, "游戏结束.png")))
        go_orig_w, go_orig_h = gameover_img.get_width(), gameover_img.get_height()
        go_scale = min(WIDTH * 0.7 / go_orig_w, HEIGHT * 0.5 / go_orig_h)
        self.images["gameover"] = pygame.transform.scale(gameover_img, (int(go_orig_w * go_scale), int(go_orig_h * go_scale)))

        plane_display_imgs = []
        for i in range(3):
            img = pygame.image.load(os.path.abspath(os.path.join(PIC_DIR, f"{i+1}{PLANE_CONFIG[i]['name']}.png")))
            plane_display_imgs.append(pygame.transform.scale(img, (180, 210)))
        self.images["planes_display"] = plane_display_imgs

        plane_game_imgs = []
        for i in range(3):
            img = pygame.image.load(os.path.abspath(os.path.join(PIC_DIR, f"{i+1}{PLANE_CONFIG[i]['name']}.png")))
            plane_game_imgs.append(pygame.transform.scale(img, (120, 160)))
        self.images["planes_game"] = plane_game_imgs

    def _load_sounds(self):
        self.sounds["bullet"] = pygame.mixer.Sound(os.path.abspath(os.path.join(SOUND_DIR, "子弹.wav")))
        self.sounds["explosion"] = pygame.mixer.Sound(os.path.abspath(os.path.join(SOUND_DIR, "爆炸.wav")))
        self.sounds["explosion"].set_volume(100.0)
        self.sounds["get"] = pygame.mixer.Sound(os.path.abspath(os.path.join(SOUND_DIR, "获得.wav")))
        
        self.sounds["fail_music"] = os.path.abspath(os.path.join(SOUND_DIR, "失败音乐.wav"))
        self.sounds["result_music"] = os.path.abspath(os.path.join(SOUND_DIR, "结算音乐.wav"))
        self.sounds["game_music"] = os.path.abspath(os.path.join(SOUND_DIR, "游戏音乐.wav"))

        self.channels["explosion"] = pygame.mixer.Channel(0)
        self.channels["bullet"] = pygame.mixer.Channel(1)
        self.channels["get"] = pygame.mixer.Channel(2)

    def _load_fonts(self):
        preferred_fonts = ["Microsoft YaHei", "SimHei", "SimSun", "Arial"]
        for font_name in preferred_fonts:
            try:
                self.fonts["title"] = pygame.font.SysFont(font_name, 56, bold=True)
                self.fonts["name"] = pygame.font.SysFont(font_name, 32, bold=True)
                self.fonts["hint"] = pygame.font.SysFont(font_name, 24, bold=True)
                self.fonts["score"] = pygame.font.SysFont(font_name, 22, bold=True)
                self.fonts["ability"] = pygame.font.SysFont(font_name, 20, bold=True)
                break
            except:
                continue

class GameState:
    def __init__(self):
        self.selected_index = 0
        self.plane_selected = None
        self.mode_selected = None
        self.game_over = False
        self.show_result = False

        self.bullets = []
        self.fire_cooldown = 0
        self.enemies = []
        self.enemy_bullets = []
        self.explosions = []
        self.pickups = []

        self.enemy_spawn_timer = 0
        self.pickup_spawn_timer = 0
        self.game_over_timer = 0
        self.shield_timer = 0
        self.pulse_active = False
        self.pulse_duration = 0

        self.energy = 0
        self.energy_max = 100
        self.player_hp = 100
        self.player_max_hp = 100
        self.score = 0
        self.high_score = 0

        self.enemy_kills = [0, 0, 0]
        
        self.fail_played = False
        self.result_played = False
        self.game_music_playing = False

        self.bg_y = 0
        self.bg_scroll_speed = (HEIGHT * 2) / 250
        self.enemy_bullet_speed = self.bg_scroll_speed * 3

    def reset(self):
        self.plane_selected = None
        self.mode_selected = None
        self.game_over = False
        self.show_result = False

        self.bullets.clear()
        self.fire_cooldown = 0
        self.enemies.clear()
        self.enemy_bullets.clear()
        self.explosions.clear()
        self.pickups.clear()

        self.enemy_spawn_timer = 0
        self.pickup_spawn_timer = 0
        self.game_over_timer = 0
        self.shield_timer = 0
        self.pulse_active = False
        self.pulse_duration = 0

        self.energy = 0
        self.player_hp = 100
        self.player_max_hp = 100
        self.score = 0
        self.enemy_kills = [0, 0, 0]

        self.fail_played = False
        self.result_played = False
        self.game_music_playing = False

        self.bg_y = 0
        pygame.mouse.set_visible(True)

class UIRenderer:
    def __init__(self, resources):
        self.resources = resources

    def draw_select_screen(self, selected_index):
        screen.blit(self.resources.images["background"], (0, 0))
        self._draw_overlay()

        title_text = self.resources.fonts["title"].render("选 择 战 机", True, GOLD)
        screen.blit(title_text, title_text.get_rect(center=(WIDTH // 2, 60)))

        card_width, card_height = 200, 260
        spacing = 40
        card_y_top = 130

        positions = [
            ((WIDTH - 2 * card_width - spacing) // 2, card_y_top),
            ((WIDTH - 2 * card_width - spacing) // 2 + card_width + spacing, card_y_top),
            ((WIDTH - card_width) // 2, card_y_top + card_height + spacing),
        ]

        for i in range(3):
            cx, cy = positions[i]
            card_rect = pygame.Rect(cx, cy, card_width, card_height)
            self._draw_card(card_rect, i == selected_index)

            img_rect = self.resources.images["planes_display"][i].get_rect(center=(cx + card_width // 2, cy + 90))
            screen.blit(self.resources.images["planes_display"][i], img_rect)

            name_text = self.resources.fonts["name"].render(PLANE_CONFIG[i]["name"], True, WHITE if i == selected_index else GRAY)
            screen.blit(name_text, name_text.get_rect(center=(cx + card_width // 2, cy + card_height - 30)))

            ability_text = self.resources.fonts["ability"].render(PLANE_CONFIG[i]["ability"], True, GOLD if i == selected_index else (180, 180, 180))
            screen.blit(ability_text, ability_text.get_rect(center=(cx + card_width // 2, cy + card_height + 18)))

        hint_text = self.resources.fonts["hint"].render("← → 选择战机    Enter / 空格 确认", True, WHITE)
        screen.blit(hint_text, hint_text.get_rect(center=(WIDTH // 2, HEIGHT - 50)))

        pygame.display.flip()

    def draw_mode_select_screen(self, mode_selected):
        screen.blit(self.resources.images["background"], (0, 0))
        self._draw_overlay()

        title_text = self.resources.fonts["title"].render("选 择 模 式", True, GOLD)
        screen.blit(title_text, title_text.get_rect(center=(WIDTH // 2, 80)))

        card_width, card_height = 220, 200
        spacing = 50
        start_x = (WIDTH - 2 * card_width - spacing) // 2
        card_y = 200

        for i in range(2):
            cx = start_x + i * (card_width + spacing)
            card_rect = pygame.Rect(cx, card_y, card_width, card_height)
            self._draw_card(card_rect, i == mode_selected)

            name_text = self.resources.fonts["name"].render(MODE_CONFIG[i]["name"], True, WHITE if i == mode_selected else GRAY)
            screen.blit(name_text, name_text.get_rect(center=(cx + card_width // 2, card_y + 60)))

            desc_text = self.resources.fonts["ability"].render(MODE_CONFIG[i]["desc"], True, GOLD if i == mode_selected else (180, 180, 180))
            screen.blit(desc_text, desc_text.get_rect(center=(cx + card_width // 2, card_y + 120)))

        hint_text = self.resources.fonts["hint"].render("← → 选择模式    Enter / 空格 确认", True, WHITE)
        screen.blit(hint_text, hint_text.get_rect(center=(WIDTH // 2, HEIGHT - 50)))

        pygame.display.flip()

    def draw_result_screen(self, score, enemy_kills):
        screen.blit(self.resources.images["background"], (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        result_title = self.resources.fonts["title"].render("游 戏 结 算", True, GOLD)
        screen.blit(result_title, result_title.get_rect(center=(WIDTH // 2, 80)))

        score_line = self.resources.fonts["name"].render(f"最终分数: {score}", True, WHITE)
        screen.blit(score_line, score_line.get_rect(center=(WIDTH // 2, 180)))

        for i, name in enumerate(ENEMY_CONFIG["names"]):
            kill_text = self.resources.fonts["name"].render(f"击落 {name}: {enemy_kills[i]} 架", True, WHITE)
            screen.blit(kill_text, kill_text.get_rect(center=(WIDTH // 2, 260 + i * 60)))

        restart_text = self.resources.fonts["hint"].render("按 R 键重新开始", True, GOLD)
        screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT - 80)))

        pygame.display.flip()

    def draw_game_hud(self, energy, energy_max, player_hp, player_max_hp, score, high_score, shield_timer):
        bar_width = int(WIDTH * 0.36)
        bar_height = 28
        bar_y = 15
        spacing = 20
        start_x = (WIDTH - 2 * bar_width - spacing) // 2
        border = 2

        self._draw_bar(start_x, bar_y, bar_width, bar_height, border, 
                       (30, 50, 100), NEON_BLUE, 
                       energy / energy_max, f"能量: {int(energy)}/{energy_max}")

        bar_right_x = start_x + bar_width + spacing
        hp_ratio = player_hp / player_max_hp
        hp_color = NEON_GREEN if hp_ratio > 0.5 else ORANGE_GRADIENT if hp_ratio > 0.25 else RED_ALERT
        self._draw_bar(bar_right_x, bar_y, bar_width, bar_height, border, 
                       (30, 60, 40), hp_color, 
                       hp_ratio, f"血量: {int(player_hp)}/{player_max_hp}")

        score_text = self.resources.fonts["score"].render(f"分数: {score}", True, WHITE)
        screen.blit(score_text, score_text.get_rect(midtop=(start_x + bar_width // 2, bar_y + bar_height + 10)))

        high_text = self.resources.fonts["score"].render(f"最高分: {high_score}", True, GOLD)
        screen.blit(high_text, high_text.get_rect(midtop=(bar_right_x + bar_width // 2, bar_y + bar_height + 10)))

        if shield_timer > 0:
            shield_text = self.resources.fonts["hint"].render(f"护盾: {shield_timer / 1000:.1f}s", True, YELLOW)
            screen.blit(shield_text, shield_text.get_rect(center=(WIDTH // 2, bar_y + bar_height + 55)))

    def _draw_overlay(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

    def _draw_card(self, rect, selected):
        if selected:
            pygame.draw.rect(screen, NEON_BLUE, rect.inflate(12, 12), border_radius=16)
            pygame.draw.rect(screen, (30, 60, 120), rect.inflate(6, 6), border_radius=14)
            pygame.draw.rect(screen, (50, 90, 180), rect, border_radius=12)
            
            glow = pygame.Surface((rect.width + 20, rect.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow, (0, 200, 255, 30), glow.get_rect(), border_radius=20)
            screen.blit(glow, (rect.x - 10, rect.y - 10))
        else:
            pygame.draw.rect(screen, (80, 80, 100), rect.inflate(6, 6), border_radius=14)
            pygame.draw.rect(screen, (30, 30, 50), rect, border_radius=12)

    def _draw_bar(self, x, y, width, height, border, bg_color, fill_color, ratio, label):
        outer_rect = pygame.Rect(x - border - 4, y - border - 4, width + 2 * border + 8, height + 2 * border + 8)
        glow = pygame.Surface(outer_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(glow, (0, 200, 255, 20), glow.get_rect(), border_radius=16)
        screen.blit(glow, outer_rect.topleft)

        pygame.draw.rect(screen, (10, 10, 30), (x - border, y - border, width + 2 * border, height + 2 * border), border_radius=14)
        pygame.draw.rect(screen, bg_color, (x, y, width, height), border_radius=12)
        
        fill_width = int(width * ratio)
        if fill_width > 0:
            fill_surface = pygame.Surface((fill_width, height))
            for w in range(fill_width):
                t = w / fill_width
                r = int(fill_color[0] * (1 - t) + NEON_BLUE[0] * t)
                g = int(fill_color[1] * (1 - t) + NEON_BLUE[1] * t)
                b = int(fill_color[2] * (1 - t) + NEON_BLUE[2] * t)
                pygame.draw.line(fill_surface, (r, g, b), (w, 0), (w, height))
            screen.blit(fill_surface, (x, y))
        
        label_text = self.resources.fonts["hint"].render(label, True, WHITE)
        screen.blit(label_text, label_text.get_rect(center=(x + width // 2, y + height // 2)))

class GameEngine:
    def __init__(self):
        self.resources = ResourceManager()
        self.state = GameState()
        self.ui = UIRenderer(self.resources)

    def run(self):
        running = True

        while running:
            dt = clock.tick(30)
            self._handle_music()
            self._handle_events()
            self._update(dt)
            self._render()

        pygame.quit()
        sys.exit()

    def _handle_music(self):
        if not self.state.game_music_playing and not self.state.game_over and not self.state.show_result:
            pygame.mixer.music.load(self.resources.sounds["game_music"])
            pygame.mixer.music.play(-1)
            self.state.game_music_playing = True

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if self.state.show_result:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.state.reset()
                continue

            if self.state.game_over:
                continue

            if self.state.plane_selected is not None and self.state.mode_selected is not None:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    if self.state.energy >= 100 and not self.state.pulse_active:
                        self.state.pulse_active = True
                        self.state.pulse_duration = 200
                        self.state.energy = 0

            if self.state.plane_selected is None:
                self._handle_plane_selection(event)
            elif self.state.mode_selected is None:
                self._handle_mode_selection(event)

    def _handle_plane_selection(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.state.selected_index = (self.state.selected_index - 1) % 3
            elif event.key == pygame.K_RIGHT:
                self.state.selected_index = (self.state.selected_index + 1) % 3
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.state.plane_selected = self.state.selected_index
                self.state.player_max_hp = PLANE_CONFIG[self.state.selected_index]["hp"]
                self.state.player_hp = self.state.player_max_hp

    def _handle_mode_selection(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.state.mode_selected = 0
            elif event.key == pygame.K_RIGHT:
                self.state.mode_selected = 1
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.state.mode_selected is not None:
                    pygame.mouse.set_visible(False)

    def _update(self, dt):
        if self.state.plane_selected is None or self.state.mode_selected is None or self.state.show_result:
            return

        self._update_background(dt)
        self._update_player(dt)
        self._update_enemies(dt)
        self._update_pickups(dt)
        self._update_collisions(dt)
        self._update_explosions(dt)
        self._update_game_over(dt)

    def _update_background(self, dt):
        bg_height = HEIGHT * 2
        screen.blit(self.resources.images["background"], (0, self.state.bg_y))
        screen.blit(self.resources.images["background"], (0, self.state.bg_y - bg_height))
        if not self.state.game_over:
            self.state.bg_y += self.state.bg_scroll_speed
            if self.state.bg_y >= bg_height:
                self.state.bg_y = 0

    def _update_player(self, dt):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if not self.state.game_over:
            stats = PLANE_CONFIG[self.state.plane_selected]
            self.state.fire_cooldown -= dt
            if mouse_pressed and self.state.fire_cooldown <= 0:
                bullet_y = mouse_y - 160 // 2
                self.state.bullets.append([mouse_x, bullet_y])
                self.resources.channels["bullet"].play(self.resources.sounds["bullet"])
                self.state.fire_cooldown = stats["fire_interval"]

        cur_bullet_speed = self.state.bg_scroll_speed * PLANE_CONFIG[self.state.plane_selected]["bullet_speed_mul"]
        for b in self.state.bullets[:]:
            b[1] -= cur_bullet_speed
            if b[1] < -30:
                self.state.bullets.remove(b)
            else:
                b_rect = self.resources.images["bullet"].get_rect(center=(b[0], b[1]))
                screen.blit(self.resources.images["bullet"], b_rect)

        if self.state.pulse_active:
            self.state.pulse_duration -= dt
            
            pygame.draw.line(screen, NEON_BLUE, (mouse_x, mouse_y), (mouse_x, -50), 15)
            pygame.draw.line(screen, (0, 100, 255), (mouse_x, mouse_y), (mouse_x, -50), 8)
            
            for e in self.state.enemies[:]:
                e_rect = self.resources.images["enemies"][e[2]].get_rect(topleft=(e[0], e[1]))
                if e_rect.left <= mouse_x <= e_rect.right and e[1] < mouse_y:
                    self.state.explosions.append([e[0], e[1], 500])
                    self.resources.channels["explosion"].play(self.resources.sounds["explosion"])
                    self.state.score += ENEMY_CONFIG["scores"][e[2]]
                    self.state.enemy_kills[e[2]] += 1
                    if self.state.score > self.state.high_score:
                        self.state.high_score = self.state.score
                    self.state.enemies.remove(e)
            
            if self.state.pulse_duration <= 0:
                self.state.pulse_active = False

    def _update_enemies(self, dt):
        if not self.state.game_over:
            self.state.enemy_spawn_timer -= dt
            if self.state.enemy_spawn_timer <= 0:
                enemy_type = random.choices([0, 1, 2], weights=ENEMY_CONFIG["weights"], k=1)[0]
                enemy_size = ENEMY_CONFIG["sizes"][enemy_type]
                enemy_x = random.randint(0, WIDTH - enemy_size[0])
                self.state.enemies.append([enemy_x, -enemy_size[1], enemy_type, ENEMY_CONFIG["hp"][enemy_type], 0])
                self.state.enemy_spawn_timer = random.randint(800, 1500)

            self.state.pickup_spawn_timer -= dt
            if self.state.pickup_spawn_timer <= 0:
                pickup_type = random.choice(["hp", "shield"])
                px = random.randint(20, WIDTH - 20)
                self.state.pickups.append([px, -35, pickup_type])
                self.state.pickup_spawn_timer = random.randint(5000, 8000)

        for e in self.state.enemies[:]:
            if not self.state.game_over:
                e[1] += self.state.bg_scroll_speed * 0.6
            if self.state.mode_selected == 1 and not self.state.game_over:
                e[4] -= dt
                if e[4] <= 0:
                    enemy_size = ENEMY_CONFIG["sizes"][e[2]]
                    eb_x = e[0] + enemy_size[0] // 2
                    eb_y = e[1] + enemy_size[1]
                    self.state.enemy_bullets.append([eb_x, eb_y])
                    e[4] = ENEMY_CONFIG["fire_interval"]
            if e[1] > HEIGHT:
                self.state.enemies.remove(e)
            else:
                screen.blit(self.resources.images["enemies"][e[2]], (e[0], e[1]))

        for eb in self.state.enemy_bullets[:]:
            if not self.state.game_over:
                eb[1] += self.state.enemy_bullet_speed
            if eb[1] > HEIGHT:
                self.state.enemy_bullets.remove(eb)
            else:
                eb_rect = self.resources.images["enemy_bullet"].get_rect(center=(eb[0], eb[1]))
                screen.blit(self.resources.images["enemy_bullet"], eb_rect)

    def _update_pickups(self, dt):
        if not self.state.game_over:
            self.state.shield_timer -= dt
            if self.state.shield_timer < 0:
                self.state.shield_timer = 0

        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_plane = self.resources.images["planes_game"][self.state.plane_selected]
        plane_rect = player_plane.get_rect(center=(mouse_x, mouse_y))

        for p in self.state.pickups[:]:
            if not self.state.game_over:
                p[1] += self.state.bg_scroll_speed
            if p[1] > HEIGHT:
                self.state.pickups.remove(p)
            else:
                p_img = self.resources.images["hp_pack"] if p[2] == "hp" else self.resources.images["shield"]
                p_rect = p_img.get_rect(center=(p[0], p[1]))
                screen.blit(p_img, p_rect)
                if p_rect.colliderect(plane_rect):
                    if p[2] == "hp":
                        self.state.player_hp = min(self.state.player_hp + 20, self.state.player_max_hp)
                    else:
                        self.state.shield_timer = 5000
                    self.resources.channels["get"].play(self.resources.sounds["get"])
                    self.state.pickups.remove(p)

    def _update_collisions(self, dt):
        if self.state.game_over:
            return

        mouse_x, mouse_y = pygame.mouse.get_pos()
        player_plane = self.resources.images["planes_game"][self.state.plane_selected]
        plane_rect = player_plane.get_rect(center=(mouse_x, mouse_y))

        stats = PLANE_CONFIG[self.state.plane_selected]

        for b in self.state.bullets[:]:
            b_rect = self.resources.images["bullet"].get_rect(center=(b[0], b[1]))
            hit = False
            for e in self.state.enemies[:]:
                e_rect = self.resources.images["enemies"][e[2]].get_rect(topleft=(e[0], e[1]))
                if b_rect.colliderect(e_rect):
                    e[3] -= stats["damage"]
                    hit = True
                    if e[3] <= 0:
                        self.state.explosions.append([e[0], e[1], 500])
                        self.resources.channels["explosion"].play(self.resources.sounds["explosion"])
                        self.state.score += ENEMY_CONFIG["scores"][e[2]]
                        self.state.enemy_kills[e[2]] += 1
                        
                        energy_gain = [10, 15, 20][e[2]]
                        self.state.energy = min(self.state.energy + energy_gain, self.state.energy_max)
                        
                        if self.state.score > self.state.high_score:
                            self.state.high_score = self.state.score
                        self.state.enemies.remove(e)
                    break
            if hit:
                self.state.bullets.remove(b)

        for eb in self.state.enemy_bullets[:]:
            eb_rect = self.resources.images["enemy_bullet"].get_rect(center=(eb[0], eb[1]))
            if self.state.shield_timer <= 0 and eb_rect.colliderect(plane_rect):
                self.state.player_hp -= 1
                self.state.enemy_bullets.remove(eb)

        for e in self.state.enemies[:]:
            e_rect = self.resources.images["enemies"][e[2]].get_rect(topleft=(e[0], e[1]))
            if self.state.shield_timer <= 0 and e_rect.colliderect(plane_rect):
                self.state.explosions.append([e[0], e[1], 500])
                self.state.player_hp = 0
                e[3] = 0
                self.state.enemies.remove(e)

        if self.state.player_hp <= 0:
            self.state.player_hp = 0
            self.state.explosions.append([mouse_x - 40, mouse_y - 40, 500])
            self.state.game_over = True
            self.state.game_over_timer = 3000

    def _update_explosions(self, dt):
        for exp in self.state.explosions[:]:
            exp[2] -= dt
            if exp[2] <= 0:
                self.state.explosions.remove(exp)
            else:
                screen.blit(self.resources.images["blowup"], (exp[0], exp[1]))

    def _update_game_over(self, dt):
        if self.state.game_over:
            if self.state.game_music_playing:
                pygame.mixer.music.stop()
                self.state.game_music_playing = False

            go_rect = self.resources.images["gameover"].get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(self.resources.images["gameover"], go_rect)

            self.state.game_over_timer -= dt
            if not self.state.fail_played:
                pygame.mixer.music.load(self.resources.sounds["fail_music"])
                pygame.mixer.music.play(0)
                self.state.fail_played = True

            if self.state.game_over_timer <= 0:
                self.state.show_result = True
                if not self.state.result_played:
                    pygame.mixer.music.load(self.resources.sounds["result_music"])
                    pygame.mixer.music.play(0)
                    self.state.result_played = True

    def _render(self):
        if self.state.plane_selected is None:
            self.ui.draw_select_screen(self.state.selected_index)
        elif self.state.mode_selected is None:
            self.ui.draw_mode_select_screen(self.state.mode_selected)
        elif self.state.show_result:
            self.ui.draw_result_screen(self.state.score, self.state.enemy_kills)
        else:
            self.ui.draw_game_hud(self.state.energy, self.state.energy_max, 
                                  self.state.player_hp, self.state.player_max_hp, 
                                  self.state.score, self.state.high_score,
                                  self.state.shield_timer)

            mouse_x, mouse_y = pygame.mouse.get_pos()
            player_plane = self.resources.images["planes_game"][self.state.plane_selected]
            plane_rect = player_plane.get_rect(center=(mouse_x, mouse_y))
            screen.blit(player_plane, plane_rect)

            if self.state.shield_timer > 0:
                shield_radius = max(120, 160) // 2 + 15
                pygame.draw.circle(screen, YELLOW, (mouse_x, mouse_y), shield_radius, 3)

            pygame.display.flip()

if __name__ == "__main__":
    game = GameEngine()
    game.run()