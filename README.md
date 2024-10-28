Description
SafeNet est une application de contrôle parental avancée permettant aux parents de surveiller et gérer l'utilisation des appareils numériques par leurs enfants. Cette solution robuste offre un ensemble d'outils puissants pour garantir la sécurité en ligne des enfants tout en encourageant une utilisation saine et équilibrée de la technologie.

Fonctionnalités principales
Surveillance en temps réel : Capture d'écran et accès caméra en direct.
Contrôle à distance : Gestion de l'appareil à distance pour un contrôle complet.
Filtrage de contenu intelligent : Blocage de contenus inappropriés en fonction de l'âge.
Gestion du temps d'écran : Limitation du temps d'utilisation des appareils.
Rapports d'activité : Suivi détaillé des activités en ligne.
Contrôle d'alimentation à distance : Possibilité d'éteindre ou redémarrer l'appareil.
Alertes personnalisables : Notifications en cas de contenu ou activité suspecte.
Interface utilisateur intuitive : Conception pensée pour une utilisation simple et rapide.
Sécurité renforcée : Chiffrement de bout en bout des communications.
Compatibilité : Fonctionne sous Windows.
Installation
Clonez ce dépôt :

bash
Copier le code
git clone https://github.com/diablo200k/SafeNet.git
Installez les dépendances :

bash
Copier le code
pip install -r requirements.txt
Exécutez le script de configuration :

bash
Copier le code
python setup_autostart.py
Configuration
Assurez-vous que le fichier app.py est configuré correctement pour lancer l'application sur votre machine locale :

python
Copier le code
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
Personnalisez les paramètres dans config.ini pour répondre à vos besoins spécifiques en termes de filtrage et de notifications.

Utilisation
Après l'installation et la configuration, SafeNet démarrera automatiquement à chaque démarrage de Windows. Accédez à l'interface de contrôle en ouvrant votre navigateur web à l'adresse suivante : http://localhost:5000.

Contribution
Les contributions sont les bienvenues ! Pour participer au développement de SafeNet :

Forkez le projet.

Créez une nouvelle branche pour votre fonctionnalité :

bash
Copier le code
git checkout -b feature/AmazingFeature
Committez vos changements :

bash
Copier le code
git commit -m 'Add some AmazingFeature'
Poussez vers votre branche :

bash
Copier le code
git push origin feature/AmazingFeature
Ouvrez une Pull Request pour soumettre vos modifications.

Licence
Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus de détails.

Contact
Auteur : Diablo200k - @diablo200k
Lien du projet : https://github.com/diablo200k/SafeNet
Avertissement
SafeNet est conçu comme un outil de soutien pour la parentalité numérique. Il ne remplace pas la supervision parentale directe ni le dialogue avec les enfants sur l'utilisation responsable d'Internet et des appareils numériques.
