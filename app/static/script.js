// Evento para buscar un Pokémon
document.getElementById('search-button').addEventListener('click', function () {
    // Obtener el valor de entrada del usuario y convertirlo a minúsculas
    const input = document.getElementById('pokemon-input').value.toLowerCase();
    const url = `http://localhost:8000/api/pokemon/${input}`; // URL de la API para buscar el Pokémon

    // Mostrar mensaje de "Buscando..."
    const pokemonInfo = document.getElementById('pokemon-info');
    pokemonInfo.innerHTML = `<p>Searching...</p>`; // Mensaje que indica que se está buscando

    // Realizar la solicitud a la API
    fetch(url)
        .then(response => {
            // Verificar si la respuesta fue exitosa
            if (!response.ok) {
                throw new Error('Pokémon not found'); // Lanzar un error si el Pokémon no se encuentra
            }
            return response.json(); // Convertir la respuesta a formato JSON
        })
        .then(data => {
            // Si hay sprites, mostrar el primero disponible; de lo contrario, usar la imagen por defecto
            const spriteUrl = data.sprites.length > 0 ? data.sprites[0] : 'default-image.png';
            pokemonInfo.innerHTML = 
                `<h2>${data.name.charAt(0).toUpperCase() + data.name.slice(1)}</h2>
                <img src="${spriteUrl}" alt="${data.name}">
                <p>Abilities: ${data.abilities.join(', ')}</p>
                <p>Pokédex Number: ${data.pokedex_number}</p>
                <p>Type: ${data.types.join(', ')}</p>`; // Mostrar información del Pokémon

            // Mostrar el botón "Actualizar" y ocultar los campos de actualización
            document.getElementById('update-button').style.display = 'block';
            document.getElementById('update-fields').style.display = 'none';
        })
        .catch(error => {
            // Manejo de errores: mostrar el mensaje de error en rojo
            pokemonInfo.innerHTML = `<p style="color: red;">${error.message}</p>`;
            document.getElementById('update-button').style.display = 'none';
            document.getElementById('update-fields').style.display = 'none';
        });
});

// Evento para mostrar los campos de actualización
document.getElementById('update-button').addEventListener('click', function () {
    // Limpiar los campos de entrada para las habilidades y tipo
    document.getElementById('abilities').value = '';
    document.getElementById('types').value = '';
    // Mostrar los campos de actualización
    document.getElementById('update-fields').style.display = 'block';
    document.getElementById('update-button').style.display = 'none'; // Ocultar el botón "Actualizar"
});

// Evento para enviar la actualización
document.getElementById('submit-update').addEventListener('click', function () {
    // Obtener y procesar las habilidades y tipos ingresados por el usuario
    const abilities = document.getElementById('abilities').value.split(',').map(item => item.trim());
    const types = document.getElementById('types').value.split(',').map(item => item.trim());

    // Solicitud para actualizar el Pokémon
    const input = document.getElementById('pokemon-input').value.toLowerCase();
    const url = `http://localhost:8000/api/pokemon/${input}`; // URL de la API para actualizar el Pokémon
    const updateData = {
        abilities: abilities,
        sprites: [], // Mantener los sprites vacíos si no se proporcionan nuevos
        types: types
    };

    // Realizar la solicitud de actualización
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updateData) // Convertir los datos de actualización a formato JSON
    })
    .then(response => {
        // Verificar si la respuesta fue exitosa
        if (!response.ok) {
            throw new Error('Error updating information'); // Lanzar un error si la actualización falla
        }
        return response.json(); // Convertir la respuesta a formato JSON
    })
    .then(data => {
        // Mostrar la información actualizada del Pokémon
        const spriteUrl = data.sprites.length > 0 ? data.sprites[0] : 'default-image.png';
        const pokemonInfo = document.getElementById('pokemon-info');
        pokemonInfo.innerHTML = 
            `<h2>${data.name.charAt(0).toUpperCase() + data.name.slice(1)}</h2>
            <img src="${spriteUrl}" alt="${data.name}">
            <p>Abilities: ${data.abilities.join(', ')}</p>
            <p>Pokédex Number: ${data.pokedex_number}</p>
            <p>Type: ${data.types.join(', ')}</p>`; // Mostrar información actualizada del Pokémon
        document.getElementById('update-fields').style.display = 'none'; // Ocultar los campos de actualización
    })
    .catch(error => {
        // Manejo de errores: mostrar un mensaje de alerta con el error
        alert(error.message);
    });
});
