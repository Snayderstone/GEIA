<script>
  import { onMount } from 'svelte';
  import Chart from 'chart.js/auto'; // Importa Chart.js

  let history = [];
  let columns = [
    { key: 'date', label: 'Fecha' },
    { key: 'interventionDate', label: 'Fecha de Intervención' },
    { key: 'eventType', label: 'Tipo de Evento' },
    { key: 'originalColumn', label: 'Nombre de la Columna Original' },
    { key: 'explanationGroq', label: 'Explicación llama 3-8b-8192' },
    { key: 'explanationOpenAI', label: 'Explicación gpt-3.5-turbo' },
    { key: 'currentAverage', label: 'Promedio Actual' },
    { key: 'predictedAverage', label: 'Predicción Promedio' },
    { key: 'absoluteEffect', label: 'Efecto Absoluto Promedio' }
  ];
  let selectedColumn = 'date'; // Columna predeterminada
  let message = ''; // Mensaje de estado para mostrar información al usuario

  // Función para extraer el valor numérico antes del paréntesis y convertirlo a float
  function extractValue(value) {
    const match = value.match(/^(\d+(\.\d+)?)/);
    return match ? parseFloat(match[0]) : 0;
  }

  function clearHistory() {
    if (history.length === 0) {
      message = 'El historial ya se encuentra vacío.';
      return;
    }

    // Confirmar con el usuario antes de borrar
    const userConfirmed = window.confirm('¿Estás seguro de que deseas eliminar el historial? Esta acción no se puede deshacer.');

    if (userConfirmed) {
      localStorage.removeItem('history'); // Elimina el historial del localStorage
      history = []; // Vacía el historial en la aplicación
      message = 'Historial borrado exitosamente.';
    } else {
      message = 'El historial no ha sido borrado.';
    }
  }

  onMount(() => {
    // Cargar el historial del localStorage cuando el componente se monta
    history = JSON.parse(localStorage.getItem('history')) || [];

    // Esperar un breve momento para que el DOM se actualice antes de crear gráficos
    setTimeout(() => {
      history.forEach((record, index) => {
        const canvas = document.getElementById(`chart-${index}`);
        if (canvas) {
          const ctx = canvas.getContext('2d');

          // Definir colores diferentes para cada barra
          const colors = [
            'rgba(75, 192, 192, 0.8)',  // Color para "Valor Promedio Actual Con"
            'rgba(153, 102, 255, 0.8)',  // Color para "Valor Promedio Predicho Sin"
            'rgba(255, 205, 86, 0.8)'    // Color para "Impacto Promedio"
          ];
          const borderColors = [
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 205, 86, 1)'
          ];

          // Crear un gráfico horizontal de barras con títulos y leyendas personalizadas
          new Chart(ctx, {
            type: 'bar', // Tipo de gráfico horizontal
            data: {
              labels: [
                'Valor Promedio Actual Con ' + record.payload.eventType,
                'Valor Promedio Predicho Sin ' + record.payload.eventType,
                'Impacto Promedio'
              ],
              datasets: [{
                label: 'Intervención: ' + record.payload.eventType,
                data: [
                  extractValue(record.result['Promedio Actual']),
                  extractValue(record.result['Predicción Promedio']),
                  extractValue(record.result['Efecto Absoluto Promedio'])
                ],
                backgroundColor: colors,
                borderColor: borderColors,
                borderWidth: 1
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              indexAxis: 'y', // Configura el gráfico para que sea horizontal
              scales: {
                x: {
                  beginAtZero: true,
                  ticks: {
                    callback: function (value) {
                      return value;
                    }
                  }
                },
                y: {
                  beginAtZero: true
                }
              },
              plugins: {
                legend: {
                  display: true,
                  position: 'top'
                },
                title: {
                  display: true,
                  text: 'Gráfico de Intervención: ' + record.payload.eventType
                }
              }
            }
          });
        }
      });
    }, 100); // Ajusta el tiempo si es necesario
  });
  
</script>


<h1>Historial de Intervenciones</h1>

<!-- Botón para borrar el historial -->
<button class="button" on:click={clearHistory}>Borrar Historial</button>
<!-- Mensaje de estado -->
{#if message}
  <p class="message">{message}</p>
{/if}

<!-- Radio buttons para seleccionar columna visible -->
<div class="header-controls">
  <p>Selecciona la columna a mostrar:</p>
  {#each columns as column}
    <label>
      <input type="radio" name="column" value={column.key} bind:group={selectedColumn}>
      {column.label}
    </label>
  {/each}
</div>

{#if history.length === 0}
  <p class="message">No hay registros en el historial.</p>
{:else}
  <table>
    <thead>
      <tr>
        {#if selectedColumn === 'date'}<th>Fecha</th>{/if}
        {#if selectedColumn === 'interventionDate'}<th>Fecha de Intervención</th>{/if}
        {#if selectedColumn === 'eventType'}<th>Tipo de Evento</th>{/if}
        {#if selectedColumn === 'originalColumn'}<th>Nombre de la Columna Original</th>{/if}
        {#if selectedColumn === 'explanationGroq'}<th>Explicación llama 3-8b-8192</th>{/if}
        {#if selectedColumn === 'explanationOpenAI'}<th>Explicación gpt-3.5-turbo</th>{/if}
        {#if selectedColumn === 'currentAverage'}<th>Promedio Actual</th>{/if}
        {#if selectedColumn === 'predictedAverage'}<th>Predicción Promedio</th>{/if}
        {#if selectedColumn === 'absoluteEffect'}<th>Efecto Absoluto Promedio</th>{/if}
        <th>Gráfico</th>
      </tr>
    </thead>
    <tbody>
      {#each history as record, index}
        <tr>
          {#if selectedColumn === 'date'}<td>{new Date(record.timestamp).toLocaleString()}</td>{/if}
          {#if selectedColumn === 'interventionDate'}<td>{record.payload.interventionDate}</td>{/if}
          {#if selectedColumn === 'eventType'}<td>{record.payload.eventType}</td>{/if}
          {#if selectedColumn === 'originalColumn'}<td>{record.payload.originalColumn}</td>{/if}
          {#if selectedColumn === 'explanationGroq'}<td>{record.result['Explicación llama 3-8b-8192']}</td>{/if}
          {#if selectedColumn === 'explanationOpenAI'}<td>{record.result['Explicación gpt-3.5-turbo']}</td>{/if}
          {#if selectedColumn === 'currentAverage'}<td>{record.result['Promedio Actual']}</td>{/if}
          {#if selectedColumn === 'predictedAverage'}<td>{record.result['Predicción Promedio']}</td>{/if}
          {#if selectedColumn === 'absoluteEffect'}<td>{record.result['Efecto Absoluto Promedio']}</td>{/if}
          <td>
            <div class="chart-container">
              <canvas id={`chart-${index}`}></canvas>
            </div>
          </td>
        </tr>
      {/each}
    </tbody>
  </table>
{/if}



<style>
  table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 20px;
  }
  th, td {
    padding: 10px;
    border: 1px solid #ddd;
    text-align: left;
  }
  td:first-child {
    max-width: 450px; /* Ajusta el valor a lo que necesites */
    white-space: normal; /* Permite el salto de línea */
    word-wrap: break-word; /* Ajusta las palabras largas */
}

  th {
    background-color: #f4f4f4;
  }
  .chart-container {
    width: 100%;
    height: 200px; /* Altura fija para el gráfico */
  }
  canvas {
    width: 100% !important; /* Asegura que el canvas sea responsivo */
    height: 100% !important; /* Asegura que el canvas se ajuste a la altura del contenedor */
  }
  .header-controls {
    margin-bottom: 10px;
  }
  .header-controls label {
    margin-right: 20px;
  }

  .button {
		background:
			linear-gradient(140.14deg, #ec540e 15.05%, #d6361f 114.99%) padding-box,
			linear-gradient(142.51deg, #ff9465 8.65%, #af1905 88.82%) border-box;
		border-radius: 7px;
		border: 2px solid transparent;
		padding: 8px 16px;
		font-size: 20px;
		color: white;
		cursor: pointer;
		transition: all 0.3s;
		display: inline-block block;
	}

  .button:hover {
		background:
			linear-gradient(140.14deg, #d6361f 15.05%, #ec540e 114.99%) padding-box,
			linear-gradient(142.51deg, #af1905 8.65%, #ff9465 88.82%) border-box;
		transform: scale(1.05);
	}

  .message {
    color: #d6361f; /* Color de mensaje de error */
    margin-top: 10px;
    font-weight: bold;
    text-align: center;
    font-size: 20px;
  }
  
</style>