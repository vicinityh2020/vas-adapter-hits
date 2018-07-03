import requests
from requests.exceptions import ConnectionError as RConnectionError
from requests.status_codes import codes

from .models import User
from .serializers import UserSerializer


class NMClient:

    def __init__(self):

        self.__username = 'german@tiny-mesh.com'
        self.__password = 'jK>bg6uUTdiK2rLH}K>AGH:y7p'
        self.__agent_id = '29e5f4b6-fa4a-4c95-a9ae-52d49625dc8a'

        self.__auth_payload = {
            'username': self.__username,
            'password': self.__password,
        }

        self.__auth_headers = {
            'x-access-token': ''
        }

        self.__baseurl = 'https://vicinity.bavenir.eu:3000'

    def auth(self):
        try:
            res = User.objects.get(user_email=self.__username)
            self.__auth_headers['x-access-token'] = res.access_token
            return True
        except User.DoesNotExist:
            res = requests.post('{}/api/authenticate'.format(self.__baseurl), json=self.__auth_payload)

        if res.status_code == codes.ok:
            user_auth = res.json()['messages']

            user = {
                'user_email': self.__username,
                'company_id': user_auth['cid'],
                'user_id': user_auth['uid'],
                'access_token': user_auth['access-token']
            }

            serialized = UserSerializer(data=user)
            serialized.save()

            self.__auth_headers['x-access-token'] = user_auth['access-token']
            return True
        else:
            return False

    def get_agent_items_ids(self):

        try:
            res = requests.get('{base}/api/agents/{agid}/items'.format(base=self.__baseurl, agid=self.__agent_id),
                               headers=self.__auth_headers)
        except RConnectionError:
            print('error getting agent items')
            return None
        else:
            if res.status_code == codes.ok:
                return res.json()
            else:
                print('get agent items succeeded, but the response code is not a 200.')
                return None
