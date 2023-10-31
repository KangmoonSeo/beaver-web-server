from fastapi import FastAPI
import openai

app = FastAPI()

@app.get("/items/{item_id}")
async def test(item_id:int):
    return {"message" : "Hellasdfasdfasdfasdfo World",
            "item_id" : item_id}

@app.get("/prompt/{prompt}")
async def prompt(prompt:str):
    openai.api_key = "empty"
    openai.api_base = "http://165.246.75.161:10111/v1"
    completion = openai.Completion.Create(model="lmsys/vicuna-7b-v1.3", prompt=prompt, max_tokens=30)
    return {"message" : completion}
