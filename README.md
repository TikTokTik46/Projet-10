# SoftDesk - Issue Tracking System API

Cette API permet de remonter et de suivre des problèmes techniques rattachés à des projets.
Elle permet aux utilisateurs connectés de créer divers projets, d'ajouter des utilisateurs à des projets spécifiques, de créer des problèmes au sein des projets et d'attribuer des libellés à ces problèmes en fonction de leurs priorités, de balises, etc.

## Installation

1. Cloner le repository GitHub.
2. Installer les dépendances en utilisant la commande `pip install -r requirements.txt`.
3. Exécuter la commande `python manage.py runserver` pour lancer le serveur depuis le répertoire SoftDesk.

## Utilisation

La documentation de l'API se trouve [ici](https://documenter.getpostman.com/view/24353229/2s93RXtBGK) !  

Pour utiliser Issue Tracking System API, vous pouvez accéder à [http://localhost:8000/API](http://localhost:8000/API) via votre navigateur web ou utiliser un logiciel permettant de créer des requêtes HTTP tel que [POSTMAN](https://www.postman.com/).  
Vous pouvez également consulter le site d'administration en accédant à [http://localhost:8000/admin](http://localhost:8000/admin) et en utilisant le compte d'administrateur (admin) disposant des droits d'administration.

Vous pouvez créer un compte ou utiliser un compte de test ci-dessous.

| Nom du compte test  | Mot de passe |
|---------------------|--------------|
| admin               | password     |
| jean-luc@gmail.com  | password     |
| jean-marc@gmail.com | password     |


## Contribuer

Les contributions sont les bienvenues ! Pour contribuer à Issue Tracking System API, veuillez ouvrir une issue ou une pull request sur GitHub.

## Licence

Ce projet est sous licence MIT. Veuillez consulter le fichier LICENSE.md pour plus d'informations.
