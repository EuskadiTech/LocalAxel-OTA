import utils

if __name__ == "__main__":
    utils.ota_updater()
    __import__("main").app.run(host="0.0.0.0", port=17170, debug=False)
