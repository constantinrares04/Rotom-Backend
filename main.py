from fastapi import FastAPI
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["rotom_db"]
ingrediente = db["ingredients"]
app=FastAPI()

@app.get("/")
def root():
	return {"API-urile iti ofera un raspuns din eter!"}

@app.get("/ing")
def get_item():
	all_ing=list(ingrediente.find())
	return {"message":f"{all_ing}"}

@app.get("/ing/{id}")
def get_item(id: str):
    if not ObjectId.is_valid(id):
        return {"message": "Format ID invalid!"}
    item = ingrediente.find_one({"_id": f"ObjectId({id})"})
    if item:
        item["_id"] = str(item["_id"])
        return {"data": item}
    else:
        return {"message": "Nu exista ingredientul cu id-ul dat!"}