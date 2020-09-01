#verify account and save
#https://www.youtube.com/watch?v=Y9EpPc19xjw

#https://www.youtube.com/watch?v=oZwyA9lUwRk

#refrence 
#https://stripe.com/docs/api/charges/create
#

from flask import Flask, render_template, url_for, request, abort
import stripe

app = Flask(__name__)
app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51HClRcBZLa0Pd5Bp86JY1VjCsuW19Z8q3UCC5UKxbZLOTZPPFdmVQohgBBfsqzI7uuPxnubjKpOaSo7NmyRvPW1l00RStYB5Me'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51HClRcBZLa0Pd5BpTtA5XAwS6tcVijvdOXSpwne3C2spqGhQDjCL12U8eh8VXnL2SRal2t7KBIEKmCc4wGop9LLZ00RQo7xHDA'

stripe.api_key = app.config['STRIPE_SECRET_KEY']

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')
	

@app.route('/charge',methods=['GET','POST'])
def charge():
	if request.method=='POST':
		# print('Data',request.form)
		# print("------------------")
		# print(request.form['stripeToken'])

		amount=int(request.form['amount'])

		customer=stripe.Customer.create(
			email=request.form['email'],
			name=request.form['Nickname'],
			source=request.form['stripeToken'],
		  description="Welcome in Cloutcube"
		)

		# `source` is obtained with Stripe.js; see https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token
		charge=stripe.Charge.create(
			customer=customer,
		  amount=amount*100,
		  currency="inr"
		  # source="tok_visa",
		  # description="Cloutcube subscrition"
		)

		print(charge)


		return render_template('thanks.html')

	return render_template('index.html')
	



if __name__ == '__main__':
	app.run(debug=True)



