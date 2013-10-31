import requests
from django.template.loader import render_to_string
import xml.etree.ElementTree as ET
import new

class PeachClient:

    def __init__(self, url, config):
        self.url = url
        self.config = config

        
    """
    I'm sure I can do this cleverly with just a dict to 
    dynamically set up the methods .. but for now I'm stumped want to do:
    PeachClient.method(context) => PeachClient.call(method, context)
    """
    def debit(self,context):
        return self.call("debit", context)

    def capture(self,context):
        return self.call("capture", context)

    def refund(self,context):
        return self.call("refund", context)

    def reversal(self,context):
        return self.call("reversal", context)
        
    def call(self, action, context):
        
        context.update(self.config) # maybe the other way round?

        template_path = 'peach/requests/{0}_template.xml' . format (action.lower(), context)
        request_body = render_to_string(template_path, context)

        self.debug_request(self.url, request_body)
        
        response = requests.post(self.url, {"load":request_body})

        self.debug_response(response)
        return response

    def debug_request(self, url, request_body):
        print "----- request"
        print "POST {0}" . format(url)
        print request_body

    def debug_response(self, response):

        print "----- response"
        print response.content
        
class PeachResponse: # rename to PeachResponseHelper ?

    @staticmethod
    def is_ok(json_response_string):
        return json_response_string.get("processing",{}).get("Result", False) == "ACK"

    @staticmethod
    def as_json(response_string):
        
        fields = {
            "identification" : {
                "path" : "Transaction/Identification",
                "fields" : ["ShortId", "UniqueID", "TransactionID", "ReferenceID"],                
                "attrs" : ["code"],
            },
            "payment" : {
                "path" : "Transaction/Payment",
                "fields" :[],
                "attrs" : ["code"],
            },
            "payment_clearing" : {
                "path" : "Transaction/Payment/Clearing",
                "fields" :["Amount", "Currency", "Descriptor", "FxRate", "FxSource", "FxDate"],

            },
            "processing" : {
                "path" : "Transaction/Processing",
                "fields": ["Timestamp", "Result", "Status", "Reason", "Return", "SecurityHash"],
                "attrs" : ["code"],
            }
        }

        root = ET.fromstring(response_string)
        response = {}
        
        for root_string, data in fields.items(): 
            path = data.get("path")
            fields = data.get("fields",[])       
            attrs = data.get("attrs",[])   

            if not response.get(root_string,False):
                response.update({root_string : {} })  

            try:
                element = root.find(path)
                if element:
                    for attr  in attrs:
                        field_attr = element.attrib.get(attr,False)
                        if field_attr:                            
                            response.get(root_string).update({ attr : field_attr })

                    for field in fields:     
                        try:                                        
                            try:
                                
                                field_element = element.findall(field)[0]
                                
                                response.get(root_string).update({
                                    field : field_element.text
                                })
                            
                            except TypeError:
                                print "field not found: {0}" . format(field)
                        except IndexError:
                            response[root_string][field] = False
            except IndexError:
                response[root_string] = False

        return response