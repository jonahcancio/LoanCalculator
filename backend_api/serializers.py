from rest_framework import serializers
from .models import Calculation, Inquirer


class CalcSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calculation
        fields = '__all__'
        depth = 1


class InquirerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquirer
        fields = '__all__'