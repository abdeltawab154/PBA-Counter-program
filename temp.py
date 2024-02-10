import mysql.connector
import tkinter as tk
from tkinter import ttk
import configparser

# Read the configuration file
config = configparser.ConfigParser()
config.read('config.ini')

# Database credentials
db_config = {
  'user': config.get('mysql', 'user'),
  'password': config.get('mysql', 'password'),
  'host': config.get('mysql', 'host'),
  'database': config.get('mysql', 'database'),
  'raise_on_warnings': config.getboolean('mysql', 'raise_on_warnings')
}

# Table name
table_name = config.get('table', 'name')

# Column names
ip_column = config.get('column', 'ip')
serial_column = config.get('column', 'serial')
id_column = config.get('column', 'id')

def update_count():
    # Connect to the MySQL database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Execute a query to get all unique IPs
    cursor.execute(f"SELECT DISTINCT {ip_column} FROM {table_name}")
    ips = cursor.fetchall()

    # Clear the frame
    for widget in frame.winfo_children():
        widget.destroy()

    for ip in ips:
        # Execute queries to get count and serial of last ID for each IP
        cursor.execute(f"SELECT COUNT({serial_column}) FROM {table_name} WHERE {ip_column}='{ip[0]}'")
        count = cursor.fetchone()[0]

        cursor.execute(f"SELECT {serial_column} FROM {table_name} WHERE {ip_column}='{ip[0]}' ORDER BY {id_column} DESC LIMIT 1")
        last_id_serial = cursor.fetchone()[0]

        # Create a frame for each IP
        ip_frame = tk.Frame(frame, bg='white', bd=5, relief="solid")
        ip_frame.pack(pady=10, fill='x')

        # Create labels for each piece of information and pack them into the frame
        ip_label = ttk.Label(ip_frame, text=f"IP: {ip[0]}", style="BW.TLabel")
        ip_label.pack(pady=2, padx=10, fill='x')

        count_label = ttk.Label(ip_frame, text=f"Number of serials: {count}", style="BW.TLabel")
        count_label.pack(pady=2, padx=10, fill='x')

        last_id_serial_label = ttk.Label(ip_frame, text=f"Serial of last ID: {last_id_serial}", style="BW.TLabel")
        last_id_serial_label.pack(pady=2, padx=10, fill='x')

    # Close the connection
    conn.close()

    # Schedule the function to be called again after 10 seconds
    root.after(10000, update_count)

# Create a tkinter window
root = tk.Tk()
root.title("Serial Counter")  # Set the window title
root.geometry("400x300")  # Set the window size
root.configure(bg='light blue')

# Create a header label
header_label = tk.Label(root, text="SMD PBA Counter Tool", font=("Helvetica", 24), bg="light blue")
header_label.pack(pady=10)

# Create a frame
frame = tk.Frame(root, bg='white', bd=5, relief="solid")
frame.place(relx=0.5, rely=0.3, relwidth=0.75, relheight=0.6, anchor='n')

# Create a label with larger font and centered text
style = ttk.Style()
style.configure("BW.TLabel", foreground="black", background="light grey", font=("Helvetica", 16), padding=10, relief="solid")

# Call the function for the first time
update_count()

root.mainloop()
