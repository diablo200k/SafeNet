import socket
import threading
import tkinter as tk
from tkinter import messagebox, Scrollbar, Frame
import sqlite3
from PIL import Image, ImageTk
from ttkthemes import ThemedTk
from tkinter import ttk  # Importer ttk pour Treeview

# Connexion à la base de données SQLite
def init_db():
    conn = sqlite3.connect('children.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS children (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Enregistrer le nom et l'adresse IP de l'enfant dans la base de données
def save_child_info(name, address):
    conn = sqlite3.connect('children.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO children (name, address) VALUES (?, ?)', (name, address))
    conn.commit()
    conn.close()

# Vérifier si l'enfant est déjà enregistré
def is_child_registered(child_name):
    conn = sqlite3.connect('children.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM children WHERE name = ?', (child_name,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Récupérer les enfants enregistrés dans la base de données
def fetch_children():
    conn = sqlite3.connect('children.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, address FROM children')
    children = cursor.fetchall()
    conn.close()
    return children

# Initialiser les icônes
online_icon = None
offline_icon = None

def load_icons():
    global online_icon, offline_icon
    online_icon = ImageTk.PhotoImage(Image.open("online.png").resize((20, 20)))
    offline_icon = ImageTk.PhotoImage(Image.open("offline.png").resize((20, 20)))

def handle_client(client_socket, addr):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            # Décoder les données reçues
            message = data.decode('utf-8')
            # Extraire le nom de l'enfant et l'adresse IP
            child_name, child_address = message.split('|')

            if is_child_registered(child_name):
                # Si l'enfant est déjà enregistré, envoyer un message d'erreur au client
                client_socket.sendall("L'enfant est déjà enregistré.".encode('utf-8'))
            else:
                save_child_info(child_name, child_address)
                app_output.insert("", "end", values=(child_name, child_address), tags=("offline",))
                update_child_status(child_name, True)
        except Exception as e:
            print(f"Erreur: {e}")
            break

    client_socket.close()

# Mettre à jour le statut de l'enfant (en ligne ou hors ligne)
def update_child_status(child_name, is_online):
    for item in app_output.get_children():
        if app_output.item(item, "values")[0] == child_name:
            # Mettre à jour l'icône en fonction de l'état
            if is_online:
                app_output.item(item, image=online_icon)
                app_output.item(item, tags=("online",))
            else:
                app_output.item(item, image=offline_icon)
                app_output.item(item, tags=("offline",))
            break

def on_child_select(event):
    selected_item = app_output.selection()
    if selected_item:
        child_name = app_output.item(selected_item[0], "values")[0]
        messagebox.showinfo("Actions", f"Actions pour {child_name}")

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9999))
    server_socket.listen(5)
    print("Serveur démarré, en attente de connexions...")
    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connexion de {addr}")
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

# Interface utilisateur Tkinter
app = ThemedTk(theme="arc")  # Appliquer un thème
app.title("Contrôle Parental")
app.geometry("600x400")

# Charger les icônes
load_icons()

# Initialiser la base de données
init_db()

# Cadre principal
main_frame = Frame(app)
main_frame.pack(pady=20)

# Configurer Treeview pour afficher les enfants
app_output = ttk.Treeview(main_frame, columns=("Nom", "Adresse"), show="headings", height=15)
app_output.heading("Nom", text="Nom")
app_output.heading("Adresse", text="Adresse")

# Ajouter barre de défilement
scrollbar = Scrollbar(main_frame, orient="vertical", command=app_output.yview)
app_output.config(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
app_output.pack(side="left", fill="both")

# Lier l'événement de sélection
app_output.bind('<<TreeviewSelect>>', on_child_select)

# Récupérer et afficher les enfants déjà enregistrés
children = fetch_children()
for child in children:
    # Supposons que tous les enfants sont hors ligne au départ
    app_output.insert("", "end", values=(child[0], child[1]), tags=("offline",))

# Démarrer le serveur dans un thread séparé
threading.Thread(target=start_server, daemon=True).start()

app.mainloop()
