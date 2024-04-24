import utils

if __name__ == "__main__":
    utils.ota_updater()
    print("\n" * 6)
    print("==============================")
    print("   LocalAxel se ha iniciado   ")
    print("==============================")
    print("                              ")
    print("  Abre la siguiente url para  ")
    print("            entrar            ")
    print("                              ")
    print("                              ")
    print(" http://127.0.0.1:17170/      ")
    print("==============================")
    print("                              ")

    __import__("main").app.run(host="0.0.0.0", port=17170, debug=False)
