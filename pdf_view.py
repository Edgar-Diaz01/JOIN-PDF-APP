# pdf_view.py

import tkinter as tk
from tkinter import filedialog, messagebox
import os

class PDFView(tk.Frame):
    """
    Vista (View): Responsable de la interfaz de usuario (Tkinter). 
    Se comunica exclusivamente con el Controlador.
    """
    def __init__(self, master, controller):
        super().__init__(master)
        self.master = master
        self.controller = controller
        
        master.title("Unir y Ordenar PDFs (MVC)")
        master.geometry("600x550")
        
        # IMPORTANTE: Eliminamos el self.pack() de aquí para controlarlo en create_widgets
        
        self.create_widgets()

    def create_widgets(self):
        # ----------------------------------------------------------------------
        # A. PIE DE PÁGINA / INFORMACIÓN (¡DEBE EMPAQUETARSE PRIMERO EN self.master!)
        # ----------------------------------------------------------------------
        __version__ = "1.0"
        __author__ = "Edgar Diaz"
        __date__ = "30 de Septiembre de 2025"

        info_text = f"Versión: {__version__} | Autor: {__author__} | Fecha: {__date__}"
        # Se empaqueta en self.master y usa tk.BOTTOM para forzar la posición
        info_label = tk.Label(self.master, text=info_text, fg="gray", font=('Arial', 8))
        info_label.pack(side=tk.BOTTOM, pady=5) 
        
        # ----------------------------------------------------------------------
        # B. EMPAQUETAR EL FRAME DE LA VISTA (Para que ocupe todo el espacio RESTANTE)
        # ----------------------------------------------------------------------
        # Este 'pack' se ejecuta justo DESPUÉS del pie de página para que no lo tape.
        self.pack(fill="both", expand=True, padx=10, pady=10) 
        
        # ----------------------------------------------------------------------
        # C. RESTO DE LOS WIDGETS (Hijos del Frame 'self')
        # ----------------------------------------------------------------------
        
        # Frame Principal de Lista y Controles (Contenedor superior)
        main_list_frame = tk.Frame(self) 
        main_list_frame.pack(pady=10, fill="both", expand=True, padx=10) 

        # 1.1. LISTBOX (Se coloca a la izquierda)
        self.listbox = tk.Listbox(main_list_frame, height=20, selectmode=tk.SINGLE)
        self.listbox.pack(side=tk.LEFT, fill="both", expand=True) 

        scrollbar = tk.Scrollbar(main_list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)

        # 1.2. FRAME DE BOTONES DE CONTROL (Se coloca a la derecha)
        control_frame = tk.Frame(main_list_frame)
        control_frame.pack(side=tk.RIGHT, padx=10)

        # Botones de control (llaman al Controlador)
        tk.Button(control_frame, text="Añadir PDFs", command=self.controller.handle_add_files, 
                  width=15, bg="#A9DFBF").pack(pady=5)
        
        tk.Button(control_frame, text="↑ Subir", command=self.controller.handle_move_up, 
                  width=15).pack(pady=5)
        tk.Button(control_frame, text="↓ Bajar", command=self.controller.handle_move_down, 
                  width=15).pack(pady=5)
        
        tk.Button(control_frame, text="Quitar Seleccionado", command=self.controller.handle_remove_file, 
                  width=15, bg="#F5B7B1").pack(pady=5)
        
        # 2. BOTÓN DE ACCIÓN FINAL (Colocado bajo el Frame principal)
        tk.Button(self, text="Unir y guardar PDF", command=self.controller.handle_merge, 
                  bg="#2ECC71", fg="white", font=('Arial', 12, 'bold'), width=40).pack(pady=30)


    # ----------------------------------------------------------------------
    # --- Métodos de Interacción (Para obtener datos de la GUI) ---

    def get_open_files_dialog(self):
        """Pide al usuario que seleccione archivos PDF."""
        return filedialog.askopenfilenames(
            title="Seleccionar archivos PDF para unir",
            filetypes=[("Archivos PDF", "*.pdf")]
        )

    def get_save_file_dialog(self):
        """Pide al usuario que elija dónde guardar."""
        return filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar archivo PDF unido como..."
        )

    def get_selected_index(self):
        """Devuelve el índice seleccionado en el Listbox, o -1 si no hay selección."""
        selected_indices = self.listbox.curselection()
        return selected_indices[0] if selected_indices else -1

    # ----------------------------------------------------------------------
    # --- Métodos de Actualización (Para que el Controlador refresque la GUI) ---

    def redraw_listbox(self, file_names, select_index=-1):
        """Borra y vuelve a cargar el Listbox con la lista de nombres del Modelo."""
        self.listbox.delete(0, tk.END)
        for name in file_names:
            self.listbox.insert(tk.END, name)
            
        if select_index != -1 and 0 <= select_index < self.listbox.size():
            self.listbox.select_clear(0, tk.END)
            self.listbox.select_set(select_index)
            self.listbox.activate(select_index)

    # --- Métodos de Feedback ---

    def show_warning(self, title, message):
        messagebox.showwarning(title, message)

    def show_success(self, title, message):
        messagebox.showinfo(title, message)

    def show_error(self, title, message):
        messagebox.showerror(title, message)