from pymongo import MongoClient

client = MongoClient()
db = client['DummyAmazon']

def user_exists(username):
	result = db['users'].find({'username':username})
	return result.count() > 0

def create_user(username):
	db['users'].insert_one(username)

def login_user(username):
	result = db['users'].find_one({'username':username})
	return result

def prodetails(productName):
	result = db['products'].find({'productName':productName})
	
	if result.count() > 0:
		return True
	return False

def addprodetails(prod_info):
	db['products'].insert_one(prod_info)


def buyer_products():
	cursor = db['products'].find({})
	return cursor

def seller_products(username):
	cursor = db['products'].find({'sellerName':username})
	return cursor

def add_to_cart(prod_id,username):
	db['users'].update({"username":username},{"$addToSet": {"cart": {"$each":[prod_id]}}})