from __future__ import division
from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
import json
from reportlab.pdfgen import canvas
import urllib2
# Create your views here.

def index(request):
    args = {}
    args.update(csrf(request))
    return render(request, 'index.html')


def predict(request):
    if request.method == "POST":

        data =  {

                "Inputs": {

                        "input1":
                        {
                            "ColumnNames": ["sms_label", "sms_body"],
                            "Values": [ [ "", request.POST.get('sms_body') ], ]
                        },        },
                    "GlobalParameters": {
        }
            }

        body = str.encode(json.dumps(data))

        url = 'https://ussouthcentral.services.azureml.net/workspaces/8a7dce9ff8034885abaec4501f06f5db/services/32a748a0efc64da4954f2d19296d2dbf/execute?api-version=2.0&details=true'
        api_key = 'd6da26KgU5ytaNmbdyozhdLGmDqS97GbVTPTkUdaP5Zh41tBva9iT+LKLgWXpC/K0LBaErbLTH7fbAXZky0M7Q=='
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

        req = urllib2.Request(url, body, headers)

        try:
            response = urllib2.urlopen(req)

            # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
            # req = urllib.request.Request(url, body, headers) 
            # response = urllib.request.urlopen(req)

            result = response.read()
            print(result) 
        except urllib2.HTTPError, error:
            print("The request failed with status code: " + str(error.code))

            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())

            print(json.loads(error.read()))

    return HttpResponse(result)
