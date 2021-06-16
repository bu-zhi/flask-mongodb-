from flask_pymongo import PyMongo
import time
from flask import Flask,request,render_template
from werkzeug.datastructures import FileStorage
import base64
app = Flask(__name__)
mongo = PyMongo(app,uri='mongodb://localhost:27017/dazuoye')#本地数据库

def find(fenlei,key):
    _users = mongo.db.image.find({fenlei: key}).limit(5)
    data = [u for u in _users]
    #print(data)
    for d in data:
        d['content'] = base64.b64encode(d['content']).decode('utf-8')
    return data

def save_to_mongo(file: FileStorage,author,number,doanload):
    """
    将post请求中的文件对象保存至Mongodb,主要是通过file.stream.read()方法直接将二进制数据读出来,给Mongodb插入用
    :param file:
    :return:
    """
    mongo.db.image.insert_one({
        'title': file.filename.split('.')[0],
        'content': file.stream.read(),
        'number':number,
        'author':author,
        'download':doanload
    })
@app.route('/')
def start():
    return render_template('users.html')

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        file = request.files.get('pic')
        author = request.form.get('author')
        number = int(request.form.get('number'))
        download = request.form.get('download')
        data = find('number',number)
        if len(data) != 0:
            return "number已存在，请换一个number"
        else:
            save_to_mongo(file,author,number,download)
            return render_template('tiaozhuang.html')


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'GET':
        return render_template('update.html')
    if request.method == 'POST':
        number = int(request.form.get('number'))
        key = request.form.get('wd')
        fenlei, key = key.split(' ', 1)
        print(number,fenlei,key)
        if fenlei == 'number':
            return "不允许修改number"
        else:
            mongo.db.image.update({'number':number},{"$set":{fenlei:key}})

            return render_template('tiaozhuang.html')

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'GET':
        return render_template('delete.html')
    if request.method == 'POST':
        key = int(request.form.get('number'))
        mongo.db.image.remove({'number': key})
    return render_template('tiaozhuang.html')

@app.route('/sousuo', methods=['GET', 'POST'])
def sousuo():
    if request.method == 'GET':
        return render_template('find.html')
    if request.method == 'POST':
        start_time = time.time()
        key = request.form.get('wd')
        fenlei, key = key.split(' ', 1)
        if fenlei == 'number':
            key = int(key)
        data = find(fenlei,key)
        if len(data)==0:
            return "没有找到"
        else:
            end_time = time.time()
            return render_template('1.html', users=data,time=end_time-start_time)

@app.errorhandler(404)#钩子函数
def page_not_found(error):
    #return "wrong"
    return render_template('404.html')

if __name__ == "__main__":
    app.run(debug=True)