# Flask Authentication Microservice

## Présentation

Ce dépôt représente le microservice d'authentification et de gestion des utilisateurs de l'application **Sport Connect**.
Ce service est responsable de l'inscription, de la connexion, de la gestion des profils et de l'authentification sécurisée des utilisateurs via JWT.

**Sport Connect** est une application web conçue pour faciliter l’organisation et la participation à des événements sportifs.
Ce projet a été développé dans le cadre du premier semestre du Master 1 Informatique, parcours Développeur Full Stack, lors des cours dédiés à la conception et à la modélisation de projets informatiques.

L’objectif principal de cette plateforme est de permettre aux amateurs de sport de trouver des partenaires,
de rejoindre des événements ou d’en organiser facilement, sans contraintes organisationnelles complexes.

Technologies utilisées:
Flask framework

## Prérequis

Avant de commencer, assurez-vous d'avoir installé :
- Python (>= 3.8)
- `pip`
- `virtualenv`

## Installation

1. **Cloner le dépôt** :
   ```sh
   git clone <URL_DU_DEPOT>
   cd <NOM_DU_PROJET>
   ```

2. **Créer un environnement virtuel** :
   ```sh
   python -m venv venv
   ```

3. **Activer l'environnement virtuel** :
   - Sur Windows :
     ```sh
     venv\Scripts\activate
     ```
   - Sur macOS/Linux :
     ```sh
     source venv/bin/activate
     ```

4. **Installer les dépendances** :
   ```sh
   pip install -r requirements.txt
   ```

## Configuration

Créer un fichier `.env` à la racine du projet et y ajouter les variables suivantes :

```ini
SECRET_KEY= // vous pouvez utiliser 'openssl rand -base64 32' pour la generer
JWT_SECRET_KEY=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
```

## Exécution de l'application

1. **Lancer l'application Flask** :
   ```sh
   flask run
   ```
   Par défaut, l'application sera accessible à `http://127.0.0.1:5000/`.

