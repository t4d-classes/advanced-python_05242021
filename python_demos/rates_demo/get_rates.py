""" main module """
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from requests import request
import time
import threading

from rates_demo.business_days import business_days


def get_rates() -> None:
    """ get the rates """

    start_date = date(2021, 1, 1)
    end_date = date(2021, 3, 31)

    rate_responses: list[str] = []

    for business_day in business_days(start_date, end_date):

        rate_url = "".join([
            "http://127.0.0.1:5000/api/",
            str(business_day),
            "?base=USD&symbols=EUR"])

        response = request("GET", rate_url)
        rate_responses.append(response.text)

    # for rate_response in rate_responses:
    #     print(rate_response)

    print(f"num of responses: {len(rate_responses)}")

    print(rate_responses)


def get_rate_task(business_day: date, responses: list[str]) -> None:
    """ get rate task function """

    rate_url = "".join([
        "http://127.0.0.1:5000/api/",
        str(business_day),
        "?base=USD&symbols=EUR"])    

    response = request("GET", rate_url)
    responses.append(response.text)


def get_rates_threaded() -> None:
    """ get the rates """

    start_date = date(2021, 1, 1)
    end_date = date(2021, 3, 31)

    rate_responses: list[str] = []
    threads: list[threading.Thread] = []

    for business_day in business_days(start_date, end_date):
        a_thread = threading.Thread(
            target=get_rate_task, args=(business_day,rate_responses))
        a_thread.start()
        threads.append(a_thread)

    for a_thread in threads:
        a_thread.join()

    print(f"num of responses: {len(rate_responses)}")
    print(rate_responses)

# threadpool version
# def get_rates_threaded() -> None:
#     """ get the rates """

#     start_date = date(2021, 1, 1)
#     end_date = date(2021, 3, 31)

#     rate_responses: list[str] = []

#     with ThreadPoolExecutor() as executor:

#         rate_responses = list(executor.map(
#             get_rate_task,
#             [ business_day for business_day
#             in business_days(start_date, end_date) ]))

#     print(f"num of responses: {len(rate_responses)}")
#     print(rate_responses)

# def get_rates_threaded_gen() -> None:
#     """ get the rates """

#     start_date = date(2021, 1, 1)
#     end_date = date(2021, 3, 31)

#     rate_responses: list[str] = []

#     with ThreadPoolExecutor() as executor:

#         executor.map(
#             lambda params: get_rate_task(*params),
#             ( (business_day, rate_responses) for business_day
#             in business_days(start_date, end_date) ))

#     print(f"num of responses: {len(rate_responses)}")


# if __name__ == "__main__":
    # start = time.time()
    # get_rates()
    # print(f"original time elapsed: {time.time() - start}")
    # start = time.time()
    # get_rates_threaded()
    # print(f"threaded time elapsed: {time.time() - start}")
    # start = time.time()
    # get_rates_threaded_gen()
    # print(f"threaded time elapsed: {time.time() - start}")
