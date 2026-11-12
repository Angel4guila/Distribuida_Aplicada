import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

URL_CATALOGO = "http://127.0.0.1:5001/catalogo"
URL_PAGOS = "http://127.0.0.1:5002/pagos/procesar"

@app.route("/tienda/juegos", methods=["GET"])
def listar_juegos():
    try:
        respuesta = requests.get(URL_CATALOGO, timeout=5)
        return jsonify(respuesta.json()), respuesta.status_code
    except requests.RequestException:
        return jsonify({"error": "El Servicio de Catálogo no está disponible"}), 503

@app.route("/tienda/comprar", methods=["POST"])
def orquestar_compra():
    datos = request.get_json()
    usuario = datos.get("usuario")
    juego_id = datos.get("juego_id")
    cantidad = datos.get("cantidad", 1)
    saldo = datos.get("saldo")

    # 1. Consultar disponibilidad y precio en el Servicio de Catálogo
    try:
        res_juego = requests.get(f"{URL_CATALOGO}/{juego_id}", timeout=5)
    except requests.RequestException:
        return jsonify({"error": "Error de conexión con el Servicio de Catálogo"}), 503

    if res_juego.status_code != 200:
        return jsonify(res_juego.json()), res_juego.status_code

    juego = res_juego.json()
    if juego["stock"] < cantidad:
        return jsonify({
            "error": f"Stock insuficiente para '{juego['titulo']}'. Disponibles: {juego['stock']}"
        }), 400

    total_pagar = juego["precio"] * cantidad

    # 2. Solicitar cobro al Servicio de Pagos
    payload_pago = {
        "usuario": usuario,
        "monto": total_pagar,
        "saldo_disponible": saldo
    }
    try:
        res_pago = requests.post(URL_PAGOS, json=payload_pago, timeout=5)
    except requests.RequestException:
        return jsonify({"error": "Error de conexión con el Servicio de Pagos"}), 503

    if res_pago.status_code != 200:
        return jsonify(res_pago.json()), res_pago.status_code

    datos_pago = res_pago.json()

    # 3. Descontar unidades en el Servicio de Catálogo
    payload_stock = {"juego_id": juego_id, "cantidad": cantidad}
    res_stock = requests.post(f"{URL_CATALOGO}/descontar", json=payload_stock, timeout=5)

    if res_stock.status_code != 200:
        return jsonify({"error": "Fallo al actualizar el inventario tras el pago"}), 500

    # 4. Emitir respuesta unificada al cliente
    return jsonify({
        "mensaje": "¡Compra realizada con éxito!",
        "ticket": {
            "folio_pago": datos_pago["folio"],
            "cliente": usuario,
            "videojuego": juego["titulo"],
            "cantidad": cantidad,
            "total_pagado": total_pagar,
            "saldo_restante": datos_pago["saldo_restante"]
        }
    }), 200

if __name__ == "__main__":
    print("Iniciando Orquestador SOA en el puerto 5000...")
    app.run(port=5000, debug=False)