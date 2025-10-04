# pdf_model.py
from pypdf import PdfWriter
import os

class PDFModel:
    """
    Modelo (Model): Contiene los datos y la lógica de negocio.
    Gestiona la lista de archivos PDF y la funcionalidad de fusión (pypdf).
    """
    def __init__(self):
        # El ESTADO: lista interna que guarda las rutas completas de los archivos
        self.pdf_files = [] 

    # ----------------------------------------------------------------------
    # --- Lógica de Acceso a Datos ---
    
    def get_file_paths(self):
        """Devuelve la lista completa de rutas."""
        return self.pdf_files

    def get_file_names(self):
        """Devuelve solo los nombres base para mostrar en la Vista."""
        return [os.path.basename(f) for f in self.pdf_files]

    # ----------------------------------------------------------------------
    # --- Lógica de Manipulación de Lista (Métodos llamados por el Controlador) ---
    
    def add_files(self, new_files):
        """Añade una lista de nuevas rutas, evitando duplicados."""
        for file in new_files:
            if file and file not in self.pdf_files:
                self.pdf_files.append(file)

    def remove_file(self, index):
        """Elimina un archivo por su índice."""
        if 0 <= index < len(self.pdf_files):
            del self.pdf_files[index]
            return True
        return False

    def move_up(self, index):
        """
        Mueve el archivo en 'index' una posición hacia arriba.
        Resuelve el AttributeError: 'PDFModel' object has no attribute 'move_up'.
        """
        # Solo se puede subir si no es el primer elemento
        if index > 0 and index < len(self.pdf_files):
            # Intercambia la posición con el elemento anterior
            self.pdf_files.insert(index - 1, self.pdf_files.pop(index))
            return True
        return False

    def move_down(self, index):
        """
        Mueve el archivo en 'index' una posición hacia abajo.
        Resuelve el AttributeError: 'PDFModel' object has no attribute 'move_down'.
        """
        # Solo se puede bajar si no es el último elemento
        if 0 <= index < len(self.pdf_files) - 1:
            # Intercambia la posición con el elemento siguiente
            self.pdf_files.insert(index + 1, self.pdf_files.pop(index))
            return True
        return False
        
    # ----------------------------------------------------------------------
    # --- Lógica de Fusión (Núcleo del negocio) ---
    
    def merge_pdfs(self, output_path):
        """Ejecuta la fusión de los PDFs en el orden actual de la lista."""
        if len(self.pdf_files) < 2:
            # Lanza una excepción que será atrapada y mostrada por el Controlador
            raise ValueError("Se necesitan al menos dos archivos para la fusión.")

        merger = PdfWriter()
        
        try:
            # 1. Agrega los archivos en el orden definido por el usuario
            for file_path in self.pdf_files:
                merger.append(file_path)
            
            # 2. Escribe y guarda el archivo final
            with open(output_path, "wb") as f:
                merger.write(f)
            
            merger.close()
            
            # 3. Limpiar el modelo después de una fusión exitosa
            self.pdf_files = []
            
        except Exception as e:
            # Propaga el error para que el Controlador informe a la Vista
            merger.close()
            raise Exception(f"Error en la escritura/fusión: {e}")