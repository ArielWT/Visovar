import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import numpy as np

def obtener_csv_mas_reciente(carpeta):
    archivos = [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.endswith('.csv')]
    if not archivos:
        return None
    return max(archivos, key=os.path.getmtime)

# Carpeta inicial
initial_dir = r"C:/Users/Ariel/Desktop/Inacap/Práctica Profesional/DATA REGISTER _MC316/Datos_csv"
ruta_csv = obtener_csv_mas_reciente(initial_dir)

class CSVViewerApp:
    def __init__(self, master):
        self.master = master
        master.title("Visualizador de CSV y Gráfico")

        self.frame = tk.Frame(master)
        self.frame.pack(padx=10, pady=10)

        self.label = tk.Label(self.frame, text="Selecciona un archivo CSV desde un servidor o carpeta local:")
        self.label.pack()

        self.load_button = tk.Button(self.frame, text="Cargar CSV", command=self.load_csv)
        self.load_button.pack(pady=5)

        self.text = tk.Text(self.frame, width=80, height=10)
        self.text.pack()

        self.row_label = tk.Label(self.frame, text="Selecciona filas (2 a 6):")
        self.row_label.pack()
        self.row_listbox = tk.Listbox(self.frame, selectmode=tk.MULTIPLE, exportselection=False)
        self.row_listbox.pack(pady=5)

        self.plot_button = tk.Button(self.frame, text="Graficar datos fijos (B/C, G/H, etc.)", command=self.plot_graph)
        self.plot_button.pack(pady=5)

        self.canvas_frame = tk.Frame(master)
        self.canvas_frame.pack()

        self.df = None

        if ruta_csv:
            self.load_csv(filepath=ruta_csv)

    def load_csv(self, filepath=None):
        if filepath is None:
            filepath = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("CSV files", "*.csv")])
        if filepath:
            try:
                self.df = pd.read_csv(filepath)
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, self.df.head().to_string())

                self.row_listbox.delete(0, tk.END)
                for i in range(1, 6):  # filas 2 a 6 (índices 1 a 5)
                    tiempo = self.df.iloc[i]["A"] if "A" in self.df.columns else f"Fila {i+1}"
                    self.row_listbox.insert(tk.END, f"Fila {i+1} - Tiempo: {tiempo}")

                messagebox.showinfo("Éxito", f"Archivo cargado correctamente:\n{os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")

    def plot_graph(self):
        if self.df is None:
            messagebox.showwarning("Advertencia", "Carga un archivo CSV primero.")
            return

        selected_row_indices = self.row_listbox.curselection()
        if not selected_row_indices:
            messagebox.showwarning("Advertencia", "Selecciona al menos una fila.")
            return

        # Pares de columnas (cuantitativo, etiqueta)
        column_pairs = [("B", "C"), ("G", "H"), ("I", "J"), ("K", "L"), ("M", "N"), ("O", "P")]

        fig, ax = plt.subplots(figsize=(10, 6))
        ancho_barra = 0.8 / len(selected_row_indices)  # ancho ajustado para filas seleccionadas

        for idx, row_idx in enumerate([i + 1 for i in selected_row_indices]):
            tiempo = self.df.iloc[row_idx]["A"] if "A" in self.df.columns else f"Fila {row_idx+1}"
            etiquetas = []
            valores = []

            for val_col, etq_col in column_pairs:
                if val_col in self.df.columns and etq_col in self.df.columns:
                    valor = self.df.iloc[row_idx][val_col]
                    etiqueta = self.df.iloc[row_idx][etq_col]
                    try:
                        valor = float(valor)
                        etiquetas.append(str(etiqueta))
                        valores.append(valor)
                    except:
                        continue  # Si no se puede convertir a float, se omite

            x = np.arange(len(etiquetas))
            offset = (idx - (len(selected_row_indices) - 1) / 2) * ancho_barra
            bars = ax.bar(x + offset, valores, width=ancho_barra, label=f"Fila {row_idx+1} - Tiempo: {tiempo}")

            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.2f}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=8)

        ax.set_xticks(np.arange(len(etiquetas)))
        ax.set_xticklabels(etiquetas, rotation=45, ha='right')
        ax.set_title("Gráfico por etiquetas y cuantitativos en filas seleccionadas")
        ax.set_xlabel("Etiquetas")
        ax.set_ylabel("Valores")
        ax.legend()
        ax.grid(True, axis='y')

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = CSVViewerApp(root)
    root.mainloop()
