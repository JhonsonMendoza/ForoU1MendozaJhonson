""" 
Importamos las librerias necesarias
para el programa
"""
from pymongo import MongoClient
from bson.objectid import ObjectId
import sys
from tkinter import YES, messagebox

#///////////////////////////////////////
#CLASE PARA ACCEDER A LA BASE DE DATOS
#/////////////////////////////////////////

class ConexionBd:
    """
    Clase ConexionBd
    Atributos
    ---------
        bdNombre : str
            nombre de la base de datos
        Url : str
            Direccion de la base de datos
        coleccion : str
            Nombre de la coleccion
    Metodos
    ---------
        def __init__(self,bdNombre,Url,coleccion):
            metodo constructor de la clase
        def ConectarBd(self):
            Conecta la base de datos creando una instancia del objeto
    """
    def __init__(self,bdNombre,Url,coleccion):
        """
        Metodo constructor de la clase
        Parametros
        -----------
            bdNombre : str
                nombre de la base de datos
            Url : str
                Direccion de la base de datos
            coleccion : str
                Nombre de la coleccion
        """
        self.bdNombre=bdNombre
        self.Url=Url
        self.coleccion=coleccion

    def ConectarBd(self):
        """
        REALIZA LA CONEXION DE LA BD CREANDO LA INSTANCIA DEL OBJETO
        """
        cliente=MongoClient(self.Url)
        baseDatos=cliente[self.bdNombre]        
        cnn=baseDatos[self.coleccion]
        return cnn

             
"""ESTABLECEMOS EL OBJETO CONEXION DE MANERA GLOBAL PARA LA CLASE USUARIOS"""
Cn=ConexionBd(bdNombre='IMC',Url='mongodb://localhost',coleccion='Usuarios')

class DaoUsu:
    """
    Clase DaoUsu
    Atributos
    ----------
        nombre: str
            ventana destinada a interfaces
        apellido: str
            Apellido del Usuario
        edad: int
            edad del Usuario
        usuario: str
            usuario de la persona
        clave: str
            Clave con la que va acceder el Usuario a su cuenta
    
    Metodos
    ----------
        def __init__(self, nombre,apellido,correo,usuario,clave,sexo):
            Constructor de la clase
            
        def insertarUsuario(self):
            guarda los datos en la base de datos

        def actualizarUsuario(self,id):
            Actualiza los datos en la base de datos

        def eliminarUsuario(self,id):():
            elimina los datos dentro de la base de datos

        def consultarTodosUsu():
            consulta si los datos se encuentran en la base de datos

        def consultarUnoUsu(self):
            consulta si un registro se encuentra en la base de datos
    """
    
    def __init__(self,provincia,canton,parroquia,colegio):
        """
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
        """
        self.provincia=provincia
        self.canton=canton
        self.parroquia=parroquia
        self.colegio=colegio 

    def insertarUsuario(self):
        """
        guarda los datos en la base de datos
        """
        try:
            Cn.ConectarBd().insert_one({'provincia':self.provincia,'canton':self.canton,'parroquia':self.parroquia,'colegio':self.colegio})
            messagebox.showinfo('Guardando','Se guardó correctamente el registro actual.')
        except Exception:
            e=sys.exc_info()[1]
            messagebox.showerror('Error',e.args[0]) 

    def actualizarUsuario(self,id):
        """
        Actualiza los datos en la base de datos
        """
        try:
            self.id=id
            idBuscar={"_id":ObjectId(self.id)}
            nuevosValores= {"$set":{'provincia':self.provincia,'canton':self.canton,'parroquia':self.parroquia,'colegio':self.colegio}}
            #PASAMOS EL DATO QUE SE ENCUENTRA EN LAS CAJAS DE TEXTO COMO PARAMETRO DE CADA ELEMENTO DE LA COLECCIO
            Cn.ConectarBd().update_one(idBuscar,nuevosValores)
            messagebox.showinfo('Actualizando','Se actualizo correctamente el registro actual.')
        except Exception:
            e=sys.exc_info()[1]
            messagebox.showerror('Error',e.args[0])

    def eliminarUsuario(self,id):
        """
        elimina los datos dentro de la base de datos
        """
        try:
            if messagebox.askyesno("Confirmación","¿Esta seguro de eliminar el registro seleccionado?")==YES:
                #SE ELIMINA EL REGISTRO SELECCIONADO
                self.id=str(id)
                idBuscar={"_id":ObjectId(self.id)}
                Cn.ConectarBd().delete_one(idBuscar)
                messagebox.showinfo('Eliminando','Se eliminó correctamente el registro actual.')
            else:
                messagebox.showinfo("Registros no afectados","No se eliminó ningún registro por que no se confirmó.")
        except Exception:
            e=sys.exc_info()[1]
            messagebox.showerror('Error',e.args[0])

    def consultarTodosUsu(self):
        """
        consulta si los datos se encuentran en la base de datos
        """
        try:
            #Consultando los datos
            resultados=Cn.ConectarBd().find()
            return resultados
        except Exception:
            e=sys.exc_info()[1]
            messagebox.showerror('Error',e.args[0])
        
        
    def consultarUnoUsu(self,id):
        """
        consulta si un registro se encuentra en la base de datos
        """
        try:
            self.id=str(id)
            idBuscar={"_id":ObjectId(self.id)}
            #Consultando los datos
            resultados=Cn.ConectarBd().find_one(idBuscar)
            return resultados
        except Exception:
            e=sys.exc_info()[1]
            messagebox.showerror('Error',e.args[0])





    
    
