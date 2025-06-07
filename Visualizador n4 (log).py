import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ======= CONFIGURACIÓN DEL LOGIN ========
USUARIO_CORRECTO = "INFYCONTROL"
CLAVE_CORRECTA = "123"

# ======= RUTA DE BÚSQUEDA DEL CSV MÁS RECIENTE ========
def obtener_csv_mas_reciente(carpeta):
    archivos = [
        os.path.join(carpeta, f)
        for f in os.listdir(carpeta)
        if f.lower().endswith('.csv')
    ]
    return max(archivos, key=os.path.getmtime) if archivos else None

initial_dir = os.path.normpath(r"C:\Users\Ariel\Desktop\Inacap\Pr\u00e1ctica Profesional\DATA REGISTER _MC316\Datos_csv")

# ======= CLASE PRINCIPAL DE LA APP ========
class CSVViewerApp:
    def __init__(self, master):
        self.master = master
        master.title("Visualizador de Archivo CSV")

        bg_color = "#C0C0C0"
        button_color = "#4F4F4F"
        button_text = "white"
        master.configure(bg=bg_color)

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

        button_frame = tk.Frame(self.frame, bg=bg_color)
        button_frame.pack(pady=5)

        self.load_button = tk.Button(button_frame, text="Cargar otro archivo CSV", command=self.load_csv,
                                     bg=button_color, fg=button_text, font=('Arial', 10, 'bold'), relief="raised")
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.refresh_button = tk.Button(button_frame, text="Actualizar con CSV más reciente", command=self.load_most_recent_csv,
                                        bg=button_color, fg=button_text, font=('Arial', 10, 'bold'), relief="raised")
        self.refresh_button.pack(side=tk.LEFT, padx=5)

        self.graph_button = tk.Button(button_frame, text="Graficar columna AI1", command=self.graficar_ai1,
                                      bg=button_color, fg=button_text, font=('Arial', 10, 'bold'), relief="raised")
        self.graph_button.pack(side=tk.LEFT, padx=5)

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

            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = list(self.df.columns)

            for col in self.df.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120, anchor='center')

            for _, row in self.df.iterrows():
                self.tree.insert("", "end", values=list(row))

            messagebox.showinfo("Éxito", f"Archivo cargado correctamente:\n{os.path.basename(filepath)}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{e}")

    def graficar_ai1(self):
        archivos = [os.path.join(initial_dir, f) for f in os.listdir(initial_dir) if f.endswith(".csv")]
        if not archivos:
            messagebox.showwarning("Advertencia", "No se encontraron archivos CSV.")
            return

        data = []
        for archivo in sorted(archivos):
            try:
                with open(archivo, "r", encoding="utf-8") as file:
                    contenido = file.read().replace(".", ",")
                with open(archivo, "w", encoding="utf-8") as file:
                    file.write(contenido)

                df = pd.read_csv(archivo, sep=";", engine="python", decimal=",")
                if "A" in df.columns and "AI1" in df.columns:
                    for _, row in df.iterrows():
                        data.append((str(row["A"]), float(str(row["AI1"]).replace(",", ".")))
            except Exception as e:
                print(f"Error leyendo {archivo}: {e}")

        if not data:
            messagebox.showwarning("Advertencia", "No se encontraron datos en la columna AI1.")
            return

        data.sort()
        tiempos, valores = zip(*data)

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(tiempos, valores, marker='o', linestyle='-', color='blue')
        ax.set_title("Fluctuación de valores en la columna AI1")
        ax.set_xlabel("Tiempo (columna A)")
        ax.set_ylabel("AI1")
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True)

        grafico_window = tk.Toplevel(self.master)
        grafico_window.title("Gráfico Columna AI1")
        grafico_window.configure(bg="silver")

        canvas = FigureCanvasTkAgg(fig, master=grafico_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

# ======= VENTANA DE LOGIN ANTES DE LA PRINCIPAL ========
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio de Sesión")
        self.root.geometry("600x360")
        self.root.configure(bg="#D3D3D3")

        tk.Label(root, text="Usuario:", bg="#D3D3D3", font=('Arial', 10)).pack(pady=5)
        self.usuario_entry = tk.Entry(root)
        self.usuario_entry.pack()

        tk.Label(root, text="Contraseña:", bg="#D3D3D3", font=('Arial', 10)).pack(pady=5)
        self.clave_entry = tk.Entry(root, show="*")
        self.clave_entry.pack()

        self.login_button = tk.Button(root, text="Ingresar", command=self.verificar_login,
                                      bg="#4F4F4F", fg="white", font=('Arial', 10, 'bold'))
        self.login_button.pack(pady=15)

        self.root.bind('<Return>', lambda event: self.verificar_login())

    def verificar_login(self):
        usuario = self.usuario_entry.get()
        clave = self.clave_entry.get()

        if usuario == USUARIO_CORRECTO and clave == CLAVE_CORRECTA:
            self.root.destroy()
            main_app = tk.Tk()
            main_app.geometry("1000x600")
            CSVViewerApp(main_app)
            main_app.mainloop()
        else:
            messagebox.showerror("Acceso Denegado", "Usuario o contraseña incorrectos.")

# ======= INICIO DE LA APLICACIÓN CON LOGIN ========
if __name__ == "__main__":
    login_root = tk.Tk()
    LoginWindow(login_root)
    login_root.mainloop()
    