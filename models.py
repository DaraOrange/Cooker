class Order:
        def __init__(self, orderName, factTime):
                self.orderName = orderName
                self.factTime = factTime
        def __lt__(self, other):
                return self.factTime < other.factTime


