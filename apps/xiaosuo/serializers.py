# -*- coding: utf-8 -*-

from rest_framework import serializers

from .models import *


class VisitHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = VisitHistory
        fields = "__all__"


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = "__all__"


class ChapterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chapter
        fields = "__all__"


class ChapterSerializer_List(serializers.ModelSerializer):
    # def get_value(self, dictionary):
    #     dictionary

    class Meta:
        model = Chapter
        # fields = "__all__"
        exclude = ["content"]


class CollectionGetSerializer(serializers.ModelSerializer):
    chapter_set = ChapterSerializer_List(many=True)

    # default_validators =

    class Meta:
        model = Collection
        exclude = ["user"]
        # fields = "__all__"
        depth = 1


class ClassificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classification
        fields = "__all__"


class PlateSerializer(serializers.ModelSerializer):
    classification_set = ClassificationSerializer(many=True)

    class Meta:
        model = Plate
        fields = "__all__"


class UserToVisitHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = UserToVisitHistory
        fields = "__all__"


class CollectionCountGetSerializer(serializers.ModelSerializer):
    # collection = CollectionSerializer(many=True, read_only=True)

    class Meta:
        model = CollectionCount
        exclude = ["user"]
        # fields = "__all__"
        depth = 1


class CollectionCountSerializer(serializers.ModelSerializer):
    # collection = CollectionSerializer(many=True, read_only=True)

    class Meta:
        model = CollectionCount
        # exclude = ["user"]
        fields = "__all__"
        # depth = 1


class ChapterCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChapterCode
        fields = "__all__"


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        exclude = ["password"]
        # fields = "__all__"
        # depth = 1
