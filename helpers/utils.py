from brownie import *

# Assert approximate integer
def approx(actual, expected, percentage_threshold):
    print(actual, expected, percentage_threshold)
    diff = int(abs(actual - expected))
    # 0 diff should automtically be a match
    if diff == 0:
        return True
    return diff < (actual * percentage_threshold // 100)


def Eth(value):
    return value / 1e18

def digg_shares_to_initial_fragments(digg, shares):
    """
    Convert shares to initial fragments scale
    For negative numbers (for example as part of a diff), use abs first
    """
    scaled = 0
    if shares < 0:
        shares = abs(shares)
        scaled = digg.sharesToInitialFragments(shares)
        scaled = -scaled
    else:
        scaled = digg.sharesToInitialFragments(shares)
    return "{:,.18f}".format(scaled / 1e18)

def digg_shares(value):
    return value / 1e68

def val(amount):
    # return amount
    if amount < Wei("0.0001 ether"):
        return "{:,.18f}".format(amount / 1e18)
    if amount < Wei("0.001 ether"):
        return "{:,.18f}".format(amount / 1e18)
    return "{:,.18f}".format(amount / 1e18)


def sec(amount):
    return "{:,.1f}".format(amount / 1e12)
