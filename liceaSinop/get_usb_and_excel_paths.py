from find_usb_path import getUSBPath
import tkinter as tk
import os, shutil
from pathlib import Path
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import shutil

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES # for drag and drop functionality
    HAS_DND = True
    BaseApp = TkinterDnD.Tk   
except ImportError:
    HAS_DND = False
    BaseApp = tk.Tk           # fallback without DnD

class App(BaseApp):          
    def __init__(self):
        super().__init__()
        self.title("Extractor de mapas")
        self.usb_path = None
        self.usb_label = "KINGSTON"
        self.excel_path = None


        ### Set geometry  --------------------------------------------------------------------------------------------------
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate 80% of the screen
        self.window_width = int(screen_width * 0.8)
        self.window_height = int(screen_height * 0.8)

        # Set window size and center it
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 4
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")


        ### Set style of Frames, Labels, and Buttons --------------------------------------------------------------------------
        style = ttk.Style(self)
        style.theme_use("clam")

        self.frameStyle = "Modern.TFrame"
        self.labelStyle = "Modern.TLabel"
        self.buttonStyle = "Modern.TButton"

        # Frame style
        style.configure(self.frameStyle, background="white")

        # Label style
        style.configure(self.labelStyle, background="white")

        # Button style
        style.configure(
            self.buttonStyle,
            background="white",
            foreground="black",
            borderwidth=1,
            focusthickness=3,
            focuscolor="none",
            font=("Helvetica", 11),
            padding=10
        )


        ### Create container, mainloop begins -------------------------------------------------------------------------------------
        
        self.container = ttk.Frame(self, style=self.frameStyle)
        self.container.pack(fill="both", expand=True)

        ttk.Label(self.container, text="Buscando USB \"KINGSTON\"...", font=("Helvetica", 14), style=self.labelStyle).pack(pady=((self.window_height//2.2),10))
        self.status = ttk.Label(self.container, text="", style=self.labelStyle)
        self.status.pack()

        self.after(1000, self.try_find_usb)

    def try_find_usb(self):
        path = getUSBPath("KINGSTON")
        if path:
            self.usb_path = path
            self.status.config(text=f"Encontrado.")
            self.after(1000, self.show_file_selector)
        else:
            self.status.config(text="No encontrado.")
            self.after(2000, self.ask_label)

    def ask_label(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        ttk.Label(self.container, text="Nombre del USB:", font=("Helvetica", 12), style=self.labelStyle).pack(pady=((self.window_height//2.5),5))
        entry = ttk.Entry(self.container)
        entry.pack(pady=5)
        ttk.Button(self.container, text="Buscar", command=lambda: self.search_label(entry.get()), style=self.buttonStyle).pack(pady=5)

    def search_label(self, label):
        path = getUSBPath(label)
        if path:
            self.usb_label = label
            self.usb_path = path
            self.show_file_selector()
        else:
            self.ask_path_manual()

    def ask_path_manual(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        ttk.Label(self.container, text="Ingresa la ruta del USB manualmente", style=self.labelStyle).pack(pady=((self.window_height//2.5),5))
        ttk.Button(self.container, text="Buscar", command=self.pick_folder, style=self.buttonStyle).pack(pady=5)

    def pick_folder(self):
        folder = filedialog.askdirectory(title="Selecciona el folder")
        if folder:
            self.usb_path = folder
            self.show_file_selector()

    def show_file_selector(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        drop_area = tk.Label(
                                self.container,
                                relief="ridge",
                                borderwidth=0,
                                pady=50, padx=50,
                                text="Arrastra .xlsx aquí" if HAS_DND else "Búsqueda manual",
                                justify="center",
                                background="#FAFAFA"  # base color
                            )
        drop_area.pack(fill="both", expand=True, pady=(30, 10), padx=50)
        ttk.Button(self.container, text="Busqueda manual", command=self.browse_excel, style=self.buttonStyle).pack(pady=10)

        if HAS_DND:
            drop_area.drop_target_register(DND_FILES)
            drop_area.dnd_bind("<<Drop>>", self.on_drop)


    def on_drop(self, event):
        file = event.data.strip().strip("{}")
        if file.lower().endswith(".xlsx"):
            self.finishFilePaths(file)
        else:
            messagebox.showerror("Documento no válido", "Por favor elige un documento .xlsx")

    def browse_excel(self):
        file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file:
            self.finishFilePaths(file)

    def finishFilePaths(self, file, df):
        self.excel_path = file
        for w in self.container.winfo_children():
            w.destroy()

        # Leemos excel y preguntamos por la sheet deseada en caso de haber mas de una
        try:
            # Get all sheet names first
            xls = pd.ExcelFile(self.excel_path)
            sheet_names = xls.sheet_names

            if len(sheet_names) == 1:
                # Only one sheet → load directly
                df = pd.read_excel(xls, sheet_name=sheet_names[0])
            else:
                # Multiple sheets → ask user which one to use
                sheet_list = "\n".join([f"{i+1}. {name}" for i, name in enumerate(sheet_names)])
                msg = f"El archivo contiene varias hojas:\n\n{sheet_list}\n\nIngresa el número de la hoja que deseas usar:"
                
                # Ask user for a number
                import tkinter.simpledialog as simpledialog
                choice = simpledialog.askinteger("Seleccionar hoja", msg, minvalue=1, maxvalue=len(sheet_names))
                if choice is None:  # user cancelled
                    return

                sheet_name = sheet_names[choice - 1]
                df = pd.read_excel(xls, sheet_name=sheet_name)

        except Exception as e:
            messagebox.showerror("Error leyendo Excel", f"No se pudo leer el Excel:\n{e}")
            return


        # Preguntamos por el nombre de la columna seccion:
        def on_focus_in(event, entry, prompt):
            if entry.get() == prompt:
                entry.delete(0, tk.END)
                entry.config(foreground="black")

        def on_focus_out(event, entry, prompt):
            if not entry.get():
                entry.insert(0, prompt)
                entry.config(foreground="gray")

        ttk.Label(self.container, text="Nombre de la columna sección:",
                font=("Helvetica", 14), style=self.labelStyle).pack(pady=((self.window_height//2.5), 10))

        # Sección
        entry1 = ttk.Entry(self.container)
        entry1.insert(0, "Ej: SECCION")
        entry1.config(foreground="gray")
        entry1.bind("<FocusIn>",  lambda e: on_focus_in(e, entry1, "Ej: SECCION"))
        entry1.bind("<FocusOut>", lambda e: on_focus_out(e, entry1, "Ej: SECCION"))
        entry1.pack(pady=5)

        # Estado (opcional)
        #entry2 = ttk.Entry(self.container)
        #entry2.insert(0, "Estado (opcional)")
        #entry2.config(foreground="gray")
        #entry2.bind("<FocusIn>",  lambda e: on_focus_in(e, entry2, "Estado (opcional)"))
        #entry2.bind("<FocusOut>", lambda e: on_focus_out(e, entry2, "Estado (opcional)"))
        #entry2.pack(pady=5)

        ttk.Button(self.container, text="Obtener mapas",
                command=lambda: self.pdf_search(entry1.get(), df),
                style=self.buttonStyle).pack(pady=5)

    def pdf_search(self, seccion: str, df: pd.DataFrame):
    # --- 1) Validate inputs and load Excel ---
        if not getattr(self, "excel_path", None) or not os.path.isfile(self.excel_path):
            messagebox.showerror("Falta archivo", "No se ha definido un Excel válido.")
            return
        if not getattr(self, "usb_path", None) or not os.path.isdir(self.usb_path):
            messagebox.showerror("Falta USB", "No se ha definido una ruta de USB válida.")
            return
    

        if seccion not in df.columns:
            messagebox.showerror("Columna no encontrada",
                                f"No existe la columna '{seccion}' en el Excel.")
            return

        # Tomar valores únicos 4 dígitos (como ints) de la columna
        svals = (
            pd.to_numeric(df[seccion], errors="coerce")
            .dropna()
            .astype(int)
            .map(lambda x: f"{x:04d}")
            .unique()
            .tolist()
        )
        if not svals:
            messagebox.showwarning("Sin valores", f"La columna '{seccion}' no contiene enteros válidos.")
            return

        # --- 2) Construir índice de PDFs por código (12-15) ---
        cartografia_dir = Path(self.usb_path) / "cartografia"
        if not cartografia_dir.exists():
            messagebox.showerror("Carpeta no encontrada",
                                f"No existe la carpeta 'cartografia' en:\n{self.usb_path}")
            return

        code_to_paths = {}
        pdf_count = 0
        for pdf in cartografia_dir.rglob("*.pdf"):
            name = pdf.name  # sólo el nombre de archivo
            if len(name) >= 16:  # necesitamos posiciones [12:16]
                code = name[12:16]
                if code.isdigit() and len(code) == 4:
                    code_to_paths.setdefault(code, []).append(pdf)
                    pdf_count += 1

        if pdf_count == 0:
            messagebox.showwarning("Sin PDFs", "No se encontraron PDFs en 'cartografia'.")
            return

        # --- 3) Elegir carpeta destino y crear export ---
        base_dest = filedialog.askdirectory(title="Elige la ubicación para guardar la carpeta exportada")
        if not base_dest:
            return  # usuario canceló

        export_dir = Path(base_dest) / "mapas"
        sin_mapa_dir = export_dir / "sin mapa"

        # If it already exists, remove it first
        if export_dir.exists():
            shutil.rmtree(export_dir)
        if sin_mapa_dir.exists():
            shutil.rmtree(sin_mapa_dir)

        # Then create it fresh
        export_dir.mkdir(parents=True, exist_ok=True)
        sin_mapa_dir.mkdir(exist_ok=True)

        # --- 4) Copiar coincidencias y registrar faltantes ---
        copied = 0
        unmatched = []

        def safe_copy(src_path: Path, dst_folder: Path):
            """Copia evitando sobrescritura; agrega sufijo en caso de colisión."""
            nonlocal copied
            dst = dst_folder / src_path.name
            if not dst.exists():
                shutil.copy2(src_path, dst)
                copied += 1
                return
            # Resolver colisión: nombre (1).pdf, (2)...
            stem, ext = src_path.stem, src_path.suffix
            i = 1
            while True:
                cand = dst_folder / f"{stem} ({i}){ext}"
                if not cand.exists():
                    shutil.copy2(src_path, cand)
                    copied += 1
                    return
                i += 1

        for code in sorted(svals):
            paths = code_to_paths.get(code, [])
            if not paths:
                unmatched.append(code)
                continue
            for p in paths:
                safe_copy(p, export_dir)

        # Escribir sin_mapa.txt
        if unmatched:
            try:
                (sin_mapa_dir / "sin_mapa.txt").write_text(
                    "\n".join(unmatched), encoding="utf-8"
                )
            except Exception as e:
                messagebox.showwarning("Aviso",
                                    f"No se pudo escribir 'sin_mapa.txt':\n{e}")

        # --- 5) Reporte final ---
        message = [
            f"PDFs escaneados: {pdf_count}",
            f"Secciones únicas en Excel: {len(svals)}",
            f"PDFs copiados: {copied}",
            f"Secciones sin mapa: {len(unmatched)}",
            f"\nCarpeta exportada:\n{export_dir}"
        ]
        messagebox.showinfo("Listo", "\n".join(message))

        # (Opcional) Abrir carpeta exportada en el explorador
        try:
            import subprocess, platform as _pf
            if _pf.system().lower().startswith("darwin"):
                subprocess.run(["open", str(export_dir)], check=False)
            elif _pf.system().lower().startswith("windows"):
                subprocess.run(["explorer", str(export_dir)], check=False)
        except Exception:
            pass

        self.container.destroy()   # close the current container/frame
        self.destroy()             # close the main window
        self.quit()                # stop the Tkinter event loop

if __name__ == "__main__":
    app = App()
    app.mainloop()
