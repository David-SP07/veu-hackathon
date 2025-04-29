let map;
let markers = [];

function initMap() {
    // Inicializa el mapa con un centro inicial.
    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 19.355, lng: -99.161 }, // Coordenadas de ejemplo
        zoom: 12
    });

    // Llamada a la API para obtener los centros y colocarlos en el mapa
    fetch('/api/centros')
        .then(response => response.json())
        .then(data => {
            data.forEach(centro => {
                const marker = new google.maps.Marker({
                    position: { lat: centro.latitud, lng: centro.longitud },
                    map: map,
                    title: centro.nombre
                });

                markers.push(marker);

                // Mostrar información cuando se hace clic en el marcador
                marker.addListener('click', () => {
                    showCentroInfo(centro);
                });
            });
        })
        .catch(error => console.error('Error al cargar los centros:', error));
}

function showCentroInfo(centro) {
    // Actualiza la información en la vista
    document.getElementById('centro-info').innerHTML = `
        <p><strong>${centro.nombre}</strong></p>
        <p>Distancia: <span id="distance">3 km</span></p>
        <p>Unidades disponibles: <span id="available-units">03</span></p>
        <p>Servicio de mantenimiento: <span id="maintenance-status">${centro.servicio_mantenimiento || 'Disponible'}</span></p>
    `;
}

function verMisTurnos() {
    // Redirige al usuario a la página para ver sus turnos
    window.location.href = '/mis-turnos';
}

function reservarTurno() {
    // Redirige al usuario a la página para reservar un turno
    window.location.href = '/reservar-turno';
}

document.addEventListener("DOMContentLoaded", () => {
    initMap();
});