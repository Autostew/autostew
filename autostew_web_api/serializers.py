from rest_framework import serializers

from autostew_web_session.models.session import Session


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Session
        fields = ('finished', 'is_result', 'is_final_result', 'timestamp')
