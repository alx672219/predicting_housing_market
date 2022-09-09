"""CSC110 COVID-19 Final Project: Modelling the Canadian Housing Market

Copyright and Usage Information
===============================

This file is Copyright (c) 2021 Terence Liu, Woojin Jang, and Charlie Tao.
"""
import datetime
from dataclasses import dataclass


@dataclass
class Mortgage:
    """Loan for a residency, including the house price.

    Attributes:
        - rate_type: The type of interest rate on the mortgage
        - fixed_rate: The interest rate when the mortgage is on fixed interest, in %
        - property_price: Price of the property that the mortgage is being taken for
        - principal: The amount borrowed from a lender
        - period: How long the mortgage is set to be paid off by, the amortization period (years)
        - date: The date at which the mortgage will begin

    Representation Invariants:
        - self.rate_type in ['fixed', 'variable']
        - self.principal <= self.property_price
    """
    rate_type: str
    fixed_rate: float
    property_price: float
    principal: float
    period: int
    date: datetime.date
