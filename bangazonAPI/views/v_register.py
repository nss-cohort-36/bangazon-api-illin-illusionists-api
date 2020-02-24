import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from bangazonAPI.models import Customer

@csrf_exempt
def login_user(request):
    ''' Handles user authentication

    Method arguments:
        request -- full HTTP request object
    '''
    # load JSON string of request body into a dict
    req_body = json.loads(request.body.decode())

    if request.method == 'POST':

        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is not None:
            # authentication was successful, respond with their token
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({'valid': True, 'token': token.key})
            return HttpResponse(data, content_type='application/json')

        else:
            # Invalid login details provided
            data = json.dumps({'valid': False})
            return HttpResponse(data, content_type='application/json')


@csrf_exempt
def register_user(request):
    '''Handles creation of new user for authentication

    Method arguments:
        request -- The full HTTP request object
    '''

    # load JSON string of request body into a dict
    req_body = json.loads(request.body.decode())

    # create new user using django's `create_user` builtin method
    new_user = User.objects.create_user(
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        first_name=req_body['first_name'],
        last_name=req_body['last_name']
    )

    # also create a customer after the django user is created
    customer = Customer.objects.create(
        user=new_user
    )

    # REST framework's token generator for new user acct
    token = Token.objects.create(user=new_user)

    # return token to client
    data = json.dumps({'token': token.key})
    return HttpResponse(data, content_type='application/json')