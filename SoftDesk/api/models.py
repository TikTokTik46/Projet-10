from django.db import models
from django.conf import settings


class Contributor(models.Model):

    CREATOR = 'CR'
    CONTRIBUTOR = 'CO'

    ROLES = [
        (CREATOR, 'Créator'),
        (CONTRIBUTOR, 'Contributor'),
    ]

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    project_id = models.ForeignKey(
        'api.Project', on_delete=models.CASCADE
        , related_name="projects_contributors")
    role = models.CharField(max_length=2,
                                  choices=ROLES)


    def __str__(self):
        return f"Projet n° : {self.project_id.id} - Contributeur : {self.user_id.get_full_name()} - Role : {self.get_role_display()}"

class Project(models.Model):

    BACK_END = 'BE'
    FRONT_END = 'FE'
    IOS = 'IO'
    ANDROID = 'AD'

    TYPES = [
        (BACK_END, 'Back-end'),
        (FRONT_END, 'Front-end'),
        (IOS, 'iOS'),
        (ANDROID, 'Android')
    ]

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    type = models.CharField(max_length=2, choices=TYPES)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE)

    def __str__(self):
        return f"Projet n° : {self.id} - Titre : {self.title}"

class Issue(models.Model):

    FAIBLE = 'FA'
    MOYENNE = 'MO'
    ELEVEE = 'EL'

    BUG = 'BG'
    AMELIORATION = 'AM'
    TACHE = 'TA'

    A_FAIRE = 'AF'
    EN_COURS = 'EC'
    TERMINE = 'TR'

    PRIORITIES = [
        (FAIBLE, 'Faible'),
        (MOYENNE, 'Moyenne'),
        (ELEVEE, 'Elevée')
    ]

    TAGS = [
        (BUG, 'Bug'),
        (AMELIORATION, 'Amélioration'),
        (TACHE, 'Tâche')
    ]

    STATUS = [
        (A_FAIRE, 'A faire'),
        (EN_COURS, 'En cours'),
        (TERMINE, 'Terminé')
    ]

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    tag = models.CharField(max_length=2, choices=TAGS)
    priority = models.CharField(max_length=2, choices=PRIORITIES)
    project_id = models.ForeignKey('api.Project', null=True,
                                   on_delete=models.CASCADE,
                                   related_name='project_issues')
    status = models.CharField(max_length=2, choices=STATUS)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE,
                                       related_name='authored_issues'
                                       )
    created_time = models.DateTimeField(auto_now_add=True)
    assigned = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE,
                                related_name='assigned_issues')

    def __str__(self):
        return f"Projet n° : {self.project_id.id} - Titre du probléme : {self.title}"

class Comment(models.Model):
    description = models.CharField(max_length=255)
    author_user_id = models.ForeignKey(settings.AUTH_USER_MODEL,
                                       on_delete=models.CASCADE)
    issue_id = models.ForeignKey('api.Issue', null=True,
                                 on_delete=models.CASCADE,
                                 related_name='issue_comments')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Projet n° : {self.issue_id.project_id.id} - Titre du probléme : {self.issue_id.title} - Commentaire : {self.description}"
