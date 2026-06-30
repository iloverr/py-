# 完善功能：1.撞墙死亡 2.撞自己死亡 3.按R键重新开始 4.游戏结束画面提示 5.温馨配色（奶油背景、蜜桃网格、珊瑚蛇头、三文鱼蛇身、番茄红食物、棕色文字）
import pygame  # 导入pygame游戏开发库
import sys  # 导入系统库，用于退出程序
import random  # 导入随机库，用于随机生成食物位置

pygame.init()  # 初始化所有pygame模块

WIDTH, HEIGHT = 800, 800  # 游戏窗口宽度和高度
CELL_SIZE = 50  # 每个格子的像素大小
COLS = WIDTH // CELL_SIZE  # 列数 = 窗口宽度除以格子大小
ROWS = HEIGHT // CELL_SIZE  # 行数 = 窗口高度除以格子大小

BG_COLOR = (255, 245, 235)  # 背景颜色（奶油色）
GRID_COLOR = (255, 228, 210)  # 网格线颜色（蜜桃色）
SNAKE_HEAD_COLOR = (255, 140, 100)  # 蛇头颜色（珊瑚色）
SNAKE_BODY_COLOR = (255, 180, 150)  # 蛇身颜色（三文鱼色）
FOOD_COLOR = (255, 100, 80)  # 食物颜色（番茄红）
TEXT_COLOR = (139, 90, 60)  # 文字颜色（棕色）
OVERLAY_COLOR = (255, 220, 200)  # 游戏结束遮罩颜色（浅粉色）
OVER_TEXT_COLOR = (180, 100, 60)  # 游戏结束文字颜色（深棕色）
RESTART_TEXT_COLOR = (200, 140, 80)  # 重新开始提示文字颜色（暖棕色）

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 创建游戏窗口
pygame.display.set_caption("贪吃蛇 - 王泽中")  # 设置窗口标题

font = pygame.font.SysFont("SimHei", 36, bold=True)  # 创建普通字体（黑体，36号，加粗）
big_font = pygame.font.SysFont("SimHei", 48, bold=True)  # 创建大号字体（黑体，48号，加粗）

snake = [(5, 1), (4, 1), (3, 1), (2, 1), (1, 1)]  # 蛇的初始身体，从蛇头到蛇尾排列

direction = (1, 0)  # 蛇的移动方向，初始向右
game_over = False  # 游戏结束标志，初始为False


def spawn_food():  # 定义生成食物函数
    while True:  # 无限循环直到找到合适位置
        fx = random.randint(0, COLS - 1)  # 随机生成食物的x坐标
        fy = random.randint(0, ROWS - 1)  # 随机生成食物的y坐标
        if (fx, fy) not in snake:  # 如果食物位置不在蛇身上
            return (fx, fy)  # 返回这个食物位置


def reset_game():  # 定义重置游戏函数
    global snake, direction, food, game_over, move_timer  # 声明要修改的全局变量
    snake = [(5, 1), (4, 1), (3, 1), (2, 1), (1, 1)]  # 重置蛇的身体
    direction = (1, 0)  # 重置方向为向右
    game_over = False  # 重置游戏结束状态
    food = spawn_food()  # 重新生成食物
    move_timer = 0  # 重置移动计时器


food = spawn_food()  # 初始化第一个食物

clock = pygame.time.Clock()  # 创建时钟对象，用于控制帧率
move_timer = 0  # 移动计时器，累计经过的毫秒数
MOVE_INTERVAL = 1000  # 蛇移动间隔（毫秒），即每1000毫秒移动一次

running = True  # 游戏主循环运行标志
while running:  # 游戏主循环
    dt = clock.tick(60)  # 控制帧率为60帧每秒，dt为上一帧到本帧经过的毫秒数

    for event in pygame.event.get():  # 遍历所有事件
        if event.type == pygame.QUIT:  # 如果点击了关闭窗口按钮
            running = False  # 退出主循环
        if event.type == pygame.KEYDOWN:  # 如果按下了键盘按键
            if event.key == pygame.K_r and game_over:  # 如果按了R键且游戏已结束
                reset_game()  # 重置游戏

    if not game_over:  # 如果游戏没有结束
        keys = pygame.key.get_pressed()  # 获取当前所有按键的按下状态
        if keys[pygame.K_w] or keys[pygame.K_UP]:  # 如果按下W键或上方向键
            if direction != (0, 1):  # 如果当前方向不是向下（防止掉头）
                direction = (0, -1)  # 方向改为向上
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:  # 如果按下S键或下方向键
            if direction != (0, -1):  # 如果当前方向不是向上（防止掉头）
                direction = (0, 1)  # 方向改为向下
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:  # 如果按下A键或左方向键
            if direction != (1, 0):  # 如果当前方向不是向右（防止掉头）
                direction = (-1, 0)  # 方向改为向左
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # 如果按下D键或右方向键
            if direction != (-1, 0):  # 如果当前方向不是向左（防止掉头）
                direction = (1, 0)  # 方向改为向右

    move_timer += dt  # 累加移动计时器
    if move_timer >= MOVE_INTERVAL and not game_over:  # 如果计时器达到间隔且游戏未结束
        move_timer = 0  # 重置移动计时器

        head_x, head_y = snake[0]  # 获取蛇头当前位置
        new_head = (head_x + direction[0], head_y + direction[1])  # 根据方向计算新蛇头位置

        if new_head[0] < 0 or new_head[0] >= COLS or new_head[1] < 0 or new_head[1] >= ROWS:  # 如果新蛇头超出边界
            game_over = True  # 游戏结束
        elif new_head in snake:  # 如果新蛇头碰到自己的身体
            game_over = True  # 游戏结束
        else:  # 否则正常移动
            snake.insert(0, new_head)  # 在蛇头位置插入新蛇头

            if new_head == food:  # 如果新蛇头吃到了食物
                food = spawn_food()  # 生成新的食物
            else:  # 如果没有吃到食物
                snake.pop()  # 移除蛇尾，保持蛇身长度不变

    screen.fill(BG_COLOR)  # 用背景色填充整个窗口

    for x in range(0, WIDTH, CELL_SIZE):  # 遍历每一列，绘制竖线
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT))  # 画竖直网格线
    for y in range(0, HEIGHT, CELL_SIZE):  # 遍历每一行，绘制横线
        pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y))  # 画水平网格线

    fx, fy = food  # 获取食物的x和y坐标
    food_rect = pygame.Rect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE)  # 创建食物矩形区域
    pygame.draw.rect(screen, FOOD_COLOR, food_rect)  # 用食物颜色填充食物矩形
    pygame.draw.rect(screen, (139, 90, 60), food_rect, 2)  # 绘制食物边框（棕色）

    for i, (sx, sy) in enumerate(snake):  # 遍历蛇的每一节身体，i是索引
        rect = pygame.Rect(sx * CELL_SIZE, sy * CELL_SIZE, CELL_SIZE, CELL_SIZE)  # 创建当前蛇节的矩形区域
        color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_BODY_COLOR  # 蛇头用珊瑚色，蛇身用三文鱼色
        pygame.draw.rect(screen, color, rect)  # 用对应颜色填充蛇节矩形
        pygame.draw.rect(screen, (139, 90, 60), rect, 2)  # 绘制蛇节边框（棕色）

    text = font.render("王泽中", True, TEXT_COLOR)  # 渲染"王泽中"文字
    screen.blit(text, (WIDTH - text.get_width() - 20, 20))  # 将文字绘制到窗口右上角

    if game_over:  # 如果游戏结束
        overlay = pygame.Surface((WIDTH, HEIGHT))  # 创建一个与窗口等大的遮罩表面
        overlay.set_alpha(180)  # 设置遮罩透明度（0-255，180为半透明）
        overlay.fill(OVERLAY_COLOR)  # 用浅粉色填充遮罩
        screen.blit(overlay, (0, 0))  # 将遮罩绘制到窗口上
        go_text = big_font.render("游戏结束", True, OVER_TEXT_COLOR)  # 渲染"游戏结束"大字
        restart_text = font.render("按 R 键重新开始", True, RESTART_TEXT_COLOR)  # 渲染"按R键重新开始"提示
        screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 40))  # 居中显示"游戏结束"
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))  # 居中显示重新开始提示

    pygame.display.flip()  # 刷新整个窗口，将绘制的内容显示出来

pygame.quit()  # 退出pygame，释放资源
sys.exit()  # 退出程序