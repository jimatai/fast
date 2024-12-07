from fastapi import FastAPI, Body
from pydantic import BaseModel

app = FastAPI()

#https://pkpd2fast.herokuapp.com/

class Parameters(BaseModel):
    gender: str = "男性"
    weight: float = 60
    age: float = 70
    scr: float = 0.85
    ccr: float = 68.63

class Intent(BaseModel):
    displayName: str = "Q6-1-check ccr"

class QueryResult(BaseModel):
    parameters: Parameters
    intent: Intent

class NestedData(BaseModel):
    queryResult: QueryResult

@app.post('/')
async def Thomson(data: NestedData):
    get = data.queryResult.parameters
    intent = data.queryResult.intent.displayName

    if intent == "Q6-1-check ccr":
        gender = get.gender
        weight = get.weight
        age = get.age
        scr = get.scr
        if scr < 0.6:
            scr = 0.6
        if gender == "男性":
            ccr = (140-age)*weight / (72*scr)
        elif gender == "女性":
            ccr = (0.85*(140-age)*weight) / (72*scr)

        if age >= 18:
            answer_ssml = f'<speak><prosody rate="1.1" pitch="-15%">推定クレアチニンクリアランスは、{str(round(ccr,2))}（ミリリットルパーミニッツ）です。\nこの推定クレアチニンクリアランスをもとに、投与量を計算してよろしいですか？</prosody></speak>'
            answer = f"推定クレアチニンクリアランスは、{str(round(ccr,2))} mL/minです。\nこの推定クレアチニンクリアランスを基に、投与量を計算してよろしいですか？"
        else:
            answer_ssml = f'<speak><prosody rate="1.1" pitch="-15%">推定クレアチニンクリアランスは、{str(round(ccr,2))}（ミリリットルパーミニッツ）です。\nこの患者は成人ではありませんが、この推定クレアチニンクリアランスをもとに、投与量を計算してよろしいですか？</prosody></speak>'
            answer = f"推定クレアチニンクリアランスは、{str(round(ccr,2))} mL/minです。\nこの患者は成人ではありませんが、この推定クレアチニンクリアランスを基に、投与量を計算してよろしいですか？"

        return {
            "fulfillmentMessages": [
                {
                    "platform": "ACTIONS_ON_GOOGLE",
                    "simpleResponses": {
                    "simpleResponses": [
                        {
                            "textToSpeech": answer_ssml,
                            "displayText": answer
                        }
                    ]
                    }
                }
            ],
            "outputContexts":[
                {
                    "name":"projects/thom-skph/agent/sessions/111101ab-c8c1-4356-b2d2-cff4e41eb0df/contexts/Q6-1-checkccr",
                    "lifespanCount": 1,
                    "parameters": {
                        "ccr": round(ccr, 2),
                        "ccrssml": answer_ssml,
                        "ccrtext": answer
                    }
                }
            ]              
        }
    
    elif intent == "Result":
        weight = get.weight
        ccr = get.ccr

        if 90 < weight:
            first_dose = "2000mg"
        elif 60 <= weight <= 90:
            first_dose = "1500mg"
        elif weight < 60:
            first_dose = "1000mg"
        else:
            first_dose = ""

        if 110 < ccr:
            second_dose = "1500mg"
            usage = "1日2回"
        elif 90 <= ccr <= 110:
            second_dose = "1250mg"
            usage = "1日2回"
        elif 75 <= ccr < 90:
            second_dose = "1000mg"
            usage = "1日2回"
        elif 55 <= ccr < 75:
            second_dose = "750mg"
            usage = "1日2回"
        elif 40 <= ccr < 55:
            second_dose = "500mg"
            usage = "1日2回"
        elif 30 <= ccr < 40:
            second_dose = "750mg"
            usage = "1日1回"
        elif 20 <= ccr < 30:
            second_dose = "500mg"
            usage = "1日1回"
        elif ccr < 20:
            second_dose = "500mg"
            usage = "1日1回、隔日"

        else:
            second_dose = ""
            usage = ""

        answer = f"バンコマイシンの1回目の投与量は、{first_dose}で、2回目以降の投与量は、1回 {second_dose}を、{usage}投与です。"

        return {
            "fulfillmentMessages": [
                {
                    "platform": "ACTIONS_ON_GOOGLE",
                    "simpleResponses": {
                    "simpleResponses": [
                        {
                            "textToSpeech": f'<speak><prosody rate="1.1" pitch="-15%">{answer}</prosody></speak>',
                            "displayText": answer
                        }
                    ]
                    }
                }
            ],
            "outputContexts":[
                {
                    "name":"projects/thom-skph/agent/sessions/111101ab-c8c1-4356-b2d2-cff4e41eb0df/contexts/Result",
                    "lifespanCount": 1,
                    "parameters": {
                        "result": answer
                    }
                }    
            ]              
        }
