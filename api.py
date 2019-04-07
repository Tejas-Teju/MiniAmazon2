from flask import Flask, render_template, request, redirect, url_for, session
from models.model import user_exists, create_user, login_user, prodetails, addprodetails, buyer_products, seller_products, add_to_cart, remove_from_cart, cart_info, find_products, clear_cart
from flask_mail import Mail, Message
import os


app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



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
					user_info['cart'] = {}
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
	return render_template('products.html',products = find_products(session))


@app.route('/addtocart',methods=['POST'])
def add_cart():
	product_id = str(request.form['id'])
	add_to_cart(product_id,session['username'])
	return redirect(url_for('products'))


@app.route('/removefromcart',methods=['POST'])
def remove_cart():
	product_id = str(request.form['id'])
	remove_from_cart(product_id,session['username'])
	return redirect(url_for('cart'))

@app.route('/cart')
def cart():

	temp= cart_info(session['username'])
	product_info = temp[0]
	quantity = temp[1]

	total = 0

	for prod,quant in zip(product_info,quantity):
		total += int(prod['price'])*quant
	session['total'] = total
	return render_template('cart.html',cart = zip(product_info,quantity), total_price = session['total'])	

@app.route("/order", methods=['POST'])
def index():
   msg = Message('Hello', sender = os.environ.get('MAIL_USERNAME'), recipients = ['tejas7464@gmail.com'])
   msg.body = f"Hello {session['username']}, \nYour order has been placed \nTotal cost = $ {session['total']}"
   mail.send(msg)
   clear_cart(session['username'])
   return "Your order has been placed...!! \n\n Please check your email"

@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('home'))
	
if __name__ == '__main__':

	app.run(debug=True) 