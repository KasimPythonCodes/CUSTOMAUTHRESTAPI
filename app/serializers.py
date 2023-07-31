from rest_framework import serializers
from app.models import UserRegistration
from django.contrib.auth.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=250,style={'input_type':'password','placeholder':'password'},write_only=True)
    class Meta:
        model = UserRegistration
        fields =['username','first_name','last_name','email','password','confirm_password']
        extra_kwargs = {'confirm_password':{'write_only':True}}
        
    def validate(self ,attr):
        password = attr.get('password')    
        confirm_password = attr.get('confirm_password')    
        if password !=confirm_password:
            raise serializers.ValidationError("Password and confirm password doen't match")
        return attr
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()        
    password = serializers.CharField(max_length=250,style={'input_type':'password','placeholder':'password'})  
    
    
        
class UserProfile(serializers.ModelSerializer):
    class Meta:
        model=UserRegistration
        fields = "__all__"