from django.db import models
from abc import ABC, abstractmethod
from datetime import date, datetime


#Herencia
class BaseModel(models.Model, ABC):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    estado = models.CharField(max_length=20, default='Activo')

    class Meta:
        abstract = True

    @abstractmethod #implementacion de metodo cada hijo
    def activar(self):
        pass

    @abstractmethod
    def desactivar(self):
        pass

    def cambiar_estado(self, nuevo_estado):
        if nuevo_estado in [Retrasado, Finalizado, pendiente, Completado]:
            self.estado = nuevo_estado
            self.save()
            return f"Estado cambiado a {nuevo_estado}"
        
class rol(BaseModel):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)
    descripcion_rol = models.TextField()

    def activar(self):
        self.estado = 'Activo'
        self.save
        return f"Rol {self.nombre_rol} desactivado"
    
    def desactivar(self):
        self.estado = 'Inactivo'
        self.save()
        return f"Rol {self.nombre_rol} desactivado"
    
    def asignar_permisos(self, *permisos):
        print(f"Permisos {', '.join(permisos)} asignados al rol {self.nombre_rol}")