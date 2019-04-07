from pymongo import MongoClient
from bson.objectid import ObjectId

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
	result = db['users'].find_one({'username':username})

	if result['cart'].get(prod_id):
		db['users'].update({"username":username},{"$inc": {f"cart.{prod_id}":1}})
	else:
		db['users'].update({"username":username},{"$set": {f"cart.{prod_id}":1}})

def remove_from_cart(prod_id,username):
	result = db['users'].find_one({'username':username})

	if result['cart'].get(prod_id) <= 1:
		db['users'].update({"username":username},{"$unset": {f"cart.{prod_id}":1}})
	else:
		db['users'].update({"username":username},{"$inc": {f"cart.{prod_id}":-1}})

def find_products(session):

	if session['c_type'] == 'buyer':

		return db['products'].find({})
	return db['products'].find({'seller':session['username']})


def cart_info(username):

	query = {'username':username}
	result = db['users'].find_one(query)['cart'].keys()

	products = []
	quantity = []
	for product_id in result:
		products.append( db['products'].find_one({'_id':ObjectId(product_id)}))
		quantity.append(db['users'].find_one({'username':username})['cart'][product_id])
					
	return (products,quantity)


def clear_cart(username):

	db['users'].update({'username':username},{"$unset":{"cart":1}})
	db['users'].update({'username':username},{"$set":{"cart":{}}})