""" connection demo """

from typing import Any
import pyodbc

docker_conn_options = [
    "DRIVER={ODBC Driver 17 for SQL Server}",
    "SERVER=127.0.0.1,1433",
    "DATABASE=ratesapp",
    "UID=sa",
    "PWD=sqlDbp@ss!",
]

with pyodbc.connect(";".join(docker_conn_options)) as con:

    new_rate: dict[str, Any] = {
        "closing": '2021-04-01',
        "rate": 0.45,
        "symbol": "HKD",
    }

    sql = " ".join([
        "insert into Rates (ClosingDate, ExchangeRate, CurrencySymbol)"
        "values (?, ?, ?)"
    ])

    rates = con.execute(sql, list(new_rate.values()))

