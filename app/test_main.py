import pytest
from fastapi.testclient import TestClient
from main import Pokemon_API

# Creamos una instancia del cliente de pruebas para nuestra API
client = TestClient(Pokemon_API)

def test_api_general():
    """Prueba para el endpoint API general."""
    # Realizamos una solicitud GET al endpoint general con el nombre "bulbasaur"
    response = client.get("/api/general?name=bulbasaur")
    # Verificamos que el código de estado de la respuesta sea 200 (OK)
    assert response.status_code == 200
    # Verificamos que la respuesta JSON contenga el nombre y la URL correctos
    assert response.json() == {"name": "bulbasaur", "url": "https://pokeapi.co/api/v2/pokemon/1/"}

def test_api_especifico():
    """Prueba para el endpoint API específico."""
    # Realizamos una solicitud GET al endpoint específico con el ID de Bulbasaur
    response = client.get("/api/pokemon/1")  # Pokémon Bulbasaur
    # Verificamos que el código de estado de la respuesta sea 200 (OK)
    assert response.status_code == 200
    data = response.json()
    # Verificamos que el nombre del Pokémon sea "bulbasaur"
    assert data["name"] == "bulbasaur"
    # Verificamos que la respuesta contenga las claves necesarias
    assert "abilities" in data
    assert "pokedex_number" in data
    assert "sprites" in data
    assert "types" in data

def test_api_especifico_not_found():
    """Prueba para el endpoint API específico con un ID no válido."""
    # Realizamos una solicitud GET al endpoint específico con un ID que no existe
    response = client.get("/api/pokemon/9999")  # ID que no existe
    # Verificamos que el código de estado de la respuesta sea 404 (No encontrado)
    assert response.status_code == 404
