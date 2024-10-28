from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
from config.db_config import get_collection, test_connection
from bson import ObjectId
import logging

app = Flask(__name__)

# Configuration du logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route('/')
def dashboard():
    try:
        if not test_connection():
            logger.error("Échec de la connexion à la base de données")
            return "Erreur de connexion à la base de données", 500

        devices_collection = get_collection('devices')
        if devices_collection is None:
            logger.error("Impossible d'obtenir la collection 'devices'")
            return "Erreur d'accès à la collection 'devices'", 500
        
        devices = list(devices_collection.find())
        activities = get_activities_summary()
        
        alerts_collection = get_collection('alerts')
        if alerts_collection is None:
            logger.error("Impossible d'obtenir la collection 'alerts'")
            return "Erreur d'accès à la collection 'alerts'", 500
        
        alerts = list(alerts_collection.find().sort('time', -1).limit(5))
        
        # Convertir ObjectId en str pour la sérialisation JSON
        for device in devices:
            device['_id'] = str(device['_id'])
        for alert in alerts:
            alert['_id'] = str(alert['_id'])
            alert['time'] = alert['time'].strftime("%Y-%m-%d %H:%M:%S") if isinstance(alert['time'], datetime) else alert['time']

        logger.debug(f"Nombre d'appareils trouvés : {len(devices)}")
        logger.debug(f"Nombre d'alertes trouvées : {len(alerts)}")

        return render_template('dashboard.html', devices=devices, activities=activities, alerts=alerts)
    except Exception as e:
        logger.error(f"Erreur dans la route dashboard : {e}")
        return "Une erreur s'est produite", 500

@app.route('/api/devices')
def get_devices():
    try:
        devices_collection = get_collection('devices')
        if devices_collection is None:
            logger.error("Impossible d'obtenir la collection 'devices'")
            return jsonify({"error": "Erreur de connexion à la base de données"}), 500
        
        devices = list(devices_collection.find())
        for device in devices:
            device['_id'] = str(device['_id'])
        return jsonify(devices)
    except Exception as e:
        logger.error(f"Erreur dans la route get_devices : {e}")
        return jsonify({"error": "Une erreur s'est produite"}), 500

@app.route('/api/activities')
def get_activities():
    return jsonify(get_activities_summary())

@app.route('/api/alerts')
def get_alerts():
    try:
        alerts_collection = get_collection('alerts')
        if alerts_collection is None:
            logger.error("Impossible d'obtenir la collection 'alerts'")
            return jsonify({"error": "Erreur de connexion à la base de données"}), 500
        
        alerts = list(alerts_collection.find().sort('time', -1).limit(5))
        for alert in alerts:
            alert['_id'] = str(alert['_id'])
            alert['time'] = alert['time'].strftime("%Y-%m-%d %H:%M:%S") if isinstance(alert['time'], datetime) else alert['time']
        return jsonify(alerts)
    except Exception as e:
        logger.error(f"Erreur dans la route get_alerts : {e}")
        return jsonify({"error": "Une erreur s'est produite"}), 500

@app.route('/api/block_device/<device_id>')
def block_device(device_id):
    try:
        devices_collection = get_collection('devices')
        if devices_collection is None:
            logger.error("Impossible d'obtenir la collection 'devices'")
            return jsonify({"error": "Erreur de connexion à la base de données"}), 500
        
        result = devices_collection.update_one(
            {"_id": ObjectId(device_id)},
            {"$set": {"status": "blocked"}}
        )
        if result.modified_count > 0:
            return jsonify({"success": True, "message": f"Device {device_id} blocked successfully"})
        else:
            return jsonify({"success": False, "message": "Device not found or already blocked"})
    except Exception as e:
        logger.error(f"Erreur dans la route block_device : {e}")
        return jsonify({"error": "Une erreur s'est produite"}), 500

def get_activities_summary():
    # Cette fonction devrait agréger les données d'activité de tous les appareils
    # Pour cet exemple, nous utilisons des données statiques
    return {
        "Social Media": 30,
        "Gaming": 25,
        "Education": 20,
        "Entertainment": 15,
        "Other": 10
    }

if __name__ == '__main__':
    app.run(debug=True)