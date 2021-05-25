""" main module """
from datetime import date
from requests import request

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

    for rate_response in rate_responses:
        print(rate_response)


if __name__ == "__main__":
    get_rates()
