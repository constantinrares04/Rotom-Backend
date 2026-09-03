from fastapi import FastAPI
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["rotom_db"]
ingrediente = db["ingredients"]
app = FastAPI()

@app.get("/")
def root():
    return {"message": "API pentru licenta."}

@app.get("/ingredients")
def get_item():
    all_ing = list(ingrediente.find({},{"_id":0,"tags":0}).sort("id", 1))
    return {"data": all_ing, "count": len(all_ing)}

@app.get("/unavailable_ingredients")
def get_item():
    all_ing = list(ingrediente.find({"quantity": {"$eq": 0}}, {"_id":0,"tags":0}).sort("id", 1))
    return {"data": all_ing, "count": len(all_ing)}

@app.get("/available_ingredients")
def get_item():
    all_ing = list(ingrediente.find({"quantity": {"$gt": 0}}, {"_id":0,"tags":0}).sort("id", 1))
    return {"data": all_ing, "count": len(all_ing)}

@app.get("/ingredients/{id}")
def get_item(id: int):
    item = ingrediente.find_one({"id": id}, {"_id":0})
    if item:
        return {"data": [item]}
    else:
        return {"error": "Ingredient not found"}
    
@app.get("/ingredients/{id}/add/{quantity}")
def get_item(id: int, quantity: float):
    item = ingrediente.find_one({"id": id}, {"_id":0,"unit":0,"tags":0,"priority":0 })
    if item:
        new_quantity = item["quantity"] + quantity
        ingrediente.update_one({"id": id}, {"$set": {"quantity": new_quantity}})
        return {"message": "Quantity updated successfully"}
    else:
        return {"error": "Ingredient not found"}

@app.get("/ingredients/{id}/sub/{quantity}")
def get_item(id: int, quantity: float):
    item = ingrediente.find_one({"id": id}, {"_id":0,"unit":0,"tags":0,"priority":0 })
    if item:
        new_quantity = item["quantity"] - quantity
        if new_quantity < 0:
            return {"error": "Insufficient quantity"}
        ingrediente.update_one({"id": id}, {"$set": {"quantity": new_quantity}})
        return {"message": "Quantity updated successfully"}
    else:
        return {"error": "Ingredient not found"}