# Pokedex API Project

This project is a Pokédex application that allows users to look up information about Pokémon using their number in the Pokédex or their name. The application uses FastAPI for the backend and provides an interactive user interface using HTML, CSS and JavaScript.

# Project Structure

The project consists of the following main files:

### **1. HTML (`index.html`)**

The HTML file defines the structure and content of the web page. It contains:

- An input field for the Pokédex number or Pokémon name.
- A button to search for Pokémon.
- An area to display the information of the searched Pokémon.
- A button and a form to update the Pokémon's information.

> [!NOTE]
> **Link to file:**
> ```` bash
> app/templates/index.html
> ````

### **2. CSS (`styles.css`)**

The CSS file provides styles for the web page. It includes:

- Styles for the body, container, buttons and inputs.
- Custom wallpaper.
- Responsive styles to ensure good display on different screen sizes.

> [!NOTE]
> **Link to file:**
> ```` bash
> app/static/styles.css
> ````

### **3. JavaScript (`script.js`)**

The JavaScript file handles the user interaction logic. It includes:

- Functionality to search for Pokémon through the API by clicking the search button.
- Error handling in case the Pokémon is not found.
- Functionality to display and send Pokémon information updates.

> [!NOTE]
> **Link to file:**
> ```` bash
> app/static/script.js
> ````

### **4. Backend (`main.py`)**

This file defines the FastAPI application and its endpoints. It contains:

- CORS configuration to allow requests from any source.
- Endpoints to look up Pokémon information and update it.
- Functions to get Pokémon data from the external API.

> [!NOTE]
> **Link to file:**
> ```` bash
> main.py
> ````

### **5. Testing (`test_main.py`)**

The test file contains test cases for API endpoints. It uses Pytest to verify:

- The correct general API response.
- The specific response for a given Pokémon.
- The response when requesting a Pokémon that does not exist.

> [!NOTE]
> **Link to file:**
> ```` bash
> test_main.py
> ````

## Requirements
> [!IMPORTANT]
> These are the requirements you need to have

- Python 3.x
- FastAPI
- Uvicorn
- HTTPX
- pytest
- pydantic
- jinja2

## Installation

1. Clone this repository.
Navigate to the project directory.
3. Create a virtual environment.

   ````bash
   python3.12 -m venv Test_Back_Py
   ````

4. Activate the virtual environment.

   ````bash
   Test_Back_Py scripts activate
   ````

5. Install the dependencies:

   ````bash
   pip install fastapi uvicorn httppx pytest pydantic jinja2
   ````

6. Run the main.py file

   ````bash
   uvicorn app.main:Pokemon_API --reload
   ````

## Explanation of how the api works
This code in FastAPI creates an API that interacts with Pokémon data from the PokeAPI.

### **1. Imports**
1. FastAPI, HTTPException, Request, Query, Path: Used to build the endpoints and handle HTTP requests.
2. StaticFiles: Allows us to serve static files (CSS, JavaScript, images).
3. CORSMiddleware: Used to manage HTTP access control (CORS), allowing clients to access the API from different sources.
4. Pydantic (BaseModel): It is the data model used to validate inputs and outputs.
5. httpx: It is the asynchronous HTTP client to make requests to other APIs.
6. Jinja2Templates: Allows us to render HTML templates with Jinja2.
7. asyncio: It is the library for asynchronous programming in Python.

### **2. Creation of the FastAPI application**
   ````bash
   Pokemon_API = FastAPI()
   ````
   This creates an instance of the FastAPI application named Pokemon_API.

### **3. Customizing the Title and Version**
   ````bash
   Pokemon_API.title = "Pokemon API"
   Pokemon_API.version = "1.0.0"
   ````
   The API title and version are set, which will appear in the OpenAPI (Swagger) documentation.

### **4. CORS configuration**
   ````bash
   Pokemon_API.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir todas las orígenes
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
   )
   ````
   CORS middleware is configured to allow requests from any source, allowing credentials and all HTTP methods and headers.

### **5. Mount Static Files**
   ````bash
   Pokemon_API.mount("/static", StaticFiles(directory="app/static"), name="static")
   ````
   Static files (images, CSS, etc.) are set up here in the app/static directory and can be accessed from the /static path.

### **6. Template Configuration**
   ````bash
   templates = Jinja2Templates(directory="templates")
   ````
   Configures the use of HTML templates found in the templates directory.

### **7. Endpoint to serve an HTML page**
   ````bash
   @Pokemon_API.get("/", response_class=HTMLResponse)
   async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
   ````
   This endpoint returns the HTML page index.html when a user accesses the root (/) of the application.
   
### **8. Data Models with Pydantic**
- Several data models are defined to structure the responses and requests:
- PokemonBase: Represents the name and URL of the Pokémon.
- PokemonDetail: Includes details such as name, abilities, Pokédex number, sprites and types.
- PokemonListResponse: Used for Pokémon lists, with the total number and details of the Pokémon.
- PokemonUpdate: Model to update the abilities, sprites or types of a Pokémon.

### **9. Function to get data from external API (PokeAPI)**
   ````bash
   async def fetch_pokemon_data(pokemon_name_or_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name_or_id}')
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="No se pudo obtener la información del Pokémon.")
   ````
This function makes an asynchronous HTTP request to the PokeAPI to get data from a specific Pokémon, using its name or ID. If the request succeeds, it returns the data in JSON format. If not, it throws an exception with the corresponding error code.

### **10. Endpoint to obtain basic information about a Pokémon.**
   ````bash
   @Pokemon_API.get('/api/general', response_model=PokemonBase, tags=['API general'])
   async def api_general(name: str = Query(...)):
    data = await fetch_pokemon_data(name)
    return {"name": data["name"], "url": f"https://pokeapi.co/api/v2/pokemon/{data['id']}/"}
   ````
This endpoint receives a Pokémon name as a query and returns its API name and URL in simplified format.

### **11. Endpoint to obtain specific details of a Pokémon.**
   ````bash
   @Pokemon_API.get('/api/pokemon/{pokemon_name_or_id}', response_model=PokemonDetail, tags=['API específico'])
   async def api_specific(pokemon_name_or_id: str):
    data = await fetch_pokemon_data(pokemon_name_or_id)
    abilities = [ability["ability"]["name"] for ability in data["abilities"]]
    pokedex_number = data["id"]
    sprites = [sprite for sprite in [data["sprites"]["front_default"], data["sprites"]["back_default"]] if sprite is not None]
    types = [t["type"]["name"] for t in data["types"]]
    return {"name": data["name"], "abilities": abilities, "pokedex_number": pokedex_number, "sprites": sprites, "types": types}
   ````
This endpoint returns more complete details of a Pokémon, such as abilities, Pokédex number, sprites and types.

### **12. Endpoint to update information of a Pokémon.**
   ````bash
   @Pokemon_API.post('/api/pokemon/{pokemon_name_or_id}', response_model=PokemonDetail, tags=['API específico'])
   async def update_pokemon(pokemon_name_or_id: str, update_data: PokemonUpdate):
    data = await fetch_pokemon_data(pokemon_name_or_id)
    abilities = update_data.abilities if update_data.abilities is not None else [ability["ability"]["name"] for ability in data["abilities"]]
    sprites = [sprite for sprite in [data["sprites"]["front_default"], data["sprites"]["back_default"]] if sprite is not None]
    types = update_data.types if update_data.types is not None else [t["type"]["name"] for t in data["types"]]
    return {"name": data["name"], "abilities": abilities, "pokedex_number": data["id"], "sprites": sprites, "types": types}
   ````
This endpoint allows you to update abilities, sprites and types of a specific Pokémon. If no update data is provided, the original data is kept.

## Presentation of the site

### **Main presentation of the site**
![image](https://github.com/user-attachments/assets/926648a6-4d91-4d53-8630-68125d246960)

### **Enter the Pokédex number or your name to perform the search**
![image](https://github.com/user-attachments/assets/bb0fba43-8e42-4687-9c4b-9082b09628b3)

### **If the search was successful, it will show the pokemon information.**
![image](https://github.com/user-attachments/assets/985ab92e-0061-4de8-a499-97b2e438cd35)

### **If the search was unsuccessful, it will display the following message “Pokémon not found”.**
![image](https://github.com/user-attachments/assets/9671a36f-5ccc-4cde-8b69-ebe8cad31671)

### **Pressing the Update Information button will show a form to perform the update.**
![image](https://github.com/user-attachments/assets/22e26bb0-6b46-4030-a5df-038f35aeb69c)

### **Enter the information you want to update and then click the Submit Update button to view the change.**
![image](https://github.com/user-attachments/assets/54eaba39-8f1e-469b-a1e9-6e665391b27b)

### **After clicking on the Send Update button we will be able to see the updated information.**
![image](https://github.com/user-attachments/assets/eef36745-aabc-47ce-9b0f-91a7d0b87856)
