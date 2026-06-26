import pymysql
from tabulate import tabulate

# 数据库连接配置
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='123456',
    database='stuinfo'
)
cursor = conn.cursor()

# 表头配置（与数据库字段对应）
HEADERS = ['ID', '姓名', '性别', '学号', '班级', '学院']

def show():
    """显示所有学生信息"""
    try:
        cursor.execute("SELECT id, name, gender, student_id, class_name, college_name FROM student")
        rows = cursor.fetchall()
        if rows:
            print(tabulate(rows, headers=HEADERS, tablefmt='grid'))
        else:
            print('暂无学生信息')
    except Exception as e:
        print(f'查询失败: {e}')

def show_help():
    """显示帮助信息"""
    help_info = '''
可用命令：
help    - 显示帮助信息
search  - 搜索学生信息
add     - 添加学生信息
delete  - 删除学生信息
change  - 修改学生信息
show    - 显示所有学生信息
exit    - 退出系统
'''
    print(help_info)

def search():
    """搜索学生信息"""
    field_hint = '''请输入要查询的字段：
1.ID
2.姓名
3.性别
4.学号
5.班级
6.所在学院
exit.退出
选择要通过哪一个字段进行查询学生信息：
'''
    while True:  # 获取一个有效的1-6之间的数字
        field = input(field_hint)
        if field == 'exit':
            return
        if field not in ['1', '2', '3', '4', '5', '6']:
            print('您输入的字段不存在，请重新输入！')
            continue
        else:
            break
    
    value = input('请输入查询条件的值：').strip()  # 去除首尾空格
    conditions = ['id', 'name', 'gender', 'student_id', 'class_name', 'college_name']
    field_name = conditions[int(field) - 1]
    
    try:
        if field_name == 'id':
            # ID 是整数类型，精确匹配
            value = int(value)
            sql = "SELECT id, name, gender, student_id, class_name, college_name FROM student WHERE id = %s"
            cursor.execute(sql, (value,))
        else:
            # 其他字段使用 LIKE 查询，字段名直接拼接到SQL（已通过白名单验证）
            sql = f"SELECT id, name, gender, student_id, class_name, college_name FROM student WHERE {field_name} LIKE %s"
            cursor.execute(sql, (f'%{value}%',))
        
        results = cursor.fetchall()
        if results:
            print(tabulate(results, headers=HEADERS, tablefmt='grid'))
        else:
            print(f'没有找到符合条件的学生！')
            # 尝试去除空格后再次查询
            if value != value.strip():
                print(f'提示：您输入的值包含空格，已自动去除')
    except ValueError:
        print('ID 必须是整数！')
    except Exception as e:
        print(f'查询失败: {e}')


def add():
    """添加学生信息"""
    try:
        name = input('请输入学生姓名：')
        gender = input('请输入学生性别（男/女）：')
        student_id = input('请输入学号（8位）：')
        class_name = input('请输入班级：')
        college_name = input('请输入学院：')
        
        cursor.execute(
            "INSERT INTO student (name, gender, student_id, class_name, college_name) VALUES (%s, %s, %s, %s, %s)",
            (name, gender, student_id, class_name, college_name)
        )
        conn.commit()
        print('添加成功！')
        print('\n当前学生列表：')
        show()
    except Exception as e:
        conn.rollback()
        print(f'添加失败: {e}')

def delete():
    show()
    """删除学生信息"""
    try:
        student_id = input('请输入要删除的学生ID：')
        cursor.execute("DELETE FROM student WHERE id = %s", (student_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print('删除成功！')
            print('\n当前学生列表：')
            show()
        else:
            print('未找到该学生')
    except Exception as e:
        conn.rollback()
        print(f'删除失败: {e}')

def change():
    show()
    """修改学生信息"""
    try:
        student_id = input('请输入要修改的学生ID：')
        
        # 先查询原信息
        cursor.execute(
            "SELECT name, gender, student_id, class_name, college_name FROM student WHERE id = %s",
            (student_id,)
        )
        row = cursor.fetchone()
        if not row:
            print('未找到该学生')
            return
        
        print(f'当前信息：姓名={row[0]}, 性别={row[1]}, 学号={row[2]}, 班级={row[3]}, 学院={row[4]}')
        
        name = input('请输入新姓名（回车保持不变）：') or row[0]
        gender = input('请输入新性别（回车保持不变）：') or row[1]
        new_student_id = input('请输入新学号（回车保持不变）：') or row[2]
        class_name = input('请输入新班级（回车保持不变）：') or row[3]
        college_name = input('请输入新学院（回车保持不变）：') or row[4]
        
        cursor.execute(
            "UPDATE student SET name=%s, gender=%s, student_id=%s, class_name=%s, college_name=%s WHERE id=%s",
            (name, gender, new_student_id, class_name, college_name, student_id)
        )
        conn.commit()
        print('修改成功！')
        print('\n当前学生列表：')
        show()
        
    except Exception as e:
        conn.rollback()
        print(f'修改失败: {e}')

def main_menu():
    """显示主菜单"""
    menu = '''欢迎使用学生信息管理系统（版本号v1.0）
    请输入命令（help：显示帮助信息）'''
    print(menu)
    command = input('>>').strip().lower()
    return command

def main():
    """主函数"""
    commands = {
        'help': show_help,
        'search': search,
        'add': add,
        'delete': delete,
        'change': change,
        'exit': exit,
        'show': show
    }
    try:
        while True:
            command = main_menu()
            if command in commands:
                if command == 'exit':
                    break
                commands[command]()
            else:
                print('命令不存在！请重新输入')
                show_help()
    finally:
        cursor.close()
        conn.close()
        print('数据库连接已关闭')

if __name__ == '__main__':
    main()
