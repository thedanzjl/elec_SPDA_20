from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from .serializers import *
from .models import *


class DocumentViewSet(viewsets.GenericViewSet, ListModelMixin, RetrieveModelMixin, UpdateModelMixin):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def _get_doc_number(path, position):
        docnum = list(filter(lambda x: x, path.split('/')))[position]  # parse request path and get document number
        if not docnum.isdigit():
            raise serializers.ValidationError({'retrieve': 'Document number must be provided'})
        return int(docnum)

    @swagger_auto_schema(
        operation_summary="Получить документ",
        responses={200: DetailDocumentSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        docnum = DocumentViewSet._get_doc_number(request.path, -1)
        # TODO: request document from DocFlow
        instance: Document = get_object_or_404(self.get_queryset(), number=docnum, users__in=[request.user])
        serializer = DetailDocumentSerializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Сгенерировать и подписать документ",
        method="POST",
        request_body=GenerateDocumentSerializer,
        responses={200: GenerateDocumentSerializer}
    )
    @action(detail=True, methods=["POST"])
    def generate(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        docnum = DocumentViewSet._get_doc_number(request.path, -2)
        # TODO: request document generation from DocFlow
        instance: Document = get_object_or_404(self.get_queryset(), number=docnum, users__in=[request.user])
        serializer = GenerateDocumentSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    # @swagger_auto_schema(
    #     operation_summary="Подписать документ",
    #     method="POST",
    #     request_body=SignDocumentSerializer,
    #     responses={200: SignDocumentSerializer}
    # )
    # @action(detail=True, methods=["POST"])
    # def sign(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     docnum = DocumentViewSet.get_doc_number(request.path, -2)
    #     # TODO: sign document via DocFlow; if signed - proceed
    #     instance: Document = get_object_or_404(self.get_queryset(), number=docnum, users__in=[request.user])
    #     serializer = SignDocumentSerializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #
    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         instance._prefetched_objects_cache = {}
    #
    #     return Response(serializer.data)
