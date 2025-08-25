from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Make sure the user exists with this username (email)
        User = get_user_model()
        try:
            user = User.objects.get(username=attrs['username'])
            if user.email != attrs['username']:  # Extra check to ensure username matches email
                raise User.DoesNotExist
        except User.DoesNotExist:
            raise ValueError('No active account found with the given credentials')

        return super().validate(attrs)

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
