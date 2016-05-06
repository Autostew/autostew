from rest_framework import serializers

from autostew_web_session.models.session import Session


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    parent = serializers.ReadOnlyField(source='session.parent')
    children = serializers.PrimaryKeyRelatedField(many=True, queryset=Session.objects.all())

    class Meta:
        model = Session
        fields = ('url', 'parent', 'children', 'finished', 'is_result', 'is_final_result', 'timestamp')
