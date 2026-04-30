from find_usb_path import getUSBPath
import tkinter as tk
import os, threading, subprocess, platform
from pathlib import Path
from tkinter import ttk, filedialog, messagebox, simpledialog
import pandas as pd
import shutil
import traceback

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES  # for drag and drop functionality
    HAS_DND = True
    BaseApp = TkinterDnD.Tk
except ImportError:
    HAS_DND = False
    BaseApp = tk.Tk  # fallback without DnD


class ProgressDialog(tk.Toplevel):
    def __init__(self, parent, title="Procesando..."):
        super().__init__(parent)
        self.title(title)
        self.transient(parent)
        self.resizable(False, False)
        self.grab_set()  # modal

        self.msg_var = tk.StringVar(value="Preparando...")
        style = ttk.Style(self)

        style.theme_use("clam")
        self.labelStyle = "Modern.TLabel"
        bg = self.cget("background")
        style.configure(self.labelStyle, background=bg)
        ttk.Label(self, textvariable=self.msg_var, style=self.labelStyle).pack(padx=16, pady=(12, 6))

        style.configure(
            "Modern.Horizontal.TProgressbar",
            troughcolor="#E8D6FF",
            background="#4F46E5",
            bordercolor="#F2F3F5",
            lightcolor="#4F46E5",
            darkcolor="#4F46E5"
        )

        self.bar = ttk.Progressbar(
            self, length=320, mode="indeterminate", maximum=100,
            style="Modern.Horizontal.TProgressbar"
        )
        self.bar.pack(padx=16, pady=(0, 12))

        self.update_idletasks()
        self._center_on_screen()

    def _center_on_screen(self):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w = self.winfo_reqwidth()
        h = self.winfo_reqheight()
        x = int((sw / 2) - (w / 2))
        y = int(((sh / 2) - (h / 2)) * 0.8)
        self.geometry(f"+{x}+{y}")


class App(BaseApp):
    def __init__(self):
        super().__init__()
        self.title("Buscador de mapas")
        self.usb_path = None
        self.usb_label = "KINGSTON"
        self.excel_path = None

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.window_width = int(screen_width * 0.5)
        self.window_height = int(screen_height * 0.5)

        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 4
        self.geometry(f"{self.window_width}x{self.window_height}+{x}+{y}")

        style = ttk.Style(self)
        style.theme_use("clam")

        self.frameStyle = "Modern.TFrame"
        self.labelStyle = "Modern.TLabel"
        self.buttonStyle = "Modern.TButton"

        style.configure(self.frameStyle, background="white")
        style.configure(self.labelStyle, background="white")
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

        self.container = ttk.Frame(self, style=self.frameStyle)
        self.container.pack(fill="both", expand=True)

        ttk.Label(
            self.container,
            text='Buscando USB "KINGSTON"...',
            font=("Helvetica", 14),
            style=self.labelStyle
        ).pack(pady=((self.window_height // 2.2), 10))
        self.status = ttk.Label(self.container, text="", style=self.labelStyle)
        self.status.pack()

        self.after(1000, self.try_find_usb)

    def try_find_usb(self):
        path = getUSBPath("KINGSTON")
        if path:
            self.usb_path = path
            self.status.config(text="Encontrado.")
            self.after(1000, self.show_file_selector)
        else:
            self.status.config(text="No encontrado.")
            self.after(2000, self.ask_label)

    def ask_label(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        ttk.Label(self.container, text="Nombre del USB:", font=("Helvetica", 12), style=self.labelStyle).pack(
            pady=((self.window_height // 2.5), 5)
        )
        entry = ttk.Entry(self.container)
        entry.pack(pady=5)
        ttk.Button(
            self.container, text="Buscar",
            command=lambda: self.search_label(entry.get()),
            style=self.buttonStyle
        ).pack(pady=5)

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
        ttk.Label(self.container, text="Ingresa la ruta del USB manualmente", style=self.labelStyle).pack(
            pady=((self.window_height // 2.5), 5)
        )
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
            background="#FAFAFA"
        )
        drop_area.pack(fill="both", expand=True, pady=(30, 10), padx=50)
        ttk.Button(self.container, text="Busqueda manual", command=self.browse_excel, style=self.buttonStyle).pack(pady=10)

        if HAS_DND:
            drop_area.drop_target_register(DND_FILES)
            drop_area.dnd_bind("<<Drop>>", self.on_drop)

    def on_drop(self, event):
        file = event.data.strip().strip("{}")
        if file.lower().endswith(".xlsx"):
            self.after(25, lambda f=file: self.finishFilePaths(f))
        else:
            messagebox.showerror("Documento no válido", "Por favor elige un documento .xlsx")

    def browse_excel(self):
        file = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file:
            self.finishFilePaths(file)

    def finishFilePaths(self, file):
        self.excel_path = file
        for w in self.container.winfo_children():
            w.destroy()

        try:
            xls = pd.ExcelFile(self.excel_path)
            sheet_names = xls.sheet_names

            if len(sheet_names) == 1:
                df = pd.read_excel(xls, sheet_name=sheet_names[0])
            else:
                sheet_list = "\n".join([f"{i+1}. {name}" for i, name in enumerate(sheet_names)])
                msg = (
                    f"El archivo contiene varias hojas:\n\n{sheet_list}\n\n"
                    "Ingresa el número de la hoja que deseas usar:"
                )
                choice = simpledialog.askinteger(
                    "Seleccionar hoja", msg, parent=self, minvalue=1, maxvalue=len(sheet_names)
                )
                if choice is None:
                    return
                sheet_name = sheet_names[choice - 1]
                df = pd.read_excel(xls, sheet_name=sheet_name)

        except Exception as e:
            messagebox.showerror("Error leyendo Excel", f"No se pudo leer el Excel:\n{e}")
            return

        cols = df.columns.tolist()
        col_list = "\n".join([f"{i+1}. {str(c).replace('\n', ' ').strip()}" for i, c in enumerate(cols)])

        msg = (
            f"El archivo contiene las siguientes columnas:\n\n{col_list}\n\n"
            "Ingresa el número de la columna que especifique la Sección:"
        )
        msg2 = (
            f"El archivo contiene las siguientes columnas:\n\n{col_list}\n\n"
            "Ingresa el número de la columna que especifique el Estado:"
        )

        choice = simpledialog.askinteger("Seleccionar columna", msg, parent=self, minvalue=1, maxvalue=len(cols))
        if choice is None:
            return

        choice2 = simpledialog.askinteger("Seleccionar columna", msg2, parent=self, minvalue=1, maxvalue=len(cols))
        if choice2 is None:
            return

        seccion_col = cols[choice - 1]
        estado_col = cols[choice2 - 1]

        self.pdf_search(seccion_col, estado_col, df)

    def pdf_search(self, seccion: str, estado: str, df: pd.DataFrame):
        if not getattr(self, "excel_path", None) or not os.path.isfile(self.excel_path):
            messagebox.showerror("Falta archivo", "No se ha definido un Excel válido.")
            return
        if not getattr(self, "usb_path", None) or not os.path.isdir(self.usb_path):
            messagebox.showerror("Falta USB", "No se ha definido una ruta de USB válida.")
            return

        if seccion not in df.columns:
            messagebox.showerror("Columna no encontrada", f"No existe la columna '{seccion}' en el Excel.")
            return
        if estado not in df.columns:
            messagebox.showerror("Columna no encontrada", f"No existe la columna '{estado}' en el Excel.")
            return

        secciones = (
            pd.to_numeric(df[seccion], errors="coerce")
            .dropna()
            .astype(int)
            .map(lambda x: f"{x:04d}")
            .tolist()
        )
        if not secciones:
            messagebox.showwarning("Sin valores", f"La columna '{seccion}' no contiene enteros válidos.")
            return

        estados = (
            pd.to_numeric(df[estado], errors="coerce")
            .dropna()
            .astype(int)
            .tolist()
        )
        if not estados:
            messagebox.showwarning("Sin valores", f"La columna '{estado}' no contiene enteros válidos.")
            return

        initial_dir = Path(self.excel_path).parent
        base_dest = filedialog.askdirectory(
            title="Elige la ubicación para guardar la carpeta exportada",
            initialdir=initial_dir
        )
        if not base_dest:
            return

        export_dir = Path(base_dest) / "mapas"
        sin_mapa_dir = export_dir / "sin mapa"

        if export_dir.exists():
            shutil.rmtree(export_dir)
        export_dir.mkdir(parents=True, exist_ok=True)

        if sin_mapa_dir.exists():
            shutil.rmtree(sin_mapa_dir)
        sin_mapa_dir.mkdir(parents=True, exist_ok=True)

        dlg = ProgressDialog(self, title="Buscando y copiando mapas...")

        def run_work():
            try:
                # Start indeterminate bar on UI thread
                self.after(0, lambda: dlg.bar.start(10))
                self.after(0, lambda: dlg.msg_var.set("Escaneando PDFs en 'cartografia'..."))

                cartografia_root = Path(self.usb_path) / "cartografia"
                if not cartografia_root.exists():
                    raise FileNotFoundError(f"No existe la carpeta 'cartografia' en:\n{self.usb_path}")

                edoSeccPathDic = {}  # {edoNum: {seccCode: [pdfPaths...]}}
                pdf_count_all = 0

                for edo in set(estados):
                    pattern = f"{edo}.*"
                    cartografia_dir = next(cartografia_root.glob(pattern), None)

                    if cartografia_dir is None or not cartografia_dir.exists():
                        raise FileNotFoundError(
                            f"No existe carpeta para el estado {edo} (patrón '{pattern}') en:\n{cartografia_root}"
                        )

                    code_to_paths = {}
                    pdf_count_state = 0

                    for pdf in cartografia_dir.rglob("*.pdf"):
                        name = pdf.name
                        if len(name) >= 16:
                            code = name[12:16]
                            if code.isdigit() and len(code) == 4:
                                code_to_paths.setdefault(code, []).append(pdf)
                                pdf_count_state += 1
                                pdf_count_all += 1

                        if pdf_count_all % 5000 == 0:
                            self.after(0, lambda c=pdf_count_all: dlg.msg_var.set(f"{c} PDFs escaneados..."))

                    if pdf_count_state == 0:
                        raise RuntimeError(f"No se encontraron PDFs para el estado {edo} en:\n{cartografia_dir}")

                    edoSeccPathDic[edo] = code_to_paths

                # Stop indeterminate and switch to determinate on UI thread
                self.after(0, lambda: dlg.bar.stop())
                self.after(0, lambda: (
                    setattr(dlg.bar, "mode", "determinate"),
                    dlg.bar.config(maximum=len(secciones), value=0),
                    dlg.msg_var.set("Copiando mapas de cada sección...")
                ))

                copied = 0
                unmatched = []
                progress_i = 0

                def safe_copy(src_path: Path, dst_folder: Path):
                    nonlocal copied
                    dst = dst_folder / src_path.name
                    if not dst.exists():
                        shutil.copy2(src_path, dst)
                        copied += 1
                        return
                    stem, ext = src_path.stem, src_path.suffix
                    i = 1
                    while True:
                        cand = dst_folder / f"{stem} ({i}){ext}"
                        if not cand.exists():
                            shutil.copy2(src_path, cand)
                            copied += 1
                            return
                        i += 1

                for edo, secc in zip(estados, secciones):
                    paths = edoSeccPathDic.get(edo, {}).get(secc, [])
                    if not paths:
                        unmatched.append(secc)
                    else:
                        for p in paths:
                            safe_copy(p, export_dir)

                    progress_i += 1
                    self.after(0, lambda i=progress_i: (
                        dlg.bar.config(value=i),
                        dlg.msg_var.set(f"{i}/{len(secciones)} secciones")
                    ))

                if unmatched:
                    try:
                        (sin_mapa_dir / "sin_mapa.txt").write_text("\n".join(unmatched), encoding="utf-8")
                    except Exception as e:
                        self.after(0, lambda err=str(e): messagebox.showwarning(
                            "Aviso", f"No se pudo escribir 'sin_mapa.txt':\n{err}"
                        ))

                def done_ui(pdf_total=pdf_count_all, copied_total=copied, unmatched_total=len(unmatched)):
                    dlg.destroy()
                    message = [
                        f"PDFs leídos: {pdf_total}",
                        f"Secciones en la muestra: {len(secciones)}",
                        f"PDFs copiados: {copied_total}",
                        f"Secciones sin mapa: {unmatched_total}",
                        f"\nCarpeta exportada:\n{export_dir}"
                    ]
                    messagebox.showinfo("Listo", "\n".join(message))
                    self.container.destroy()
                    self.destroy()
                    self.quit()

                self.after(0, done_ui)

            except Exception:
                tb = traceback.format_exc()
                self.after(0, lambda tb=tb: (dlg.destroy(), messagebox.showerror("Error", tb)))

        threading.Thread(target=run_work, daemon=True).start()


if __name__ == "__main__":
    app = App()
    app.mainloop()