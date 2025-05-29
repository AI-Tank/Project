from flask import Flask, render_template, request
from hello import hello

app = Flask(__name__)

@app.route('/')
def home():
   # return 'This is Home!'
   name = request.args.get('name','사용자')
   greeting = hello(name)
   return f"{greeting}"#, render_template('index.html')
   # return render_template('index.html')

@app.route('/login_do')
def login():
   # return 'This is Home!'
   return render_template('login_do.html')

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)