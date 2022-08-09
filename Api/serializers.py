from rest_framework import serializers


class ClothesPlanSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=122, allow_null=False)


class GetPlanWeatherIDSerializer(serializers.Serializer):
    pk = serializers.IntegerField()


class GetWeatherClothesTimeSerializer(serializers.Serializer):
    location = serializers.CharField(max_length=122, allow_null=False)
    _time = serializers.IntegerField()
