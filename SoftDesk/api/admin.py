from django.contrib import admin
from .models import Contributor, Project, Issue, Comment

# Register your models here.
admin.site.register(Contributor)
admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Comment)
