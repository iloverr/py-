"""
学生信息管理系统 - 注册登录功能演示
功能说明：
1. 注册功能：创建新账号
2. 登录功能：验证账号密码
3. 数据库表包含：编号 (id)、账号 (username)、密码 (password)
"""

import pymysql

# 数据库连接配置
DB_CONFIG = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123456',
    'database': 'student_login',
    'charset': 'utf8mb4'
}

def get_connection():
    """获取数据库连接"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"数据库连接失败：{e}")
        return None

def register():
    """学生注册功能"""
    print("\n=== 学生注册 ===")
    username = input("请输入账号：").strip()
    
    if not username:
        print("账号不能为空！")
        return
    
    password = input("请输入密码：").strip()
    
    if not password:
        print("密码不能为空！")
        return
    
    conn = get_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # 检查账号是否已存在
        cursor.execute("SELECT id FROM students WHERE username = %s", (username,))
        if cursor.fetchone():
            print("该账号已被注册！")
            return
        
        # 插入新用户
        cursor.execute(
            "INSERT INTO students (username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()
        print("注册成功！")
        
    except Exception as e:
        conn.rollback()
        print(f"注册失败：{e}")
    finally:
        cursor.close()
        conn.close()

def login():
    """学生登录功能"""
    print("\n=== 学生登录 ===")
    username = input("请输入账号：").strip()
    password = input("请输入密码：").strip()
    
    if not username or not password:
        print("账号和密码不能为空！")
        return
    
    conn = get_connection()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # 查询账号和密码
        cursor.execute(
            "SELECT id, username FROM students WHERE username = %s AND password = %s",
            (username, password)
        )
        result = cursor.fetchone()
        
        if result:
            print(f"登录成功！欢迎，{result[1]}（ID: {result[0]}）")
        else:
            print("账号或密码错误！")
            
    except Exception as e:
        print(f"登录失败：{e}")
    finally:
        cursor.close()
        conn.close()

def show_menu():
    """显示主菜单"""
    print("\n" + "=" * 40)
    print("     学生信息管理系统（注册登录）")
    print("=" * 40)
    print("1. 注册")
    print("2. 登录")
    print("3. 退出")
    print("=" * 40)

def main():
    """主函数"""
    while True:
        show_menu()
        choice = input("请选择功能（1-3）：").strip()
        
        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            print("再见！")
            break
        else:
            print("输入错误，请重新选择！")

if __name__ == '__main__':
    main()
