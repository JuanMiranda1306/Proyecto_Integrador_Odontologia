import customtkinter as ctk
from tkinter import ttk, messagebox
from clientes_controller import ver_clientes, agregar_cliente, eliminar_cliente
from datetime import datetime

class OrthoGuzmanApp:
    def __init__(self, root, parent_root):
        self.root = root
        self.parent_root = parent_root
        self.root.title("Gestión de Clientes - Ortho Guzmán 🦷")
        self.root.geometry("1000x650")
        self.root.resizable(True, True)
        
        self.configurar_estilo_treeview()
        self.crear_interfaz()
        self.cargar_clientes()

    def configurar_estilo_treeview(self):
        style = ttk.Style()
        style.theme_use("default")

        bg_color = self.root._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
        text_color = self.root._apply_appearance_mode(ctk.ThemeManager.theme["CTkLabel"]["text_color"])

        style.configure("Treeview",
                        background=bg_color,
                        foreground=text_color,
                        fieldbackground=bg_color,
                        bordercolor=bg_color,
                        borderwidth=0)
        style.map('Treeview', background=[('selected', '#3B82F6')])

        style.configure("Treeview.Heading",
                        background=self.root._apply_appearance_mode(ctk.ThemeManager.theme["CTkButton"]["fg_color"]),
                        foreground=text_color,
                        font=('Arial', 12, 'bold'),
                        borderwidth=0)

    def crear_interfaz(self):
        ctk.CTkLabel(
            self.root,
            text="Gestión de Clientes - Ortho Guzmán 🦷",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=15)

        btn_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Ver Clientes 🔄", command=self.cargar_clientes).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkButton(btn_frame, text="Agregar Cliente ➕", command=self.agregar_cliente).grid(row=0, column=1, padx=10, pady=5)
        ctk.CTkButton(btn_frame, text="Eliminar Cliente 🗑️", command=self.eliminar_cliente, fg_color="#F44336", hover_color="#D32F2F").grid(row=0, column=2, padx=10, pady=5)
        ctk.CTkButton(btn_frame, text="Regresar al Panel 🚪", command=self.volver_dashboard, fg_color="#424242", hover_color="#616161").grid(row=0, column=3, padx=10, pady=5)

        ctk.CTkFrame(self.root, height=2, fg_color="#3B82F6").pack(fill="x", pady=10)

        columnas = (
            "ID", "Nombre Completo", "Edad", "Tratamiento Previo",
            "Contacto", "Presupuesto/Tratamiento", "Abierto Costo",
            "Dra Encargada", "Fecha Entrada", "Fecha Salida"
        )

        self.tree = ttk.Treeview(self.root, columns=columnas, show="headings", height=15)
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=130)
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

    def cargar_clientes(self):
        """Carga todos los clientes en el Treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        clientes = ver_clientes()
        for c in clientes:
            self.tree.insert("", "end", values=(
                c["id"],
                c["nombre_completo"],
                c["edad"],
                c["tratamiento_previo"],
                c["recordatorio_contacto"],
                c["presupuesto_tratamiento"],
                c["abierto_costo"],
                c["dra_encargada"],
                c["fecha_entrada"],
                c["fecha_salida"]
            ))

    def agregar_cliente(self):
        """Ventana para agregar un nuevo cliente."""
        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Agregar Cliente - Ortho Guzmán 🦷")
        ventana.geometry("400x650")
        ventana.transient(self.root)
        ventana.grab_set()
        ventana.focus_force()

        frame = ctk.CTkScrollableFrame(ventana)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        campos = {
            "Nombre Completo": ctk.CTkEntry(frame, width=250),
            "Edad": ctk.CTkEntry(frame, width=250),
            "Tratamiento Previo (Sí/No)": ctk.CTkOptionMenu(frame, values=["Sí", "No"]),
            "Recordatorio (Teléfono o Correo)": ctk.CTkEntry(frame, width=250),
            "Presupuesto o Tratamiento": ctk.CTkEntry(frame, width=250),
            "Abierto al costo": ctk.CTkOptionMenu(frame, values=["Sí", "No"]),
            "Dra Encargada": ctk.CTkEntry(frame, width=250),
            "Fecha Entrada (YYYY-MM-DD HH:MM)": ctk.CTkEntry(frame, width=250),
            "Fecha Salida (YYYY-MM-DD HH:MM)": ctk.CTkEntry(frame, width=250)
        }

        for i, (label, entry) in enumerate(campos.items()):
            ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(weight="bold")).pack(pady=(10, 5))
            entry.pack(pady=5)

        def guardar():
            try:
                nombre = campos["Nombre Completo"].get().strip()
                edad = int(campos["Edad"].get().strip())
                previo = campos["Tratamiento Previo (Sí/No)"].get()
                recordatorio = campos["Recordatorio (Teléfono o Correo)"].get().strip()
                presupuesto = campos["Presupuesto o Tratamiento"].get().strip()
                abierto = campos["Abierto al costo"].get()
                dra = campos["Dra Encargada"].get().strip()
                fecha_entrada = datetime.strptime(campos["Fecha Entrada (YYYY-MM-DD HH:MM)"].get().strip(), "%Y-%m-%d %H:%M")
                fecha_salida = datetime.strptime(campos["Fecha Salida (YYYY-MM-DD HH:MM)"].get().strip(), "%Y-%m-%d %H:%M")
            except Exception as e:
                messagebox.showerror("Error", f"Datos inválidos o formato incorrecto:\n{e}")
                return

            if not nombre or not recordatorio or not dra:
                messagebox.showwarning("Campos vacíos", "Debe llenar todos los campos obligatorios.")
                return

            if agregar_cliente(nombre, edad, previo, recordatorio, presupuesto, abierto, dra, fecha_entrada, fecha_salida):
                messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
                ventana.destroy()
                self.cargar_clientes()
            else:
                messagebox.showerror("Error", "No se pudo agregar el cliente.")

        ctk.CTkButton(frame, text="Guardar Cliente", command=guardar, width=200, font=ctk.CTkFont(weight="bold")).pack(pady=(20, 10))
        ctk.CTkButton(frame, text="Cancelar", command=ventana.destroy, width=200, fg_color="gray").pack(pady=5)

    def eliminar_cliente(self):
        """Ventana para eliminar cliente por ID."""
        ventana = ctk.CTkToplevel(self.root)
        ventana.title("Eliminar Cliente")
        ventana.geometry("300x200")
        ventana.transient(self.root)
        ventana.grab_set()
        ventana.focus_force()

        frame = ctk.CTkFrame(ventana)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="ID del cliente a eliminar:", font=ctk.CTkFont(weight="bold")).pack(pady=(15, 5))
        entry_id = ctk.CTkEntry(frame, width=200)
        entry_id.pack(pady=5)

        def eliminar():
            try:
                cliente_id = int(entry_id.get().strip())
            except ValueError:
                messagebox.showerror("Error", "El ID debe ser un número entero.")
                return

            confirm = messagebox.askyesno("Confirmar eliminación", f"¿Deseas eliminar al cliente con ID {cliente_id}?")
            if confirm:
                if eliminar_cliente(cliente_id):
                    messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                    self.cargar_clientes()
                    ventana.destroy()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el cliente. Verifica el ID.")

        ctk.CTkButton(frame, text="Eliminar", command=eliminar, width=150, fg_color="#F44336", hover_color="#D32F2F", font=ctk.CTkFont(weight="bold")).pack(pady=(20, 5))
        ctk.CTkButton(frame, text="Cancelar", command=ventana.destroy, width=150, fg_color="gray").pack(pady=5)

    def volver_dashboard(self):
        """Regresa al panel principal."""
        self.root.destroy()
        if self.parent_root.winfo_exists():
            self.parent_root.deiconify()
