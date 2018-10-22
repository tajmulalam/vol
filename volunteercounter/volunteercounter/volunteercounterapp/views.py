from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from .utils import Utils
import json
from django.http import JsonResponse
from .models import User
from .models import QrScanData
from datetime import *
from django.http import HttpResponseRedirect
import time
from datetime import date
from django.core.mail import EmailMessage
import uuid
from django.core import serializers

def index(request):
    user = checkUserAliveInSession(request)
    if user is False:
        return render_to_response('login.html')
    else:
        return redirect('/qrresults/')


@csrf_exempt
def login(request):
    if request.method == 'GET':
        return render_to_response('login.html')
    elif request.method == 'POST':
        data = json.loads(request.body)
        print(data['username'])
        if data['username'] == 'admin' and data['password'] == 'abc@123':
            request.session['user'] = True
            # email = EmailMessage(validUser[1].username, 'test msg', to=[validUser[1].email])
            # email.send()
            return HttpResponse(json.dumps({"status": '200', "sessionID": True}),
                                content_type='application/json')
        else:
            return HttpResponse(json.dumps({"status": '500', "sessionID": False}),
                                content_type='application/json')

    else:
        return render_to_response('login.html')


def logout(request):
    try:
        del request.session['user']
    except:
        pass
    return redirect('/login/')


@csrf_exempt
def qrresults(request):
    user = checkUserAliveInSession(request)
    print(user)
    if user is False:
        return render_to_response('login.html')
    else:
        if request.method == 'GET':
            return render_to_response('qrresults.html', {'sessionID': user})
        elif request.method == 'POST':
            data = json.loads(request.body)
            print(data)
            result = validateFields(data)
            if result[1]:
                qrscanData = QrScanData.objects.all().filter(scannedAt__range=[data['frmDate'], data['toDate']])
                qs_json = json.dumps(list(qrscanData))
                return HttpResponse(json.dumps({"msg": result[0], "status": '200', "qrscanData":qs_json}),
                                    content_type='application/json')
            else:
                return HttpResponse(json.dumps({"msg": result[0], "status": '500', "qrscanData": None}),
                                    content_type='application/json')
        else:
            return render_to_response('login.html')


# api

@csrf_exempt
def sendscanData(request):
    TOKEN = "QRDATA"
    if request.method == 'GET':
        return HttpResponse(json.dumps({"status": "404", "msg": "Access denied"}), content_type='application/json')
    elif request.method == 'POST':
        headerToken = request.META.get('HTTP_TOKEN')
        if headerToken.lower() == TOKEN.lower():
            data = json.loads(request.body)
            print(data)
            obj = QrScanData.objects.create(qrCode=data['qrCode'], user_id=data['user_id'])
            status = obj.id
            if status != 0:
                return HttpResponse(json.dumps({"status": "200", "msg": "Scan Successfull"}),
                                    content_type='application/json')
            else:
                return HttpResponse(json.dumps({"status": "500", "msg": "Scan Failed"}),
                                    content_type='application/json')
        else:
            return HttpResponse(json.dumps({"status": "404", "msg": "Access denied"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({"status": "404", "msg": "Access denied"}), content_type='application/json')


@csrf_exempt
def register(request):
    TOKEN = "REGISTER"
    if request.method == 'POST':
        # print (request.body)
        utils = Utils()
        headerToken = request.META.get('HTTP_TOKEN')
        print(headerToken)
        if headerToken.lower() == TOKEN.lower():
            # str(request.body, encoding='utf-8')
            data = json.loads(request.body)
            print(data)
            verificationCode = getRendomVerificationCode(6)
            obj = User(fullName=data['fullName'], password=data['password'], email=data['email'],
                       verificationCode=verificationCode)
            obj.save()
            if obj.id > 0:
                email = EmailMessage("Verification needed for your Volunteer Counter account",
                                     'User bellow verification code to verified your account. Verification Code is: ' + verificationCode,
                                     to=[data['email']])
                email.send()
                return HttpResponse(json.dumps({"status": "200", "msg": "Register Successfull"}),
                                    content_type='application/json')
            else:
                return HttpResponse(json.dumps({"status": "500", "msg": "Register Failed"}),
                                    content_type='application/json')
        else:
            return HttpResponse(json.dumps({"status": "404", "msg": "Access denied"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({"status": "404", "msg": "Access denied"}), content_type='application/json')


@csrf_exempt
def verifyUser(request):
    TOKEN = "VERIFYUSER"
    if request.method == 'POST':
        # print (request.body)
        utils = Utils()
        headerToken = request.META.get('HTTP_TOKEN')
        print(headerToken)
        if headerToken.lower() == TOKEN.lower():
            # str(request.body, encoding='utf-8')
            data = json.loads(request.body)
            print(data)
            user = User.objects.get(verificationCode=data['verificationCode'])
            print(user)
            user.isVerified = True
            user.save()
            if user.isVerified:
                return HttpResponse(json.dumps({"status": "200", "msg": "Verification Successfull"}),
                                    content_type='application/json')
            else:
                return HttpResponse(json.dumps({"status": "500", "msg": "Verification Failed"}),
                                    content_type='application/json')
        else:
            return HttpResponse(json.dumps({"status": "404", "msg": "Access denied"}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({"status": "404", "msg": "Access denied"}), content_type='application/json')


@csrf_exempt
def signin(request):
    TOKEN = "LOGIN"
    if request.method == 'POST':
        # print (request.body)
        utils = Utils()
        headerToken = request.META.get('HTTP_TOKEN')
        print(headerToken)
        if headerToken.lower() == TOKEN.lower():
            # str(request.body, encoding='utf-8')
            data = json.loads(request.body)
            print(data)
            resultJson = utils.checkCredentials(data['email'], data['password'])
            print(resultJson)  # management exempt implement
            if resultJson[0] == '200':
                return HttpResponse(
                    json.dumps({"status": resultJson[0], "msg": "valid user", "user_id": resultJson[1].id}),
                    content_type='application/json')  # found valid user
            elif resultJson[0] == '300':
                return HttpResponse(
                    json.dumps({"status": resultJson[0], "msg": "Account verification needed", "user_id": -1}),
                    content_type='application/json')  # verification needed
            else:
                return HttpResponse(json.dumps({"status": "500", "msg": "Access Denied", "customer_id": -1}),
                                    content_type='application/json')  # Token error found
        else:
            return HttpResponse(json.dumps({"status": "500", "msg": "Access Denied", "customer_id": -1}),
                                content_type='application/json')  # Token error found
    else:
        pass


""""This is the common method for checking user session"""


def checkUserAliveInSession(request):
    if request.session.has_key('user'):
        userID = False
        userID = request.session['user']
        return userID
    else:
        return False


def validateFields(data):
    errorMsg = ""
    result = []
    isFrmDateOK = False
    isToDateOK = False

    if isBlank(data['frmDate']):
        isFrmDateOK = False
        errorMsg += "From date is required" + "</br>"
    else:
        isFrmDateOK = True
        if isBlank(data['toDate']):
            isToDateOK = False
            errorMsg += "To date is required" + "</br>"
        else:
            frmDate = convertToDate(data['frmDate'])
            toDate = convertToDate(data['toDate'])
            print(frmDate)
            print(toDate)
            if frmDate <= toDate:
                isToDateOK = True
            else:
                errorMsg += "From date must be greater or less then to date." + "</br>"
                isToDateOK = False
    # time.sleep(5)
    if isFrmDateOK and isToDateOK:
        result.append("Validation Ok")
        result.append(True)
        return result
    else:
        result.append(errorMsg)
        result.append(False)
        print(errorMsg)
        return result


def isBlank(myString):
    return not (myString and myString.strip())


def convertToDate(s):
    return datetime.strptime(s, '%Y-%m-%d')


def getRendomVerificationCode(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())  # Convert UUID format to a Python string.
    random = random.upper()  # Make all characters uppercase.
    random = random.replace("-", "")  # Remove the UUID '-'.
    return random[0:string_length]  # Return the random string.
