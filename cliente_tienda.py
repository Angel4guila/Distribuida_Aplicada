import requests

URL_ORQUESTADOR = "http://127.0.0.1:5000/tienda"

def mostrar_catalogo():
    try:
        res = requests.get(f"{URL_ORQUESTADOR}/juegos", timeout=5)
        if res.status_code != 200:
            print("\n[!] Error:", res.json().get("error"))
            return
        juegos = res.json()
        print("\n" + "="*52)
        print(f"{'ID':<4} | {'TÍTULO':<22} | {'PRECIO':<10} | {'STOCK':<6}")
        print("-"*52)
        for j in juegos:
            print(f"{j['id']:<4} | {j['titulo']:<22} | ${j['precio']:<9.2f} | {j['stock']:<6}")
        print("="*52)
    except requests.RequestException:
        print("\n[!] No se pudo conectar con el Orquestador SOA.")

def comprar_juego(usuario, saldo):
    try:
        juego_id = int(input("\nIngresa el ID del videojuego a comprar: "))
        cantidad = int(input("Ingresa la cantidad: "))
        if cantidad <= 0:
            print("[!] La cantidad debe ser mayor a 0.")
            return saldo
    except ValueError:
        print("[!] Entrada inválida. Ingresa números enteros.")
        return saldo

    payload = {
        "usuario": usuario,
        "juego_id": juego_id,
        "cantidad": cantidad,
        "saldo": saldo
    }

    try:
        res = requests.post(f"{URL_ORQUESTADOR}/comprar", json=payload, timeout=5)
        datos = res.json()

        if res.status_code == 200:
            ticket = datos["ticket"]
            print("\n" + "*"*45)
            print("          TICKET DE COMPRA - SOA")
            print("*"*45)
            print(f"Folio de Transacción : {ticket['folio_pago']}")
            print(f"Cliente              : {ticket['cliente']}")
            print(f"Juego adquirido      : {ticket['videojuego']} (x{ticket['cantidad']})")
            print(f"Total pagado         : ${ticket['total_pagado']:.2f}")
            print(f"Saldo restante       : ${ticket['saldo_restante']:.2f}")
            print("*"*45)
            return ticket["saldo_restante"]
        else:
            print(f"\n[X] Operación rechazada: {datos.get('error')}")
            return saldo
    except requests.RequestException:
        print("\n[!] Error al conectar con el Orquestador SOA.")
        return saldo

def main():
    print("=== BIENVENIDO A LA TIENDA DE VIDEOJUEGOS (SOA) ===")
    usuario = input("Ingresa tu nombre de usuario: ").strip() or "Gamer_01"
    try:
        saldo = float(input("Ingresa tu saldo inicial ($): "))
    except ValueError:
        saldo = 2500.0
        print(f"Saldo asignado por defecto: ${saldo:.2f}")

    while True:
        print(f"\nUsuario: {usuario} | Saldo disponible: ${saldo:.2f}")
        print("1. Ver catálogo de videojuegos")
        print("2. Comprar un videojuego")
        print("3. Recargar saldo")
        print("4. Salir")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            mostrar_catalogo()
        elif opcion == "2":
            saldo = comprar_juego(usuario, saldo)
        elif opcion == "3":
            try:
                abono = float(input("Monto a recargar ($): "))
                if abono > 0:
                    saldo += abono
                    print(f"[✓] Nuevo saldo: ${saldo:.2f}")
            except ValueError:
                print("[!] Monto inválido.")
        elif opcion == "4":
            print("¡Gracias por visitar la tienda!")
            break
        else:
            print("[!] Opción no válida.")

if __name__ == "__main__":
    main()