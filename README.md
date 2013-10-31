Django-Peach
============

Django wrapper to the [Peach Payment Gateway](http://peachpayments.com/). 

**Disclaimer:** This is still a work in progress. Currently supports: 

* debit
* capture
* refund
* reversal

**note:** even though we support the debit method, we would advise you consider using copy and pay for taking payments do you don't have to worry about PCI compliance. (we just needed `debit()` for the tests)

###Todo: 

* Implement entire XML API 
* Views for rendering the _copy and pay_ form

Developed by the chaps at [Tangent Solutions](http://www.tangentsolutions.co.za)

---

It let's you do things like: 

	from django_peach.client import PeachClient, PeachResponse
	peach = PeachClient(settings.PEACH_API_URL, settings.PEACH_CONFIG)
	data = {
		"holder" : "Joe Soap",
		"number" : "4111111111111111",
		"cvv"    : "123",
		...
	}

	peach_response = peach.debit(data)
	peach_response_as_json = PeachResponse.as_json(peach_response.content)
	


## Getting Started.

### Dependencies:

* requests
* lxml

(use pip install)


Download the code and put it in your project. (I'll get round to packaging this later!)

**Add to `INSTALLED_APPS`**

	INSTALLED_APPS = (
		...
		'django_peach',
		...
	)

**Example usage:**

	config = {}
	config["sender"] = "..."
	config["token"] = "..."
	config["channel"] = "..."
	config["userpwd"] = "..."
	config["userid"] = "..."
	config["mode"] = "INTEGRATOR_TEST"

	url = "https://test.ctpe.net/payment/ctpe"

	## Make a refund:
	context = {}
	context["uniqueid"] = uniqueid
	context["transactionid"] = transactionid
	context["amount"] = "50.00" 
	context["currency"] = "ZAR"

	peach = PeachClient(url, config)
	response = peach.refund(context)


This will return the xml response from Peach as a string. You can use `PeachResponse` to transform this into something more useful (like `json`):

	response_json = PeachResponse.as_json(response.content)


##Note: 

We would advise that you place your config into `settings.py`. e.g.:

	PEACH_API_URL = "https://test.ctpe.net/payment/ctpe"
	PEACH_CONFIG = {
		"sender" : "..",
		"token" : "..",
		"channel" : "..",
		"userpwd" : "..",
		"mode" : "..",
	}

Then you can just do: 

	from django_peach.client import PeachClient
	from django.conf import settings

	peach = PeachClient(settings.PEACH_API_URL, settings.PEACH_CONFIG)
	response = peach.refund(context)



	