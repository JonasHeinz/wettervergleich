from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import csv
import altair as alt
import datetime as dt

app = FastAPI()

allow_origins = [
    "http://localhost:3000",
    "https://wettervergleich.vercel.app",
    "https://wettervergleich-git-main-jonasheinzs-projects.vercel.app/",
    "https://wettervergleich-jfglsmnhe-jonasheinzs-projects.vercel.app/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=allow_origins,
    allow_headers=["*"],
)

FILE_PATH = "./data/wetterdaten_combined.csv"


def parse_date(date_str):
    try:
        return dt.datetime.fromisoformat(date_str).replace(tzinfo=None)
    except ValueError:
        return None


def filter(parameter, date, interval):
    endDate = date

    if interval == "jahr":
        endDate = dt.datetime(date.year + 1, date.month, date.day)
    elif interval == "monat":
        next_month = date.month + 1 if date.month < 12 else 1
        next_year = date.year if date.month < 12 else date.year + 1
        endDate = dt.datetime(next_year, next_month, date.day)
    elif interval == "woche":
        endDate = date + dt.timedelta(weeks=1)

    filtered_data = []
    with open(FILE_PATH, mode="r", newline="", encoding="utf-8") as file:
        data = csv.DictReader(file)
        for row in data:
            if row["Datum"] != "Datum" and row["Wert"].strip():
                row_date = parse_date(row["Datum"])
                if (
                    date <= row_date <= endDate
                    and row["Parameter"] == parameter
                    and row["Standort"] == "Zch_Stampfenbachstrasse"
                ):
                    filtered_data.append({
                        "Datum": row_date.isoformat(),
                        "Wert": float(row["Wert"]),
                        "Legende": date.year
                    })

    return filtered_data


def einheit(parameter):
    if parameter == "T":
        return "°C"
    elif parameter == "RainDur":
        return "min"
    elif parameter == "StrGlo":
        return "W/m2"


@app.get("/specs/")
async def get_spec(parameter, date, year, interval):
    parsed_date = parse_date(date)
    dateBefore = parsed_date.replace(year=int(year))

    filtered = filter(parameter, parsed_date, interval)

    filteredBefore = filter(parameter, dateBefore, interval)
    # for row in filteredBefore:
    #     row["Datum"] = parse_date(row["Datum"]).replace(
    #         year=parse_date(row["Datum"]).year + parsed_date.year - int(year)).isoformat()

    # chart = alt.Chart(alt.Data(values=filtered)).mark_line().encode(
    #     alt.X("Datum:T", axis=alt.Axis(format="%b %d"), title=None),
    #     alt.Y("Wert:Q", title=einheit(parameter),
    #           axis=alt.Axis(titleFontSize=18)),
    #     alt.Color("Legende:N",  scale=alt.Scale(scheme='viridis'))
    # )
    # chartBefore = alt.Chart(alt.Data(values=filteredBefore)).mark_line().encode(
    #     alt.X("Datum:T", axis=alt.Axis(format="%b %d"), title=None),
    #     alt.Y("Wert:Q"),
    #     alt.Color("Legende:N",  scale=alt.Scale(scheme='viridis'),
    #               legend=alt.Legend(title="Jahr", labelFontSize=18,  titleFontSize=18, orient='bottom',
    #                                 ))
    # ).properties(
    #     title=f'Wettervergleich {year} zu {parsed_date.year}',
    #     width=600,
    #     height=400,
    # )

    # mean = round(sum(float(d["Wert"]) for d in filtered) / len(filtered), 2)
    # meanBefore = round(sum(float(d["Wert"])
    #                    for d in filteredBefore) / len(filteredBefore), 2)

    # chartCombined = alt.layer(chart, chartBefore).configure_axis(
    #     grid=False
    # ).configure_view(
    #     stroke=None,
    # ).configure_title(
    #     fontSize=24,
    # ).to_dict()

    return JSONResponse(content={"mean": filtered, "meanBefore": filteredBefore, "einheit": einheit(parameter), "vis": filteredBefore})
