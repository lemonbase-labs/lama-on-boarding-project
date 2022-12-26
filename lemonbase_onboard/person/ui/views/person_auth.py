from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated

from person.application.requests.person_register import PersonRegisterRequest
from person.application.requests.person_login import PersonLoginRequest
from person.application.services.person_auth import PersonAuthAppService


class PersonAuthViewSet(viewsets.ViewSet):
    def get_permissions(self):
        if self.action == "logout":
            return [IsAuthenticated()]
        else:
            return []

    @action(url_path="login", methods=["post"], detail=False)
    def login(self, request):
        person_login_request = PersonLoginRequest(**request.data)

        user = authenticate(
            request=request,
            username=person_login_request.username,
            password=person_login_request.password,
        )

        if not user:
            return Response(None, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)
        return Response(None, status=status.HTTP_202_ACCEPTED)

    @action(url_path="logout", methods=["post"], detail=False)
    def logout(self, request):
        logout(request)

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    @action(url_path="register", methods=["post"], detail=False)
    def register(self, request):
        person_register_request = PersonRegisterRequest(**request.data)
        person = PersonAuthAppService.register(person_register_request)

        return Response(person.dict(), status.HTTP_201_CREATED)
