from rest_framework import generics
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate

from .handler import token_expire_handler, expires_in
# from .serializers import UserSigninSerializer


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def ObtainToken(request):
    username = request.data.get('username')
    password = request.data.get('password')
    print("{} and {}".format(username, password))
    if username is None or password is None:
        return Response(
            {
                'error': 'Provide both username or password'
            },
            status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if not user:
        return Response(
            {
                'error': 'Invalid Credentials'
            },
            status=status.HTTP_400_BAD_REQUEST)
    token, _ = Token.objects.get_or_create(user=user)

    # token_expire_handler will check, if the token is expired it will generate new one
    # is_expired, token = token_expire_handler(token)
    # user_serialized = UserSigninSerializer(user)
    # if is_expired:
    #     return Response(
    #         {
    #             'error': 'Token has expired'
    #         },
    #         status=status.HTTP_400_BAD_REQUEST)
    return Response(
        {
            'user': username,
            'token': token.key,
            'expires_in': expires_in(token),
            'time expired': 'in-minutes',
        },
        status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def CheckTokenExpired(request):
    username = request.data.get('username')
    password = request.data.get('password')
    print("{} and {}".format(username, password))
    if username is None or password is None:
        return Response(
            {
                'error': 'Provide both username or password'
            },
            status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if not user:
        return Response(
            {
                'error': 'Invalid Credentials'
            },
            status=status.HTTP_400_BAD_REQUEST)
    token = Token.objects.filter(user=user)
    if token.count() >= 1:
        token = token[0]
    else:
        return Response(
            {
                'error': 'Token not exists!'
            },
            status=status.HTTP_400_BAD_REQUEST)
    return Response(
        {
            'user': username,
            'token': token.key,
            'expires_in': expires_in(token),
            'time expired': 'in-minutes',
        },
        status=status.HTTP_200_OK)
