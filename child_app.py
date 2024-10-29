import socket
import time
import psutil
import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox
from ttkthemes import ThemedTk

def get_parent_info():
    parent_ip = simpledialog.askstring("Adresse IP du Parent", "Entrez l'adresse IP du parent :")
    child_name = simpledialog.askstring("Nom de l'Enfant", "Entrez le nom de l'enfant :")

    if parent_ip and child_name:
        start_reporting(parent_ip, child_name)
    else:
        messagebox.showwarning("Informations manquantes", "Veuillez entrer l'adresse IP et le nom de l'enfant.")

def start_reporting(parent_ip, child_name):
    while True:
        # Établir la connexion avec le serveur parental
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                print(f"Tentative de connexion à {parent_ip} sur le port 9999...")
                client_socket.connect((parent_ip, 9999))
                message = f"{child_name}|{parent_ip}"  # Envoie le nom de l'enfant et l'IP
                client_socket.sendall(message.encode('utf-8'))
                print("Données envoyées avec succès.")
            except Exception as e:
                print(f"Erreur lors de l'envoi des données : {e}")
        time.sleep(10)  # Simuler le temps d'utilisation

if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # Appliquer un thème
    root.title("Application Enfant")
    root.geometry("300x200")
    get_parent_info()  # Demander les informations du parent
    root.mainloop()  # Lancer l'interface
