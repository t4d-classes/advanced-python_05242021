""" main module """

import time

from rates_demo.get_rates import get_rates_threaded
from rates_demo.rates_api_server import rates_api_server

if __name__ == "__main__":

    with rates_api_server():

        start = time.time()
        get_rates_threaded()
        print(f"threaded time elapsed: {time.time() - start}")

