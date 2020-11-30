from djoser.serializers import UserCreateSerializer

class UserRegistrationSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ('id', 'username', 'first_name', 'patronymic', 'last_name', 'email', 'password')