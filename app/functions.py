#Functions for robo app

def to_USD(Number):
    Number = float(Number)
    Number = "${0:,.2f}".format(Number)
    return Number