from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer, UserRegistrationSerializer

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exeption=True)
        user = serializer.save()
        return Response(
            {
                "message": "пользователь успешкно зарегистрирован",
                "user": UserSerializer(user).data
            },
            status=status.HTTP_201_CREATED
        )

