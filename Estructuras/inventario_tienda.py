#Luna Sharick Carrtero Hernandez - Karen Sofia Hernandez Reyes - Luna Isabela Opsina Alvarez


# ================== IMPORTACIONES ==================
import os                # Para limpiar la consola (os.system)
import sqlite3           # Para manejar la base de datos SQLite
from colorama import init, Fore   # Para usar colores en los textos de consola

# Inicializa colorama 
init(autoreset=True)


# ================== BASE DE DATOS ==================
DB_NAME = "inventario.db"   # Nombre del archivo de base de datos

def crear_bd():
    """Crea la tabla en la base de datos si no existe"""
    conn = sqlite3.connect(DB_NAME)   # Conecta a la base de datos
    c = conn.cursor()                 # Crea un cursor para ejecutar comandos SQL
    # Crea la tabla productos si no existe aún
    c.execute('''CREATE TABLE IF NOT EXISTS productos (
                    codigo INTEGER PRIMARY KEY,
                    nombre TEXT,
                    cantidad INTEGER)''')
    conn.commit()   # Guarda cambios
    conn.close()    # Cierra la conexión

def guardar_producto_bd(codigo, nombre, cantidad):
    """Guarda un producto en la base de datos o lo actualiza si ya existe"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Inserta un producto nuevo o reemplaza si el código ya existe
    c.execute("INSERT OR REPLACE INTO productos (codigo, nombre, cantidad) VALUES (?,?,?)",
              (codigo, nombre, cantidad))
    conn.commit()
    conn.close()

def eliminar_producto_bd(codigo):
    """Elimina un producto de la base de datos por código"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM productos WHERE codigo=?", (codigo,))
    conn.commit()
    conn.close()

def cargar_inventario(inventario):
    """Carga los productos guardados en la BD al árbol binario"""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT codigo, nombre, cantidad FROM productos")
    # Inserta cada producto leído en el árbol de inventario
    for codigo, nombre, cantidad in c.fetchall():
        inventario.insertar(int(codigo), nombre, int(cantidad))
    conn.close()


# ================== CLASES ==================
class NodoProducto:
    """Clase que representa un nodo del árbol binario (cada producto)"""
    def __init__(self, codigo, nombre, cantidad):
        self.codigo = codigo      # Código del producto (clave)
        self.nombre = nombre      # Nombre del producto
        self.cantidad = cantidad  # Cantidad en inventario
        self.izq = None           # Nodo hijo izquierdo
        self.der = None           # Nodo hijo derecho

class InventarioTienda:
    """Clase que representa el árbol binario de productos"""
    def __init__(self):
        self.raiz = None  # La raíz del árbol empieza vacía

    # ---------- Insertar producto ----------
    def insertar(self, codigo, nombre, cantidad):
        """Inserta un producto en el árbol (o actualiza si ya existe)"""
        self.raiz = self._insertar_rec(self.raiz, codigo, nombre, cantidad)

    def _insertar_rec(self, nodo, codigo, nombre, cantidad):
        """Función recursiva para insertar en el árbol"""
        if nodo is None:
            return NodoProducto(codigo, nombre, cantidad)  # Si está vacío, crea el nodo
        if codigo < nodo.codigo:  # Si el código es menor, va a la izquierda
            nodo.izq = self._insertar_rec(nodo.izq, codigo, nombre, cantidad)
        elif codigo > nodo.codigo:  # Si es mayor, va a la derecha
            nodo.der = self._insertar_rec(nodo.der, codigo, nombre, cantidad)
        else:  # Si ya existe, actualiza nombre y cantidad
            nodo.nombre = nombre
            nodo.cantidad = cantidad
        return nodo

    # ---------- Buscar producto ----------
    def buscar(self, codigo):
        """Busca un producto por código"""
        return self._buscar_rec(self.raiz, codigo)

    def _buscar_rec(self, nodo, codigo):
        """Búsqueda recursiva en el árbol"""
        if nodo is None or nodo.codigo == codigo:  # Si no existe o lo encontró
            return nodo
        if codigo < nodo.codigo:  # Buscar en el lado izquierdo
            return self._buscar_rec(nodo.izq, codigo)
        else:  # Buscar en el lado derecho
            return self._buscar_rec(nodo.der, codigo)

    # ---------- Eliminar producto ----------
    def eliminar(self, codigo):
        """Elimina un producto por código"""
        self.raiz = self._eliminar_rec(self.raiz, codigo)

    def _eliminar_rec(self, nodo, codigo):
        """Función recursiva para eliminar un nodo"""
        if nodo is None:
            return nodo
        if codigo < nodo.codigo:  # Buscar en el lado izquierdo
            nodo.izq = self._eliminar_rec(nodo.izq, codigo)
        elif codigo > nodo.codigo:  # Buscar en el lado derecho
            nodo.der = self._eliminar_rec(nodo.der, codigo)
        else:
            # Caso 1: no tiene hijo izquierdo
            if nodo.izq is None:
                return nodo.der
            # Caso 2: no tiene hijo derecho
            elif nodo.der is None:
                return nodo.izq
            # Caso 3: tiene dos hijos -> se busca el mínimo en la derecha
            sucesor = self._minimo(nodo.der)
            nodo.codigo = sucesor.codigo
            nodo.nombre = sucesor.nombre
            nodo.cantidad = sucesor.cantidad
            nodo.der = self._eliminar_rec(nodo.der, sucesor.codigo)
        return nodo

    def _minimo(self, nodo):
        """Encuentra el nodo con el valor mínimo (izquierda más profunda)"""
        actual = nodo
        while actual.izq is not None:
            actual = actual.izq
        return actual

    # ---------- Mostrar inventario ----------
    def mostrar_inventario(self):
        """Muestra todo el inventario en orden ascendente (inorden)"""
        self._inorden(self.raiz)

    def _inorden(self, nodo):
        """Recorrido inorden: izquierda - raíz - derecha"""
        if nodo is not None:
            self._inorden(nodo.izq)
            # Imprime en amarillo los productos
            print(Fore.YELLOW + f"Código: {nodo.codigo}, Nombre: {nodo.nombre}, Cantidad: {nodo.cantidad}")
            self._inorden(nodo.der)


# ================== FUNCIÓN PARA DIBUJAR EL ÁRBOL ==================
def imprimir_arbol(nodo, nivel=0, prefijo=""):
    """Imprime el árbol binario"""
    if nodo is not None:
        # Imprime el nodo con indentación y color azul
        print(' ' *(4 * nivel)  + Fore.CYAN + f"{prefijo}-> ({nodo.codigo}, {nodo.nombre}, {nodo.cantidad})")
        # Si tiene hijos, imprime recursivamente
        if nodo.izq or nodo.der:
            imprimir_arbol(nodo.izq, nivel + 1, "L-> ")
            imprimir_arbol(nodo.der, nivel + 1, "R-> ") 


# ================== MENÚ INTERACTIVO ==================
def menu():
    """Función principal que muestra el menú y controla el programa"""
    crear_bd()  # Crea la base de datos si no existe
    inventario = InventarioTienda()  # Crea el árbol binario
    cargar_inventario(inventario)    # Carga productos desde la BD

    while True:
        # Limpia pantalla según el sistema operativo
        os.system('cls' if os.name == 'nt' else 'clear')

        # Menú en color cyan
        print(Fore.CYAN + "===== MENÚ INVENTARIO DE TIENDA =====")
        print("1. Agregar producto")
        print("2. Buscar producto")
        print("3. Editar producto")
        print("4. Eliminar producto")
        print("5. Mostrar inventario")
        print("6. Ver árbol")
        print("7. Salir")

        # Opción elegida
        opcion = input(Fore.GREEN + "Seleccione una opción: ")

        # ---- Opción 1: Agregar producto ----
        if opcion == "1":
            try:
                codigo = int(input("Código del producto: "))
                nombre = input("Nombre del producto: ")
                cantidad = int(input("Cantidad: "))
            except ValueError:
                input(Fore.RED + "Entrada inválida. Presione Enter...")
                continue
            inventario.insertar(codigo, nombre, cantidad)
            guardar_producto_bd(codigo, nombre, cantidad)
            input(Fore.GREEN + "Producto agregado/actualizado. Presione Enter...")

        # ---- Opción 2: Buscar producto ----
        elif opcion == "2":
            try:
                codigo = int(input("Ingrese el código a buscar: "))
            except ValueError:
                input(Fore.RED + "Código inválido. Presione Enter...")
                continue
            prod = inventario.buscar(codigo)
            if prod:
                input(Fore.GREEN + f"Encontrado: Código {prod.codigo}, Nombre {prod.nombre}, Cantidad {prod.cantidad}. Presione Enter...")
            else:
                input(Fore.RED + "Producto no encontrado. Presione Enter...")

        # ---- Opción 3: Editar producto ----
        elif opcion == "3":
            try:
                codigo = int(input("Código del producto a editar: "))
            except ValueError:
                input(Fore.RED + "Código inválido. Presione Enter...")
                continue
            prod = inventario.buscar(codigo)
            if prod:
                # Si no escribe nada, se mantiene el valor anterior
                nombre = input(f"Nuevo nombre (actual: {prod.nombre}): ") or prod.nombre
                cantidad = input(f"Nueva cantidad (actual: {prod.cantidad}): ")
                cantidad = int(cantidad) if cantidad else prod.cantidad
                inventario.insertar(codigo, nombre, cantidad)
                guardar_producto_bd(codigo, nombre, cantidad)
                input(Fore.GREEN + "Producto editado. Presione Enter...")
            else:
                input(Fore.RED + "Producto no encontrado. Presione Enter...")

        # ---- Opción 4: Eliminar producto ----
        elif opcion == "4":
            try:
                codigo = int(input("Código del producto a eliminar: "))
            except ValueError:
                input(Fore.RED + "Código inválido. Presione Enter...")
                continue
            inventario.eliminar(codigo)
            eliminar_producto_bd(codigo)
            input(Fore.GREEN + "Producto eliminado (si existía). Presione Enter...")

        # ---- Opción 5: Mostrar inventario ----
        elif opcion == "5":
            print("\nInventario actual:")
            inventario.mostrar_inventario()
            input(Fore.GREEN + "\nPresione Enter para continuar...")

        # ---- Opción 6: Ver árbol ----
        elif opcion == "6":
            print("\nÁrbol binario actual:")
            imprimir_arbol(inventario.raiz)
            input(Fore.GREEN + "\nPresione Enter para continuar...")

        # ---- Opción 7: Salir ----
        elif opcion == "7":
            print(Fore.CYAN + "Saliendo del programa...")
            break

        # ---- Opción inválida ----
        else:
            input(Fore.RED + "Opción no válida. Presione Enter...")


# ================== EJECUCIÓN ==================
if __name__ == "__main__":
    # Si ejecutamos el script directamente, arranca el menú
    menu()
