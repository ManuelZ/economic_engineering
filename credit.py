from __future__ import annotations

# Standard-Library imports
import datetime as dt

# External imports
import pandas as pd
from sympy import Symbol
from sympy.solvers import nsolve
from dateutil.relativedelta import relativedelta
from pandas.tseries.offsets import Day, Easter, CustomBusinessDay
from pandas.tseries.holiday import nearest_workday, AbstractHolidayCalendar, Holiday

# Local imports
from config import (
    EAR,
    CAPITAL,
    PAYMENT_DAY,
    PERIODS,
    BUY_DATE
)
from economic_engineering import (
    p_given_f,
    p_given_a,
    EAR_to_EMR,
    EMR_to_EDR,
)

DATE_FORMAT = '%d/%m/%Y'


class PeruHolidayCalendar(AbstractHolidayCalendar):
    """ Perú Holiday Calendar. To be revised. """
    rules = [
        Holiday("New Year's Day", month=1, day=1, observance=nearest_workday),
        Holiday("New Year's 2nd Day", month=1, day=2, observance=nearest_workday),
        Holiday("Jueves Santo", month=1, day=1, offset=[Easter(), Day(-3)]),
        Holiday("Dia del trabajo", month=5, day=1),
        Holiday("Viernes Santo", month=1, day=1, offset=[Easter(), Day(-2)]),
        Holiday("San Pedro y San Pablo", month=6, day=29),
        Holiday("Dia de la independencia 1", month=7, day=28),
        Holiday("Dia de la independencia 2", month=7, day=29),
        Holiday("Batalla de Junin", month=8, day=6),
        Holiday("Santa Rosa de Lima", month=8, day=30),
        Holiday("Combate de Angamos", month=10, day=8),
        Holiday("Dia de todos los santos", month=11, day=1),
        Holiday("Dia de la Inmaculada Concepcion", month=12, day=8),
        Holiday("Batalla de Ayacucho", month=12, day=9),
        Holiday("Navidad", month=12, day=25),
    ]


def is_business_day(business_days:pd.offsets.CustomBusinessDay, date: dt.datetime):
    """
    If the comparison `date == business_days.rollforward(date)` is equal, the 
    date meets the business day rules and can be considered a valid business day. 
    (The `.rollforward` method adjusts the date only if it's not a valid business day).

    Parameters:
        - business_days: Custom business day offset used to define business days.
        - date: The date to be evaluated.
    """
    return date == business_days.rollforward(date)


def get_payment_dates(buy_date:dt.datetime, payment_day:int, timesteps:int, debug:bool=False):
    """
    Calculate a series of payment dates based on the start date, payment day, and the number of timesteps.
    
    Parameters:
    - buy_date: The day when the acquisition was made.
    - payment_day: The desired day of the month for payments.Determines 
     the desired day of the month for payments. If the calculated payment date 
     falls on a non-business day, the date is adjusted to the next valid 
     business day based on the business day rules defined by the `offseter`.
    - timesteps: The number of payment dates to calculate.
    
    Returns:
        # TODO: review this
        - list of datetime.date: A list of payment dates, starting from the month following the buy_date,
          with each subsequent payment date adjusted to the next valid business day based on the given payment_day
          and business day rules defined by the `offseter`.

    """

    offseter = CustomBusinessDay(calendar=PeruHolidayCalendar())

    # Find the closest payday to today
    # Check the payment logic here and explain
    # I'm expressing that the first payment will be done not on the closest payday
    # but on the following one. Is this always like that?
    payday = buy_date + relativedelta(day=payment_day, months=1)

    paydays = []
    for _ in range(timesteps):
        payday += relativedelta(day=payment_day, months=1)

        if not is_business_day(offseter, payday):
            if debug: print(f"{payday.strftime(DATE_FORMAT)} is not a business day, ", end="")
            payday = offseter.rollforward(payday)
            if debug: print(f"{payday.strftime(DATE_FORMAT)} is.")
        
        paydays.append(payday)
    
    return paydays


def calculate_payment_amount(
    capital:float,
    i_edr: float,
    buy_date: dt.datetime,
    payment_dates: list[dt.datetime]
    ) -> tuple[float]:
    """
    Calculate monthly equal payment amounts for a series of potentially unequally spaced payment dates.

    Parameters
        - capital
        - payment_dates
        - i_edr: Effective daily interest rate

    Return
        - float: Constant payment amount for the n-1 payment dates.
        - float: Final payment amount that ensures the total payments cover 
        the entire capital amount. Accounts for the rounding adjustment of the
        constant payment amount.
    """

    F_sym = Symbol("F", real=True)

    Eq = capital
    for date in payment_dates:
        days = (date - buy_date).days
        Eq -= p_given_f(F_sym, i_edr, days)

    [F_val] = nsolve([Eq], [F_sym], [1])

    rounded_val = round(F_val, 2)
    
    # To account for the rounding
    last_val = round(F_val + (F_val - rounded_val) * len(payment_dates), 2)
    
    return rounded_val, last_val


if __name__ == "__main__":

    # Amount borrowed
    capital = CAPITAL
    # Effective Annual Rate
    i_ear = EAR
    # Number of periods
    periods = PERIODS
    # Payment date, string
    payment_day = PAYMENT_DAY
    # Day when the borrow/buy was made
    buy_date = BUY_DATE

    
    # Effective Monthly Rate
    i_emr = EAR_to_EMR(i_ear)
    
    # Effective Daily Rate
    i_edr = EMR_to_EDR(i_emr)

    # Simple calculation of the constant monthly payment
    A_sym = Symbol("A", real=True)
    Eq = capital - p_given_a(A_sym, i=i_emr, n=12)
    [A_val] = nsolve([Eq], [A_sym], [183])
    print(f"Periodic payment (simple calculation) = {A_val:.2f}")

    # Exact calculation of the constant monthly payment
    buy_date = dt.datetime.strptime(buy_date, DATE_FORMAT)
    payment_dates = get_payment_dates(buy_date, payment_day=payment_day, timesteps=periods)
    A, last_A = calculate_payment_amount(capital, i_edr, buy_date, payment_dates)
    print(f"Periodic payment (exact calculation) = {A}")
    print(f"Last payment (exact calculation) = {last_A}")