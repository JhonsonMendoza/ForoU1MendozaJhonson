"""
IMPORTAMOS LA CLASE DE NEGOCIO DE DATOS
"""
import BackEnd as Dao 
"""
traigo todos los elementos de la biblioteca
"""
from tkinter import * 
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sys
from tkinter import font
from bson.objectid import ObjectId
from datetime import date
#HAGO LA CONEXION CON MONGODB
from pymongo import MongoClient
#IMPORTAMOS LA CLASE PARA EXPORTAR PDF
from classPDF import *


class Usuarios:
    '''
    Clase Usuarios.
    
    Atributos
    ----------
        provincia: str
            provincia del usuario
        canton: str
            canton del Usuario
        parroquia: int
            parroquia del Usuario
        colegio: str
            colegio de la persona
    
    Metodos
    ----------
        def __init__(self, provincia,canton,parroquia,colegio):
            Constructor de la clase
            
        def registroUsuario(self):
            Se piden diversos datos necesarios para el registro de
            ----------
            guarda los datos en la base de datos

        def eliminar():
            elimina datis de la base de datos

        def editar():
            edita datos dentro de la base de datos

        def actualizar():
            actualiza la base de datos con los que habian sido editados
        
        def validar()
            exige al usuario llenar todos los campos para el registro
        
        def limpiar():
            limpia las cajas de texto.

        def obtenerVista(self):
            permite visualizar los usuarios registrados y algunos
            detalles mas.
    '''

    def __init__(self,provincia,canton,parroquia,colegio):
        '''
        Construye todos los atributos necesarios para el Usuario.
        Parametros
        ----------
            nombre: str
                Nombre del Usuario
            apellido: str
                Apellido del Usuario
            sexo: str
                sexo del Usuario
            edad: str
                edad del Usuario
            usuario: str
                usuario a registrar
            clave: str
                Clave con la que va acceder el Usuario a su cuenta
        '''
        self.provincia=provincia
        self.canton=canton
        self.parroquia=parroquia
        self.colegio=colegio

    def registroUsuario(self, ventana):
        
        """Permite que el usuario se registre
        ingresando una serie de datos.

        Parametros
        ----------
            ventana: str
                permite crear las interfaces
        """
        self.window=ventana
        self.window.title('Registro de Usuarios')
        self.window.geometry("1600x600") 
        
        """CREAMOS DOS CONTENEDORES"""
        contenedor=LabelFrame(self.window, text='Registro de datos')
        contenedor.grid(row=0, column=0, columnspan=2,pady=5)

        contenedorLv=LabelFrame(self.window, text='')
        contenedorLv.grid(row=13, column=0, columnspan=2,pady=5)
        
        """CREAR ETIQUETAS CON SUS CAJAS DE TEXTO """
        Label(contenedor,text='provincia:', bg="light blue").grid(row=1, column=0,sticky=W+E)
        self.provincia=Entry(contenedor)
        self.provincia.grid(row=1,column=1,sticky=W+E)

        Label(contenedor,text='canton:', bg="light blue").grid(row=2, column=0,sticky=W+E)
        self.canton=Entry(contenedor)
        self.canton.grid(row=2,column=1,sticky=W+E)

        Label(contenedor,text='parroquia:', bg="light blue").grid(row=4, column=0,sticky=W+E)
        self.parroquia=Entry(contenedor)
        self.parroquia.grid(row=4,column=1,sticky=W+E)

        Label (contenedor, text="colegio",bg = "light blue").grid(row=6, column=0,sticky=W+E)
        self.colegio = Entry (contenedor)
        self.colegio.grid(row=6,column=1,sticky=W+E)


        """CREAMOS UNA VISTA DE DATOS"""
        columnas = ('#1', '#2', '#3', '#4')
        self.vista=ttk.Treeview(contenedorLv,height=14,columns=columnas)
        self.vista.grid(row=13,column=0, columnspan=2)
        self.vista.heading('#0',text='Id',anchor=CENTER)
        self.vista.heading('#1',text='Provincia',anchor=CENTER)
        self.vista.heading('#2',text='Canton',anchor=CENTER)
        self.vista.heading('#3',text='Parroquia',anchor=CENTER)
        self.vista.heading('#4',text='Colegio',anchor=CENTER)

        """LLENAMOS DE DATOS LA VISTA"""
        self.ObtenerVista()

        def Salir():
            ventana.destroy()

        """CREAMOS LOS BOTONES QUE VAMOS A DEJAR ACTIVOS EN LA EDICION"""
        ttk.Button(contenedor, text='Guardar',command=self.Guardar).grid(row=10, column=0,sticky=W+E)
        ttk.Button(contenedor, text='Eliminar',command=self.Eliminar).grid(row=10, column=1,sticky=W+E)
        ttk.Button(contenedor, text='Actualizar',command=self.Actualizar).grid(row=11, column=0,sticky=W+E)
        ttk.Button(contenedor, text='Salir',command=Salir).grid(row=11, column=1,sticky=W+E)  
        ttk.Button(contenedor, text='Editar',command=self.Editar).grid(row=12, column=0,sticky=W+E)                                     
        
    def ObtenerVista(self):
        """
        METODO PARA CONSULTAR LA COLECCION COMPLETA
        """
        registros=self.vista.get_children()
        for elemento in registros:
            self.vista.delete(elemento)
        """Consultando los datos"""
        self.adapatadorUsu=Dao.DaoUsu(provincia=self.provincia.get(),canton=self.canton.get(),parroquia=self.parroquia.get(),colegio=self.colegio.get())
        resultados=self.adapatadorUsu.consultarTodosUsu()
        """llenando los datos"""
        for Fila in resultados:
            self.vista.insert('', 0, text= Fila["_id"],
            values = (Fila["provincia"],Fila["canton"],Fila["parroquia"],Fila["colegio"]))
    
    def limpiarCajas(self):
        """
        SE LIMPIAN LOS CUADROS DE TEXTO PRIMERO
        """
        self.provincia.delete(0,END)
        self.canton.delete(0,END)
        self.parroquia.delete(0,END)
        self.colegio.delete(0,END)
                       
    def validar(self):
        """
        VALIDACION DE LOS DATOS
        """
        return len(self.provincia.get())!=0 and len(self.canton.get())!=0 and len(self.parroquia.get())!=0 and len(self.colegio.get())!=0
        
    def Guardar(self):
        """
        METODO PARA GUARDAR UN REGISTRO
        """
        try:
            """REALIZAMOS EL GUARDADO DEL REGISTRO SI ES QUE NO HAY ERRORES"""
            if self.validar():
                """INSTANCIAMOS EL OBJETO DE DATOS USUARIO"""
                self.adapatadorUsu=Dao.DaoUsu(provincia=self.provincia.get(),canton=self.canton.get(),parroquia=self.parroquia.get(),colegio=self.colegio.get())
                self.adapatadorUsu.insertarUsuario()
                self.ObtenerVista()
                self.limpiarCajas()
            else:
                messagebox.showwarning("Error de validación","Ingrese información requerida, hay campos sin llenar.")
        except Exception:
                e=sys.exc_info()[1]
                messagebox.showerror('Error',e.args[0])

    def Eliminar(self):
        """
        METODO PARA ELIMINAR UN REGISTRO
        """
        """REALIZAMOS LA ELIMINACION DEL REGISTRO SI ES QUE NO HAY ERRORES"""
        try:
            """CAPTURAMOS EL ID DEL REGISTRO SELECCIONADO EN LA VISTA(LISTVIEW)"""
            self.vista.item(self.vista.selection())['text'][0]
        except IndexError as e:
            messagebox.showerror("Error","Seleccione un registro para eliminar.")
            return
        idUsu=self.vista.item(self.vista.selection())['text']
        self.adapatadorUsu.eliminarUsuario(idUsu)
        self.ObtenerVista()

    def Actualizar(self): 
        """
        METODO PARA ACTUZALIZAR UN REGISTRO
        """ 
        try:
            if self.validar():
                """CAPTURAMOS EL ID DEL REGISTRO SELECCIONADO EN LA VISTA(LISTVIEW)"""
                idUsu=str(self.vista.item(self.vista.selection())['text'])
                self.adapatadorUsu=Dao.DaoUsu(provincia=self.provincia.get(),canton=self.canton.get(),parroquia=self.parroquia.get(),colegio=self.colegio.get())
                self.adapatadorUsu.actualizarUsuario(idUsu)
                self.ObtenerVista()
                self.limpiarCajas()
            else:
                messagebox.showwarning("Error de validación","Ingrese información requerida, hay campos sin llenar.")
        except Exception as e:
            e=sys.exc_info()[1]
            messagebox.showerror('Error',e.args[0])      

    def Editar(self):
        """
        METODO PARA EDITAR UN REGISTRO
        """
        try:
            """CAPTURAMOS EL ID DEL REGISTRO SELECCIONADO EN LA VISTA(LISTVIEW)"""
            self.vista.item(self.vista.selection())['text'][0]
        except IndexError as e:
            messagebox.showerror("Error","Seleccione un registro para editar.")
            return
        
        self.limpiarCajas()
        """CAPTURAMOS EL ID DEL REGISTRO SELECCIONADO EN LA VISTA(LISTVIEW)"""
        id=str(self.vista.item(self.vista.selection())['text'])
        res=self.adapatadorUsu.consultarUnoUsu(id)
        self.provincia.insert(0,str(res['provincia']))
        self.canton.insert(0,str(res['canton']))
        self.parroquia.insert(0,str(res['parroquia']))
        self.colegio.insert(0,str(res['colegio']))


#////////////////////////////////////////////
#MENU PRINICIPAL DEL SISTEMA
#///////////////////////////////////////////

class menuPrincipal:
    '''
    Atributos
    ----------
    ventana:str
        crea la interfaz correspondiente
    
    Metodo
    ----------
    def __init__(self, ventana):
        Constructor de la clase
        
    def salir(self):
        sale por completo del programa/cierra interfaces.

    def Registrarse():
        permite abrir las interfaces de la clase Usuario

    def obtenerVista(self):
        permite visualizar las interfaces de la clase Control

    
    '''
    def __init__(self,ventana):
        """
        Metodo constructor
        ---------------
        """
        self.window=ventana
        self.window.title('Menu Principal')
        self.window.geometry("600x200+400+300")
              
        """CREAMOS UN CONTENEDOR"""
        contenedor=LabelFrame(self.window, text='Menu Principal')
        contenedor.grid(row=0, column=0, columnspan=2,pady=5)

        def Salir():
            """Destruye todas las interfaces"""
            ventana.destroy()

        def Registrarse():
            """Metodo que permite abrir las interfaces correspondiente al
            registro de los Usuarios"""
            ventana = Toplevel()
            aplicacion=Usuarios("","","","")
            aplicacion.registroUsuario(ventana)
            ventana.mainloop()

        """CREAMOS LOS BOTONES"""
        ttk.Button(contenedor, text='REGISTRO',command=Registrarse).grid(row=4, column=5,sticky=W+E)
        ttk.Button(contenedor, text='SALIR', command=Salir).grid(row=4, column=6,sticky=W+E)

