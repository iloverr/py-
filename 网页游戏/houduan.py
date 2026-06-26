from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# 10个关卡的迷宫尺寸（逐渐变大）
LEVEL_CONFIGS = [
    {'width': 11, 'height': 11, 'name': '第1关 - 新手试炼'},
    {'width': 13, 'height': 13, 'name': '第2关 - 渐入佳境'},
    {'width': 15, 'height': 15, 'name': '第3关 - 小试牛刀'},
    {'width': 17, 'height': 17, 'name': '第4关 - 稳步前进'},
    {'width': 19, 'height': 19, 'name': '第5关 - 中级挑战'},
    {'width': 21, 'height': 21, 'name': '第6关 - 高级考验'},
    {'width': 23, 'height': 23, 'name': '第7关 - 大师之路'},
    {'width': 25, 'height': 25, 'name': '第8关 - 极限挑战'},
    {'width': 27, 'height': 27, 'name': '第9关 - 最终试炼'},
    {'width': 31, 'height': 31, 'name': '第10关 - 猪猪大师'},
]

def generate_maze(width, height):
    """生成迷宫"""
    # 初始化迷宫（1为墙，0为路）
    maze = [[1 for _ in range(width)] for _ in range(height)]

    # 使用递归回溯法生成迷宫
    def carve(x, y):
        maze[y][x] = 0
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and maze[ny][nx] == 1:
                maze[y + dy // 2][x + dx // 2] = 0
                carve(nx, ny)

    # 从起点开始生成迷宫
    start_x, start_y = 1, 1
    carve(start_x, start_y)

    # 确保起点和终点是通路
    maze[1][1] = 0
    maze[height - 2][width - 2] = 0

    return maze

def find_path(maze):
    """使用BFS找到从起点到终点的最短路径"""
    height = len(maze)
    width = len(maze[0])

    start = (1, 1)
    end = (width - 2, height - 2)

    queue = [start]
    visited = {start: None}

    while queue:
        current = queue.pop(0)

        if current == end:
            # 重建路径
            path = []
            while current:
                path.append(current)
                current = visited[current]
            return path[::-1]

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            next_pos = (current[0] + dx, current[1] + dy)

            if (0 <= next_pos[0] < width and
                0 <= next_pos[1] < height and
                maze[next_pos[1]][next_pos[0]] == 0 and
                next_pos not in visited):
                visited[next_pos] = current
                queue.append(next_pos)

    return None

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/maze/<int:level>')
def get_maze(level):
    """获取指定关卡的迷宫"""
    if level < 1 or level > 10:
        return jsonify({'error': 'Invalid level'}), 400

    config = LEVEL_CONFIGS[level - 1]

    # 生成迷宫
    maze = generate_maze(config['width'], config['height'])

    # 确保迷宫有解
    path = find_path(maze)
    attempts = 0
    while path is None and attempts < 100:
        maze = generate_maze(config['width'], config['height'])
        path = find_path(maze)
        attempts += 1

    return jsonify({
        'level': level,
        'name': config['name'],
        'width': config['width'],
        'height': config['height'],
        'maze': maze,
        'time_limit': 60  # 60秒
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
