import database as db
import helpers as h
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING


class CenterMixing: # No heredan de nada
    def centrar(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int(ws/2 - w/2)
        y = int(hs/2 - h/2)
        self.geometry(f"{w}x{h}+{x}+{y}") ## Posiciones de pixels, todos los valores deben ser enteros (int)


class CreateClienteWindow(Toplevel, CenterMixing): ## Ventana hija de creación
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Crear cliente")
        self.build()
        self.centrar()
        self.transient(parent)
        self.grab_set() ## Hace que si o si se interactue con la ventana hija

    def build(self):
        frame = Frame(self)
        frame.pack(padx = 20, pady = 10)

        Label(frame, text="DNI: 2 ints y 1 upper char").grid(row = 0, column = 0)
        Label(frame, text="Nombre: de 2 a 30 chars").grid(row = 0, column = 1)
        Label(frame, text="Apellido: de 2 a 30 chars").grid(row = 0, column = 2)

        dni = Entry(frame) ## input de datos por teclado
        dni.grid(row = 1, column = 0)
        dni.bind("<KeyRelease>", lambda event: self.validate(event, 0)) ## Configuración de un evento validador
        nombre = Entry(frame)
        nombre.grid(row = 1, column = 1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 1))
        apellido = Entry(frame)
        apellido.grid(row = 1, column = 2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 2))

        frame = Frame(self)
        frame.pack(pady = 10)

        crear = Button(frame, text = "Crear", command = self.create_client)
        crear.configure(state = DISABLED)
        crear.grid(row = 0, column = 0)
        Button(frame, text = "Cancelar", command = self.close).grid(row = 0, column = 1)

        self.validaciones = [0, 0, 0]
        self.crear = crear ## A nivel de instancia para reutilizarlo
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def create_client(self):
        self.master.treeview.insert(
            parent = '', index = 'end', iid = self.dni.get(),
            values = (self.dni.get(), self.nombre.get(), self.apellido.get()))
        db.Clientes.crear(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close()

    def close(self): ## Destruir ventana hija
        self.destroy()
        self.update()

    def validate(self, event, index):
        valor = event.widget.get()
        valido = h.dni_valido(valor, db.Clientes.lista) if index == 0 \
            else (valor.isalpha() and len(valor) >= 2 and len(valor) <= 30)
        event.widget.configure({"bg": "Green" if valido else "Red"})
        # Cambiar el estado del botón en base a las validaciones
        self.validaciones[index] = valido
        self.crear.config(state = NORMAL if self.validaciones == [1, 1, 1] else DISABLED)


class EditClientWindow(Toplevel, CenterMixing):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Actualizar cliente")
        self.build()
        self.centrar()
        self.transient(parent)
        self.grab_set()

    def build(self):
        frame = Frame(self)
        frame.pack(padx = 20, pady = 10)

        Label(frame, text="DNI (no editable)").grid(row = 0, column = 0)
        Label(frame, text="Nombre: de 2 a 30 chars").grid(row = 0, column = 1)
        Label(frame, text="Apellido: de 2 a 30 chars").grid(row = 0, column = 2)

        dni = Entry(frame)
        dni.grid(row = 1, column = 0)
        nombre = Entry(frame)
        nombre.grid(row = 1, column = 1)
        nombre.bind("<KeyRelease>", lambda event: self.validate(event, 0))
        apellido = Entry(frame)
        apellido.grid(row = 1, column = 2)
        apellido.bind("<KeyRelease>", lambda event: self.validate(event, 1))

        cliente = self.master.treeview.focus()
        campos = self.master.treeview.item(cliente, 'values')
        dni.insert(0, campos[0])
        dni.config(state = DISABLED)
        nombre.insert(0, campos[1])
        apellido.insert(0, campos[2])

        frame = Frame(self)
        frame.pack(pady = 10)

        actualizar = Button(frame, text = "Actualizar", command = self.edit_client)
        actualizar.grid(row = 0, column = 0)
        Button(frame, text = "Cancelar", command = self.close).grid(row = 0, column = 1)

        self.validaciones = [1, 1]
        self.actualizar = actualizar
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido

    def edit_client(self):
        cliente = self.master.treeview.focus()
        self.master.treeview.item(cliente, values = (
            self.dni.get(), self.nombre.get(), self.apellido.get()))
        db.Clientes.modificar(self.dni.get(), self.nombre.get(), self.apellido.get())
        self.close()

    def close(self):
        self.destroy()
        self.update()

    def validate(self, event, index):
        valor = event.widget.get()
        valido = (valor.isalpha() and len(valor) >= 2 and len(valor) <= 30)
        event.widget.configure({"bg": "Green" if valido else "Red"})
        # Cambiar el estado del botón en base a las validaciones
        self.validaciones[index] = valido
        self.actualizar.config(state=NORMAL if self.validaciones == [1, 1] else DISABLED)


class MainWindow(Tk, CenterMixing):
    def __init__(self):
        super().__init__()
        self.title("Gestor de clientes")
        self.build()
        self.centrar()

    def build(self):
        ##button = Button(self, text = "Hola", command = self.hola) ## Creación de un botón
        ##button.pack()
        frame = Frame(self)
        frame.pack()

        treeview = ttk.Treeview(frame)
        treeview['columns'] = ('DNI', 'nombre', 'apellido') ## Creación de columnas

        treeview.column('#0', width = 0, stretch = NO) ## Hacer primer columna de 0 pixels
        treeview.column('DNI', anchor = CENTER)
        treeview.column('nombre', anchor = CENTER)
        treeview.column('apellido', anchor = CENTER)

        treeview.heading('DNI', text = "DNI", anchor = CENTER) ## Dar nombres visibles a las columnas
        treeview.heading('nombre', text = "Nombre", anchor = CENTER)
        treeview.heading('apellido', text = "Apellido", anchor = CENTER)

        scrollbar = Scrollbar(frame) ## Creación de barra de scroll
        scrollbar.pack(side = RIGHT, fill = Y) ## Scroll a la derecha
        treeview['yscrollcommand'] = scrollbar.set ## treeview importa el scroll

        for cliente in db.Clientes.lista:
            treeview.insert( ## Inserción de un cliente al treview
                parent = '', index = 'end', iid = cliente.dni,
                values = (cliente.dni, cliente.nombre, cliente.apellido)
            )
        treeview.pack()

        frame = Frame(self)
        frame.pack(pady = 20)

        Button(frame, text = "Crear", command = self.create).grid(row = 0, column = 0) ## grid() es como pack() pero en forma de grilla
        Button(frame, text = "Modificar", command = self.edit).grid(row = 0, column = 1)
        Button(frame, text = "Borrar", command = self.delete).grid(row = 0, column = 2)
        
        self.treeview = treeview ## Exportación como atributo de instancia, para usarlo en otras partes del proyecto

    def delete(self):
        cliente = self.treeview.focus()
        if cliente:
            campos = self.treeview.item(cliente, "values")
            confirmar = askokcancel(
                title = "Confirmar borrado",
                message = f"Borrar {campos[1]} {campos[2]}?",
                icon = WARNING
            )
            if confirmar:
                self.treeview.delete(cliente)
                db.Clientes.eliminar(campos[0])

    def create(self):
        CreateClienteWindow(self)
    
    def edit(self):
        if self.treeview.focus():
            EditClientWindow(self)

    ##def hola(self):
    ##    print("Hello world!")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()