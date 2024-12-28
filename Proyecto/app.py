from flask import Flask, render_template, request, redirect, url_for
import pymongo
import os

app = Flask(__name__)

# Conexion a MongoDB
myClient = pymongo.MongoClient("mongodb://mongodb:27017")
myDb = myClient["base_de_datos"]
collection = myDb["juegos"] 

# Se inicia con datos inicialmente para evitar hacer un llenado de datos en cada prueba. SOLO PARA EXPOSICION, despues borrar.
def inicializar_datos():
    if collection.count_documents({}) == 0:  # verificar si la coleccion esta vacia
        datos_iniciales = [
            {"id": "1", "nombre": "Catan", "jugadores_min": 3, "jugadores_max": 4, "limite_edades": "10", "pais_origen": "Alemania", "costo_usd": 45.99},
            {"id": "2", "nombre": "Carcassonne", "jugadores_min": 2, "jugadores_max": 5, "limite_edades": "8", "pais_origen": "Francia", "costo_usd": 34.99},
            {"id": "3", "nombre": "Ticket to Ride", "jugadores_min": 2, "jugadores_max": 5, "limite_edades": "8", "pais_origen": "Estados Unidos", "costo_usd": 39.99},
            {"id": "4", "nombre": "Dixit", "jugadores_min": 3, "jugadores_max": 6, "limite_edades": "8", "pais_origen": "Francia", "costo_usd": 29.99},
            {"id": "5", "nombre": "Pandemic", "jugadores_min": 2, "jugadores_max": 4, "limite_edades": "8", "pais_origen": "Estados Unidos", "costo_usd": 44.99},
            {"id": "6", "nombre": "Chess", "jugadores_min": 2, "jugadores_max": 2, "limite_edades": "6", "pais_origen": "India", "costo_usd": 19.99},
            {"id": "7", "nombre": "Monopoly", "jugadores_min": 2, "jugadores_max": 6, "limite_edades": "8", "pais_origen": "Estados Unidos", "costo_usd": 24.99},
            {"id": "8", "nombre": "Scrabble", "jugadores_min": 2, "jugadores_max": 4, "limite_edades": "10", "pais_origen": "Reino Unido", "costo_usd": 21.99},
            {"id": "9", "nombre": "Uno", "jugadores_min": 2, "jugadores_max": 10, "limite_edades": "7", "pais_origen": "Estados Unidos", "costo_usd": 9.99},
            {"id": "10", "nombre": "The Mind", "jugadores_min": 2, "jugadores_max": 4, "limite_edades": "8", "pais_origen": "Alemania", "costo_usd": 14.99},
        ]
        collection.insert_many(datos_iniciales)  # Inserta los datos iniciales

inicializar_datos()

# -----------------------------------------------------------------------------


# Pagina principal
@app.route('/')
def listar():
    datos = list(collection.find())
    return render_template('index.html', datos=datos)

# Eliminar un elemento
@app.route('/eliminar/<id>', methods=['POST'])
def eliminar(id):
    collection.delete_one({"id": id})      # Busco en base a la id pasada y borro
    return redirect(url_for('listar'))  # Muestro nuevamente con el valor borrado

# Agregar un elemento, nueva pagina
@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nuevo_dato = {      # Nuevo diccionario con lo datos a agregar
            "id": request.form['id'],
            "nombre": request.form['nombre'],
            "jugadores_min": int(request.form['jugadores_min']),
            "jugadores_max": int(request.form['jugadores_max']),
            "limite_edades": request.form['limite_edades'],
            "pais_origen": request.form['pais_origen'],
            "costo_usd": float(request.form['costo_usd']),
        }
        # Hay que chequear que no exista el ID en la base antes de guardarlo
        if collection.find_one({"id": nuevo_dato["id"]}):   # Existe? Entonces error
            return render_template('id_exist.html')
        collection.insert_one(nuevo_dato)
        return redirect(url_for('listar'))
    return render_template('add.html')


# Editar alguna entrada en la tabla
@app.route('/editar/<id>', methods=['GET', 'POST'])
def editar(id):
    # Primer metodo se obtiene la entrada en la base
    if request.method == 'GET':
        juego = collection.find_one({"id": id})
        if juego is None:
            return "Juego no encontrado", 404
        return render_template('edit.html', juego=juego)

    # Posteriormente, se actualiza los datos de la ID correspondiente
    if request.method == 'POST':
        actualizado_dato = {    # Diccionario con los datos nuevos
            "id": request.form['id'],
            "nombre": request.form['nombre'],
            "jugadores_min": int(request.form['jugadores_min']),
            "jugadores_max": int(request.form['jugadores_max']),
            "limite_edades": request.form['limite_edades'],
            "pais_origen": request.form['pais_origen'],
            "costo_usd": float(request.form['costo_usd']),
        } 
        collection.update_one({"id": id}, {"$set": actualizado_dato}) # Actualiza los datos
        return redirect(url_for('listar'))  # Vuelve a "inicio"

# Realizar busqueda, solamente por nombre, pais, costo
@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    if request.method == 'POST':    # Caso donde se pasan los criterios de busqueda
        criterio = request.form.get('criterio')     # Nombre, pais, precio
        query = request.form.get('query')   # Valor a buscar, por ejemplo: "Argentina"

        if criterio == "costo_usd":         # Como costo_usd es un float, hay que convertirlo a tal tipo
            try:
                query = float(query)  # Convertir a numero
                filtro = {criterio: query}
            except ValueError:
                return redirect(url_for('listar'))  # Redirige si no es un numero valido
        else:
            filtro = {criterio: {"$regex": query, "$options": "i"}}

        datos = list(collection.find(filtro))   
        return render_template('index.html', datos=datos, query=query, criterio=criterio)

    return redirect(url_for('listar'))
