from flask import Flask, render_template, request, redirect, url_for, session
from models.model import user_exists, create_user, login_user, prodetails, addprodetails, buyer_products, seller_products, add_to_cart

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/contact')
def contact():

	return "contact details"

@app.route('/login', methods =['POST','GET'])
def login():

	if request.method == 'POST':

		username = request.form['username']
		password = request.form['password']
		user = login_user(username)
		if user is None:
			return "user doesn't exist"

		if user['username'] == username and user['password'] == password:
			session['username'] = user['username']
			session['c_type'] = user['c_type']
			if session['c_type'] == 'seller':
				return render_template('addproduct.html')
			return redirect(url_for('home'))
		return redirect(url_for('home'))
	return redirect(url_for('home'))

@app.route('/signup', methods=['POST'])
def signup():
	if request.method == 'POST':
		user_info = {}
		user_info['username'] = request.form['username']
		user_info['email'] = request.form['email']
		user_info['password'] = request.form['password']
		rpassword = request.form['rpassword']
		user_info['c_type'] = request.form['c_type']

		if user_exists(user_info['username']) is False:
			if user_info['password'] == rpassword:
				if user_info['c_type'] == 'buyer':
					user_info['cart'] = []
				create_user(user_info)
				return redirect(url_for('home'))
			return "Passwords don't match"
		return 'User Exists'
	return(url_for('home'))

@app.route('/addproducts', methods=['POST'])
def add():
	if request.method == 'POST':
		prod_info = {}
		prod_info['productName'] = request.form['productName']
		prod_info['price'] = request.form['price']
		prod_info['description'] = request.form['description']
		prod_info['sellerName'] = session['username']
		
		
		if prodetails(prod_info['productName']) is True:
			return 'Product already added'
		else:
			addprodetails(prod_info)
			return redirect(url_for('products'))
		return(render_template('addproduct.html'))
		
	return(url_for('home'))	

@app.route('/products')
def products():
	if session['c_type'] == 'buyer':
		return render_template('products.html', products = buyer_products())
	return render_template('products.html', products = seller_products(session['username']))


@app.route('/cart',methods=['POST'])
def add_cart():
	product_id = request.form['id']
	add_to_cart(product_id,session['username'])
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('home'))
	
if __name__ == '__main__':

	app.run(debug=True) 