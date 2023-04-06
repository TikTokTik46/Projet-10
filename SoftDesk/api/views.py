from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission
from django.http import Http404

from api.models import Projects, Contributors, Issues, Comments
from api.serializers import (
    ProjectsListSerializer,
    ProjectsDetailSerializer,
    ContributorsSerializer,
    IssuesListSerializer,
    IssuesDetailSerializer,
    CommentsListSerializer,
    CommentsDetailSerializer,
    UserSerializer
)

class IsProjectOwnerOrContributor(BasePermission):

        def has_permission(self, request, view):

            user_id = request.user
            project_id = view.kwargs.get('project_id')
            contributor = Contributors.objects.filter(user_id=user_id,
                                                      project_id=project_id)
            if contributor.exists():
                if request.method in ['GET', 'HEAD', 'OPTIONS']:
                    return True
                return contributor.get().role == 'CR'
            return False


class IsOwnerOrReadOnly(BasePermission):
    """
    Permission pour n'autoriser que les créateurs de l'objet à le modifier ou le supprimer.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Write permissions are only allowed to the owner of the object.
        return obj.author_user_id == request.user


class IsProjectContributor(BasePermission):

    def has_permission(self, request, view):

        user_id = request.user
        project_id = view.kwargs.get('project_id')
        contributor = Contributors.objects.filter(user_id=user_id,
                                       project_id=project_id)
        if contributor.exists():
            return True
        return False


class UserCreate(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'user_id': user.id},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectsViewSet(ModelViewSet):

    serializer_class = ProjectsListSerializer
    detail_serializer_class = ProjectsDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        contributors = Contributors.objects.filter(user_id=user)
        # Création d'une liste de projets correspondant à ces objets Contributors
        projects = [contributor.project_id for contributor in contributors]
        # Utilisation de cette liste pour récupérer les projets correspondants
        queryset = Projects.objects.filter(
            id__in=[project.id for project in projects])
        return queryset

    def get_serializer_class(self):
        if self.action in ['retrieve', 'create', 'update']:
            # Utiliser le serializer de détail pour la création
            return self.detail_serializer_class
        return super().get_serializer_class()

    def perform_create(self, serializer):
        #Permet de créer un objet contributor lié au projet avec l'utilisateur comme créateur
        project = serializer.save(author_user_id=self.request.user)

        # Création d'un objet Contributors pour l'utilisateur courant
        contributor = Contributors(user_id=self.request.user, project_id=project, role=Contributors.CREATOR)
        contributor.save()

        return Response(serializer.data)


class ContributorsViewSet(ModelViewSet):
    serializer_class = ContributorsSerializer
    permission_classes = [IsAuthenticated, IsProjectOwnerOrContributor]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        contributors = Contributors.objects.filter(project_id=project_id)
        return contributors

    def perform_create(self, serializer):
        serializer.save(project_id=Projects.objects.get(pk=self.kwargs.get('project_id')), role= Contributors.CONTRIBUTOR)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        if instance.role == 'CR':
            raise serializers.ValidationError(
                "Impossible de supprimer le créateur du projet"
            )
        instance.delete()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project_id"] = self.kwargs.get('project_id')
        return context

class IssuesViewSet(ModelViewSet):
    serializer_class = IssuesListSerializer
    detail_serializer_class = IssuesDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsProjectContributor]

    def get_queryset(self):
        project_id = self.kwargs.get('project_id')
        issues = Issues.objects.filter(project_id=project_id)
        return issues

    def perform_create(self, serializer):
        serializer.save(project_id=
                        Projects.objects.get(pk=self.kwargs.get('project_id')),
                        author_user_id=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action in ['retrieve', 'create', 'update']:
            # Utiliser le serializer de détail pour la création
            return self.detail_serializer_class
        return super().get_serializer_class()


class CommentsViewSet(ModelViewSet):
    serializer_class = CommentsListSerializer
    detail_serializer_class = CommentsDetailSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly, IsProjectContributor]

    def get_queryset(self):
        issue_id = self.kwargs.get('issue_id')
        comments = Comments.objects.filter(issue_id=issue_id)
        return comments

    def perform_create(self, serializer):
        serializer.save(issue_id=
                        Issues.objects.get(pk=self.kwargs.get('issue_id')),
                        author_user_id=self.request.user)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action in ['retrieve', 'create', 'update']:
            # Utiliser le serializer de détail pour la création
            return self.detail_serializer_class
        return super().get_serializer_class()

