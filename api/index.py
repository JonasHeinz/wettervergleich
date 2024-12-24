from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import altair as alt

app = FastAPI()

allow_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def filter(parameter="T", station="Zch_Stampfenbachstrasse", date=pd.to_datetime('2021-05-30 00:00:00+01:00'), year="2022", interval="monat"):

    data = pd.read_csv("./data/wetterdaten_combined.csv")

    data['Datum'] = pd.to_datetime(data['Datum'])
    endDate = date
    if interval == "jahr":
        endDate += pd.DateOffset(year=1)
    elif interval == "monat":
        endDate += pd.DateOffset(months=1)
    elif interval == "woche":
        endDate += pd.DateOffset(weaks=1)

    print(endDate)

    data = data[data['Datum'] >= date]
    data = data[data['Datum'] <= endDate]
    data = data[data['Parameter'] == parameter]
    data = data[data['Standort'] == station]
    return data


@app.get("/specs/")
async def get_spec():
    print(filter())

    chart = alt.Chart(filter()).mark_point().encode(
        x='Datum',
        y='Wert'
    )
    return JSONResponse(content=chart.to_dict())
