from datetime import time
import datetime


def diff_in_time(time1, time2):
        minutes = time2.minute-time1.minute
        seconds = time2.second-time1.second
        if seconds < 0:
                seconds += 60
                minutes -= 1
        return time(0, minutes, seconds)

class Order:
        def __init__(self, orderId, orderName, factTime, addTime, status):
                self.orderId = orderId
                self.orderName = orderName
                self.factTime = factTime
                self.addTime = addTime
                self.status = status
                
        def __lt__(self, other):
                timestamp = datetime.datetime.now().time()
                time_left1 = diff_in_time(diff_in_time(self.addTime, timestamp), self.factTime)
                time_left2 = diff_in_time(diff_in_time(other.addTime, timestamp), other.factTime)
                return time_left1 < time_left2

# class OrderNew: 
# 	def __init__(self,orderId, planLeadTime, factLeadTime, factTime):
# 		self.orderId = orderId
# 		self.planLeadTime = planLeadTime
# 		self.factTime = factTime 
# 		self.factTime = factTime
# 		self.factLeadTime = factLeadTime
# 	def __lt__(self, other):
# 		return order.get_diff() < other.get_diff()
	# def get_diff(self)
	# 	return self.PlanLeadTime - (self.StartTime + food.PlanLeadTime)



# class FullOrder:
# 	def __init__ (self, orderId, cookerId, status, startTime, planLeadTime, extraTime):
# 		self.orderId = orderId
# 		self.cookerId = cookerId
# 		self.status = status
# 		self.startTime = startTime
# 		self.planLeadTime = planLeadTime
# 		self.extraTime = extraTime
