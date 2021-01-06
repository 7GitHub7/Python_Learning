from flask import Flask, render_template, request, url_for, flash, redirect, make_response
from werkzeug.exceptions import abort
import json

import sqlite3

app = Flask(__name__)
app.secret_key = "super secret key"

class Product:
    name = ""
    unit_price = 0
    unit_in_stock = 0

    def __init__(self, name, unit_price, unit_in_stock):   
        self.name = name
        self.unit_price = unit_price
        self.unit_in_stock = unit_in_stock


class Client:
    name = ""
    wallet = 100
    
    def __init__(self, name):   
        self.name = name
    
        
        

product_list = []
client_list = [] 
product_list.append(Product("cukier_(opak._1_kg)",100,2))
product_list.append(Product("maka_(opak._1_kg)",2.69,150))
product_list.append(Product("czekolada_(100_gr)",3.40,50))

Adam  = Client("Adam")
Basia  = Client("Basia")
Celina  = Client("Celina")

client_list.append(Adam)
client_list.append(Basia)
client_list.append(Celina)


@app.route('/Adam')
def index():
  return render_template('index.html', product_list= product_list,client = Adam)

@app.route('/Basia')
def basia():
  return render_template('index.html', product_list= product_list,client = Basia)

@app.route('/Celina')
def celina():
  return render_template('index.html', product_list= product_list, client = Celina)  


@app.route('/buy', methods=["POST"])
def button():
    
    client_name = request.form['client_name']
    product_name = request.form['product_name']
    resp = make_response(redirect(f"/{client_name}"))
    client = Adam
    if request.cookies.get(client_name):
        client_history = json.loads(request.cookies.get(client_name))
    else:
        client_history = []        

    client_history.append(product_name)
    client_history_as_json = json.dumps(client_history)

    

    

    for product in product_list:
        if product_name in product.name:
            if product.unit_in_stock == 0:
                flash("Brak produktu w magazynie :(")
                return resp

            for client in client_list:
                if client.name == client_name:    
                    if (client.wallet - product.unit_price) < 0:
                        flash("Doładuj konto")
                        return resp
                    product.unit_in_stock = product.unit_in_stock -1
                    client.wallet = client.wallet - product.unit_price    

           
           

            resp.set_cookie(client_name,  str(client_history_as_json))
                        
    return resp


@app.route('/topup', methods=["POST"])
def topup():
    if request.method == "POST":
        client_name = request.form['client_name']
        client_topup_value = abs(float(request.form['value']))

        for client in client_list:
            if client.name == client_name:
                if (client.wallet + client_topup_value) <= 100:
                    client.wallet = client.wallet+ client_topup_value
                else:
                    flash('Maksymalna kwota którą możesz mieć w portfelu to 100zł')
                
        
    return redirect(f"/{client_name}")

@app.route('/shopping_list', methods=["POST"])
def shopping_list():
    client_name = request.form['client_name']
    flash("")
    flash(request.cookies.get(client_name))
            
    return redirect(f"/{client_name}")