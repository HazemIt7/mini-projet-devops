from app import app  # Importer l'instance Flask depuis votre fichier app.py


def test_hello_route():
    """Teste si la route '/' retourne un code 200 OK"""
    client = app.test_client()  # Créer un client de test Flask
    response = client.get('/')  # Faire une requête GET sur '/'

    assert response.status_code == 200  # Vérifier que le statut est 200
    assert b"Hello World" in response.data  # Vérifier que la réponse 
