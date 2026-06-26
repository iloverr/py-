from flask import Flask,render_template
import pymysql
app = Flask(__name__)

def execSQL(sql):
    conn = pymysql.connect(host='localhost',user='root',password='123456')
    cursor = conn.cursor()
    cursor.execute('USE blog')
    try:
        cursor.execute(sql)
        conn.commit()
        return cursor.fetchall()
    except BaseException as e:
        conn.rollback()
        print("e")
    cursor.close()
    conn.close()

@app.route('/')
def index():
    sql='select id,title from boke'
    blogs = execSQL(sql)
    return render_template('bloglist.html',blogs=blogs)

@app.route('/blog/<int:id>')
def blog(id):
    sql='select * from boke where id=%s'%id
    blog = execSQL(sql)
    if blog:
        return render_template('blog.html',blog=blog[0])
    else:
        return "<a href='/'>返回博客列表</a>"
        
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5050,debug=True)