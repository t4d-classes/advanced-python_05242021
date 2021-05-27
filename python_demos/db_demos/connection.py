""" connection demo """

import pyodbc

docker_conn_options = [
    "DRIVER={ODBC Driver 17 for SQL Server}",
    "SERVER=127.0.0.1,1433",
    "DATABASE=ratesapp",
    "UID=sa",
    "PWD=sqlDbp@ss!",
]

with pyodbc.connect(";".join(docker_conn_options)) as con:

    sql = " ".join([
        "select ratesid, closingdate,"
        "CurrencySymbol as currency_symbol, exchangerate",
        "from rates"
    ])

    rates = con.execute(sql)

    for rate in rates:
        # print(rate[2])
        print(rate.currency_symbol)
