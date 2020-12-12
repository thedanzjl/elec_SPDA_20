from django.utils.timezone import now
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name'
        )


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    users = UserSerializer(many=True)

    class Meta:
        model = Document
        fields = (
            'number',
            'users',
            'sign_date',
            'sign_status'
        )


class DetailDocumentSerializer(DocumentSerializer):
    uri = serializers.SerializerMethodField()

    class Meta(DocumentSerializer.Meta):
        model = DocumentSerializer.Meta.model
        fields = DocumentSerializer.Meta.fields + ('uri',)

    @swagger_serializer_method(serializer_or_field=serializers.CharField(help_text='Получить URI на pdf документа'))
    def get_uri(self, obj: Document):
        return obj.path


class GenerateDocumentSerializer(DetailDocumentSerializer):
    class Meta(DetailDocumentSerializer.Meta):
        model = DetailDocumentSerializer.Meta.model
        fields = ()

    def update(self, instance: Document, validated_data):
        if not instance.sign_status:
            instance.sign_status = True
            instance.sign_date = now()
            instance.save()
        return instance


# class SignDocumentSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Document
#         fields = []
#
#     def update(self, instance: Document, validated_data):
#         if not instance.sign_status:
#             instance.sign_status = True
#             instance.sign_date = now()
#             instance.save()
#         return instance
