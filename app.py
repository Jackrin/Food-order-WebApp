from flask import Flask, render_template, request, json
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING)
orders = (client["hamburger"])["Orders"]

@app.route("/")
def app_main():
    return render_template('index.html')

@app.route('/order', methods=["GET","POST"])
def order():
    data = request.form.to_dict()
    name = data.get("name")
    lastName = data.get("lastName")
    query = orders.find_one({"name":name, "lastName":lastName})
    count = orders.count_documents({"name":name, "lastName":lastName})
    print(count)
    if data.get("name") == "" or data.get("name") == None or data.get("lastName") == "" or data.get("lastName") == None:
        return render_template("order.html", feedback="Nome o cognome mancanti")
    data.pop("name", None)
    data.pop("lastName", None)
    dataList = list(data.keys())
    order = {
        "name" : name,
        "lastName" : lastName,
        "ingredients" : dataList,
        "served" : False,
    }
    if count > 0:
        orders.update_one({'_id' : ObjectId(query["_id"])},{'$set': {'ingredients':dataList}})
        return render_template("order.html", update="Ordine aggiornato")
    try:
        query = orders.insert_one(order)
    except:
        print("Query error")
    else:
        print("Added order")
    return render_template("order.html", order=order)

@app.route("/admin", methods=["GET","POST"])
def admin():
    data = request.form.to_dict()
    toRemove = data.get("id")
    if toRemove != None:
        orders.delete_one({"_id": ObjectId(toRemove)})
    cursor = list(orders.find())
    return render_template('admin.html', data=cursor)
