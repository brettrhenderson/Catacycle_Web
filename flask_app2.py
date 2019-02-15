from app import app
import logging

logging.basicConfig(level=logging.WARNING)

if __name__ == "__main__":
    app.debug = True
    app.run()
