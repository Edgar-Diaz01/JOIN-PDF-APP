import tkinter as tk
from tkinter import filedialog, messagebox
from pypdf import PdfWriter
import os

class PDFMergerApp:
    def __init__(self, master):
        self.master = master
        master.title("Unir y Ordenar PDFs")
        master.geometry("600x450")
        
        # Lista interna que guarda las rutas de los archivos seleccionados
        self.pdf_files = [] 
        
        # --- Configuración de la Interfaz ---
        # Define las variables
        __version__ = "1.0"
        __author__ = "Edgar Diaz"
        __date__ = "30 de Septiembre de 2025"

        # Crea la etiqueta de información y colócala en la parte inferior
        info_text = f"Versión: {__version__} | Autor: {__author__} | Fecha: {__date__}"
        info_label = tk.Label(master, text=info_text, fg="gray", font=('Arial', 8))
        info_label.pack(side=tk.BOTTOM, pady=5)

        # Este frame contendrá el Listbox a la izquierda y los botones de orden a la derecha.
        main_list_frame = tk.Frame(master)
        main_list_frame.pack(pady=10, fill="x", padx=20)

        # 1. LISTBOX (Se coloca a la izquierda del main_list_frame)
        self.listbox = tk.Listbox(main_list_frame, height=20, selectmode=tk.SINGLE)
        self.listbox.pack(side=tk.LEFT, fill="both", expand=True)

        scrollbar = tk.Scrollbar(main_list_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill="y") # El scrollbar se pega al Listbox
        self.listbox.config(yscrollcommand=scrollbar.set)

        # 2. FRAME DE BOTONES DE CONTROL (Se coloca a la derecha del main_list_frame)
        control_frame = tk.Frame(main_list_frame)
        control_frame.pack(side=tk.RIGHT, padx=10) # <-- Nuevo: side=tk.RIGHT

        # Botón para Añadir
        tk.Button(control_frame, text="Añadir PDFs", command=self.add_files, width=15, bg="#A9DFBF").pack(pady=5)
        
        # Botones de Orden (Subir/Bajar)
        tk.Button(control_frame, text="↑ Subir", command=self.move_up, width=15).pack(pady=5)
        tk.Button(control_frame, text="↓ Bajar", command=self.move_down, width=15).pack(pady=5)
       
        # Botón para Quitar
        tk.Button(control_frame, text="Quitar Seleccionado", command=self.remove_file, width=15, bg="#F5B7B1").pack(pady=5)
        

        # 3. Botón de Acción Final (Queda en la parte inferior, fuera del frame anterior)
        tk.Button(master, text="Unir y guardar PDF", command=self.merge_pdfs, 
          bg="#2ECC71", fg="white", font=('Arial', 12, 'bold'), width=40).pack(pady=20)
        

    # --- Funciones de la GUI (Tkinter) ---

    def add_files(self):
        """Permite al usuario seleccionar uno o varios archivos PDF."""
        files = filedialog.askopenfilenames(
            title="Seleccionar archivos PDF para unir",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        for file in files:
            if file not in self.pdf_files:
                self.pdf_files.append(file)
                # Muestra solo el nombre del archivo en el Listbox
                self.listbox.insert(tk.END, os.path.basename(file))
                
    def remove_file(self):
        """Elimina el archivo seleccionado del Listbox y de la lista interna."""
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            return
        
        index = selected_indices[0]
        self.listbox.delete(index)
        del self.pdf_files[index]

    def move_up(self):
        """Mueve el archivo seleccionado una posición hacia arriba, reordenando la fusión."""
        try:
            selected = self.listbox.curselection()[0]
            if selected > 0:
                # Reordena en la lista interna (self.pdf_files)
                self.pdf_files.insert(selected - 1, self.pdf_files.pop(selected))
                
                # Reordena en la interfaz (self.listbox)
                text = self.listbox.get(selected)
                self.listbox.delete(selected)
                self.listbox.insert(selected - 1, text)
                self.listbox.select_clear(0, tk.END)
                self.listbox.select_set(selected - 1)
        except IndexError:
            pass # No hay nada seleccionado

    def move_down(self):
        """Mueve el archivo seleccionado una posición hacia abajo, reordenando la fusión."""
        try:
            selected = self.listbox.curselection()[0]
            if selected < self.listbox.size() - 1:
                # Reordena en la lista interna (self.pdf_files)
                self.pdf_files.insert(selected + 1, self.pdf_files.pop(selected))

                # Reordena en la interfaz (self.listbox)
                text = self.listbox.get(selected)
                self.listbox.delete(selected)
                self.listbox.insert(selected + 1, text)
                self.listbox.select_clear(0, tk.END)
                self.listbox.select_set(selected + 1)
        except IndexError:
            pass # No hay nada seleccionado

    # --- Función de Fusión (pypdf) ---

    def merge_pdfs(self):
        """Ejecuta la fusión de los PDFs en el orden actual de la lista."""
        if len(self.pdf_files) < 2:
            messagebox.showwarning("Advertencia", "Necesitas al menos dos archivos PDF en la lista.")
            return

        # 1. Preguntar dónde guardar el archivo final
        output_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar archivo PDF unido como..."
        )

        if not output_path:
            return  # El usuario canceló la acción de guardar

        merger = PdfWriter()
        
        try:
            # 2. Iterar sobre la lista de archivos EN EL ORDEN DEFINIDO POR EL USUARIO
            for file_path in self.pdf_files:
                merger.append(file_path)
            
            # 3. Escribir y guardar el archivo final
            with open(output_path, "wb") as f:
                merger.write(f)
            
            merger.close()
            messagebox.showinfo("Éxito", f"PDF unido y guardado exitosamente.")
            
            # Opcional: Limpiar la lista después de la fusión exitosa
            self.pdf_files = []
            self.listbox.delete(0, tk.END)

        except Exception as e:
            # Manejo de error si hay problemas con la escritura o lectura
            messagebox.showerror("Error de Fusión", f"Ocurrió un error al unir los archivos: {e}")
        
# --- Inicio de la Aplicación ---
if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()