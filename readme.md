# NephroCare
NephroCare is a web application designed to assist patients with chronic kidney disease (CKD) in managing their health. The application provides a platform for patients to track their symptoms, medications, and appointments, as well as access educational resources about CKD.

# Frontend

## Table of Contents
  - [NephroCare](#nephrocare)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
    - [Authentification](#authentification)
    - [Gestion des patients](#gestion-des-patients)
    - [Gestion des examens](#gestion-des-examens)
    - [Gestion des rendez-vous](#gestion-des-rendez-vous)
    - [Alertes et notifications](#alertes-et-notifications)
    - [Gestion de compte](#gestion-de-compte)
  - [Technologies Used](#technologies-used)
  - [Setup](#setup)
  - [Development Server](#development-server)
  - [Production](#production)

## Features

### Authentification

- Connexion des utilisateurs
- Gestion des rôles (médecin, administrateur)

Pour vous connecter à l'application, accédez à l'URL suivante : [http://localhost:3000/login](http://localhost:3000/login) ou directement sur la version en ligne: [https://nephro-care.vercel.app/login](https://nephro-care.vercel.app/login). Vous pouvez vous connecter avec les identifiants suivants :

- email: test@gmail.com
- password: 12345678

### Gestion des patients

- Ajout, modification et suppression de patients
- Consultation des informations médicales et des antécédents médicaux
- Suivi des résultats d'examens et des traitements

Pour ajouter un patient, accédez à l'URL suivante : [http://localhost:3000/home/patients](http://localhost:3000/home/patients). Vous pouvez ajouter un patient en remplissant le formulaire avec les informations requises. Vous pouvez également consulter la liste des patients et modifier ou supprimer leurs informations.

### Gestion des examens

- Ajout, modification et suppression d'examens
- Consultation des résultats d'examens
- Suivi des traitements et des prescriptions

Pour ajouter un examen, accédez à l'URL suivante : [http://localhost:3000/home/examens](http://localhost:3000/home/examens). Vous pouvez ajouter un examen en remplissant le formulaire avec les informations requises. Vous pouvez également consulter les résultats des examens ainsi que les prescriptions associées.

### Gestion des rendez-vous

- Programmation automatisée des rendez-vous à la création d'examen
- Consultation des rendez-vous programmés
- Gestion des annulations et des modifications de rendez-vous

Pour programmer un rendez-vous, accédez à l'URL suivante : [http://localhost:3000/home/appointments](http://localhost:3000/home/appointments). Vous pouvez programmer un rendez-vous en remplissant le formulaire avec les informations requises. Vous pouvez également consulter la liste des rendez-vous d'une date précise, en cliquant sur cette date dans le calendrier.

### Alertes et notifications

- Alertes pour les résultats d'examens anormaux
- Notifications pour les rendez-vous à venir

Pour consulter les alertes et notifications, accédez à l'URL suivante : [http://localhost:3000/home/notifications](http://localhost:3000/home/notifications).

### Gestion de compte

- Modification des informations personnelles
- Changement de mot de passe
- Suppression de compte

Pour gérer votre compte, accédez à l'URL suivante : [http://localhost:3000/home/settings/account](http://localhost:3000/home/settings/account).

## Technologies Used
- **Nuxt.js**: A powerful framework for building server-rendered Vue.js applications.
- **Tailwind CSS**: A utility-first CSS framework for creating custom designs.
- **Pinia**: A state management library for Vue.js applications.

## Setup

Look at the [Nuxt documentation](https://nuxt.com/docs/getting-started/introduction) to learn more.

Make sure to install dependencies:

```bash
# npm
npm install

# pnpm
pnpm install

# yarn
yarn install

# bun
bun install
```

## Development Server

Start the development server on `http://localhost:3000`:

```bash
# npm
npm run dev

# pnpm
pnpm dev

# yarn
yarn dev

# bun
bun run dev
```

## Production

Build the application for production:

```bash
# npm
npm run build

# pnpm
pnpm build

# yarn
yarn build

# bun
bun run build
```

Locally preview production build:

```bash
# npm
npm run preview

# pnpm
pnpm preview

# yarn
yarn preview

# bun
bun run preview
```

Check out the [deployment documentation](https://nuxt.com/docs/getting-started/deployment) for more information.

# Backend

## Installation
 
Pour travailler ou utiliser ce référentiel, suivez les étapes ci-dessous :

1. Ouvrir le dossier dans un terminal

2. Créer un environnement virtuel nommé env:
```bash
python -m venv env
``` 

3. Activer l'environnement virtuel
```bash
env\Scripts\activate
```

4. Installer Django et les dépendances du projet:
```bash
pip install -r requirements.txt
```
 
5. Demarrer le serveur d'application django:
```bash
python manage.py runserver
```
 
6. Accéder à la documentation de l'API:
[http://localhost:8000/docs/](http://localhost:8000/docs/)
