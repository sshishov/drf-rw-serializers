# -*- coding: utf-8 -*-

from typing import Any, TypeVar

from django.db.models import Model
from rest_framework import generics, mixins, request, response, serializers

from .mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin

Mo = TypeVar('Mo', bound=Model)


class GenericAPIView(generics.GenericAPIView[Mo]):

    def get_serializer_class(self) -> type[serializers.Serializer[Mo]]:
        """
        Return the class to use for the serializer.
        Defaults to using `self.serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        assert (
            self.serializer_class is not None or
            getattr(self, 'read_serializer_class', None) is not None
        ), (
            "'%s' should either include one of `serializer_class` and `read_serializer_class` "
            "attribute, or override one of the `get_serializer_class()`, "
            "`get_read_serializer_class()` method."
            % self.__class__.__name__
        )

        return self.serializer_class

    def get_read_serializer(self, *args: Any, **kwargs: Any) -> serializers.Serializer[Mo]:
        """
        Return the serializer instance that should be used for serializing output.
        """
        serializer_class = self.get_read_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_read_serializer_class(self) -> type[serializers.Serializer[Mo]]:
        """
        Return the class to use for the serializer.
        Defaults to using `self.read_serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins get full serialization, others get basic serialization)
        """
        if getattr(self, 'read_serializer_class', None) is None:
            return self.get_serializer_class()

        return self.read_serializer_class

    def get_write_serializer(self, *args: Any, **kwargs: Any) -> serializers.Serializer[Mo]:
        """
        Return the serializer instance that should be used for validating
        and deserializing input.
        """
        serializer_class = self.get_write_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_write_serializer_class(self) -> type[serializers.Serializer[Mo]]:
        """
        Return the class to use for the serializer.
        Defaults to using `self.write_serializer_class`.
        You may want to override this if you need to provide different
        serializations depending on the incoming request.
        (Eg. admins can send extra fields, others cannot)
        """
        if getattr(self, 'write_serializer_class', None) is None:
            return self.get_serializer_class()

        return self.write_serializer_class


class CreateAPIView(CreateModelMixin[Mo], GenericAPIView[Mo]):

    def post(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        return self.create(request, *args, **kwargs)


class UpdateAPIView(UpdateModelMixin[Mo], GenericAPIView[Mo]):

    def put(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        return self.update(request, *args, **kwargs)

    def patch(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        return self.partial_update(request, *args, **kwargs)


class ListAPIView(ListModelMixin[Mo], GenericAPIView[Mo]):

    def get(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        return self.list(request, *args, **kwargs)


class RetrieveAPIView(RetrieveModelMixin[Mo], GenericAPIView[Mo]):

    def get(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        return self.retrieve(request, *args, **kwargs)


class ListCreateAPIView(ListModelMixin[Mo],
                        CreateModelMixin[Mo],
                        GenericAPIView[Mo]):

    def get(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        return self.list(request, *args, **kwargs)

    def post(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        return self.create(request, *args, **kwargs)


class RetrieveDestroyAPIView(RetrieveModelMixin[Mo],
                             mixins.DestroyModelMixin[Mo],
                             GenericAPIView[Mo]):

    def get(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        return self.destroy(request, *args, **kwargs)


class RetrieveUpdateAPIView(RetrieveModelMixin[Mo],
                            UpdateModelMixin[Mo],
                            GenericAPIView[Mo]):

    def get(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        return self.update(request, *args, **kwargs)

    def patch(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        return self.partial_update(request, *args, **kwargs)


class RetrieveUpdateDestroyAPIView(RetrieveModelMixin[Mo],
                                   UpdateModelMixin[Mo],
                                   mixins.DestroyModelMixin[Mo],
                                   GenericAPIView[Mo]):

    def get(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        return self.retrieve(request, *args, **kwargs)

    def put(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        return self.update(request, *args, **kwargs)

    def patch(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request: request.Request, *args: Any, **kwargs: Any) -> response.Response:
        return self.destroy(request, *args, **kwargs)
