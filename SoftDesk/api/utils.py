from rest_framework import serializers
from django.utils import timezone

# Permet de convertir la date en fonction de la timezone locale au format J/M/A H:M
def display_time(obj):
    # Renvoie l'heure locale
    local_date = timezone.localtime(obj.created_time)
    return local_date.strftime("%d/%m/%Y %H:%M")

# Permet de retourner le nom de l'utilisateur
def display_name(obj_user_field):
    return obj_user_field.get_full_name()

# Permet de retourner l'ID de l'objet
def display_id(obj):
    return obj.id


# Cette fonction permet de renvoyer un message d'erreur personnalisé
# lorsque l'utilisateur renseigne incorrectement un choicefield.

def choice_fields_validator(data, choice_fields):
    errors = {}

    # Verification de la valeure envoyée, retourne un message perssonalisé
    # en cas d'erreure
    for field, choices in choice_fields.items():
        tag_value = data.get(field, '')
        if tag_value not in dict(choices):
            errors[field] = [
                'Valeur non valide. Choisissez parmi les options suivantes : ' + str(
                    dict(choices))]

    # Lancement de l'exception s'il y a des erreurs
    if errors:
        raise serializers.ValidationError(errors)
