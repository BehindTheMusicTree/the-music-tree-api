#!/usr/bin/env python

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status


REFRESH_TOKEN_FIELD = "refresh_token"


class LogoutView(APIView):


    def post(self, request):
        try:
            refresh_token = request.data[REFRESH_TOKEN_FIELD]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)