from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User


from api.models import Contributors, Projects, Issues, Comments

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True)
    password_confirmation = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Un utilisateur avec cette adresse e-mail existe déjà.")
        return value

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
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


class ProjectIdMixin:
    def get_project_id(self, obj):
        return obj.id


class AuthorNameMixin:
    def get_author_name(self, obj):
        return obj.author_user_id.get_full_name()


class ProjectsListSerializer(ModelSerializer, ProjectIdMixin, AuthorNameMixin):
    project_id = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = ['project_id', 'title', 'type', 'author_user_id', 'author_name']


class ProjectsDetailSerializer(ModelSerializer, ProjectIdMixin,AuthorNameMixin):
    project_id = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = ['project_id', 'title', 'description', 'type', 'author_user_id', 'author_name']
        read_only_fields = ['project_id', 'author_user_id', 'author_name']


class ContributorsSerializer(ModelSerializer):
    contributor_id = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()

    class Meta:
        model = Contributors
        fields = ['contributor_id', 'user_id', 'user_name', 'role']
        read_only_fields = ['contributor_id','role', 'user_name']

    def get_contributor_id(self, obj):
        return obj.id

    def get_user_name(self, obj):
        return obj.user_id.get_full_name()

    def get_role(self, obj):
        return obj.get_role_display()

    def validate_user_id(self, data):
        # data correspond aux donnés qui doivent être validés, ici user_id
        project_id = self.context['request'].parser_context['kwargs'].get('project_id')
        if Contributors.objects.filter(
                project_id=project_id, user_id=data).exists():
            raise serializers.ValidationError(
                "User déjà présent dans les contributeurs"
            )
        return data


class IssuesListSerializer(ModelSerializer):
    issue_id = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()

    class Meta:
        model = Issues
        fields = ['issue_id', 'title', 'tag', 'priority', 'status', 'created_time']

    def get_issue_id(self, obj):
        return obj.id

    def get_created_time(self, obj):
        return obj.created_time.strftime("%d/%m/%Y %H:%M")

class IssuesDetailSerializer(ModelSerializer, AuthorNameMixin):
    issue_id = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()

    class Meta:
        model = Issues
        fields = ['issue_id', 'title', 'description', 'tag', 'priority', 'project_id',
                  'status', 'author_user_id', 'author_name', 'created_time']
        read_only_fields = ['project_id', 'author_user_id']

    def get_issue_id(self, obj):
        return obj.id

    def get_created_time(self, obj):
        return obj.created_time.strftime("%d/%m/%Y %H:%M")

class CommentsListSerializer(ModelSerializer):
    comment_id = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['comment_id', 'description', 'author_user_id',
                  'issue_id']

    def get_comment_id(self, obj):
        return obj.id


class CommentsDetailSerializer(ModelSerializer, AuthorNameMixin):
    comment_id = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['comment_id', 'description', 'author_user_id', 'author_name'
                  'issue_id', 'created_time']
        read_only_fields = ['comment_id', 'author_user_id', 'issue_id']


    def get_comment_id(self, obj):
        return obj.id