import main
import utils

if __name__ == "__main__":
    utils.ota_updater()
    main.app.run(host="0.0.0.0", port=17170, debug=False)
