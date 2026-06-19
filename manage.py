from abc import ABC, abstractmethod
from datetime import datetime, timedelta


# CLASE ABSTRACTA: PIEZA
class Pieza(ABC):
    """Clase base abstracta. No se puede instanciar directamente."""
    
    def __init__(self, id_pieza, modelo, marca, estado="stock"):
        # Atributos privados (encapsulamiento)
        self.__id_pieza = id_pieza
        self.__modelo = modelo
        self.__marca = marca
        self.__estado = estado  # stock, en_equipo, dañada, desechada
    
    # Métodos para acceder a atributos privados (getters)
    def get_id(self):
        return self.__id_pieza
    
    def get_modelo(self):
        return self.__modelo
    
    def get_marca(self):
        return self.__marca
    
    def get_estado(self):
        return self.__estado
    
    # Método para modificar el estado con validación (setter)
    def set_estado(self, nuevo_estado):
        if nuevo_estado in ("stock", "en_equipo", "dañada", "desechada"):
            self.__estado = nuevo_estado
        else:
            print("Estado no válido")
    
    # Métodos abstractos (obligan a las subclases a implementarlos)
    @abstractmethod
    def diagnosticar(self):
        pass
    
    @abstractmethod
    def reparar(self):
        pass
    
    @abstractmethod
    def calcular_garantia(self, fecha_compra):
        pass
    
    # Método concreto (común para todas)
    def obtener_info(self):
        return f"ID: {self.__id_pieza} | {self.__marca} {self.__modelo} | Estado: {self.__estado}"



# SUBCLASE: PROCESADOR
class Procesador(Pieza):
    def __init__(self, id_pieza, modelo, marca, nucleos, frecuencia, estado="stock"):
        super().__init__(id_pieza, modelo, marca, estado)
        self.nucleos = nucleos
        self.frecuencia = frecuencia
    
    def diagnosticar(self):
        if self.get_estado() == "dañada":
            return "El procesador falla en pruebas de estrés."
        return "El procesador funciona bien."
    
    def reparar(self):
        if self.get_estado() == "dañada":
            self.set_estado("stock")
            return "Procesador reemplazado por garantía (3 años)."
        return "No necesita reparación."
    
    def calcular_garantia(self, fecha_compra):
        return fecha_compra + timedelta(days=3*365)  # 3 años


# SUBCLASE: MEMORIA RAM
class MemoriaRAM(Pieza):
    def __init__(self, id_pieza, modelo, marca, capacidad_gb, tipo, estado="stock"):
        super().__init__(id_pieza, modelo, marca, estado)
        self.capacidad_gb = capacidad_gb
        self.tipo = tipo
    
    def diagnosticar(self):
        if self.get_estado() == "dañada":
            return "La RAM tiene errores de memoria (sectores defectuosos)."
        return "La RAM está estable."
    
    def reparar(self):
        if self.get_estado() == "dañada":
            self.set_estado("desechada")
            return "La RAM no se repara, se desecha."
        return "No necesita reparación."
    
    def calcular_garantia(self, fecha_compra):
        return fecha_compra + timedelta(days=5*365)  # 5 años


# SUBCLASE: DISCO DURO
class DiscoDuro(Pieza):
    def __init__(self, id_pieza, modelo, marca, capacidad_tb, rpm, estado="stock"):
        super().__init__(id_pieza, modelo, marca, estado)
        self.capacidad_tb = capacidad_tb
        self.rpm = rpm
    
    def diagnosticar(self):
        if self.get_estado() == "dañada":
            return "El disco tiene sectores dañados y lecturas lentas."
        return "El disco está en buen estado."
    
    def reparar(self):
        if self.get_estado() == "dañada":
            self.set_estado("stock")
            return "Disco formateado y sectores defectuosos remapeados."
        return "No necesita reparación."
    
    def calcular_garantia(self, fecha_compra):
        return fecha_compra + timedelta(days=2*365)  # 2 años


# FUNCIÓN POLIMÓRFICA
def procesar_piezas(lista_piezas):
    """Recibe cualquier lista de piezas y ejecuta métodos comunes."""
    for p in lista_piezas:
        print("=" * 50)
        print(p.obtener_info())
        print("Diagnóstico:", p.diagnosticar())
        print("Reparación:", p.reparar())
        fecha_compra = datetime(2025, 1, 1)
        fin = p.calcular_garantia(fecha_compra)
        print("Garantía hasta:", fin.strftime("%Y-%m-%d"))
        print("---")


# PRUEBA
if __name__ == "__main__":
    # Creamos varias piezas de distintos tipos
    piezas = [
        Procesador(1, "Core i7", "Intel", 8, 3.2, "en_equipo"),
        MemoriaRAM(2, "Vengeance", "Corsair", 16, "DDR4", "dañada"),
        DiscoDuro(3, "BarraCuda", "Seagate", 2, 7200, "stock")
    ]
    
    # Las procesamos todas juntas (polimorfismo)
    procesar_piezas(piezas)