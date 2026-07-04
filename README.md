# IFRI_MentorLink 

page web fonctionnelle permettant la recherche de mentors compatibles, sans authentification. Le matching est calculé côté serveur à partir des matières demandées et de l'heure souhaitée, avec une tolérance horaire de ± 1 heure.

## Technologies

- **Frontend** : HTML / CSS / JavaScript
- **Backend** : Django 
- **Base de données** : MySQL

## Structure du projet

```
ifri_mentorlink/
├── manage.py
├── requirements.txt
├── ifri_mentorlink/          # configuration du projet Django
│   ├── settings.py           # config MySQL, apps, templates
│   └── urls.py
└── matching/                 # application principale
    ├── models.py             # Mentor, Availability
    ├── matching_utils.py     # algorithme de matching + scoring
    ├── views.py               # page + endpoint JSON /api/search/
    ├── urls.py
    ├── admin.py
    ├── management/commands/seed_mentors.py   # pré-remplissage (5 mentors)
    ├── migrations/0001_initial.py
    ├── templates/matching/index.html
    └── static/matching/{css,js}/
```

## Installation

### 1. Créer un environnement virtuel et installer les dépendances

```bash
python -m venv venv
source venv/bin/activate        # Windows : venv\Scripts\activate
pip install -r requirements.txt
```

> `mysqlclient` nécessite les en-têtes de développement MySQL sur votre
> système (`sudo apt install default-libmysqlclient-dev build-essential
> pkg-config` sous Ubuntu/Debian, ou `brew install mysql-client` sous macOS).

### 2. Créer la base de données MySQL

```sql
CREATE DATABASE ifri_mentorlink_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Configurer les identifiants

Par défaut, `ifri_mentorlink/settings.py` utilise `root` sans mot de passe sur
`127.0.0.1:3306`. Vous pouvez surcharger ces valeurs avec des variables
d'environnement au lieu de modifier le fichier :

```bash
export DB_NAME=ifri_mentorlink_db
export DB_USER=root
export DB_PASSWORD=votre_mot_de_passe
export DB_HOST=127.0.0.1
export DB_PORT=3306
```

### 4. Appliquer les migrations et pré-remplir la base

```bash
python manage.py migrate
python manage.py seed_mentors
```

`seed_mentors` insère 5 mentors de démonstration (matières, disponibilités,
filière, format de mentorat). Relancez avec `--flush` pour repartir de zéro :

```bash
python manage.py seed_mentors --flush
```

### 5. Créer un compte administrateur (pour accéder à /admin/)

Pour pouvoir ajouter, modifier ou supprimer des mentors via l'interface
d'administration Django, créez un compte :

```bash
python manage.py createsuperuser
```

Renseignez un nom d'utilisateur et un mot de passe (au moins 8 caractères,
différent du nom d'utilisateur). Une fois le serveur lancé, connectez-vous
sur **http://127.0.0.1:8000/admin/** avec ces identifiants.

### 6. Lancer le serveur

```bash
python manage.py runserver
```

Ouvrez ensuite **http://127.0.0.1:8000/** — la page de recherche s'affiche
directement, aucune connexion n'est requise.

## Fonctionnement du matching

L'endpoint `GET /api/search/?subjects=...&time=HH:MM&filiere=...` (appelé en
AJAX par `script.js`) applique, pour chaque mentor :

1. **Compétences** : au moins une matière en commun entre la recherche et les
   matières du mentor (comparaison insensible à la casse). Sans matière
   commune, le mentor est écarté.
2. **Horaire** : l'heure souhaitée doit tomber dans un créneau de
   disponibilité du mentor, avec une tolérance de **± 1 heure**. Sans
   créneau compatible, le mentor est écarté.
3. **Filière (optionnelle)** : n'élimine aucun mentor, mais bonifie le score
   si elle correspond à la filière du mentor.

### Score de compatibilité (sur 100)

| Composante                                            | Points max |
|---------------------------------------------------------|:---------:|
| Proportion de matières en commun                        | 60        |
| Correspondance horaire (30 si exacte, 20 si via tolérance)| 30      |
| Filière correspondante (bonus optionnel)                 | 10       |

Les résultats sont triés par score décroissant et affichés sous forme de
fiches indiquant le nom, les matières en commun, les disponibilités, le
format de mentorat et le score.

## Notes

- Aucune authentification n'est implémentée, conformément au cahier des charges.
- Le CSRF Django n'est pas requis ici car l'API n'utilise que des requêtes GET
  en lecture seule (pas de création/modification de données depuis le frontend).
- L'interface d'administration Django (`/admin/`) permet d'ajouter/modifier des mentors manuellement une fois un superutilisateur créé
  (`python manage.py createsuperuser`).
