from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data):
        try:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError("This User is already exists.")

            if data.get('password') != data.get('confirm_password'):
                raise serializers.ValidationError('Password and Confirm Password Does Not Match.')
            return data
        except Exception as err:
            raise serializers.ValidationError({'error': err.args[0]})

    def create(self, validated_data):
        try:
            user = User(mobile=validated_data['mobile'], email=validated_data['email'],
                        first_name=validated_data['first_name'], last_name=validated_data['last_name'])
            user.set_password(validated_data['password'])
            user.save()
            return user
        except Exception as err:
            raise serializers.ValidationError({'error': err.args[0]})


class UserLoginSerializers(serializers.ModelSerializer):
    mobile = serializers.CharField(max_length=15, validators=[validate_mobile_number])
    password = serializers.CharField()

    class Meta:
        model = User
        fields = (
            "mobile",
            'password',
        )

    def validate(self, data):
        mobile_number = data.get('mobile')
        password = data.get('password')

        user = authenticate(self.context.get('request'), mobile=mobile_number, password=password)

        if not user:
            raise AuthenticationFailed('Invalid mobile number or password')

        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

    final_result = serializers.SerializerMethodField()

    def validate(self, data):
        try:
            if Product.objects.filter(p_name=data['p_name'], cat=data['cat']).exists():
                raise serializers.ValidationError("In the Same Category Same Product is not Allowed.")
            return data
        except Exception as err:
            raise serializers.ValidationError({'error': err.args[0]})

    def get_final_result(self, obj):
        try:
            discount = obj.offer
            amount = obj.prize
            discount_amount = amount * (discount / 100)
            final_amount = amount - discount_amount
            return {'discount_amount': discount_amount, 'final_amount': final_amount,
                    'discount_percentage': f"{discount} %"}
        except Exception as err:
            raise serializers.ValidationError({'error': err.args[0]})

    def create(self, validated_data):
        instance = super().create(validated_data)
        return instance


class AddToCartSerializers(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate(self, data):
        user = self.context['request'].user
        try:
            product = Product.objects.get(pk=data['product_id'])
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist.")

        if data['quantity'] <= 0:
            raise serializers.ValidationError("Quantity should be positive.")

        if data['quantity'] > product.available:
            raise serializers.ValidationError("Insufficient quantity available.")

        return data

