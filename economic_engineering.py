

def f_given_p(P, i, n):
    """Future value of a unique amount in the present.
    
    Parameters:
        P: present value
        i: compound interest rate in each period
        n: number of periods
    """
    return P * ((1 + i) ** n)


def p_given_f(F, i, n):
    """Present value of a unique amount in the future.
    
    Parameters:
        F: future value
        i: compound interest rate in each period
        n: number of periods
    """
    return F * (1 / ((1 + i) ** n))


def p_given_a(A, i, n):
    """Present value of a uniform payment series.
    
    Parameters:
        A: constant disbursement amount per period
        i: compound interest rate in each period
        n: number of periods
    """
    return A * (((1 + i) ** n) - 1) / (i * ((1 + i) ** n))


def a_given_p(p, i, n):
    """Uniform payment series amount given a present value.

    Parameters:
        P: Present unique value
        i: Compound interest rate in each period
        n: Number of periods
    """
    return (p * i) / (1 - (1 + i) ** (-n))


def f_given_a(A, i, n):
    """Future value of a uniform payment series.

    Parameters:
        A: constant disbursement amount per period
        i: compound interest rate in each period
        n: number of periods
    """
    return A * ((((1 + i) ** n) - 1) / i)


def NAR_to_effective_period_rate(EAR, n=12):
    """Nominal Annual Rate to Effective Period Rate.
    
    Parameters:
        EAR: Effective Annual Rate
        N: Number of compounding periods in one year
    """
    # E.g. if n=12, this is Effective Monthly Rate   
    return EAR / n


def NAR_to_EAR(NAR, n=12):
    """Nominal Annual Rate to Effective Annual Rate.

    Parameters:
        NAR: Nominal Annual Rate
        n: Number of compounding periods in one year
    """
    effective_period_rate = NAR / n
    return ((1 + effective_period_rate) ** n) - 1


def EAR_to_NAR(EAR, n=12):
    """Effective Annual Rate to Nominal Annual Rate.
    
    Parameters:
        EAR: Effective Annual Rate
        n: Number of capitalization periods in one year.
    """
    return n * (((1 + EAR) ** (1 / n)) - 1)


def EAR_to_EMR(EAR:float)->float:
    """
    Convert an Effective Annual Rate (EAR) into an Effective Monthly Rate (EMR).
    The Effective Annual Rate represents the interest rate when capitalization
    occurs on an annual basis. The objective here is to determine the equivalent
    rate that would apply when capitalization takes place monthly.

    Parameters:
        EAR: The Effective Annual Rate as a decimal, e.g., 0.08 for 8%.

    Returns:
        monthly_rate: The calculated Effective Monthly Rate as a decimal, 
        representing the equivalent rate for monthly capitalization.
    """
    return ((1 + EAR) ** (1/12)) - 1


def EMR_to_EAR(EMR):
    """Effective Monthly Rate to Effective Annual Rate"""
    return ((1 + EMR) ** (12)) - 1


def EMR_to_EDR(EMR):
    """Effective Monthly Rate to Effective Daily Rate"""
    return ((1 + EMR) ** (1/30)) - 1


def EDR_to_EAR(EDR):
    """Effective Daily Rate to Effective Annual Rate"""
    return ( (1 + EDR) ** 360) - 1
