""" rate server module """

from typing import Optional, Any
from multiprocessing.sharedctypes import Synchronized # type: ignore
import multiprocessing as mp
import sys
import socket
import threading
import re
import json
import requests
import pyodbc

conn_options = [
    "DRIVER={ODBC Driver 17 for SQL Server}",
    "SERVER=127.0.0.1,1433",
    "DATABASE=ratesapp",
    "UID=sa",
    "PWD=sqlDbp@ss!",
]

conn_str = ";".join(conn_options)

# Task 1 - Cache Rate Results

# Upgrade the application to check the database for a given exchange rate
# (date, currency)

# If the exchange rate was previously retrieved and stored in the
# database, then return it

# If the exchange rate is not in the database, then download it, add it to
# the database and return it

# Task 2 - Clear Rate Cache

# Add a command for clearing the rate cache from the server command
# prompt. Name the command "clear".

CLIENT_COMMAND_PARTS = [
    r"^(?P<name>[A-Z]*) ",
    r"(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2}) ",
    r"(?P<symbol>[A-Z]{3})$",
]

CLIENT_COMMAND_REGEX = re.compile("".join(CLIENT_COMMAND_PARTS))

class ClientConnectionThread(threading.Thread):
    """ client connection thread """

    def __init__(self,
                 conn: socket.socket,
                 client_count: Synchronized,
                 ) -> None:
        threading.Thread.__init__(self)
        self.conn = conn
        self.client_count = client_count

    def run(self) -> None:

        self.conn.sendall(b"Connected to the Rate Server")

        while True:
            data = self.conn.recv(2048)
            if not data:
                break

            client_command_str = data.decode('UTF-8')

            client_command_match = CLIENT_COMMAND_REGEX.match(
                client_command_str)

            if not client_command_match:
                self.conn.sendall(b"Invalid Command Format")
            else:
                self.process_client_command(client_command_match.groupdict())
        
        with self.client_count.get_lock():
            self.client_count.value -= 1

    def process_client_command(self, client_command: dict[str, Any]) -> None:
        """ process client command """

        if client_command["name"] == "GET":

            with pyodbc.connect(conn_str) as con:

                closing_date = client_command["date"]
                currency_symbol = client_command["symbol"]

                rate_sql = " ".join([
                    "select exchangerate as exchange_rate from rates",
                    "where closingdate = ? and currencysymbol = ?"
                ])

                with con.cursor() as cur:

                    cur.execute(rate_sql, (closing_date, currency_symbol))

                    rate = cur.fetchone()

                    if rate:
                        self.conn.sendall(
                            str(rate.exchange_rate).encode('UTF-8'))
                        return

                url = "".join([
                    "http://127.0.0.1:5000/api/",
                    closing_date,
                    "?base=USD&symbols=",
                    currency_symbol,
                ])

                response = requests.request("GET", url)
                rate_data = json.loads(response.text)

                exchange_rate = rate_data["rates"][client_command["symbol"]]

                insert_rate_sql = " ".join([
                    "insert into rates",
                    "(closingdate, currencysymbol, exchangerate)",
                    "values (?, ?, ?)"
                ])

                con.execute(insert_rate_sql,
                    (closing_date, currency_symbol, exchange_rate))


                self.conn.sendall(str(exchange_rate).encode("UTF-8"))

        else:
            self.conn.sendall(b"Unknown Command Name")


def rate_server(host: str, port: int, client_count: Synchronized) -> None:
    """rate server"""

    with socket.socket(
        socket.AF_INET, socket.SOCK_STREAM) as socket_server:
        
        socket_server.bind( (host, port) )
        socket_server.listen()

        while True:

            conn, _ = socket_server.accept()

            with client_count.get_lock():
                client_count.value += 1

            client_con_thread = ClientConnectionThread(conn, client_count)
            client_con_thread.start()




class RateServerError(Exception):
    """ rate server error class """


def command_start_server(
    server_process: Optional[mp.Process],
    client_count: Synchronized) -> mp.Process:
    """ command start server """

    if server_process and server_process.is_alive():
        print("server is already running")
    else:
        server_process = mp.Process(
            target=rate_server, args=('127.0.0.1', 5050, client_count))
        server_process.start()
        print("server started")

    return server_process


def command_stop_server(
    server_process: Optional[mp.Process]) -> Optional[mp.Process]:
    """ command stop server """

    if not server_process or not server_process.is_alive():
        print("server is not running")
    else:
        server_process.terminate()
        print("server stopped")

    server_process = None

    return server_process


def command_server_status(server_process: Optional[mp.Process]) -> None:
    """ output the status of the server """

    # typeguard
    if server_process and server_process.is_alive():
        print("server is running")
    else:
        print("server is stopped")


def command_client_count(client_count: int) -> None:
    """ output the number of clients connected """
    print(f"{client_count} client(s) connected")


def command_clear_cache() -> None:
    """ command clear cache """

    with pyodbc.connect(conn_str) as con:
        con.execute("delete from rates")

    print("cache cleared")


def command_exit(server_process: Optional[mp.Process]) -> None:
    """ exit the rates server app """

    if server_process and server_process.is_alive():
        server_process.terminate()


def main() -> None:
    """Main Function"""

    try:

        client_count: Synchronized = mp.Value('i', 0)
        server_process: Optional[mp.Process] = None

        while True:

            command = input("> ")

            if command == "start":
                server_process = command_start_server(
                    server_process, client_count)
            elif command == "stop":
                server_process = command_stop_server(server_process)
            elif command == "status":
                command_server_status(server_process)
            elif command == "count":
                command_client_count(client_count.value)
            elif command == "clear":
                command_clear_cache()
            elif command == "exit":
                command_exit(server_process)
                break

    except KeyboardInterrupt:
        command_exit(server_process)

    sys.exit(0)


if __name__ == '__main__':
    main()
