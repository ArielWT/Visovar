import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os

def obtener_csv_mas_reciente(carpeta):
    archivos = [
        os.path.join(carpeta, f)
        for f in os.listdir(carpeta)
        if f.lower().endswith('.csv')
    ]
    return max(archivos, key=os.path.getmtime) if archivos else None

initial_dir = os.path.normpath(r"C:\Users\Ariel\Desktop\Inacap\Práctica Profesional\DATA REGISTER _MC316\Datos_csv")

class CSVViewerApp:
    def __init__(self, master):
        self.master = master
        master.title("Visualizador de Variables")

        bg_color = "#C0C0C0"  # Plateado
        button_color = "#4F4F4F"  # Gris oscuro
        button_text = "white"

        master.configure(bg=bg_color)

        # Estilo tabla
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="white",
                        font=('Arial', 10))
        style.map("Treeview", background=[("selected", "#6A9FB5")])
        style.configure("Treeview.Heading",
                        font=('Arial', 10, 'bold'),
                        background="#A9A9A9",
                        foreground="black")

        self.frame = tk.Frame(master, bg=bg_color)
        self.frame.pack(padx=10, pady=10, fill='both', expand=True)

        self.label = tk.Label(self.frame, text="Visualizador del archivo CSV más reciente",
                              font=('Arial', 12, 'bold'), bg=bg_color)
        self.label.pack(pady=5)

        # Botones
        button_frame = tk.Frame(self.frame, bg=bg_color)
        button_frame.pack(pady=5)

        self.load_button = tk.Button(button_frame, text="Cargar otro archivo CSV", command=self.load_csv,
                                     bg=button_color, fg=button_text, font=('Arial', 10, 'bold'), relief="raised")
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.refresh_button = tk.Button(button_frame, text="Actualizar Archivo", command=self.load_most_recent_csv,
                                        bg=button_color, fg=button_text, font=('Arial', 10, 'bold'), relief="raised")
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        # Tabla con scroll
        self.tree = ttk.Treeview(self.frame, show='headings')
        self.tree.pack(padx=10, pady=10, fill='both', expand=True)

        self.scroll_x = ttk.Scrollbar(self.frame, orient='horizontal', command=self.tree.xview)
        self.scroll_x.pack(fill='x')
        self.tree.configure(xscrollcommand=self.scroll_x.set)

        self.scroll_y = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        self.scroll_y.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=self.scroll_y.set)

        self.df = None
        self.load_most_recent_csv()

    def load_csv(self, filepath=None):
        if filepath is None:
            filepath = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("CSV files", "*.csv")])
        if filepath:
            self._load_and_display(filepath)

    def load_most_recent_csv(self):
        ruta_csv = obtener_csv_mas_reciente(initial_dir)
        if ruta_csv:
            self._load_and_display(ruta_csv)
        else:
            messagebox.showwarning("Advertencia", f"No se encontró ningún archivo CSV en:\n{initial_dir}")

    def _load_and_display(self, filepath):
        try:
            self.df = pd.read_csv(filepath, encoding='utf-8', sep=None, engine='python')

            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.tree["columns"] = list(self.df.columns)

            for col in self.df.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120, anchor='center')

            for index, row in self.df.iterrows():
                self.tree.insert("", "end", values=list(row))

            messagebox.showinfo("Éxito", f"Archivo cargado correctamente:\n{os.path.basename(filepath)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    app = CSVViewerApp(root)
    root.mainloop()
