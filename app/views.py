"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.http import HttpResponse
from django.template import RequestContext
from datetime import datetime
from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.template.context_processors import csrf
import json
import urllib2

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'SMS Spam Detection',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'SMS Spam Detection | Contact',
            'message':'Gohar Irfan Chaudhry.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'SMS Spam Detection | About',
            'message':'Application description.',
            'year':datetime.now().year,
        }
    )

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

        url = 'https://ussouthcentral.services.azureml.net/workspaces/1e62dc94e2034300bacd736d2384f0c7/services/4863f181cbf94854b43a07b98709ad19/execute?api-version=2.0&details=true'
        api_key = 'd6da26KgU5ytaNmbdyozhdLGmDqS97GbVTPTkUdaP5Zh41tBva9iT+LKLgWXpC/K0LBaErbLTH7fbAXZky0M7Q=='
        headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

        req = urllib2.Request(url, body, headers)

        try:
            response = urllib2.urlopen(req)

            # If you are using Python 3+, replace urllib2 with urllib.request in the above code:
            # req = urllib.request.Request(url, body, headers) 
            # response = urllib.request.urlopen(req)

            ans = json.loads(response.read())
            print(ans)
            for i in ans['Results']:
                for j in ans['Results'][i]:
                    for k in ans['Results'][i][j]:
                        if k == "Values":
                            res = ans['Results'][i][j][k][0]
                            res.append(request.POST.get('sms_body'))
                            return result(request, res)
        except urllib2.HTTPError, error:
            print("The request failed with status code: " + str(error.code))
            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
            print(json.loads(error.read()))
            ans = error.info()
        # return HttpResponse(ans)
        return error(request, ans)

def result(request, extraData=None):
    """Renders the result page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/result.html',
        {
            'title':'SMS Spam Detection | Result',
            'year':datetime.now().year,
            'label':extraData[0],
            'score':extraData[1],
            'sms_body':extraData[2],
        }
    )

def error(request, extraData=None):
    """Renders the error page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/result.html',
        {
            'title':'SMS Spam Detection | Error',
            'year':datetime.now().year,
            'message':extraData,
        }
    )