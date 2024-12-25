from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import altair as alt

app = FastAPI()

allow_origins = [
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def filter(parameter, date, interval):

    data = pd.read_csv("./data/wetterdaten_combined.csv")

    data['Datum'] = pd.to_datetime(data['Datum'])
    endDate = date
    if interval == "jahr":
        endDate += pd.DateOffset(years=1)
    elif interval == "monat":
        endDate += pd.DateOffset(months=1)
    elif interval == "woche":
        endDate += pd.DateOffset(weeks=1)

    data = data[data['Datum'] >= date]
    print(endDate)
    data = data[data['Datum'] <= endDate]

    data = data[data['Parameter'] == parameter]
    data = data[data['Standort'] == "Zch_Stampfenbachstrasse"]

    return data


@app.get("/specs/")
async def get_spec(parameter, date, year, interval):
    date = pd.to_datetime(date)
    dateBefore = date.replace(year=int(year))
    filtered = filter(parameter, date, interval)
    filteredBefore = filter(parameter, dateBefore, interval)
    filtered['Datum'] = filtered['Datum'].apply(lambda x: x.replace(year=2000))
    filteredBefore['Datum'] = filteredBefore['Datum'].apply(
        lambda x: x.replace(year=2000))
    chart = alt.Chart(filtered).mark_line(color="blue").encode(
        alt.X('Datum:T', axis=alt.Axis(format="%b %d")),
        alt.Y('Wert:Q'),
    )
    chartBefore = alt.Chart(filteredBefore).mark_line(color="orange").encode(
        alt.X('Datum:T', axis=alt.Axis(format="%b %d")),
        alt.Y('Wert:Q'),
    )

    return JSONResponse(content=(alt.layer(chart, chartBefore)).to_dict())
