from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de datos simulada en memoria
CATALOGO = {
    1: {"id": 1, "titulo": "Elden Ring", "precio": 1200.0, "stock": 5},
    2: {"id": 2, "titulo": "Cyberpunk 2077", "precio": 950.0, "stock": 3},
    3: {"id": 3, "titulo": "Hollow Knight", "precio": 300.0, "stock": 10},
    4: {"id": 4, "titulo": "Baldur's Gate 3", "precio": 1350.0, "stock": 2}
}

@app.route("/catalogo", methods=["GET"])
def obtener_catalogo():
    return jsonify(list(CATALOGO.values())), 200

@app.route("/catalogo/<int:juego_id>", methods=["GET"])
def obtener_juego(juego_id):
    juego = CATALOGO.get(juego_id)
    if not juego:
        return jsonify({"error": "Juego no encontrado"}), 404
    return jsonify(juego), 200

@app.route("/catalogo/descontar", methods=["POST"])
def descontar_stock():
    datos = request.get_json()
    juego_id = datos.get("juego_id")
    cantidad = datos.get("cantidad", 1)

    juego = CATALOGO.get(juego_id)
    if not juego:
        return jsonify({"error": "Juego no encontrado"}), 404
    if juego["stock"] < cantidad:
        return jsonify({"error": "Stock insuficiente"}), 400

    juego["stock"] -= cantidad
    return jsonify({
        "mensaje": "Inventario actualizado",
        "juego": juego
    }), 200

if __name__ == "__main__":
    print("Iniciando Servicio de Catálogo en el puerto 5001...")
    app.run(port=5001, debug=False)