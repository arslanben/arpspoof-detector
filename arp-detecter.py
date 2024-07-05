import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess
import threading
import time
from datetime import datetime, timedelta

class ARPMonitor:
    def __init__(self, master):
        self.master = master
        master.title("Windows ARP Intrusion Detection Monitor")
        master.geometry("500x400")

        self.label = tk.Label(master, text="ARP Attack Detection (Windows)")
        self.label.pack()

        self.start_button = tk.Button(master, text="Start Monitoring", command=self.start_monitoring)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop Monitoring", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack()

        self.status_label = tk.Label(master, text="Status: Pending")
        self.status_label.pack()

        self.log_area = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=60, height=15, state='disabled')
        self.log_area.pack(padx=10, pady=10)

        self.is_running = False
        self.initial_arp_cache = {}
        self.arp_cache = {}
        self.last_alert_times = {}
        self.ongoing_attacks = set()

    def start_monitoring(self):
        self.is_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Monitoring")
        self.log("Monitoring initiated.")
        
        current_arp_table = self.get_windows_arp_table()
        self.arp_cache = current_arp_table.copy()
        
        if not self.initial_arp_cache:
            self.initial_arp_cache = current_arp_table.copy()
        
        self.check_arp_changes(current_arp_table)
        
        threading.Thread(target=self.monitor_thread, daemon=True).start()

    def stop_monitoring(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped")
        self.log("Monitoring stopped.")

    def monitor_thread(self):
        while self.is_running:
            try:
                current_arp_table = self.get_windows_arp_table()
                self.check_arp_changes(current_arp_table)
                time.sleep(5)
            except Exception as e:
                self.log(f"Error: {e}")
                time.sleep(5)

    def get_windows_arp_table(self):
        arp_table = {}
        try:
            output = subprocess.check_output(["arp", "-a"], universal_newlines=True)
            for line in output.split('\n'):
                if line.strip() and not line.startswith('Interface') and not line.startswith('Internet'):
                    parts = line.split()
                    if len(parts) >= 2:
                        ip, mac = parts[0], parts[1]
                        if mac != "ff-ff-ff-ff-ff-ff":
                            arp_table[ip] = mac.replace('-', ':')
        except subprocess.CalledProcessError as e:
            self.log(f"ARP table could not be retrieved: {e}")
        return arp_table

    def check_arp_changes(self, current_arp_table):
        attack_detected = False
        for ip, mac in current_arp_table.items():
            if ip in self.arp_cache:
                if self.arp_cache[ip] != mac:
                    self.potential_attack_detected(ip, self.arp_cache[ip], mac)
                    attack_detected = True
            else:
                self.log(f"New device detected: IP: {ip}, MAC: {mac}")
            self.arp_cache[ip] = mac

        for ip in list(self.arp_cache.keys()):
            if ip not in current_arp_table:
                self.log(f"Device removed: IP: {ip}, MAC: {self.arp_cache[ip]}")
                del self.arp_cache[ip]

        if not attack_detected:
            self.check_for_attack_end(current_arp_table)

    def check_for_attack_end(self, current_arp_table):
        if self.arp_cache == self.initial_arp_cache:
            self.log("ARP table returned to initial state. Attack ended.")
            self.ongoing_attacks.clear()

    def potential_attack_detected(self, ip, old_mac, new_mac):
        current_time = datetime.now()
        if ip not in self.last_alert_times or (current_time - self.last_alert_times[ip]) >= timedelta(seconds=7):
            message = f"Potential ARP attack detected!\nIP: {ip}\nOld MAC: {old_mac}\nNew MAC: {new_mac}"
            self.alert(message)
            self.log(message)
            self.last_alert_times[ip] = current_time
            self.ongoing_attacks.add(ip)
        
            threading.Thread(target=self.alert_repeater, args=(ip, old_mac, new_mac), daemon=True).start()

    def alert_repeater(self, ip, old_mac, new_mac):
        while ip in self.ongoing_attacks and self.is_running:
            time.sleep(7)
            if ip in self.ongoing_attacks and self.is_running:
                message = f"Potential ARP attack detected!\nIP: {ip}\nOld MAC: {old_mac}\nNew MAC: {new_mac}"
                self.alert(message)
                self.log(message)

    def alert(self, message):
        messagebox.showwarning("ARP Attack Detected", message)

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, log_message)
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = ARPMonitor(root)
    root.mainloop()
