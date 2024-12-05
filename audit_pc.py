import psutil
import platform
import socket
import os
import subprocess
import wmi
import tkinter as tk
from tkinter import ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import time

def get_user_name():
    root = tk.Tk()
    root.title("Nom de l'utilisateur")
    
    label = tk.Label(root, text="Entrez votre nom:")
    label.pack(pady=10)
    
    entry = tk.Entry(root)
    entry.pack(pady=10)
    
    user_name = [None]
    
    def on_submit():
        user_name[0] = entry.get()
        root.quit()
    
    submit_button = tk.Button(root, text="Soumettre", command=on_submit)
    submit_button.pack(pady=10)
    
    root.mainloop()
    root.destroy()
    
    return user_name[0]

def collect_system_info(progress_var):
    system_info = {}
    total_steps = 15
    
    # Informations sur le système
    progress_var.set((1/total_steps) * 100)
    system_info["Nom de l'ordinateur"] = platform.node()
    system_info["Système d'exploitation"] = platform.system() + " " + platform.release()
    system_info["Architecture"] = platform.architecture()[0]
    system_info["Processeur"] = platform.processor()
    time.sleep(0.5)

    # Informations sur le disque dur
    progress_var.set((2/total_steps) * 100)
    try:
        cmd = "wmic diskdrive get serialnumber"
        serial_number = subprocess.check_output(cmd, shell=True).decode().strip().split("\n")[1]
        system_info["Numéro de série du disque dur"] = serial_number
    except Exception as e:
        system_info["Numéro de série du disque dur"] = "Non disponible"
    time.sleep(0.5)

    # Mémoire
    progress_var.set((3/total_steps) * 100)
    memory = psutil.virtual_memory()
    system_info["Mémoire totale"] = f"{memory.total / (1024**3):.2f} GB"
    system_info["Mémoire libre"] = f"{memory.available / (1024**3):.2f} GB"
    system_info["Utilisation mémoire"] = f"{memory.percent}%"
    time.sleep(0.5)

    # Disques
    progress_var.set((4/total_steps) * 100)
    try:
        disk = psutil.disk_usage('C:')
        system_info["Espace disque total"] = f"{disk.total / (1024**3):.2f} GB"
        system_info["Espace disque libre"] = f"{disk.free / (1024**3):.2f} GB"
        system_info["Utilisation disque"] = f"{disk.percent}%"
    except Exception as e:
        system_info["Espace disque"] = f"Erreur de lecture : {str(e)}"
    time.sleep(0.5)

    # Partitions de disque
    progress_var.set((5/total_steps) * 100)
    partitions = psutil.disk_partitions()
    partition_info = []
    for partition in partitions:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            partition_info.append(f"{partition.device}: {usage.percent}% utilisé")
        except Exception as e:
            partition_info.append(f"{partition.device}: Erreur de lecture")
    system_info["Partitions de disque"] = ", ".join(partition_info)
    time.sleep(0.5)

    # Applications installées
    progress_var.set((6/total_steps) * 100)
    try:
        installed_apps = subprocess.check_output("wmic product get name", shell=True).decode().split("\n")[1:]
        installed_apps = [app.strip() for app in installed_apps if app.strip()]
        system_info["Applications installées"] = ", ".join(installed_apps[:10])  # Limité à 10 pour la lisibilité
    except Exception as e:
        system_info["Applications installées"] = "Non récupérable"
    time.sleep(0.5)

    # Utilisateurs connectés
    progress_var.set((7/total_steps) * 100)
    users = psutil.users()
    system_info["Comptes connectés"] = ", ".join([user.name for user in users])
    time.sleep(0.5)

    # Etat de la batterie
    progress_var.set((8/total_steps) * 100)
    battery = psutil.sensors_battery()
    if battery:
        system_info["Etat de la batterie"] = f"{battery.percent}% - {'En charge' if battery.power_plugged else 'Sur batterie'}"
    else:
        system_info["Etat de la batterie"] = "Non disponible"
    time.sleep(0.5)

    # Réseau
    progress_var.set((9/total_steps) * 100)
    system_info["Nom de l'hôte"] = socket.gethostname()
    system_info["Adresse IP"] = socket.gethostbyname(socket.gethostname())
    net_if_addrs = psutil.net_if_addrs()
    network_info = []
    for interface, addrs in net_if_addrs.items():
        for addr in addrs:
            if addr.family == socket.AF_INET:
                network_info.append(f"{interface} - {addr.address}")
    system_info["Interfaces réseau"] = ", ".join(network_info)
    time.sleep(0.5)

    # Informations sur le BIOS
    progress_var.set((10/total_steps) * 100)
    w = wmi.WMI()
    bios = w.Win32_BIOS()[0]
    system_info["BIOS - Version"] = bios.Version
    system_info["BIOS - Fabricant"] = bios.Manufacturer
    system_info["BIOS - Date"] = bios.ReleaseDate
    time.sleep(0.5)

    # Température du processeur
    progress_var.set((11/total_steps) * 100)
    try:
        temperatures = psutil.sensors_temperatures()
        if temperatures and "coretemp" in temperatures:
            system_info["Température CPU"] = f"{temperatures['coretemp'][0].current}°C"
        else:
            system_info["Température CPU"] = "Non disponible"
    except Exception as e:
        system_info["Température CPU"] = "Non disponible"
    time.sleep(0.5)

    # Services en cours d'exécution
    progress_var.set((12/total_steps) * 100)
    services = [service.name() for service in psutil.win_service_iter()]
    system_info["Services actifs"] = ", ".join(services[:10])  # Limité à 10 pour la lisibilité
    time.sleep(0.5)

    # Processus actifs
    progress_var.set((13/total_steps) * 100)
    active_processes = [p.name() for p in psutil.process_iter(['name'])]
    system_info["Processus actifs"] = ", ".join(active_processes[:10])  # Limité à 10 pour la lisibilité
    time.sleep(0.5)

    # CPU - Charge par cœur
    progress_var.set((14/total_steps) * 100)
    cpu_percent = psutil.cpu_percent(percpu=True)
    system_info["Charge CPU par cœur"] = ", ".join([f"Cœur {i}: {percent}%" for i, percent in enumerate(cpu_percent)])
    time.sleep(0.5)

    # Bande passante réseau
    progress_var.set((15/total_steps) * 100)
    net_io = psutil.net_io_counters()
    system_info["Bande passante réseau (octets)"] = f"Reçu: {net_io.bytes_recv / 1024 / 1024:.2f} MB, Envoyé: {net_io.bytes_sent / 1024 / 1024:.2f} MB"
    time.sleep(0.5)

    return system_info

def create_pdf_report(system_info, user_name):
    pdf_filename = f"Rapport_Audit_{user_name}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Rapport d'audit système pour {user_name}")
    
    c.setFont("Helvetica", 12)
    y = height - 80
    for key, value in system_info.items():
        if y < 50:  # Nouvelle page si on atteint le bas
            c.showPage()
            y = height - 50
        c.drawString(50, y, f"{key}: {value}")
        y -= 20
    
    c.save()
    return pdf_filename

def run_audit():
    try:
        user_name = get_user_name()
        
        root = tk.Tk()
        root.title("Audit en cours")
        
        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
        progress_bar.pack(pady=20, padx=20, fill=tk.X)
        
        label = tk.Label(root, text="Collecte des informations système en cours...")
        label.pack(pady=10)
        
        root.update()
        
        system_info = collect_system_info(progress_var)
        
        pdf_filename = create_pdf_report(system_info, user_name)
        
        label.config(text=f"Audit terminé. Rapport sauvegardé : {pdf_filename}")
        root.mainloop()
    except Exception as e:
        print(f"Une erreur est survenue : {str(e)}")
        # Vous pouvez ajouter ici un message d'erreur dans une fenêtre si vous le souhaitez

if __name__ == "__main__":
    run_audit()
