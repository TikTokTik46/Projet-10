from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from api.utils import convert_time


from api.models import Contributors, Projects, Issues, Comments

class ProjectMixin:
    def get_project_id(self, obj):
        return obj.id

    def get_type(self, obj):
        return obj.get_type_display()

    def get_author_name(self, obj):
        return obj.author_user_id.get_full_name()


class IssueMixin:
    def get_issue_id(self, obj):
        return obj.id

    def get_created_time(self, obj):
        return convert_time(obj)

    def get_tag(self, obj):
        return obj.get_tag_display()

    def get_status(self, obj):
        return obj.get_status_display()

    def get_priority(self, obj):
        return obj.get_priority_display()

    def get_author_name(self, obj):
        return obj.author_user_id.get_full_name()

class CommentMixin:
    def get_comment_id(self, obj):
        return obj.id

    def get_created_time(self, obj):
        return convert_time(obj)

    def get_author_name(self, obj):
        return obj.author_user_id.get_full_name()


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


class ProjectsListSerializer(ModelSerializer, ProjectMixin):
    project_id = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = ['project_id', 'title', 'type', 'author_user_id', 'author_name']


class ProjectsDetailSerializer(ModelSerializer, ProjectMixin):
    project_id = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = ['project_id', 'title', 'description', 'type', 'author_user_id', 'author_name']
        read_only_fields = ['project_id', 'author_user_id', 'author_name']

    def to_internal_value(self, data):
        # Permet de retourner une erreur personnalisée si la valeur de Type ne correspond pas aux choix possibles.
        type_value = data.get('type', '')
        if type_value not in dict(Projects.TYPES):
            raise serializers.ValidationError({'type': ['Valeur non valide. Choisissez parmi les options suivantes : ' + str(dict(Projects.TYPES))]})

        return super().to_internal_value(data)


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


class IssuesListSerializer(ModelSerializer, IssueMixin):
    issue_id = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()
    priority = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Issues
        fields = ['issue_id', 'title', 'tag', 'priority', 'status', 'created_time']


class IssuesDetailSerializer(ModelSerializer, IssueMixin):
    issue_id = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    created_time = serializers.SerializerMethodField()

    class Meta:
        model = Issues
        fields = ['issue_id', 'title', 'description', 'tag', 'priority', 'project_id',
                  'status', 'author_user_id', 'author_name', 'created_time']
        read_only_fields = ['project_id', 'author_user_id']

    def to_internal_value(self, data):
        # Initialisation de la liste des erreurs
        errors = {}

        # Vérification de la validité du tag
        tag_value = data.get('tag', '')
        if tag_value not in dict(Issues.TAGS):
            errors['tag'] = [
                'Valeur non valide. Choisissez parmi les options suivantes : ' + str(
                    dict(Issues.TAGS))]

        # Vérification de la validité de la priorité
        priority_value = data.get('priority', '')
        if priority_value not in dict(Issues.PRIORITIES):
            errors['priority'] = [
                'Valeur non valide. Choisissez parmi les options suivantes : ' + str(
                    dict(Issues.PRIORITIES))]

        # Vérification de la validité de la priorité
        status_value = data.get('status', '')
        if status_value not in dict(Issues.STATUS):
            errors['status'] = [
                'Valeur non valide. Choisissez parmi les options suivantes : ' + str(
                    dict(Issues.STATUS))]

        # Lancement de l'exception s'il y a des erreurs
        if errors:
            raise serializers.ValidationError(errors)

        # Si tout est ok, retourne les données vérifiées
        return super().to_internal_value(data)

class CommentsListSerializer(ModelSerializer, CommentMixin):
    comment_id = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['comment_id', 'description', 'author_user_id',
                  'issue_id']


class CommentsDetailSerializer(ModelSerializer, CommentMixin):
    comment_id = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ['comment_id', 'description', 'author_user_id', 'author_name',
                  'issue_id', 'created_time']
        read_only_fields = ['comment_id', 'author_user_id', 'issue_id', 'author_name']
