import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import logging

# Configuration du logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Utilisez une variable d'environnement pour le mot de passe
DB_PASSWORD = os.environ.get('SAFENET_DB_PASSWORD', 'BFGCGSJXCytBx3Tw')

# L'URI de connexion
URI = f"mongodb+srv://mhsssan63:{DB_PASSWORD}@safenet.owxnd.mongodb.net/?retryWrites=true&w=majority&appName=safenet"

def get_database():
    try:
        # Créez un nouveau client et connectez-vous au serveur
        client = MongoClient(URI, server_api=ServerApi('1'))
        
        # Envoyez une commande ping pour confirmer une connexion réussie
        client.admin.command('ping')
        logger.info("Connexion à MongoDB réussie!")
        
        # Retournez la base de données
        return client.safenet
    except Exception as e:
        logger.error(f"Erreur de connexion à MongoDB: {e}")
        return None

# Fonction pour obtenir une collection spécifique
def get_collection(collection_name):
    try:
        db = get_database()
        if db:
            collection = db[collection_name]
            logger.debug(f"Collection obtenue avec succès: {collection_name}")
            return collection
        else:
            logger.error("La base de données n'a pas pu être obtenue")
    except Exception as e:
        logger.error(f"Erreur lors de l'accès à la collection {collection_name}: {e}")
    return None

# Fonction de test de connexion
def test_connection():
    db = get_database()
    if db:
        logger.info("Test de connexion réussi")
        return True
    else:
        logger.error("Test de connexion échoué")
        return False

# Exemple d'utilisation
if __name__ == "__main__":
    if test_connection():
        devices = get_collection('devices')
        if devices:
            document = {"name": "Test Device", "status": "online"}
            result = devices.insert_one(document)
            logger.info(f"Document inséré avec l'id: {result.inserted_id}")
        else:
            logger.error("Impossible d'accéder à la collection 'devices'")
    else:
        logger.error("Impossible de se connecter à la base de données")