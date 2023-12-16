# -*- coding: utf-8 -*-

from typing import Any, TypeVar

from django.db.models import Model
from rest_framework import mixins, request, response, status

Mo = TypeVar('Mo', bound=Model)

class UpdateModelMixin(mixins.UpdateModelMixin[Mo]):

    def update(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        write_serializer = self.get_write_serializer(
            instance, data=request.data, partial=partial)
        write_serializer.is_valid(raise_exception=True)
        self.perform_update(write_serializer)

        # pylint: disable=protected-access
        if getattr(instance, '_prefetched_objects_cache', None) is not None:

            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        # pylint: enable=protected-access
        read_serializer = self.get_read_serializer(instance)

        return response.Response(read_serializer.data)


class CreateModelMixin(mixins.CreateModelMixin[Mo]):

    def create(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        write_serializer = self.get_write_serializer(data=request.data)
        write_serializer.is_valid(raise_exception=True)
        self.perform_create(write_serializer)

        read_serializer = self.get_read_serializer(write_serializer.instance)
        headers = self.get_success_headers(read_serializer.data)

        return response.Response(read_serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ListModelMixin(mixins.ListModelMixin[Mo]):

    def list(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_read_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_read_serializer(queryset, many=True)
        return response.Response(serializer.data)


class RetrieveModelMixin(mixins.RetrieveModelMixin[Mo]):

    def retrieve(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        instance = self.get_object()
        serializer = self.get_read_serializer(instance)
        return response.Response(serializer.data)
