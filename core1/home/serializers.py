from rest_framework import serializers
from home.models import Person,Color
from django.contrib.auth.models import User



class RegisterSerializer(serializers.Serializer): # to make custom serializer 
    username = serializers.CharField()
    email= serializers.EmailField()
    password = serializers.CharField()

    def validate(self,data):
        if data['username']:
            if User.objects.filter(username= data['username']).exists():
                raise serializers.ValidationError("username is taken")
        if data['email']:
            if User.objects.filter(email= data['email'] ).exists():
                raise serializers.ValidationError("username is taken")
        return data

    def create(self,validated_data):
        user = User.objects.create(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()

    password = serializers.CharField()
class ColorSerializers(serializers.ModelSerializer):
     class Meta:
        model = Color
        fields = ['color_name','id']
       

class PeopleSerializers(serializers.ModelSerializer):
    color_id =  ColorSerializers(read_only=True)
    #color_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Person
        fields = '__all__'
    def get_color_info(self, objs):
        if objs.color_id: 
            color_objs = Color.objects.get(id=objs.color_id.id)
            return {
                'id': color_objs.id,
               'color_name': color_objs.color_name,
               
            }
        return None 
     

    def validate(self, data):
        special_characters="!@#$%^&*()_+?-=,<>/"
        name = data.get('name', '') 
        if any(c in special_characters for c in name):
            raise serializers.ValidationError('name should not contain special chars')
        if data['age'] < 18:
            raise serializers.ValidationError('age should be greater than 18')
        return data