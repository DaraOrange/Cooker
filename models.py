class Order:
	def __init__(self, orderName, factTime):
        self.orderName = orderName
        self.factTime = factTime
    def __lt__(self, other):
        return self.factTime < other.factTime

class Employee:
	def __init__(self, empId, userId, name) :
		self.empId = empId
		self.userId = userId
		self.name = name

class User:
	def __init__(self, userId, role, status) :
		self.userId = userId
		self.role = role
		self.status = status

class Meal:
	def __init__(self, mealId, planLeadTime, receipt, ingredients) :
		self.mealId = mealId
		self.planLeadTime = planLeadTime
		self.receipt = receipt
		self.ingredients = ingredients