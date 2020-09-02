# Flask-Stripe-Tutorial
This tutorial shows how to add Stripe to a Flask application for accepting one-time payments.

```
try:
  # Use Stripe's library to make requests...
  pass
except stripe.error.CardError as e:
  # Since it's a decline, stripe.error.CardError will be caught

  print('Status is: %s' % e.http_status)
  print('Type is: %s' % e.error.type)
  print('Code is: %s' % e.error.code)
  # param is '' in this case
  print('Param is: %s' % e.error.param)
  print('Message is: %s' % e.error.message)
except stripe.error.RateLimitError as e:
  # Too many requests made to the API too quickly
  pass
except stripe.error.InvalidRequestError as e:
  # Invalid parameters were supplied to Stripe's API
  pass
except stripe.error.AuthenticationError as e:
  # Authentication with Stripe's API failed
  # (maybe you changed API keys recently)
  pass
except stripe.error.APIConnectionError as e:
  # Network communication with Stripe failed
  pass
except stripe.error.StripeError as e:
  # Display a very generic error to the user, and maybe send
  # yourself an email
  pass
except Exception as e:
  # Something else happened, completely unrelated to Stripe
  pass
  

```
<h1>use stripe default number</h1>
https://stripe.com/docs/testing`
