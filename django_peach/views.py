from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string
from django.shortcuts import render
import requests
import uuid

"""
SENDER: ff8080813dab64c0013dcaf6c4ef0de6
USER LOGIN: ff8080813dab64c0013dcaf6c4f00dea
USER PWD: jYBdGJ8a
SECRET: eBnQ9rZSAWSENyHP


Channel: ff8080813dab64c0013dcaf73fce0ded


token: 952325C49FCB1FABBC3370F175F7DCD9.sbg-vm-fe02
"""

"""
data = {
    'IDENTIFICATION.TRANSACTIONID' : ''
    'IDENTIFICATION.REFERENCEID' : "ff80808141e49f560141e5d6e89b4242",
    'PAYMENT.CODE' :"CC.CP",
    'PRESENTATION.AMOUNT':'40.00',
    'PRESENTATION.CURRENCY':'ZAR',
    'SECURITY.SENDER': 'ff8080813dab64c0013dcaf6c4ef0de6',
    'TRANSACTION.CHANNEL': 'ff8080813dab64c0013dcaf73fce0ded',
    'TRANSACTION.MODE': 'INTEGRATOR_TEST',
    'USER.LOGIN': 'ff8080813dab64c0013dcaf6c4f00dea',
    'USER.PWD': 'jYBdGJ8a'
}
"""

def get_token(request):
    data = {
        'IDENTIFICATION.TRANSACTIONID' : str(uuid.uuid4()),
        'NAME.GIVEN' : 'Joe',
        'NAME.FAMILY' : 'Soap', 
        'ADDRESS.STREET' : '38 New Street',
        'ADDRESS.ZIP': '6140',
        'ADDRESS.CITY' : 'Grahamstown',
        'ADDRESS.COUNTRY': 'South Africa',
        'CONTACT.EMAIL' : 'info@38.co.za',
        'PAYMENT.TYPE': 'PA',
        'PRESENTATION.AMOUNT': '50.99',
        'PRESENTATION.CURRENCY': 'ZAR',
        'SECURITY.SENDER': 'ff8080813dab64c0013dcaf6c4ef0de6',
        'TRANSACTION.CHANNEL': 'ff8080813dab64c0013dcaf73fce0ded',
        'TRANSACTION.MODE': 'INTEGRATOR_TEST',
        'USER.LOGIN': 'ff8080813dab64c0013dcaf6c4f00dea',
        'USER.PWD': 'jYBdGJ8a'
    }
    url = "https://test.ctpe.net/frontend/GenerateToken"

    response = requests.post(url, data)

    token = response.json().get("transaction").get("token")
    return render(request, "peach/cc_form.html", {"token":token})

def payment_result(request):
    
    token = request.GET.get("token")
    url = "https://test.ctpe.net/frontend/GetStatus;jsessionid={0}" .format( token )
    response = requests.post(url)

    return HttpResponse(response.content)

def payment_test(request):

    url = "https://test.ctpe.net/payment/ctpe"

    values = {}

    # header requirements
    values["sender"] = "ff8080813dab64c0013dcaf6c4ef0de6"
    values["token"] = "ff8080813dab64c0013dcaf6c4ef0de6"
    values["channel"] = "ff8080813dab64c0013dcaf73fce0ded"
    values["userpwd"] = "jYBdGJ8a"
    values["userid"] = "ff8080813dab64c0013dcaf6c4f00dea"
    values["mode"] = "INTEGRATOR_TEST";


    values["uniqueid"] = "ff80808141e49f560141e9c6d6072687"
    values["transactionid"] = "8bcd9387-9315-4b10-b281-a5a3d9935191"
    values["amount"] = "40.00";
    values["currency"] = "ZAR";


    """
    values["txid"] = "4711";
    values["refid"] = "";

    values["number"] = "4200000000000000";
    values["holder"] = "Mark Cowerer";


    values["brand"] = "VISA";
    values["verification"] = "131";
    values["year"] = "2007";
    values["month"] = "11";

    values["paymethod"] = "CC";
    values["paytype"] = "DB";
    values["amount"] = "50.00";
    values["usage"] = "great-goods#1234";
    values["currency"] = "EUR";
    values["email"] = "mark.cowerer@yahoo.com";
    values["ip"] = "101.102.211.192";
    values["state"] = "DE1";
    values["zip"] = "81371";
    values["city"] = "Munich";
    values["street"] = "Homestreet 17";
    values["country"] = "DE";
    values["salutation"] = "MR";
    values["family"] = "Cowerer";
    values["given"] = "Mark";
    """

    request_body = render_to_string('peach/requests/capture_template.xml', values)

    print "----- request"
    print "POST {0}" . format(url)
    print request_body

    response = requests.post(url, {"load":values})

    print "----- response"
    print response.content

    return HttpResponse(response)


payment_types = [
    ('PA', 'Preauthorisation'),
    ('DB', 'Debit'),
    ('CP', 'Capture'),
    ('CD', 'Credit'),
    ('RV', 'Reversal'),
]

