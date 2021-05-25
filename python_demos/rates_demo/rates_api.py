""" main module """
from typing import Any
from random import randint
import pathlib
import csv
import math
import time
from flask import Flask, jsonify, abort, request, Response

rates: list[dict[str,Any]] = []

app = Flask(__name__)

@app.route("/check")
def check() -> str:
    """ health check route function """
    return "READY"

@app.route("/api/<rate_date>")
def rates_by_date(rate_date: str) -> Response:
    """ rates by date route function """

    time.sleep(randint(1, 5) * 0.05)

    for rate in rates:

        if rate["Date"] == rate_date:

            base_country = request.args.get("base", "EUR")

            if "symbols" in request.args:
                country_symbols = request.args["symbols"].split(",")
            else:
                country_symbols = [col for col in rate if col != "Date"]

                # [for col in rate if col != "Date" do col]

            country_rates = {
                country_code: country_rate / rate[base_country]
                for (country_code, country_rate) in rate.items()
                if country_code != "Date" and
                country_code in country_symbols and
                not math.isnan(country_rate)
            }

            return jsonify({
                "date": rate["Date"],
                "base": base_country,
                "rates": country_rates
            })


    abort(404)


def load_rates_history(rates_file_path: pathlib.Path) -> list[dict[str,Any]]:
    """ load rates history function """

    rates_history: list[dict[str,Any]] = []

    with open(rates_file_path) as rates_file:

        rates_file_csv = csv.DictReader(rates_file)

        for rate_row in rates_file_csv:

            rate_entry = { "Date": rate_row["Date"], "EUR": 1.0 }

            for rate_col in rate_row:
                if rate_col != "Date" and len(rate_col) > 0:
                    if rate_row[rate_col] == "N/A":
                        rate_entry[rate_col] = math.nan
                    else:
                        rate_entry[rate_col] = float(rate_row[rate_col])

            rates_history.append(rate_entry)

    return rates_history

def start_rates_api() -> None:
    """ start rates api function """

    global rates

    rates_file_path = pathlib.Path("..", "data", "eurofxref-hist.csv")

    rates = load_rates_history(rates_file_path)

    app.run()


if __name__ == "__main__":
    start_rates_api()
