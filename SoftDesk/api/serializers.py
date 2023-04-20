from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from api.utils import display_time, display_name, \
    display_id, choice_fields_validator
from api.models import Contributor, Project, Issue, Comment


class ProjectMixin:
    def get_project_id(self, obj):
        return display_id(obj)

    def get_type(self, obj):
        return obj.get_type_display()

    def get_author_name(self, obj):
        return display_name(obj.author_user_id)


class IssueMixin:
    def get_issue_id(self, obj):
        return display_id(obj)

    def get_created_time(self, obj):
        return display_time(obj)

    def get_tag(self, obj):
        return obj.get_tag_display()

    def get_status(self, obj):
        return obj.get_status_display()

    def get_priority(self, obj):
        return obj.get_priority_display()

    def get_author_name(self, obj):
        return display_name(obj.author_user_id)

    def get_assigned_name(self, obj):
        return display_name(obj.assigned)

class CommentMixin:
    def get_comment_id(self, obj):
        return display_id(obj)

    def get_created_time(self, obj):
        return display_time(obj)

    def get_author_name(self, obj):
        return display_name(obj.author_user_id)


class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True)
    password_confirmation = serializers.CharField(write_only=True,
                                                  required=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Un utilisateur avec cette adresse e-mail existe déjà.")
        return value

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError(
                "Les mots de passe ne correspondent pas.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


class ProjectsListSerializer(ModelSerializer, ProjectMixin):
    project_id = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'type', 'author_user_id',
                  'author_name']
        read_only_field = ['author_name']


class ProjectsDetailSerializer(ModelSerializer, ProjectMixin):
    project_id = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['project_id', 'title', 'description', 'type',
                  'author_user_id', 'author_name']
        read_only_fields = ['project_id', 'author_user_id', 'author_name']

    def to_internal_value(self, data):
        choice_fields = {'type': Project.TYPES}
        choice_fields_validator(data, choice_fields)
        return super().to_internal_value(data)


class ContributorsSerializer(ModelSerializer):
    contributor_id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = Contributor
        fields = ['contributor_id', 'user_id', 'user_name', 'role']
        read_only_fields = ['contributor_id','role', 'user_name']

    def get_contributor_id(self, obj):
        return obj.id

    def get_user_name(self, obj):
        return display_name(obj.user_id)

    def get_role(self, obj):
        return obj.get_role_display()

    def validate_user_id(self, data):
        # data correspond aux donnés qui doivent être validés, ici user_id
        project_id = self.context['request'].parser_context['kwargs'].get(
            'project_id')
        if Contributor.objects.filter(
                project_id=project_id, user_id=data).exists():
            raise serializers.ValidationError(
                "User déjà présent dans les contributeurs"
            )
        return data


class IssuesListSerializer(ModelSerializer, IssueMixin):
    issue_id = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    assigned_name = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['issue_id', 'title', 'tag', 'priority',
                  'status', 'created_time','author_name','assigned_name']


class IssuesDetailSerializer(ModelSerializer, IssueMixin):
    issue_id = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()
    assigned_name = serializers.SerializerMethodField()

    class Meta:
        model = Issue
        fields = ['issue_id', 'title', 'description', 'tag','priority',
                  'project_id', 'status', 'author_user_id',
                  'created_time','assigned','author_user_id', 'author_name',
                  'assigned_name']
        read_only_fields = ['project_id', 'author_user_id']

    def to_internal_value(self, data):
        choice_fields = {'tag': Issue.TAGS,
                   'priority': Issue.PRIORITIES,
                   'status': Issue.STATUS}
        choice_fields_validator(data, choice_fields)
        return super().to_internal_value(data)

class CommentsListSerializer(ModelSerializer, CommentMixin):
    comment_id = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['comment_id', 'issue_id', 'description',
                  'author_user_id', 'author_name']


class CommentsDetailSerializer(ModelSerializer, CommentMixin):
    comment_id = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['comment_id', 'issue_id', 'description',
                  'author_user_id', 'author_name', 'created_time']
        read_only_fields = ['comment_id', 'author_user_id', 'issue_id',
                            'author_name']
