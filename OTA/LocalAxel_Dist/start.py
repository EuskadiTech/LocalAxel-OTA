import utils
import microdot as _1
import pysondb as _2

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
    e = exec(open("OTA_Files/main.py").read())
