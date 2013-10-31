"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django_peach.client import PeachClient, PeachResponse
import random
import uuid
from django.template.loader import render_to_string

from django.conf import settings


"""
todo: refactory: 

    common steps: 
    1. _make_debit(amount) #returns response_json
    2. _get_common_context(response_json) # returns context with transactionid and uniqueid
"""


class PeachIntegrationTest(TestCase):
    
    def setUp(self):

        config = settings.PEACH_CONFIG
        # header requirements
        

        self.config = config
        self.url = "https://test.ctpe.net/payment/ctpe"

    def test_pay(self):

        config = self.config
        url = self.url

        peach = PeachClient(url, config)
        context = self._get_payment_context()
        response = peach.call("debit", context)

        response_json = PeachResponse.as_json(response.content)

        self.assertEqual("ACK", response_json.get("processing").get("Result", False) )


    def test_partial_capture(self):

        config = self.config
        url = self.url

        hold_amount = 50
        take_amount = 40

        ## Make a payment:
        peach = PeachClient(url, config)
        context = self._get_payment_context(hold_amount)
        context["paytype"] = "PA";
        response = peach.debit(context)

        response_json = PeachResponse.as_json(response.content)

        transactionid = response_json.get("identification").get("TransactionID")
        uniqueid = response_json.get("identification").get("UniqueID")


        ## Capture it:
        context = {}
        context["uniqueid"] = uniqueid
        context["transactionid"] = transactionid
        context["amount"] = "{0}.00" .format(take_amount) # todo: do the amounts properly
        context["currency"] = "ZAR";

        peach = PeachClient(self.url, self.config)
        response = peach.capture(context)

        response_json = PeachResponse.as_json(response.content)

        self.assertEqual("ACK", response_json.get("processing").get("Result", False) )

    def test_refund_capture(self):

        config = self.config
        url = self.url

        hold_amount = 50
        
        ## Make a payment:
        peach = PeachClient(url, config)
        context = self._get_payment_context(hold_amount)
        context["paytype"] = "DB";
        response = peach.call("debit", context)

        response_json = PeachResponse.as_json(response.content)

        transactionid = response_json.get("identification").get("TransactionID")
        uniqueid = response_json.get("identification").get("UniqueID")


        ## Refund it:
        context = {}
        context["uniqueid"] = uniqueid
        context["transactionid"] = transactionid
        context["amount"] = "{0}.00" .format(hold_amount) # todo: do the amounts properly
        context["currency"] = "ZAR";

        peach = PeachClient(self.url, self.config)
        response = peach.refund(context)

        response_json = PeachResponse.as_json(response.content)

        self.assertEqual("ACK", response_json.get("processing").get("Result", False) )

    def test_reversal(self):

        config = self.config
        url = self.url

        hold_amount = 50
        
        ## Make a payment:
        peach = PeachClient(url, config)
        context = self._get_payment_context(hold_amount)
        context["paytype"] = "DB";
        response = peach.call("debit", context)

        response_json = PeachResponse.as_json(response.content)

        transactionid = response_json.get("identification").get("TransactionID")
        uniqueid = response_json.get("identification").get("UniqueID")


        ## Refund it:
        context = {}
        context["uniqueid"] = uniqueid
        context["transactionid"] = transactionid
        
        peach = PeachClient(self.url, self.config)
        response = peach.reversal(context)

        response_json = PeachResponse.as_json(response.content)

        self.assertEqual("ACK", response_json.get("processing").get("Result", False) )


    def test_parse_response(self):


        response_templates = [
            "peach/tests/capture_fail.xml",
            "peach/tests/debit_success.xml",
            "peach/tests/capture_success.xml",
            "peach/tests/invalid_request.xml",
        ]



        for template_path in response_templates:
            xml_string = render_to_string(template_path, {})

            print xml_string
            print "------"

            json = PeachResponse.as_json(xml_string)
            print json
            print "------"

    def _get_payment_context(self, amount=False):

        random_number = random.choice(range(0,100))
        if not amount: 
            amount = random_number


        context = {}
        context['holder'] = 'Christo {0}' . format (random_number)
        context['number'] = '4111111111111111'
        context['verification'] = '123'
        context['brand'] = 'VISA'
        context['month'] = '10'
        context['year'] = '2014'

        context["transactionid"] = str(uuid.uuid4())
        context["paymethod"] = "CC";
        context["paytype"] = "DB";
        context["amount"] = "{0}.00" . format(amount);
        #context["usage"] = "great-goods#1234";
        context["currency"] = "ZAR";
        context["email"] = "info@38.co.za";
        context["city"] = "Johannesburg";
        context["street"] = "64 2nd ave, Parkhurst";
        context["country"] = "ZA";
        context["salutation"] = "MR";
        context["family"] = "Soap{0}" . format(random_number);
        context["given"] = "Joe{0}" . format(random_number);

        return context






        
