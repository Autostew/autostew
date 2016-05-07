from rest_framework import serializers

from autostew_web_session.models.session import Session


class SessionSerializer(serializers.ModelSerializer):
    children = serializers.PrimaryKeyRelatedField(many=True, queryset=Session.objects.all())

    class Meta:
        model = Session