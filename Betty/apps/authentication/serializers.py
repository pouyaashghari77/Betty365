from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    # birth_date = serializers.DateField(required=False)
    # security_question = serializers.CharField(required=False)
    # security_answer = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password',
                  'email', 'first_name', 'last_name',
                  # 'birth_date', 'security_question', 'security_answer'
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
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            # birth_date=validated_data.get('birth_date'),
            # security_question=validated_data.get('security_question'),
            # security_answer=validated_data.get('security_answer'),
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")
