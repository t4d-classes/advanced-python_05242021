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

    sql = "select * from Rates where RatesId = ?"

    with con.cursor() as cur:
        cur.execute(sql, (2,))
        rate = cur.fetchone()
        print(rate)

    sql = "select count(*) as rate_count from Rates where RatesId in (?, ?, ?)"

    with con.cursor() as cur:
        cur.execute(sql, (2,4,5))
        result = cur.fetchone()
        print(result.rate_count)        




