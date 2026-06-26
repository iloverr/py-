from flask import Flask,render_template
app = Flask(__name__)

student_dict = {
    '张三': 90,
    '李四': 80,
    '王五': 70,
    '赵六': 60,
}
@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html',name=name)

@app.route('/')
def index1():
    return render_template('item.html',student_dict=student_dict)

@app.route('/score/<int:score>')
def score(score):
    return render_template('score.html',score=score)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)