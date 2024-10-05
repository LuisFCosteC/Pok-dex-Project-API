from fastapi import FastAPI, HTTPException, Request, Query, Path
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
import asyncio

# -------------------- Creamos la Aplicación -------------------- 
Pokemon_API = FastAPI()

# -------------------- Modificamos el Título -------------------- 
# Establecemos el título y la versión de la API
Pokemon_API.title = "Pokemon API"
Pokemon_API.version = "1.0.0"

# -------------------- Configuramos CORS -------------------- 
Pokemon_API.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las orígenes
    allow_credentials=True,  # Permitir credenciales
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los encabezados
)

# -------------------- Montar Archivos Estáticos -------------------- 
Pokemon_API.mount("/static", StaticFiles(directory="app/static"), name="static")

# -------------------- Configuración de Plantillas -------------------- 
templates = Jinja2Templates(directory="templates")

# -------------------- Endpoint para Servir la Página HTML -------------------- 
@Pokemon_API.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# -------------------- Modelo de Datos -------------------- 
class PokemonBase(BaseModel):
    name: str  # Nombre del Pokémon
    url: str  # URL del Pokémon en la API

class PokemonDetail(BaseModel):
    name: str  # Nombre del Pokémon
    abilities: List[str]  # Habilidades del Pokémon
    pokedex_number: int  # Número de la Pokédex
    sprites: List[str]  # Sprites del Pokémon
    types: List[str]  # Tipos del Pokémon

class PokemonListResponse(BaseModel):
    total_count: int  # Total de Pokémon
    pokemons: List[PokemonDetail]  # Lista de detalles de Pokémon

class PokemonUpdate(BaseModel):
    abilities: List[str] = None  # Habilidades para actualizar (opcional)
    sprites: List[str] = None  # Sprites para actualizar (opcional)
    types: List[str] = None  # Tipos para actualizar (opcional)

# -------------------- Función para Obtener Datos de Pokémon -------------------- 
async def fetch_pokemon_data(pokemon_name_or_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name_or_id}')
        if response.status_code == 200:
            return response.json()  # Retornar datos del Pokémon si la respuesta es exitosa
        else:
            raise HTTPException(status_code=response.status_code, detail="No se pudo obtener la información del Pokémon.")  # Lanzar excepción si hay un error

# -------------------- Endpoint API General -------------------- 
@Pokemon_API.get('/api/general', response_model=PokemonBase, tags=['API general'])
async def api_general(name: str = Query(...)):
    data = await fetch_pokemon_data(name)  # Obtener datos del Pokémon
    return {"name": data["name"], "url": f"https://pokeapi.co/api/v2/pokemon/{data['id']}/"}  # Retornar nombre y URL del Pokémon

# -------------------- Endpoint API Específico -------------------- 
@Pokemon_API.get('/api/pokemon/{pokemon_name_or_id}', response_model=PokemonDetail, tags=['API específico'])
async def api_specific(pokemon_name_or_id: str):
    data = await fetch_pokemon_data(pokemon_name_or_id)  # Obtener datos del Pokémon
    abilities = [ability["ability"]["name"] for ability in data["abilities"]]  # Extraer habilidades
    pokedex_number = data["id"]  # Obtener número de la Pokédex
    sprites = [
        sprite for sprite in [
            data["sprites"]["front_default"],
            data["sprites"]["back_default"]
        ] if sprite is not None  # Filtrar sprites no nulos
    ]
    types = [t["type"]["name"] for t in data["types"]]  # Extraer tipos
    return {
        "name": data["name"],
        "abilities": abilities,
        "pokedex_number": pokedex_number,
        "sprites": sprites,
        "types": types
    }

# -------------------- Endpoint para Editar la Información de un Pokémon -------------------- 
@Pokemon_API.post('/api/pokemon/{pokemon_name_or_id}', response_model=PokemonDetail, tags=['API específico'])
async def update_pokemon(pokemon_name_or_id: str, update_data: PokemonUpdate):
    data = await fetch_pokemon_data(pokemon_name_or_id)  # Obtener datos del Pokémon
    abilities = update_data.abilities if update_data.abilities is not None else [ability["ability"]["name"] for ability in data["abilities"]]  # Actualizar habilidades
    sprites = [
        sprite for sprite in [
            data["sprites"]["front_default"],
            data["sprites"]["back_default"]
        ] if sprite is not None  # Filtrar sprites no nulos
    ]
    types = update_data.types if update_data.types is not None else [t["type"]["name"] for t in data["types"]]  # Actualizar tipos
    return {
        "name": data["name"],
        "abilities": abilities,
        "pokedex_number": data["id"],
        "sprites": sprites,
        "types": types
    }
