from rest_framework import serializers
from .models import ListModel
from userprofile.models import Users
import re
from rest_framework.exceptions import APIException

def data_validate(data):
    script_obj = re.findall(r'script', str(data), re.IGNORECASE)
    select_obj = re.findall(r'select', str(data), re.IGNORECASE)
    if script_obj:
        raise APIException({'detail': 'Bad Data can‘not be store'})
    elif select_obj:
        raise APIException({'detail': 'Bad Data can‘not be store'})
    else:
        return data

def openid_validate(data):
    if Users.objects.filter(openid=data).exists():
        return data
    else:
        raise APIException({'detail': 'User does not exists'})

def appid_validate(data):
    if Users.objects.filter(appid=data).exists():
        return data
    else:
        raise APIException({'detail': 'User does not exists'})

class GoodsspecsGetSerializer(serializers.ModelSerializer):
    goods_specs = serializers.CharField(read_only=True, required=False)
    creater = serializers.CharField(read_only=True, required=False)
    class Meta:
        model = ListModel
        exclude = ['openid', 'is_delete', ]
        read_only_fields = ['id', 'openid', 'appid', 'create_time', 'update_time', ]

class GoodsspecsPostSerializer(serializers.ModelSerializer):
    openid = serializers.CharField(read_only=False, required=False, validators=[openid_validate])
    goods_specs = serializers.CharField(read_only=False,  required=True, validators=[data_validate])
    creater = serializers.CharField(read_only=False, required=True, validators=[data_validate])
    class Meta:
        model = ListModel
        exclude = ['is_delete', ]
        read_only_fields = ['id', 'create_time', 'update_time', ]

class GoodsspecsUpdateSerializer(serializers.ModelSerializer):
    goods_specs = serializers.CharField(read_only=False, required=True, validators=[data_validate])
    creater = serializers.CharField(read_only=False, required=True, validators=[data_validate])
    class Meta:
        model = ListModel
        exclude = ['openid', 'is_delete', ]
        read_only_fields = ['id', 'create_time', 'update_time', ]

class GoodsspecsPartialUpdateSerializer(serializers.ModelSerializer):
    goods_specs = serializers.CharField(read_only=False, required=False, validators=[data_validate])
    creater = serializers.CharField(read_only=False, required=False, validators=[data_validate])
    class Meta:
        model = ListModel
        exclude = ['openid', 'is_delete', ]
        read_only_fields = ['id', 'create_time', 'update_time', ]
