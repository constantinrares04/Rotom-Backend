from fastapi import FastAPI

app=FastAPI()

@app.get("/")

def root():
	return {"Sara, why are you gay?"}

@app.get("/item")
def get_item():
	return {"Sara is NO LONGER gay!"}

