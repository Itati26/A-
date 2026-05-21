class Nodo:
    def __init__(self, datos):
        self.datos = datos
        self.padre = None
        self.hijos = []
        self.costo = 0

    def get_datos(self):
        return self.datos

    def get_padre(self):
        return self.padre

    def set_padre(self, padre):
        self.padre = padre

    def get_hijos(self):
        return self.hijos

    def set_hijos(self, hijos):
        self.hijos = hijos

    def get_costo(self):
        return self.costo

    def set_costo(self, costo):
        self.costo = costo

    def en_lista(self, lista):
        for nodo in lista:
            if self.igual(nodo):
                return True
        return False

    def igual(self, nodo):
        return self.datos == nodo.get_datos()
