from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

#https://pkpd2fast.herokuapp.com/

class Parameters(BaseModel):
    medicine:str = "アセトアミノフェン",
    unit: str = "kg",
    number: float = 10

class Intent(BaseModel):
    displayName: str = "薬"

class QueryResult(BaseModel):
    parameters: Parameters
    intent: Intent

class NestedData(BaseModel):
    queryResult: QueryResult

@app.post('/')
async def Thomson(data: NestedData):
    get = data.queryResult.parameters
    intent = data.queryResult.intent.displayName

    if intent == "薬":
        number = get.number
        dosage = number * 10

        return {
            "fulfillmentText":
                f"投与量は{dosage}mgです。"            
        }