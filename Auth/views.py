from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


# Login
class SignIn(APIView):
    """

    This api accepts username, password as parameters and will return auth token.
    
    authenticate() function return user object with respect given username password else None.

    For invalid credentials it will return 404 

    """

    def post(self, request, format=None):
        try:
            username = request.data['username']
            password = request.data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                try:
                    token = Token.objects.get(user=user)
                except Exception as ex:
                    print(ex)
                    token = None

                if token is None:
                    token = Token.objects.create(user=user)

                # login(request, user)

                res = {
                    "token": str(token),
                    "login": True,
                    "msg": "Login Successful"
                }

                return Response(res, status=status.HTTP_200_OK)

            res = {"token": '', "login": False, "msg": "Login Unsuccessful"}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response(
                {
                    "token": '',
                    "login": False,
                    "msg": type(ex).__name__
                },
                status=status.HTTP_404_NOT_FOUND)


# Logout
class SignOut(APIView):
    """

    This api accepts auth token.

    If token is not valid this will return 404 or invalid token
    
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        try:
            token = Token.objects.get(user_id=request.user)
            if token is not None:
                # logout(request)
                token.delete()
                res = {"login": False, "msg": "Logout Successful"}
                return Response(res, status=status.HTTP_200_OK)
        except Exception as ex:
            res = {"login": False, "msg": type(ex).__name__}
            return Response(res, status=status.HTTP_404_NOT_FOUND)
