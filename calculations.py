"""CSC110 COVID-19 Final Project: Modelling the Canadian Housing Market

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Terence Liu, Woojin Jang, and Charlie Tao.
"""
import math
import random
import datetime
import read_data as read
from mortgage import Mortgage


def projected_house_price(house: Mortgage, projection: int, want_total: bool,
                          interval=1) -> dict:
    """Returns a dictionary with a projection of how the property of interest will accrue or
    decrease, with the current mortgage loan applied to it. This assumes that the amount the
    borrower is able to pay stays the same, which means the mortgage for the house will increase
    as the house price increases.
    """
    predicted_prices = {}
    projected_rates = {}
    house_indices = read.csv_to_dict('data_files/real_residential_property_prices_change.csv')
    projected_change = proj_change(house_indices, projection, add_months(house.date, 1), -3, 1.0)
    avail_balance = house.property_price - house.principal
    new_house_price = house.property_price
    is_var = house.rate_type == 'variable'
    
    # Gets the projected interest rates if variable interest rate is chosen
    if is_var:
        projected_rates = proj_rates(projection, house.date)

    # For every calculated projected change, find the new house value
    for date in projected_change:
        new_house_price = (1 + projected_change[date] / 100) * new_house_price

        principal = new_house_price - avail_balance

        # Applies variable mortgage if variable, fixed if fixed.
        if is_var:
            month_pay = var_monthly_payment(principal, projected_rates, house.period, interval,
                                            date)
        else:
            month_pay = fixed_monthly_payment(principal, house.fixed_rate, house.period, date)

        # If the total house price is needed, does that. If not, defaults to monthly.
        if want_total:
            total_price = month_pay[date] * house.period * 12
        else:
            total_price = month_pay[date]

        predicted_prices[date] = total_price

    return predicted_prices


def proj_rates(projection: int, date: datetime.date) -> dict[datetime.date: float]:
    """Predicts the interest rates for variable interest based on prime interest data and the
    proj_change function depending on projection amount of time.
    """
    rate_data = read.csv_to_dict('data_files/mortgage_interest_rate.csv')
    return proj_change(rate_data, projection, add_months(date, 1), -1, 2.45)


def proj_change(data: dict[datetime.date: float], projection: int,
                date: datetime.date, increment: int, baseline: float) -> dict[datetime.date: float]:
    """Attempts to predict the coming months. Specifically will be used for the index and change
    datasets. Uses chaotic projection to try to simulate the unpredictability of the market, but
    the general trend is still the same.
    """
    projected_change = {date: baseline}
    change_dict = calc_change(data, increment)
    new_change = baseline

    # Finding the standard deviation
    values = list(change_dict.values())
    average_change = sum(values) / len(values)
    print(average_change)
    s_deviate = math.sqrt(sum([(v - average_change) ** 2 for v in values]) / len(values))
    print(s_deviate)

    # Applying the standard deviation to the projected dates.
    for i in range(0, math.floor(projection * 12 / abs(increment))):
        random_change = random.normalvariate(average_change, s_deviate)
        new_change += random_change
        print(new_change)
        projected_change[add_months(date, abs(increment) * (i + 1))] = new_change

    return projected_change


def calc_change(data: dict[datetime.date: float], increment: int) -> dict[datetime.date: float]:
    """Calculates and returns the difference between every two data dates in the dictionary

    >>> sample_data = {datetime.date(2021, 12, 1): 3.0, datetime.date(2022, 1, 1): 10.0}
    >>> calc_change(sample_data, -1)
    {datetime.date(2022, 1, 1): 7.0}
    >>> sample_data = {datetime.date(2021, 10, 1): 3.0, datetime.date(2022, 1, 1): 10.0}
    >>> calc_change(sample_data, -3)
    {datetime.date(2022, 1, 1): 7.0}
    >>> sample_data = {datetime.date(2021, 4, 1): 3.0, datetime.date(2022, 1, 1): 10.0}
    >>> calc_change(sample_data, -9)
    {datetime.date(2022, 1, 1): 7.0}
    """
    change_dict = {}

    for date in data:
        if add_months(date, increment) in data:
            change_dict[date] = data[date] - data[add_months(date, increment)]

    return change_dict


def fixed_monthly_payment(principal: float, rate: float, time: int, date: datetime.date) -> dict:
    """Calculates the monthly payment based on the principle, interest rate, and
    amortization period (time)

    >>> fixed_monthly_payment(100000, 5, 25, datetime.date(2021, 12, 1))
    {datetime.date(2021, 12, 1): 584.59}
    """
    p = principal
    r = rate / 100 / 12
    t = time

    monthly_payment = p * r * ((1 + r) ** (12 * t)) / ((1 + r) ** (12 * t) - 1)

    return {date: round(monthly_payment, 2)}


def var_monthly_payment(principal: float, rate_data: dict[datetime.date: float], period: int,
                        interval: float, date: datetime.date) -> dict:
    """Calculates the monthly payment based on the principle, variable interest rate, and
    amortization period (period). This will depend on our predictive model for the prime
    interest rate.

    Preconditions:
     - period % interval == 0
     - period >= interval
     - interval != 0.0
     - date.day == 1
    """
    month_to_payment = {}
    new_date = date

    for _ in range(0, 6):
        month_to_payment[new_date] =\
            fixed_monthly_payment(principal, rate_data[date], period, new_date)[new_date]
        new_date = add_months(new_date, int(interval))

    return month_to_payment


def add_months(date: datetime.date, months: int) -> datetime.date:
    """Adds months to the datetime.date object, increasing the year by 1 for every 12 months added.
    Months can be negative, which would add negative months, thus subtract months.

    >>> today = datetime.date(2022, 1, 14)
    >>> add_months(today, 19).isoformat()
    '2023-08-14'
    >>> add_months(today, -1).isoformat()
    '2021-12-14'
    >>> add_months(today, -3).isoformat()
    '2021-10-14'
    >>> add_months(today, 1).isoformat()
    '2022-02-14'
    """
    new_month = date.month + months
    new_year = date.year + math.floor(new_month / 12)

    if new_month == 0:
        new_year = date.year + math.floor(new_month / 12) - 1

    new_date = datetime.date(new_year, (new_month - 1) % 12 + 1,
                             date.day)
    return new_date
