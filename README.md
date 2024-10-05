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
> **Link to file:** `app/templates/index.html`.

### **2. CSS (`styles.css`)**

The CSS file provides styles for the web page. It includes:

- Styles for the body, container, buttons and inputs.
- Custom wallpaper.
- Responsive styles to ensure good display on different screen sizes.

> [!NOTE]
> **Link to file:** `app/static/styles.css`.

### **3. JavaScript (`script.js`)**

The JavaScript file handles the user interaction logic. It includes:

- Functionality to search for Pokémon through the API by clicking the search button.
- Error handling in case the Pokémon is not found.
- Functionality to display and send Pokémon information updates.

> [!NOTE]
> **Link to file:** `app/static/script.js`.

### **4. Backend (`main.py`)**

This file defines the FastAPI application and its endpoints. It contains:

- CORS configuration to allow requests from any source.
- Endpoints to look up Pokémon information and update it.
- Functions to get Pokémon data from the external API.

> [!NOTE]
> **Link to file:** `main.py`.

### **5. Testing (`test_main.py`)**

The test file contains test cases for API endpoints. It uses Pytest to verify:

- The correct general API response.
- The specific response for a given Pokémon.
- The response when requesting a Pokémon that does not exist.

> [!NOTE]
> **Link to file:** `test_main.py`

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

4. Activate the virtual environment.

   ````bash
   Test_Back_Py scripts activate

5. Install the dependencies:

   ````bash
   pip install fastapi uvicorn httppx pytest pydantic jinja2 

6. Run the main.py file

   ````bash
   uvicorn app.main:Pokemon_API --reload

## Presentation of the site

### **Main presentation of the site**
![image](https://github.com/user-attachments/assets/926648a6-4d91-4d53-8630-68125d246960)

### **Enter the Pokédex number or your name to perform the search**
![image](https://github.com/user-attachments/assets/bb0fba43-8e42-4687-9c4b-9082b09628b3)

### **If the search was successful, it will show the pokemon information.**
![image](https://github.com/user-attachments/assets/985ab92e-0061-4de8-a499-97b2e438cd35)

### **If the search was unsuccessful, it will display the following message “Pokémon not found”.**
![image](https://github.com/user-attachments/assets/9671a36f-5ccc-4cde-8b69-ebe8cad31671)

### **Pressing the Update Information button will show a form to perform the update. **
![image](https://github.com/user-attachments/assets/22e26bb0-6b46-4030-a5df-038f35aeb69c)

### **Enter the information you want to update and then click the Submit Update button to view the change.**
![image](https://github.com/user-attachments/assets/54eaba39-8f1e-469b-a1e9-6e665391b27b)

### **After clicking on the Send Update button we will be able to see the updated information.**
![image](https://github.com/user-attachments/assets/eef36745-aabc-47ce-9b0f-91a7d0b87856)
