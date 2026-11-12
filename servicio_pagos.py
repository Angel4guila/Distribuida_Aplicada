import uuid
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/pagos/procesar", methods=["POST"])
def procesar_pago():
    datos = request.get_json()
    usuario = datos.get("usuario")
    monto = datos.get("monto", 0.0)
    saldo_disponible = datos.get("saldo_disponible", 0.0)

    if monto <= 0:
        return jsonify({"aprobado": False, "error": "Monto inválido"}), 400

    if saldo_disponible < monto:
        return jsonify({
            "aprobado": False,
            "error": f"Fondos insuficientes. Total: ${monto:.2f}, Disponible: ${saldo_disponible:.2f}"
        }), 402

    folio_transaccion = str(uuid.uuid4())[:8].upper()
    nuevo_saldo = saldo_disponible - monto

    return jsonify({
        "aprobado": True,
        "folio": f"TX-{folio_transaccion}",
        "usuario": usuario,
        "monto_cobrado": monto,
        "saldo_restante": nuevo_saldo
    }), 200

if __name__ == "__main__":
    print("Iniciando Servicio de Pagos en el puerto 5002...")
    app.run(port=5002, debug=False)