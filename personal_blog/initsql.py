import pymysql

# 连接数据库
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='123456',
    charset='utf8'
)
cursor = conn.cursor()

# 创建数据库
try:
    cursor.execute('CREATE DATABASE IF NOT EXISTS blog')
    cursor.execute('USE blog')
    
    # 创建博客表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS boke (
            id INT PRIMARY KEY AUTO_INCREMENT,
            title VARCHAR(255),
            content TEXT,
            create_time VARCHAR(50)
        )
    ''')
    
    # 删除原有数据（重置）
    cursor.execute('DELETE FROM boke')
    
    # 插入博客内容
    blogs = [
        ('今天我变成了一只小猪', '今天早上醒来，我发现自己变成了一只小猪！粉色的鼻子、圆圆的肚子，还有短短的尾巴。一开始我很惊讶，但很快就适应了。小猪的生活似乎也挺不错的，不用工作，每天就是吃和睡。', '2024-01-15'),
        ('小猪的生活好开心', '当小猪的第一天过得非常开心！我在泥坑里打滚，吃了好多美味的食物，还认识了其他小动物朋友。原来做一只无忧无虑的小猪是这么幸福的事情！', '2024-01-16'),
        ('小猪吃的饭好好吃', '今天吃了好多好吃的！有甜甜的胡萝卜、嫩嫩的青草，还有主人给的玉米棒。小猪的饭菜真是太美味了，我吃得肚子圆圆的，心满意足！', '2024-01-17'),
        ('我是小猪我爱睡觉', '作为一只小猪，睡觉是我的特长！白天晒着太阳睡觉，晚上窝在温暖的猪圈里睡觉。睡觉的时候还会做美梦，梦见好多好吃的东西！', '2024-01-18'),
        ('我这么变得越来越笨', '最近我发现自己好像变得越来越笨了。以前我还会算数学题，现在连简单的加法都忘了。不过没关系，笨笨的小猪也很可爱呀！', '2024-01-19'),
        ('永远当一只小猪生活下去', '经过这几天的体验，我爱上了小猪的生活！无忧无虑、开开心心，每天都过得很充实。我决定永远当一只小猪生活下去，做一只快乐的小猪！', '2024-01-20'),
    ]
    
    cursor.executemany('INSERT INTO boke (title, content, create_time) VALUES (%s, %s, %s)', blogs)
    conn.commit()
    
    print('Success!')
    print('Inserted', len(blogs), 'blogs')
    
except Exception as e:
    print('Error:', str(e))
    conn.rollback()
finally:
    cursor.close()
    conn.close()