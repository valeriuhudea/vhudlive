from django.contrib.auth.models import User, Group
from .models import *
from rest_framework import serializers


### API Serialization Models ### 
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'is_staff', 'groups', 'is_active']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class DataSerializer(serializers.ModelSerializer):
    #data_of = serializers.ReadOnlyField(source='storage_data')
    class Meta:
        model = Data
        fields = ('id', 'name', 'details', 'units', 'updated_date', 'active', 'data_of')

class StorageSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    storage_data = DataSerializer(many=True, read_only=True, source='data_of')
    
    class Meta:
        model = Storage
        fields = ('id', 'name', 'type', 'active', 'created_date', 'updated_date', 'storage_data', 'owner')

    
'''
    def create(self, validated_data):
        vhuds_data = validated_data.pop('vhud_data')
        virtualhud = VirtualHUD.objects.create(**validated_data)
        for vhud_data in vhuds_data:
            Data.objects.create(vhud_linked=virtualhud, **vhud_data)
        return virtualhud

    def update(self, instance, validated_data):
        vhuds_data = validated_data.pop('vhud_data')
        datas = (instance.vhud_data).all()
        datas = list(datas)
        instance.name = validated_data.get('name', instance.name)
        instance.type = validated_data.get('type', instance.type)
        instance.active = validated_data.get('active', instance.active)
        #instance.created_date = validated_data.get('created_date', instance.created_date)
        #instance.owner = validated_data.get('owner', instance.owner)
        instance.save()

        for vhud_data in vhuds_data:
            data = datas.pop(0)
            data.name = vhud_data.get('name', data.name)
            data.details = vhud_data.get('details', data.details)
            data.units = vhud_data.get('units', data.units)
            data.active = vhud_data.get('active', data.active)
            data.save()
        return instance '''  

    
