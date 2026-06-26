# 完善功能：1.撞墙死亡 2.撞自己死亡 3.按R键重新开始 4.游戏结束画面提示 5.优化游戏视图，添加了新的背景图片、食物图片、小猪头图片、猪屁股图片 6.添加了"王泽中"文字显示 7.优化了蛇身绘制方式，使用圆形代替矩形 8.优化了蛇头和蛇尾的贴图旋转，使其朝向与移动方向一致
import pygame  # 导入pygame游戏开发库
import sys  # 导入系统库，用于退出程序
import pygame  # 导入pygame游戏开发库，提供图形、声音、事件等功能
import sys  # 导入系统库，用于退出程序和获取系统信息
import random  # 导入随机库，用于随机生成食物位置
import os  # 导入os库，用于构建文件路径

pygame.init()  # 初始化所有pygame模块，必须在使用pygame前调用

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本文件所在的绝对路径目录
PIC_DIR = os.path.join(BASE_DIR, "pic")  # 构建pic文件夹的绝对路径

WIDTH, HEIGHT = 960, 960  # 设置游戏窗口的宽度和高度，960x960像素的正方形窗口
CELL_SIZE = 80  # 每个格子的像素大小，地图被划分为12x12的网格
COLS = WIDTH // CELL_SIZE  # 计算列数 = 960 / 80 = 12，即水平方向有12个格子
ROWS = HEIGHT // CELL_SIZE  # 计算行数 = 960 / 80 = 12，即垂直方向有12个格子

BG_COLOR = (30, 30, 30)  # 背景颜色（深灰色），在实际渲染中被背景图片覆盖
GRID_COLOR = (50, 50, 50)  # 网格线颜色（灰色），在实际渲染中也被背景图片覆盖
SNAKE_HEAD_COLOR = (0, 200, 0)  # 蛇头颜色（绿色），在实际渲染中蛇头使用的是小猪头图片
SNAKE_BODY_COLOR = (255, 220, 220)  # 蛇身颜色（浅粉色），用于绘制圆形蛇身节
FOOD_COLOR = (220, 50, 50)  # 食物颜色（红色），在实际渲染中食物使用的是冰淇淋图片
TEXT_COLOR = (255, 255, 255)  # 文字颜色（白色），用于显示"王泽中"文字

screen = pygame.display.set_mode((WIDTH, HEIGHT))  # 创建一个960x960的窗口对象，返回用于绘制的surface
pygame.display.set_caption("贪吃蛇 - 王泽中")  # 设置窗口标题栏显示的文字

bg_img = pygame.image.load(os.path.join(PIC_DIR, "背景1.jpg"))  # 加载背景图片，从pic文件夹读取jpg文件
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))  # 将背景图片缩放到窗口大小960x960

fail_img = pygame.image.load(os.path.join(PIC_DIR, "失败图片.jpg"))  # 加载游戏失败时显示的图片
fail_img = pygame.transform.scale(fail_img, (WIDTH, HEIGHT))  # 将失败图片缩放到窗口大小

head_img_base = pygame.image.load(os.path.join(PIC_DIR, "小猪头.png"))  # 加载小猪头图片，作为蛇头的贴图
orig_w, orig_h = head_img_base.get_size()  # 获取小猪头图片的原始宽度和高度
scale = max(CELL_SIZE / orig_w, CELL_SIZE / orig_h)  # 计算缩放比例，取宽高比中较大的值，确保图片填满格子
new_w = int(orig_w * scale)  # 按比例计算缩放后的宽度并转为整数
new_h = int(orig_h * scale)  # 按比例计算缩放后的高度并转为整数
head_img_base = pygame.transform.scale(head_img_base, (new_w, new_h))  # 将小猪头图片缩放到填满格子的大小
if new_w > CELL_SIZE or new_h > CELL_SIZE:  # 如果缩放后图片尺寸超出格子大小
    head_img_base = head_img_base.subsurface(((new_w - CELL_SIZE) // 2, (new_h - CELL_SIZE) // 2, CELL_SIZE, CELL_SIZE))  # 从中心裁剪出CELL_SIZE大小的区域，确保图片正好是格子大小

food_img = pygame.image.load(os.path.join(PIC_DIR, "冰淇淋.png"))  # 加载冰淇淋图片，作为食物的贴图
orig_w2, orig_h2 = food_img.get_size()  # 获取冰淇淋图片的原始宽度和高度
scale2 = max(CELL_SIZE / orig_w2, CELL_SIZE / orig_h2)  # 计算缩放比例，确保图片能填满格子
new_w2 = int(orig_w2 * scale2)  # 按比例计算缩放后的宽度
new_h2 = int(orig_h2 * scale2)  # 按比例计算缩放后的高度
food_img = pygame.transform.scale(food_img, (new_w2, new_h2))  # 将冰淇淋图片缩放至填满格子
if new_w2 > CELL_SIZE or new_h2 > CELL_SIZE:  # 如果缩放后图片超出格子范围
    food_img = food_img.subsurface(((new_w2 - CELL_SIZE) // 2, (new_h2 - CELL_SIZE) // 2, CELL_SIZE, CELL_SIZE))  # 从中心裁剪出80x80的正方形区域

tail_img_base = pygame.image.load(os.path.join(PIC_DIR, "猪屁股.png"))  # 加载猪屁股图片，作为蛇尾的贴图
orig_w3, orig_h3 = tail_img_base.get_size()  # 获取猪屁股图片的原始宽高
scale3 = max(CELL_SIZE / orig_w3, CELL_SIZE / orig_h3)  # 计算缩放比例
new_w3 = int(orig_w3 * scale3)  # 计算缩放后的宽度
new_h3 = int(orig_h3 * scale3)  # 计算缩放后的高度
tail_img_base = pygame.transform.scale(tail_img_base, (new_w3, new_h3))  # 缩放猪屁股图片
if new_w3 > CELL_SIZE or new_h3 > CELL_SIZE:  # 如果缩放后超出格子
    tail_img_base = tail_img_base.subsurface(((new_w3 - CELL_SIZE) // 2, (new_h3 - CELL_SIZE) // 2, CELL_SIZE, CELL_SIZE))  # 从中心裁剪
tail_img_base = pygame.transform.rotate(tail_img_base, -180)  # 将猪屁股图片旋转180度，使其朝向与蛇尾方向一致

font = pygame.font.SysFont("SimHei", 36, bold=True)  # 创建字体对象，使用黑体、36号字、加粗，用于显示文字

snake = [(5, 1), (4, 1), (3, 1), (2, 1), (1, 1)]  # 蛇的初始身体坐标列表，从蛇头(5,1)到蛇尾(1,1)，共5节

direction = (1, 0)  # 蛇的初始移动方向，x=1表示向右移动，y=0表示垂直不动
game_over = False  # 游戏结束标志，初始为False表示游戏进行中


def spawn_food():  # 定义生成食物函数，确保食物不会出现在蛇身上
    while True:  # 无限循环，直到找到合法位置
        fx = random.randint(0, COLS - 1)  # 在0到11之间随机生成食物的列坐标
        fy = random.randint(0, ROWS - 1)  # 在0到11之间随机生成食物的行坐标
        if (fx, fy) not in snake:  # 检查食物位置是否与蛇的身体重叠
            return (fx, fy)  # 如果不重叠，返回这个合法位置


def reset_game():  # 定义重置游戏函数，用于游戏结束后按R键重新开始
    global snake, direction, food, game_over, move_timer  # 声明要修改的全局变量，否则函数内赋值会创建局部变量
    snake = [(5, 1), (4, 1), (3, 1), (2, 1), (1, 1)]  # 将蛇重置为初始的5节身体
    direction = (1, 0)  # 将移动方向重置为向右
    game_over = False  # 将游戏结束标志重置为False
    food = spawn_food()  # 重新调用spawn_food()函数生成新食物
    move_timer = 0  # 将移动计时器清零，确保新游戏开始后立即进入正常移动节奏


food = spawn_food()  # 游戏开始时调用spawn_food()生成第一个食物

clock = pygame.time.Clock()  # 创建Clock对象，用于控制游戏帧率和计算帧间时间差
move_timer = 0  # 移动计时器变量，累计从上次移动后经过的毫秒数
MOVE_INTERVAL = 1000  # 蛇移动的时间间隔，1000毫秒=1秒，即蛇每秒移动一格

running = True  # 主循环运行标志，为True时持续运行，为False时退出循环
while running:  # 游戏主循环，游戏的核心运行逻辑都在这个循环内
    dt = clock.tick(60)  # 控制帧率为60FPS，并返回上一帧到本帧经过的毫秒数存入dt变量

    for event in pygame.event.get():  # 遍历pygame事件队列中的所有事件
        if event.type == pygame.QUIT:  # 如果检测到用户点击了窗口关闭按钮
            running = False  # 将运行标志设为False，退出主循环
        if event.type == pygame.KEYDOWN:  # 如果检测到键盘按下事件
            if event.key == pygame.K_r and game_over:  # 如果按下的是R键且游戏当前已结束
                reset_game()  # 调用reset_game()函数重置游戏

    if not game_over:  # 如果游戏没有结束，才处理方向控制和移动逻辑
        keys = pygame.key.get_pressed()  # 获取当前帧所有键盘按键的按下状态，返回一个布尔值列表
        if keys[pygame.K_w] or keys[pygame.K_UP]:  # 如果W键或上方向键被按下
            if direction != (0, 1):  # 防止掉头：如果当前方向不是向下，才允许转向
                direction = (0, -1)  # 设置方向为向上（x不变，y减1）
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:  # 如果S键或下方向键被按下
            if direction != (0, -1):  # 防止掉头：如果当前方向不是向上，才允许转向
                direction = (0, 1)  # 设置方向为向下（x不变，y加1）
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:  # 如果A键或左方向键被按下
            if direction != (1, 0):  # 防止掉头：如果当前方向不是向右，才允许转向
                direction = (-1, 0)  # 设置方向为向左（x减1，y不变）
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # 如果D键或右方向键被按下
            if direction != (-1, 0):  # 防止掉头：如果当前方向不是向左，才允许转向
                direction = (1, 0)  # 设置方向为向右（x加1，y不变）

    move_timer += dt  # 将本帧经过的时间累加到移动计时器中
    if move_timer >= MOVE_INTERVAL and not game_over:  # 如果计时器达到1秒间隔且游戏未结束
        move_timer = 0  # 重置移动计时器为零，开始下一个移动周期

        head_x, head_y = snake[0]  # 获取蛇头当前的坐标（蛇列表的第一个元素）
        new_head = (head_x + direction[0], head_y + direction[1])  # 根据当前方向计算新蛇头的位置

        if new_head[0] < 0 or new_head[0] >= COLS or new_head[1] < 0 or new_head[1] >= ROWS:  # 判断新蛇头是否超出地图边界（0~11）
            game_over = True  # 撞墙了，游戏结束
        elif new_head in snake:  # 判断新蛇头位置是否与蛇身任何一节重叠
            game_over = True  # 撞到自己了，游戏结束
        else:  # 既没有撞墙也没有撞到自己，可以正常移动
            snake.insert(0, new_head)  # 在蛇列表头部插入新蛇头，蛇身整体向前移动一格

            if new_head == food:  # 判断新蛇头是否吃到了食物
                food = spawn_food()  # 吃到了食物，调用spawn_food()生成新食物（蛇尾不删，蛇变长）
            else:  # 没有吃到食物
                snake.pop()  # 删除蛇尾最后一节，保持蛇身长度不变

    screen.blit(bg_img, (0, 0))  # 将背景图片绘制到窗口的(0,0)位置，覆盖整个窗口

    fx, fy = food  # 解包食物的坐标，fx为列坐标，fy为行坐标
    food_rect = pygame.Rect(fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE)  # 创建食物在屏幕上的矩形区域（像素坐标）
    screen.blit(food_img, food_rect)  # 将冰淇淋图片绘制到食物所在的矩形区域

    for i, (sx, sy) in enumerate(snake):  # 遍历蛇的每一节，i为索引（0表示蛇头），(sx,sy)为当前节的格子坐标
        rect = pygame.Rect(sx * CELL_SIZE, sy * CELL_SIZE, CELL_SIZE, CELL_SIZE)  # 将格子坐标转换为像素坐标的矩形区域
        if i == 0:  # 如果是蛇头（索引为0）
            if direction == (1, 0):  # 如果蛇正在向右移动
                rotated_head = pygame.transform.rotate(head_img_base, -90)  # 将小猪头图片逆时针旋转90度，使猪头朝右
            elif direction == (0, 1):  # 如果蛇正在向下移动
                rotated_head = pygame.transform.rotate(head_img_base, -180)  # 旋转180度，使猪头朝下
            elif direction == (-1, 0):  # 如果蛇正在向左移动
                rotated_head = pygame.transform.rotate(head_img_base, 90)  # 顺时针旋转90度，使猪头朝左
            else:  # 如果蛇正在向上移动（direction == (0, -1)）
                rotated_head = head_img_base  # 不旋转，保持原始朝向（猪头朝上）
            screen.blit(rotated_head, rect)  # 将旋转后的小猪头图片绘制到蛇头位置
        elif i == len(snake) - 1:  # 如果是蛇尾（最后一节）
            px, py = snake[i - 1]  # 获取蛇尾前一节的坐标，用于计算蛇尾的朝向
            tail_dir = (sx - px, sy - py)  # 计算蛇尾的朝向向量（当前节位置减去前一节位置）
            if tail_dir == (1, 0):  # 如果蛇尾朝向右侧
                rotated_tail = pygame.transform.rotate(tail_img_base, -90)  # 旋转猪屁股图片使其朝右
            elif tail_dir == (0, 1):  # 如果蛇尾朝向下侧
                rotated_tail = pygame.transform.rotate(tail_img_base, -180)  # 旋转猪屁股图片使其朝下
            elif tail_dir == (-1, 0):  # 如果蛇尾朝向左侧
                rotated_tail = pygame.transform.rotate(tail_img_base, 90)  # 旋转猪屁股图片使其朝左
            else:  # 如果蛇尾朝向上侧（tail_dir == (0, -1)）
                rotated_tail = tail_img_base  # 不旋转，猪屁股图片默认朝上
            screen.blit(rotated_tail, rect)  # 将旋转后的猪屁股图片绘制到蛇尾位置
        else:  # 如果是蛇身中间部分（既不是蛇头也不是蛇尾）
            center = (sx * CELL_SIZE + CELL_SIZE // 2, sy * CELL_SIZE + CELL_SIZE // 2)  # 计算格子中心点的像素坐标
            pygame.draw.circle(screen, SNAKE_BODY_COLOR, center, CELL_SIZE // 2)  # 在中心点绘制浅粉色圆形，半径为格子的一半
            pygame.draw.circle(screen, (0, 0, 0), center, CELL_SIZE // 2, 2)  # 绘制黑色圆形边框，线宽为2像素

    text = font.render("王泽中", True, TEXT_COLOR)  # 使用字体渲染"王泽中"文字，True表示开启抗锯齿，白色文字
    screen.blit(text, (WIDTH - text.get_width() - 20, 20))  # 将文字绘制到窗口右上角，距离右边20像素，距离顶部20像素

    if game_over:  # 如果游戏结束标志为True
        screen.blit(fail_img, (0, 0))  # 在窗口(0,0)位置绘制失败图片，覆盖整个窗口作为失败背景
        go_text = font.render("猪猪失败了", True, (173, 216, 230))  # 渲染"猪猪失败了"文字，使用浅蓝色（RGB: 173,216,230）
        restart_text = font.render("按R键重新开始", True, (255, 255, 0))  # 渲染"按R键重新开始"文字，使用黄色（RGB: 255,255,0）
        screen.blit(go_text, (WIDTH // 2 - go_text.get_width() // 2, HEIGHT // 2 - 40))  # 将失败文字水平居中显示，垂直位置在中间偏上40像素
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))  # 将重新开始提示水平居中，在失败文字下方

    pygame.display.flip()  # 更新整个窗口显示，将本帧绘制的所有内容一次性刷新到屏幕上

pygame.quit()  # 退出pygame，释放所有pygame占用的资源
sys.exit()  # 终止Python程序，返回操作系统