import tkinter as tk
from tkinter import ttk, messagebox
from acl import users, files
from file_manager import read_file_for_gui, write_file_from_gui
from models import has_permission

class BibaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Biba")

        # Variables
        self.selected_user = tk.StringVar()
        self.selected_file = tk.StringVar()

        # Frame Usuario
        user_frame = ttk.LabelFrame(root, text="Seleccionar Usuario")
        user_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ttk.Label(user_frame, text="Usuario:").grid(row=0, column=0, padx=5, pady=5)
        user_combo = ttk.Combobox(user_frame, textvariable=self.selected_user, values=list(users.keys()), state="readonly")
        user_combo.grid(row=0, column=1, padx=5, pady=5)
        user_combo.bind("<<ComboboxSelected>>", self.reset_interface)

        self.user_info = ttk.Label(user_frame, text="Nivel: ")
        self.user_info.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Frame Archivo
        file_frame = ttk.LabelFrame(root, text="Seleccionar Archivo")
        file_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        ttk.Label(file_frame, text="Archivo:").grid(row=0, column=0, padx=5, pady=5)
        file_combo = ttk.Combobox(file_frame, textvariable=self.selected_file, values=list(files.keys()), state="readonly")
        file_combo.grid(row=0, column=1, padx=5, pady=5)
        file_combo.bind("<<ComboboxSelected>>", self.reset_interface)

        self.file_info = ttk.Label(file_frame, text="Nivel: ")
        self.file_info.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Botones
        button_frame = ttk.Frame(root)
        button_frame.grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(button_frame, text="Leer Archivo", command=self.read_file).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Escribir Archivo", command=self.write_file).grid(row=0, column=1, padx=5)

        # Área de texto (inicialmente oculta)
        self.text_area = tk.Text(root, height=15, width=60, state='disabled')
        self.text_area.grid(row=3, column=0, padx=10, pady=10)
        self.text_area.grid_remove()

        # Botón Guardar (inicialmente oculto)
        self.save_button = ttk.Button(root, text="Guardar Cambios", command=self.save_changes, state='disabled')
        self.save_button.grid(row=4, column=0, padx=10, pady=5)
        self.save_button.grid_remove()

    def reset_interface(self, event):
        self.text_area.grid_remove()
        self.text_area.config(state='disabled')
        self.text_area.delete('1.0', tk.END)
        self.save_button.grid_remove()
        self.save_button.config(state='disabled')
        user = self.selected_user.get()
        file = self.selected_file.get()
        if user:
            self.user_info.config(text=f"Nivel: {users[user]}")
        if file:
            self.file_info.config(text=f"Nivel: {files[file]}")

    def read_file(self):
        user = self.selected_user.get()
        file = self.selected_file.get()
        if not user or not file:
            messagebox.showerror("Error", "Seleccione usuario y archivo.")
            return
        
        if has_permission(user, file, "read"):
            content = read_file_for_gui(f'{file}', user)
            self.text_area.grid()
            self.text_area.config(state='normal')
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert(tk.END, content)
            self.text_area.config(state='disabled')
            messagebox.showinfo("Lectura", "Lectura exitosa.")
        else:
            messagebox.showerror("Acceso Denegado", "No tiene permiso para leer este archivo.")

    def write_file(self):
        user = self.selected_user.get()
        file = self.selected_file.get()
        if not user or not file:
            messagebox.showerror("Error", "Seleccione usuario y archivo.")
            return
        
        if has_permission(user, file, "write"):
            content = read_file_for_gui(f'{file}', user)
            self.text_area.grid()
            self.text_area.config(state='normal')
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert(tk.END, content)
            self.save_button.grid()
            self.save_button.config(state='normal')
            messagebox.showinfo("Escritura", "Puede editar y guardar cambios.")
        else:
            messagebox.showerror("Acceso Denegado", "No tiene permiso para escribir en este archivo.")

    def save_changes(self):
        user = self.selected_user.get()
        file = self.selected_file.get()
        new_content = self.text_area.get('1.0', tk.END).strip()
        result = write_file_from_gui(f'{file}', user, new_content)
        messagebox.showinfo("Guardado", result)
        self.text_area.config(state='disabled')
        self.save_button.grid_remove()
        self.save_button.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = BibaGUI(root)
    root.mainloop()