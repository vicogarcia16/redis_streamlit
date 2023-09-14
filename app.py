import streamlit as st
from redis_db import (
    crear_producto, leer_producto,
    mostrar_productos, actualizar_producto,
    eliminar_producto
)

# Configuración de la página
st.set_page_config(page_title='Tienda de Productos', layout='wide')

# Título de la página
st.title('Tienda de Productos')

# Función para mostrar la página de Mostrar productos
def mostrar_pagina_mostrar_productos():
    st.header('Productos')
    df = mostrar_productos()
    if not df.empty:
        st.dataframe(df.set_index(df.columns[0]), height=200, use_container_width=True )
    else:
        st.write('No hay productos disponibles')

# Función para mostrar la página de Crear producto
def mostrar_pagina_crear_producto():
    st.header('Crear producto')
    nombre = st.text_input('Nombre')
    precio = st.text_input('Precio')

    if st.button('Crear'):
        if not nombre or not precio:
            st.warning('Por favor, ingresa un nombre y un precio válidos')
        else:
            try:
                precio = float(precio)
                crear_producto(nombre, precio)
                st.success('Producto creado exitosamente')
                # Limpiar campos después de la creación
                nombre = ''
                precio = ''
            except ValueError:
                st.warning('Por favor, ingresa un precio válido (número o número decimal)')

def mostrar_pagina_actualizar_producto():
    st.header('Actualizar producto')
    with st.form('update_form'):
        id_busqueda = st.text_input('ID de producto a buscar')
        st.form_submit_button('Buscar')

    if id_busqueda:
        producto = leer_producto(id_busqueda)
        if producto != 'Producto no encontrado':
            st.subheader('Datos del Producto a Actualizar:')
            nombre_actual, precio_actual = producto.split(', ')
            st.text(f'ID: {id_busqueda}')
            with st.form('update_data'):
                nuevo_nombre = st.text_input('Nuevo nombre', nombre_actual.split(": ")[1])
                nuevo_precio = st.text_input('Nuevo precio', precio_actual.split(": ")[1])
                if st.form_submit_button('Actualizar'):
                    if (not nuevo_nombre and not nuevo_precio) or\
                        (not nuevo_nombre or not nuevo_precio):
                        st.warning('Por favor, ingresa el nuevo valor de nombre y precio')   
                    else:
                        mensaje = actualizar_producto(id_busqueda, nuevo_nombre, nuevo_precio)
                        st.success(mensaje)
        else:
            st.warning('Producto no encontrado')

# Función para mostrar la página de Eliminar producto
def mostrar_pagina_eliminar_producto():
    st.header('Eliminar producto')
    id_eliminar = st.text_input('ID de producto a eliminar')
    confirmar_eliminar = st.checkbox('Confirmar eliminación')
    if st.button('Eliminar'):
        if not id_eliminar:
            st.warning('Por favor, ingresa un ID válido')
        elif confirmar_eliminar:
            mensaje = eliminar_producto(id_eliminar)
            if mensaje:
                st.success(mensaje)
            else:
                st.warning('Producto no encontrado')
        else:
            st.warning('Por favor, confirma la eliminación')

# Barra lateral para navegar entre páginas
st.sidebar.title('Opciones')
pagina_elegida = st.sidebar.selectbox('Selecciona una opción', ('Mostrar productos', 'Crear producto', 'Actualizar producto', 'Eliminar producto'))

# Mostrar la página seleccionada
if pagina_elegida == "Mostrar productos":
    mostrar_pagina_mostrar_productos()
elif pagina_elegida == "Crear producto":
    mostrar_pagina_crear_producto()
elif pagina_elegida == "Actualizar producto":
    mostrar_pagina_actualizar_producto()
elif pagina_elegida == "Eliminar producto":
    mostrar_pagina_eliminar_producto()
