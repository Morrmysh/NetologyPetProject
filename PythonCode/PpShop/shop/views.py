from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny


class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self, request):
        pass

    def post(self, request):
        pass