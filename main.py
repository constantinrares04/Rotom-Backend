from fastapi import FastAPI, Query # pyright: ignore[reportMissingImports]
from pymongo import MongoClient # pyright: ignore[reportMissingImports]

client = MongoClient("mongodb://localhost:27017/")
db = client["rotom_db"]
retete = db["retete"]
ingrediente = db["ingrediente"]
app = FastAPI()

@app.get("/")
def root():
    return {"message": "API pentru licenta."}

@app.get("/ing/all")
def get_item():
    all_ing = list(ingrediente.find({},{"_id":0}).sort("id", 1))
    return {"data": all_ing, "count": len(all_ing)}

@app.get("/ings/unavailable")
def get_item():
    all_ing = list(ingrediente.find({"quantity": {"$eq": 0}}, {"_id":0,"tags":0,"unit":0,"priority":0}).sort("id", 1))
    return {"data": all_ing, "count": len(all_ing)}

@app.get("/ing/available")
def get_item():
    all_ing = list(ingrediente.find({"quantity": {"$gt": 0}}, {"_id":0,"tags":0}).sort("id", 1))
    return {"data": all_ing, "count": len(all_ing)}

@app.get("/ing/{id}")
def get_item(id: int):
    item = ingrediente.find_one({"id": id}, {"_id":0})
    if item:
        return {"data": [item]}
    else:
        return {"error": "Ingredient not found"}
    
@app.put("/modify/{id}")
def modify_quantity(id: int, quantity: float):
    item = ingrediente.find_one({"id": id}, {"_id": 0, "unit": 0, "tags": 0, "priority": 0})
    if item:
        new_quantity = item["quantity"] + quantity
        if new_quantity < 0:
            return {"error": "Insufficient quantity"}

        ingrediente.update_one({"id": id}, {"$set": {"quantity": new_quantity}})
        return {"message": "Quantity updated successfully", "new_quantity": new_quantity}
    else:
        return {"error": "Ingredient not found"}

@app.get("/recipies/all")
def get_item():
    all_rec = list(retete.find({}, {"_id": 0, "id": 1, "name": 1}).sort("id", 1))
    return {"data": all_rec, "count": len(all_rec)}

@app.get("/recipies/ing/{ing_id}")
def get_item(ing_id: int):
    items = list(retete.find({"ingredients": {"$in": [ing_id]}}, {"_id": 0}).sort("id", 1))
    if items:
        return {"data": items, "count": len(items)}
    else:
        return {"error": "Recipe not found"}

@app.get("/recipies/ing_list")
def get_recipes_by_ingredients(ids: list[int] = Query(...)):
    query = {
        "ingredients": {"$exists": True, "$ne": []},
        "$expr": {"$setIsSubset": ["$ingredients", ids]},
    }
    recipes = list(
        retete.aggregate(
            [
                {"$match": query},
                {"$sample": {"size": 10}},
                {"$project": {"_id": 0, "id": 1, "name": 1}},
            ]
        )
    )
    return {"data": recipes, "count": len(recipes)}

@app.get("/recipies/{id}")
def get_item(id: int):
    item = retete.find_one({"id": id}, {"_id":0})
    if item:
        return {"data": [item]}
    else:
        return {"error": "Recipe not found"}
