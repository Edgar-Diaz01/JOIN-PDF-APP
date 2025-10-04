# main_app.py

import tkinter as tk
# Importamos las clases de los otros archivos
# Asegúrate de que estos archivos (pdf_model.py y pdf_view.py) existan en la misma carpeta
from pdf_model import PDFModel
from pdf_view import PDFView 

class PDFController:
    """
    Actúa como intermediario entre la Vista (GUI) y el Modelo (Lógica de Negocio).
    Maneja los eventos de la GUI y actualiza el Modelo y la Vista.
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view # Esta referencia se asigna completamente en el bloque __main__

    # --- Manejadores de Eventos (Responden a los clics de la Vista) ---
    
    def handle_add_files(self):
        """Maneja el clic en el botón 'Añadir PDFs'."""
        # 1. Pide a la Vista la interacción con el usuario (diálogo)
        # Esto resuelve el AttributeError si el método está bien definido en PDFView
        files = self.view.get_open_files_dialog() 
        
        if files:
            # 2. Notifica al Modelo para actualizar los datos
            self.model.add_files(files)
            
            # 3. Le pide a la Vista que se actualice con los nuevos datos del Modelo
            self.view.redraw_listbox(self.model.get_file_names())

    def handle_remove_file(self):
        """Maneja el clic en el botón 'Quitar Seleccionado'."""
        index = self.view.get_selected_index()
        if index != -1:
            # 1. Notifica al Modelo
            self.model.remove_file(index)
            
            # 2. Le pide a la Vista que se actualice
            self.view.redraw_listbox(self.model.get_file_names())

    def handle_move_up(self):
        """Maneja el clic en el botón '↑ Subir'."""
        index = self.view.get_selected_index()
        if index > 0:
            # 1. Notifica al Modelo
            success = self.model.move_up(index)
            
            # 2. Actualiza la Vista
            if success:
                new_index = index - 1
                self.view.redraw_listbox(self.model.get_file_names(), new_index)

    def handle_move_down(self):
        """Maneja el clic en el botón '↓ Bajar'."""
        index = self.view.get_selected_index()
        
        # Necesitamos la longitud actual para saber si puede bajar
        if index != -1 and index < len(self.model.pdf_files) - 1:
            # 1. Notifica al Modelo
            success = self.model.move_down(index)
            
            # 2. Actualiza la Vista
            if success:
                new_index = index + 1
                self.view.redraw_listbox(self.model.get_file_names(), new_index)

    def handle_merge(self):
        """Maneja el clic en el botón 'Unir y guardar PDF'."""
        if len(self.model.pdf_files) < 2:
            self.view.show_warning("Advertencia", "Necesitas al menos dos archivos PDF en la lista.")
            return

        # 1. Pide a la Vista la ruta de guardado (I/O del usuario)
        output_path = self.view.get_save_file_dialog()
        if not output_path:
            return

        try:
            # 2. Llama a la lógica de negocio del Modelo
            self.model.merge_pdfs(output_path)
            
            # 3. Feedback y actualización de la Vista tras el éxito
            self.view.show_success("Éxito", f"PDF unido y guardado exitosamente en:\n{output_path}")
            self.view.redraw_listbox(self.model.get_file_names()) # La lista se limpia en el Modelo
            
        except ValueError as ve:
             # Manejo específico del error de validación (ej. menos de 2 archivos)
             self.view.show_warning("Advertencia", str(ve))
        except Exception as e:
            # 4. Manejo de error general (archivos corruptos, permisos, etc.)
            self.view.show_error("Error de Fusión", f"Ocurrió un error al unir los archivos: {e}")


# --------------------------------------------------------------------------------------
## --- Inicio de la Aplicación ---
# --------------------------------------------------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    
    # 1. Crear el Modelo (Datos y Lógica)
    model = PDFModel()
    
    # 2. Crear el Controlador (El pegamento). Inicialmente sin Vista.
    controller = PDFController(model, None) 
    
    # 3. Crear la Vista (La Interfaz). La Vista se conecta al Controlador.
    # ¡Asegúrate de que tu PDFView esté corregido para usar 'self' como padre!
    view = PDFView(root, controller)
    
    # 4. Asignar la Vista al Controlador para cerrar el ciclo de dependencias.
    controller.view = view 

    root.mainloop()