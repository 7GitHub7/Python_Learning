from flask import Flask, render_template

app = Flask(__name__)

class Store():
    produckts = {"cukier": 2.3 , "mąka":2.69, "czekolada":2}



@app.route('/Adam')
def hello():
   return render_template("index.html") 

# @app.route('/Basia')
# def hello():
#     name = request.args.get("name", "World")
#     return f'Hello, {escape(name)}!'

# @app.route('/Celina')
# def hello():
#     name = request.args.get("name", "World")
#     return f'Hello, {escape(name)}!'