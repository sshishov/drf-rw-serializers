# -*- coding: utf-8 -*-

from typing import TypeVar

from django.db.models import Model
from rest_framework import viewsets, mixins

from .generics import GenericAPIView
from .mixins import CreateModelMixin, UpdateModelMixin, ListModelMixin, RetrieveModelMixin

Mo = TypeVar('Mo', bound=Model)


class GenericViewSet(GenericAPIView[Mo],
                     viewsets.GenericViewSet[Mo]):
    pass


class ModelViewSet(CreateModelMixin[Mo],
                   RetrieveModelMixin[Mo],
                   UpdateModelMixin[Mo],
                   mixins.DestroyModelMixin[Mo],
                   ListModelMixin[Mo],
                   GenericViewSet[Mo]):
    pass


class ReadOnlyModelViewSet(RetrieveModelMixin[Mo],
                           ListModelMixin[Mo],
                           GenericViewSet[Mo]):
    pass
