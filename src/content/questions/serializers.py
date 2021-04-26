from rest_framework import serializers
from .models import Question, QuestionImageAsset, QuestionVideoAsset, QuestionAudioAsset

class QuestionImageAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionImageAsset
        fields = ['image']

class QuestionAudioAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAudioAsset
        fields = ['audio_file']

class QuestionVideoAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionVideoAsset
        fields = ['url']

class QuestionSerializer(serializers.ModelSerializer):
    answeroption_set = AnswerOptionSerializer(many=True)
    image_assets = serializers.SerializerMethodField('get_image_assets')
    video_assets = serializers.SerializerMethodField('get_video_assets')
    audio_assets = serializers.SerializerMethodField('get_audio_assets')

    def get_image_assets(self, obj):
        qs = obj.get_questionimageasset_set()
        serializer = QuestionImageAssetSerializer(instance=qs, many=True)
        return serializer.data

    def get_audio_assets(self, obj):
        qs = obj.get_questionaudioasset_set()
        serializer = QuestionAudioAssetSerializer(instance=qs, many=True)
        return serializer.data

    def get_video_assets(self, obj):
        qs = obj.get_questionvideoasset_set()
        serializer = QuestionVideoAssetSerializer(instance=qs, many=True)
        return serializer.data

    class Meta:
        model = Question
        fields = ['id', 'topic', 'question_text' , 'answeroption_set', 'image_assets', 'video_assets', 'audio_assets']