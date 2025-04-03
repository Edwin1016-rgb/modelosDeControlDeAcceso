import tkinter as tk
from tkinter import ttk, messagebox
from models import can_read, can_write
from acl import users, files

class BellLaPadulaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Bell-LaPadula")

        # Variables
        self.selected_user = tk.StringVar()
        self.selected_file = tk.StringVar()

        # Frame Usuario
        user_frame = ttk.LabelFrame(root, text="Seleccionar Usuario")
        user_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        ttk.Label(user_frame, text="Usuario:").grid(row=0, column=0, padx=5, pady=5)
        user_combo = ttk.Combobox(user_frame, textvariable=self.selected_user, values=list(users.keys()), state="readonly")
        user_combo.grid(row=0, column=1, padx=5, pady=5)
        user_combo.bind("<<ComboboxSelected>>", self.update_user_info)

        self.user_info = ttk.Label(user_frame, text="Nivel: ")
        self.user_info.grid(row=0, column=15, columnspan=2, padx=5, pady=5)
        self.user_info.config(font=("Arial", 10, "bold"))

        # Frame Archivo
        file_frame = ttk.LabelFrame(root, text="Seleccionar Archivo")
        file_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        ttk.Label(file_frame, text="Archivo:").grid(row=0, column=0, padx=5, pady=5)
        self.file_combo = ttk.Combobox(file_frame, textvariable=self.selected_file, state="readonly")
        self.file_combo.grid(row=0, column=1, padx=5, pady=5)
        self.file_combo.bind("<<ComboboxSelected>>", self.update_file_info)

        self.file_info = ttk.Label(file_frame, text="Nivel: ")
        self.file_info.grid(row=0, column=15, columnspan=2, padx=5, pady=5)
        self.file_info.config(font=("Arial", 10, "bold"))

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

    def update_user_info(self, event):
        user = self.selected_user.get()
        if user:
            self.user_info.config(text=f"Nivel: {users[user]}")
            
            # Filtrar archivos accesibles según el nivel de usuario
            user_level = users[user]
            accessible_files = [file for file, level in files.items() if level <= user_level]

            # Actualizar el Combobox de archivos
            self.file_combo["values"] = accessible_files
            self.selected_file.set("")  # Limpiar selección anterior

            # Ocultar y limpiar el área de texto
            self.text_area.config(state='normal')
            self.text_area.delete('1.0', tk.END)
            self.text_area.config(state='disabled')
            self.text_area.grid_remove()
            self.save_button.grid_remove()

    def update_file_info(self, event):
        file = self.selected_file.get()
        if file:
            self.file_info.config(text=f"Nivel: {files[file]}")

    def read_file(self):
        user = self.selected_user.get()
        file = self.selected_file.get()
        if not user or not file:
            messagebox.showerror("Error", "Seleccione usuario y archivo.")
            return
        
        if can_read(user, file):
            try:
                with open(f'blp/files/{file}', 'r') as f:
                    content = f.read()
                self.text_area.config(state='normal')
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert(tk.END, content)
                self.text_area.config(state='disabled')
                self.text_area.grid()
                self.save_button.grid_remove()
                messagebox.showinfo("Lectura", "Lectura exitosa.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
        else:
            messagebox.showerror("Acceso Denegado", "No tiene permiso para leer este archivo.")

    def write_file(self):
        user = self.selected_user.get()
        file = self.selected_file.get()
        if not user or not file:
            messagebox.showerror("Error", "Seleccione usuario y archivo.")
            return
        
        if can_write(user, file):
            try:
                with open(f'blp/files/{file}', 'r') as f:
                    content = f.read()
                self.text_area.config(state='normal')
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert(tk.END, content)
                self.text_area.grid()
                self.save_button.config(state='normal')
                self.save_button.grid()
                messagebox.showinfo("Escritura", "Puede editar y guardar cambios.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo: {e}")
        else:
            messagebox.showerror("Acceso Denegado", "No tiene permiso para escribir en este archivo.")

    def save_changes(self):
        file = self.selected_file.get()
        new_content = self.text_area.get('1.0', tk.END)
        try:
            with open(f'blp/files/{file}', 'w') as f:
                f.write(new_content.strip())
            messagebox.showinfo("Guardado", "Archivo guardado con éxito.")
            self.text_area.config(state='disabled')
            self.save_button.config(state='disabled')
            self.text_area.grid_remove()
            self.save_button.grid_remove()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BellLaPadulaGUI(root)
    root.mainloop()
