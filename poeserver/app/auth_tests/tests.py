# Testing DRF OAuth2.0 (https://github.com/RealmTeam/django-rest-framework-social-oauth2)

from oauth2_provider.models import get_application_model, AccessToken
from django.contrib.auth import get_user_model
from oauth2_provider.settings import oauth2_settings

Application = get_application_model()
UserModel = get_user_model()

from django.test import TestCase, Client

TEST_USER_PASSWORD = '123456'


class DRFSocialOAuthSetupTest(TestCase):

    def setUp(self):

        self.test_user = UserModel.objects.create_user("test_user", "test@user.com", TEST_USER_PASSWORD)

        self.application = Application(
            name="Test Application",
            redirect_uris="",
            user=self.test_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )
        self.application.save()
        
        # Every test needs a client.
        self.client = Client()

    def tearDown(self):
        self.application.delete()
        self.test_user.delete()

    def test_drf_social_oauth2_setup(self):
        '''Following testing steps found at https://github.com/RealmTeam/django-rest-framework-social-oauth2#testing-the-setup'''

        def retrieve_token(self):
            '''
            Retrieve an access token for a user       
            curl -X POST -d "client_id=<client_id>&client_secret=<client_secret>&grant_type=password&username=<user_name>&password=<password>" http://localhost:8000/auth/token
            '''
            return self.client.post(
                '/auth/token', 
                {
                    'client_id': self.application.client_id, 
                    'client_secret': self.application.client_secret, 
                    'grant_type': self.application.authorization_grant_type,
                    'username': self.application.user.username, 
                    'password': TEST_USER_PASSWORD
                }
            )

        def refresh_token(self, previous_refresh_token):
            '''
            Refresh an access token via its refresh token       
            curl -X POST -d "grant_type=refresh_token&client_id=<client_id>&client_secret=<client_secret>&refresh_token=<your_refresh_token>" http://localhost:8000/auth/token        
            '''
            return self.client.post(
                '/auth/token', 
                {
                    'grant_type': 'refresh_token',
                    'client_id': self.application.client_id, 
                    'client_secret': self.application.client_secret, 
                    'refresh_token': previous_refresh_token             # Use refresh token from previous test
                }
            )
        
        def revoke_single_token(self, access_token):
            '''
            Revoke a single access token       
            curl -X POST -d "client_id=<client_id>&client_secret=<client_secret>&token=<your_token>" http://localhost:8000/auth/revoke-token
            '''
            return self.client.post(
                '/auth/revoke-token', 
                {
                    'client_id': self.application.client_id,  
                    'client_secret': self.application.client_secret, 
                    'token': access_token                             
                }
            )
        
        def revoke_all_tokens(self, token):
            '''
            Revoke all tokens for a user       
            curl -H "Authorization: Bearer <token>" -X POST -d "client_id=<client_id>" http://localhost:8000/auth/invalidate-sessions
            '''
            return self.client.post(
                '/auth/invalidate-sessions', 
                {
                    'client_id': self.application.client_id  
                },
                HTTP_AUTHORIZATION=f'Bearer {token}'
            )


        # Retrieve token for user       
        response = retrieve_token(self)                                             ;print(f'Token retrieval returned: {response.json()=}')
        self.assertEqual(response.status_code, 200)                         
        self.assertIn('access_token', response.json())  
        # Refresh token  
        response = refresh_token(self, response.json()['refresh_token'])            ;print(f'Token refresh returned: {response.json()=}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())  

        # Revoke a single token  
        response = revoke_single_token(self, response.json()['access_token'])       ;print(f'Single token removal returned: {response.content=}')
        self.assertEqual(response.status_code, 204)
        tokens_list = AccessToken.objects.filter(user=self.application.user)        ;print(f'{tokens_list=}')
        self.assertQuerysetEqual(tokens_list, [])                                 # even though we only provided token0 to revoke_all_tokens, 

        # Revoke all tokens for the user (generate two tokens, use token0 to delete token0 and token1)
        token0 = retrieve_token(self).json()['access_token']
        token1 = retrieve_token(self).json()['access_token']
        response = revoke_all_tokens(self, token0)                                  ;print(f'Multiple token removal returned: {response.content=}')
        self.assertEqual(response.status_code, 204)
        tokens_list = AccessToken.objects.filter(user=self.application.user)        ;print(f'{tokens_list=}')
        self.assertQuerysetEqual(tokens_list, [])                                 # even though we only provided token0 to revoke_all_tokens, 
                   
                                                                                    # all tokens have been removed (token list should be empty)
class DRFSocialOAuthIntegrationTest(TestCase):

    def setUp(self):

        self.test_user = UserModel.objects.create_user("test_user", "test@user.com", TEST_USER_PASSWORD)

        self.application = Application(
            name="Test Application",
            redirect_uris="",
            user=self.test_user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,  # https://github.com/jazzband/django-oauth-toolkit/blob/master/oauth2_provider/models.py
        )
        self.application.save()
        
        # Every test needs a client.
        self.client = Client()

    def tearDown(self):
        self.application.delete()
        self.test_user.delete()
    
    def test_drf_social_oauth2_integration(self):
        '''Following testing steps found at curl -X POST -d "grant_type=convert_token&client_id=<django-oauth-generated-client_id>&client_secret=<django-oauth-generated-client_secret>&backend=google-oauth2&token=<google_token>" http://localhost:8000/auth/convert-token'''

        def convert_fb_token(self):
            '''
            Convert Facebook token to our access token       
            curl -X POST -d "grant_type=convert_token&client_id=<client_id>&client_secret=<client_secret>&backend=facebook&token=<facebook_token>" http://localhost:8000/auth/convert-token
            '''
            return self.client.post(
                '/auth/convert-token', 
                {
                    'grant_type': 'convert_token',
                    'client_id': self.application.client_id, 
                    'client_secret': self.application.client_secret, 
                    'backend': 'facebook', 
                    'token': 'EAAIzuLTlo04BAEgFOlm0QMpAEB2H0ZCrp9qqpXZBmHnug2CHeSoRcprCk8nyVoMmwr5hubZAPELPBA2W1ZBZB1vnZCLKZACFcZBswc4F8rBUaxzk08iutNGX2zZCOin7bee7u3qa0nNQbwnlSZCFZBhVq9LIrO6UuM7v4KlDZBIZCPCO08AZDZD'
                }
            )
        
        response = convert_fb_token(self)            ;print(f'Fb token conversion returned: {response.content=}')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json())  