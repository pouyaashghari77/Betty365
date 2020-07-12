from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    birth_date = serializers.DateField(required=False)
    country = serializers.CharField()
    confirm_password = serializers.CharField(write_only=True)
    # security_question = serializers.CharField(required=False)
    # security_answer = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'confirm_password',
                  'first_name', 'last_name', 'country',
                  'birth_date',  # 'security_question', 'security_answer'
                  )
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        validated_data = super(CreateUserSerializer, self).validate(attrs)
        password = validated_data['password']
        confirm_password = validated_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('Passwords do not match.')
        return validated_data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)
        return user


# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()
#
#     def validate(self, data):
#         user = authenticate(**data)
#         if user and user.is_active:
#             return user
#         raise serializers.ValidationError("Unable to log in with provided credentials.")
