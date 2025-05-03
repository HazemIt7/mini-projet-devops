from flask import Flask
import platform

app = Flask(__name__)


@app.route('/')
def hello():
    # Affiche "Hello World from..." et le nom d'hôte du conteneur
    hostname = platform.node()
    return f"Hello World from {hostname}!\n"


if __name__ == "__main__":
    # Écoute sur toutes les interfaces (0.0.0.0) sur le port 5000
    app.run(host='0.0.0.0', port=5000)
