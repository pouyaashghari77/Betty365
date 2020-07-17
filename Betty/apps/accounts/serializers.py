from rest_framework import serializers

from Betty.apps.authentication.serializers import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'first_name', 'last_name', 'birth_date',
            'country', 'security_question', 'security_answer', 'balance'
        )
