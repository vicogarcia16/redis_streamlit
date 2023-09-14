import redis
import pandas as pd

r = redis.Redis(host='redis', port=6379, db=0)

def crear_producto(nombre, precio):
    id = r.incr('next_id')
    r.hset('productos', id, f'Nombre: {nombre}, Precio: {precio}')

def leer_producto(id):
    producto = r.hget('productos', id)
    if producto:
        return producto.decode('utf-8')
    else:
        return 'Producto no encontrado'

def mostrar_productos():
    productos = r.hgetall('productos')
    data = []
    for id, producto in productos.items():
        nombre, precio = producto.decode('utf-8').split(', ')
        data.append({'ID': id.decode('utf-8'), 'Nombre': nombre.split(': ')[1], 'Precio': precio.split(': ')[1]})
    df = pd.DataFrame(data)
    return df

def actualizar_producto(id, nombre, precio):
    if r.hexists('productos', id):
        producto_actual = r.hget('productos', id).decode('utf-8')
        nombre_actual, precio_actual = producto_actual.split(', ')
        nuevo_nombre = nombre_actual.split(': ')[1] if nombre == '' else nombre
        nuevo_precio = precio_actual.split(': ')[1] if precio == '' else precio
        nuevo_producto = f'Nombre: {nuevo_nombre}, Precio: {nuevo_precio}'
        r.hset('productos', id, nuevo_producto)
        return 'Producto actualizado'

def eliminar_producto(id):
    if r.hexists('productos', id):
        r.hdel('productos', id)
        return 'Producto eliminado'
