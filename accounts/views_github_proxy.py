import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decouple import config
import json

CLIENT_ID = config('github_client_id')
CLIENT_SECRET = config('github_client_secret')

def get_access_token(request):
    if request.method == 'GET':
        try:
            code = request.GET.get('code')
            if code:
                if(len(code)!=20):
                    return JsonResponse(data={'message':'enter valid code'},status=400)

                params = {
                    'client_id': CLIENT_ID,
                    'client_secret': CLIENT_SECRET,
                    'code': code,
                }
                response = requests.post("https://github.com/login/oauth/access_token", data=params)
                response_content = response.content
                if 'error' in str(response_content):
                    return JsonResponse(data={'message':response_content},status=400)
                else:
                    response_text = response_content.decode('utf-8')
                    parameters = response_text.split('&')
                    parameter_dict = {}
                    for param in parameters:
                        key, value = param.split('=')
                        parameter_dict[key] = value
                    return JsonResponse(data={'access_token':str(parameter_dict['access_token'])})
            else:
                return JsonResponse(data={'message':'code is not provided'},status=400)
        except Exception as e:
            return JsonResponse(data={'message':f'something went wrong ( {e} )'},status=400)
    else:
        return {'status':405}



@csrf_exempt
def get_user_data(request):
    if request.method == 'GET':
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        headers = {
            'Authorization': authorization_header,
        }
        response = requests.get('https://api.github.com/user', headers=headers)
        data = response.json()
        return JsonResponse(data)
    else:
        return {'status':405,'message':f'{request.method} is not allowed'}