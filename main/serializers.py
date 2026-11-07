from django.utils.html import strip_tags
from rest_framework import serializers

from main.models import Project, Experience, Education

def clean_text(value):
    return strip_tags(value).strip()

def clean_required(value, label):
    value = clean_text(value)
    if not value:
        raise serializers.ValidationError(f"{label} can't be empty.")
    return value

class PortofolioItemSerializer(serializers.ModelSerializer):
    star_count = serializers.SerializerMethodField()
    is_starred = serializers.SerializerMethodField()
    starred_by_names = serializers.SerializerMethodField()

    def get_star_count(self, obj):
        return obj.starred_by.count()

    def get_is_starred(self, obj):
        request = self.context.get("request")
        if request is None or not request.user.is_authenticated:
            return False
        return request.user in obj.starred_by.all()

    def get_starred_by_names(self, obj):
        return ", ".join(user.username for user in obj.starred_by.all())

    def validate(self, attrs):
        started = attrs.get("started_at", getattr(self.instance, "started_at", None))
        ended = attrs.get("ended_at", getattr(self.instance, "ended_at", None))
        if started and ended and ended < started:
            raise serializers.ValidationError({"ended_at": "End date can't be earlier than start date."})
        return attrs

class ProjectSerializer(PortofolioItemSerializer):
    class Meta:
        model = Project
        fields = [
            "id", "title", "description", "tech_stack",
            "project_url", "project_image_url",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        return clean_required(value, "Title")

    def validate_description(self, value):
        return clean_required(value, "Description")
    
    def validate_tech_stack(self, value):
        return strip_tags(value)

class ExperienceSerializer(PortofolioItemSerializer):
    class Meta:
        model = Experience
        fields = [
            "id", "title", "description", "category",
            "thumbnail", "started_at", "ended_at",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]

    def validate_title(self, value):
        return clean_required(value, "Title")

    def validate_description(self, value):
        return clean_required(value, "Description")

class EducationSerializer(PortofolioItemSerializer):
    class Meta:
        model = Education
        fields = [
            "id", "institution", "description", "degree", 
            "started_at", "ended_at",
            "star_count", "is_starred", "starred_by_names",
        ]
        read_only_fields = ["id"]
    
    def validate_institution(self, value):
        return clean_required(value, "Institution")

    def validate_description(self, value):
        return clean_required(value, "Description")

    def validate_degree(self, value):
        return clean_required(value, "Degree")