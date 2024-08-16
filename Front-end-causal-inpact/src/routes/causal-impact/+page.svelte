<script>
	import Papa from 'papaparse';
	import { writable } from 'svelte/store';
	import { Chart, registerables } from 'chart.js';
	import 'chartjs-adapter-date-fns';
	import annotationPlugin from 'chartjs-plugin-annotation';
	import DataTable from './DataTable.svelte';
	import { marked } from 'marked'; // Importa la biblioteca marked
	Chart.register(...registerables, annotationPlugin);
	let barChart; // Declare a variable to store the bar chart instance
	let pieChart; // Declare a variable to store the pie chart instance
	let data = [];
	let dateColumn = '';
	let originalColumn = '';
	let interventionDate = '';
	let controlColumns = '';
	let eventType = '';
	let isFileUploaded = writable(false);
	let chart;
	let chartCanvas;
	let apiResults = writable(null); // Variable para almacenar resultados de la API
	let isLoading = writable(false); // Variable para controlar el spinner
	let isModalOpen = writable(false); // Controla la apertura del modal
	let newEventType = ''; // Almacena el nuevo tipo de evento
	let showGenerateButton = writable(false); // Variable para controlar la visibilidad del botón

	// Función para cargar el archivo seleccionado
	function handleFileUpload(event) {
		const selectedFile = event.target.files[0];
		if (selectedFile) {
			const reader = new FileReader();
			reader.onload = function (e) {
				if (selectedFile.type === 'text/csv') {
					Papa.parse(e.target.result, {
						header: true,
						skipEmptyLines: true,
						complete: function (result) {
							data = result.data;
							isFileUploaded.set(true);
							console.log('CSV file loaded successfully.');
							console.log('Columns:', Object.keys(data[0] || {}));
						}
					});
				} else if (
					selectedFile.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
				) {
					import('xlsx').then(({ read, utils }) => {
						const workbook = read(e.target.result, { type: 'binary' });
						const sheetName = workbook.SheetNames[0];
						const sheet = workbook.Sheets[sheetName];
						data = utils.sheet_to_json(sheet, { header: 1 });
						isFileUploaded.set(true);
						console.log('Excel file loaded successfully.');
						console.log('Columns:', data[0] || []);
					});
				} else {
					alert('Unsupported file type. Please upload a CSV or Excel file.');
				}
			};
			if (selectedFile.type === 'text/csv') {
				reader.readAsText(selectedFile);
			} else if (
				selectedFile.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
			) {
				reader.readAsBinaryString(selectedFile);
			} else {
				alert('Unsupported file type. Please upload a CSV or Excel file.');
			}
		} else {
			alert('No file selected.');
		}
	}

	// Función para validar los datos de entrada
	function validateInputs() {
		if (dateColumn && originalColumn && controlColumns && interventionDate && eventType) {
			if (!data.length) {
				alert('Por favor, cargue un archivo primero.');
				return;
			}

			const headers = Object.keys(data[0] || {});
			console.log('Available columns:', headers);

			if (!headers.includes(dateColumn)) {
				alert(`La columna '${dateColumn}' no está en los datos.`);
				return;
			}

			if (!headers.includes(originalColumn)) {
				alert(`La columna '${originalColumn}' no está en los datos.`);
				return;
			}

			const controlCols = controlColumns.split(',').map((col) => col.trim());
			const missingControlCols = controlCols.filter((col) => !headers.includes(col));
			if (missingControlCols.length > 0) {
				alert(
					`La columna o las columnas de control no están con esos nombres en los datos: ${missingControlCols.join(', ')}`
				);
				return;
			}

			const isInterventionDatePresent = data.some((row) => {
				const rowDate = new Date(row[dateColumn]);
				return rowDate.toISOString().slice(0, 10) === interventionDate;
			});

			if (!isInterventionDatePresent) {
				alert(
					`La fecha de intervención ${interventionDate} no está en los datos de la columna '${dateColumn}' o asegúrese de que la fecha esté en formato DD-MM-YYYY.`
				);
				return;
			}

			alert('Datos validados correctamente.');
			displayData();
			showGenerateButton.set(true); // Mostrar el botón después de validar y visualizar
		} else {
			alert('Por favor, complete todos los campos o cargue un archivo.');
		}
	}

	// Para recorrer los datos del archivo
	function displayData() {
		if (chart) {
			chart.destroy();
		}

		// Extraer las etiquetas (fechas) y los datasets
		const labels = data.map((row) => new Date(row[dateColumn])); // Usar la columna de fechas especificada
		const datasets = [];

		if (data.length > 0) {
			// Verificar si la columna original está presente en los datos
			if (data[0].hasOwnProperty(originalColumn)) {
				const originalData = data.map((row) => row[originalColumn]);
				datasets.push({
					label: `Original Column: ${originalColumn}`,
					data: originalData,
					borderColor: 'blue',
					borderWidth: 2,
					fill: false
				});
			} else {
				console.warn(`La columna '${originalColumn}' no se encuentra en los datos.`);
			}

			// Procesar las columnas de control
			const controlCols = controlColumns.split(',').map((col) => col.trim());
			controlCols.forEach((col) => {
				if (data[0].hasOwnProperty(col)) {
					const controlData = data.map((row) => row[col]);
					datasets.push({
						label: `Control Column: ${col}`,
						data: controlData,
						borderColor: 'green',
						borderWidth: 2,
						fill: false
					});
				} else {
					console.warn(`La columna de control '${col}' no se encuentra en los datos.`);
				}
			});
		} else {
			console.error('No data available to display.');
			return;
		}

		// Crear el gráfico de líneas
		if (chartCanvas) {
			try {
				chart = new Chart(chartCanvas, {
					type: 'line',
					data: {
						labels: labels,
						datasets: datasets
					},
					options: {
						responsive: true,
						maintainAspectRatio: false,
						scales: {
							x: {
								type: 'time',
								time: {
									unit: 'day'
								},
								title: {
									display: true,
									text: 'Date'
								}
							},
							y: {
								title: {
									display: true,
									text: 'Value'
								}
							}
						},
						plugins: {
							annotation: {
								annotations: {
									eventLine: {
										type: 'line',
										xMin: new Date(interventionDate).getTime(),
										xMax: new Date(interventionDate).getTime(),
										borderColor: 'red',
										borderWidth: 2,
										label: {
											content: eventType,
											enabled: true,
											position: 'top'
										}
									}
								}
							}
						}
					}
				});
				console.log('Chart created successfully.');
			} catch (error) {
				console.error('Error creating chart:', error);
			}
		} else {
			console.error('Chart canvas not found.');
		}
	}

	// ... Función para enviar datos al backend: ...------------------------------------------------------
	let loadingExplanationGroq = writable(''); // Para la explicación en carga
	let loadingExplanationOpenAI = writable(''); // Para la explicación de OpenAI en carga

	async function sendDataToBackend() {
		if (
			dateColumn &&
			originalColumn &&
			controlColumns &&
			interventionDate &&
			eventType &&
			data.length > 0
		) {
			const payload = {
				dateColumn: {
					name: dateColumn,
					data: data.map((row) => row[dateColumn])
				},
				originalColumn: {
					name: originalColumn,
					data: data.map((row) => row[originalColumn])
				},
				controlColumns: controlColumns.split(',').map((col) => ({
					name: col.trim(),
					data: data.map((row) => row[col.trim()])
				})),
				interventionDate,
				eventType
			};

			try {
				isLoading.set(true); // Mostrar el spinner

				const response = await fetch(
					'https://back-end-causal-impact-production.up.railway.app/api/impact',
					{
						method: 'POST',
						headers: {
							'Content-Type': 'application/json'
						},
						body: JSON.stringify(payload)
					}
				);

				if (!response.ok) {
					throw new Error('Network response was not ok');
				}

				const result = await response.json();

				apiResults.set(result); // Guardar el resultado de la API en la variable de estado

				// Extraer los datos necesarios del resultado y guardarlos en el historial
				const record = {
					timestamp: new Date().toISOString(),
					payload: {
						interventionDate: payload.interventionDate,
						eventType: payload.eventType,
						originalColumn: payload.originalColumn.name
					},
					result: {
						'Promedio Actual': result.summary['Promedio Actual'],
						'Predicción Promedio': result.summary['Predicción Promedio'],
						'Efecto Absoluto Promedio': result.summary['Efecto Absoluto Promedio'],
						'Explicación llama 3-8b-8192': result.groq['explanation'],
						'Explicación gpt-3.5-turbo': result.openai['explanation']
					}
				};

				// Guardar el registro en el localStorage
				const storedHistory = JSON.parse(localStorage.getItem('history')) || [];
				storedHistory.push(record);
				localStorage.setItem('history', JSON.stringify(storedHistory));
				console.log('Histori' + record);

				// Simular la carga de la explicación
				loadingExplanationGroq.set(''); // Reiniciar el estado de la explicación
				loadingExplanationOpenAI.set(''); // Reiniciar el estado de la explicación

				const explanationGroq = result.groq.explanation || '';
				const explanationOpenAI = result.openai.explanation || '';

				let index = 0;
				const typingSpeed = 25; // Velocidad de escritura en milisegundos mayor valor mas leto el texto

				const interval = setInterval(() => {
					if (index < explanationGroq.length || index < explanationOpenAI.length) {
						// Actualizar loadingExplanation si aún hay caracteres por agregar
						if (index < explanationGroq.length) {
							loadingExplanationGroq.update((prev) => prev + explanationGroq[index]);
						}
						// Actualizar loadingExplanationOpenAI si aún hay caracteres por agregar
						if (index < explanationOpenAI.length) {
							loadingExplanationOpenAI.update((prev) => prev + explanationOpenAI[index]);
						}
						index++;
					} else {
						clearInterval(interval); // Detener el intervalo cuando todo el texto ha sido agregado
					}
				}, typingSpeed);

				// Crear gráficos del atributo summary
				if (result.summary) {
					drawBarChart(result.summary);
					drawPieChart(result.summary);
					createTable(result.summary);
				}

				// Convertir el texto de Markdown a HTML
				loadingExplanationGroq.set(marked(explanationGroq));
				loadingExplanationOpenAI.set(marked(explanationOpenAI));
			} catch (error) {
				console.error('Error al enviar datos al backend:', error);
				alert('Hubo un error al enviar los datos al backend.');
			} finally {
				isLoading.set(false); // Ocultar el spinner
				showGenerateButton.set(false); // Ocultar el botón después de enviar los datos al backend
			}
		} else {
			alert('Por favor, complete todos los campos o cargue un archivo.');
		}
	}

	// Función para extraer el valor numérico antes del paréntesis y convertirlo a float
	function extractValue(value) {
		const match = value.match(/^(\d+(\.\d+)?)/);
		return match ? parseFloat(match[0]) : 0;
	}

	// Graficos de barras y pastel de los resultados del backend  valores reales, predicciones e impacto
	// Función para crear el gráfico de barras
	function drawBarChart(summary) {
		if (barChart) {
			barChart.destroy(); // Destruir el gráfico de barras existente
		}

		const ctx = document.getElementById('barChart').getContext('2d');
		barChart = new Chart(ctx, {
			type: 'bar',
			data: {
				labels: [
					'Valor Promedio Actual Con ' + eventType,
					'Valor Promedio Predicho Sin ' + eventType,
					'Impacto Promedio'
				],
				datasets: [
					{
						label: 'Intervención: ' + eventType,
						data: [
							parseFloat(summary['Promedio Actual']),
							extractValue(summary['Predicción Promedio']),
							extractValue(summary['Efecto Absoluto Promedio'])
						],
						backgroundColor: [
							'rgba(75, 192, 192, 0.2)',
							'rgba(153, 102, 255, 0.2)',
							'rgba(255, 205, 86, 0.2)'
						],
						borderColor: [
							'rgba(75, 192, 192, 1)',
							'rgba(153, 102, 255, 1)',
							'rgba(255, 205, 86, 1)'
						],
						borderWidth: 1
					}
				]
			},
			options: {
				responsive: true,
				maintainAspectRatio: false,
				scales: {
					y: {
						beginAtZero: true,
						ticks: {
							callback: function (value) {
								return value;
							}
						}
					}
				}
			}
		});
	}

	// Función para crear el gráfico de pastel
	function drawPieChart(summary) {
		if (pieChart) {
			pieChart.destroy(); // Destruir el gráfico de pastel existente
		}

		const ctx = document.getElementById('pieChart').getContext('2d');
		pieChart = new Chart(ctx, {
			type: 'pie',
			data: {
				labels: [
					'Valor Promedio Actual Con ' + eventType,
					'Valor Promedio Predicho Sin ' + eventType,
					'Impacto Promedio'
				],
				datasets: [
					{
						label: 'Intervención: ' + eventType,
						data: [
							parseFloat(summary['Promedio Actual']),
							extractValue(summary['Predicción Promedio']),
							extractValue(summary['Efecto Absoluto Promedio'])
						],
						backgroundColor: [
							'rgba(54, 162, 235, 0.2)',
							'rgba(255, 206, 86, 0.2)',
							'rgba(75, 192, 192, 0.2)'
						],
						borderColor: [
							'rgba(54, 162, 235, 1)',
							'rgba(255, 206, 86, 1)',
							'rgba(75, 192, 192, 1)'
						],
						borderWidth: 1
					}
				]
			},
			options: {
				responsive: true,
				plugins: {
					legend: {
						position: 'top'
					},
					tooltip: {
						callbacks: {
							label: function (tooltipItem) {
								const value = tooltipItem.raw;
								return `${tooltipItem.label}: ${value}`;
							}
						}
					}
				}
			}
		});
	}

	// Función para crear la tabla
	function createTable(summary) {
		const tableBody = document.getElementById('summaryTableBody');

		// Limpiar la tabla existente
		tableBody.innerHTML = '';

		const rows = [
			{ desc: 'Valor Promedio Actual Con: ' + eventType, value: summary['Promedio Actual'] },
			{
				desc: 'Valor Promedio Predicción Sin: ' + eventType,
				value: summary['Predicción Promedio']
			},
			{ desc: 'Impacto Absoluto Promedio', value: summary['Efecto Absoluto Promedio'] },
			{ desc: 'Valor Acumulado Actual Con: ' + eventType, value: summary['Acumulado Actual'] },
			{ desc: 'Impacto Absoluto Acumulado', value: summary['Efecto Absoluto Acumulado'] },
			{ desc: 'Impacto Relativo Acumulado', value: summary['Efecto Relativo Acumulado'] },
			{ desc: 'Impacto Relativo Promedio', value: summary['Efecto Relativo Promedio'] },
			{
				desc: 'Valor Acumulada Predicción Sin: ' + eventType,
				value: summary['Predicción Acumulada']
			}
		];

		rows.forEach((row) => {
			const tr = document.createElement('tr');
			tr.className = 'border-b border-gray-200 hover:bg-gray-100';
			tr.innerHTML = `
            <td class="py-3 px-6 text-left whitespace-nowrap">${row.desc}</td>
            <td class="py-3 px-6 text-left">${row.value}</td>
        `;
			tableBody.appendChild(tr);
		});
	}

	// Obtener la imagen base64 del resultado de la API
	$: imageUrl = $apiResults?.image ? `data:image/png;base64,${$apiResults.image}` : '';

	// Abrir el modal
	function openModal() {
		isModalOpen.set(true);
	}

	// Cerrar el modal
	function closeModal() {
		isModalOpen.set(false);
	}

	// Agregar el nuevo tipo de evento al select
	function addEventType() {
		if (newEventType.trim()) {
			eventType = newEventType; // Asigna el nuevo tipo de evento
			closeModal(); // Cierra el modal
			// Aquí puedes agregar lógica adicional si necesitas actualizar algo más
		} else {
			alert('El tipo de evento no puede estar vacío.');
		}
	}
</script>

<svelte:head>
	<title>Upload and Analyze Data</title>
	<!-- Importamos las librerías Chart.js y chartjs-adapter-date-fns -->
	<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
	<script src="https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns"></script>
	<script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-annotation"></script>
</svelte:head>


<!-- Segmento para codigo HTML -->
<section class="container mx-auto">
	<div class="flex flex-col md:flex-row gap-4">
		<!-- Columna Izquierda -->
		<div class="w-full md:w-2/3">
			<h1 class="text-2xl font-bold mb-4">Upload Your CSV or Excel File</h1>

			<!-- Botón de Carga -->
			<label class="button mb-4 block">
				<input type="file" accept=".csv, .xlsx" on:change={handleFileUpload} class="hidden" />
				Upload File
			</label>
			<DataTable {data} />
		</div>

		<!-- Columna Derecha -->
		<div class="w-full md:w-1/3 mt-6 md:mt-0">
			<h2 class="text-xl font-semibold mb-4 text-center"><b> Input Details</b></h2>

			<label for="date-column" class="block mb-2"><b>Date Column Name:</b></label>
			<input
				type="text"
				id="date-column"
				bind:value={dateColumn}
				disabled={$isFileUploaded === false}
				class="block w-full mb-4 px-3 py-2 border rounded"
				placeholder="Name of the date column"
			/>

			<label for="original-column" class="block mb-2"> <b>Original Column Name:</b></label>
			<input
				type="text"
				id="original-column"
				bind:value={originalColumn}
				disabled={$isFileUploaded === false}
				class="block w-full mb-4 px-3 py-2 border rounded"
				placeholder="Name target column"
			/>

			<label for="intervention-date" class="block mb-2">
				<b>Intervention Date (DD-MM-YYYY):</b></label
			>
			<input
				type="date"
				id="intervention-date"
				bind:value={interventionDate}
				disabled={$isFileUploaded === false}
				class="block w-full mb-4 px-3 py-2 border rounded"
			/>

			<label for="control-columns" class="block mb-2">
				<b>Control Columns (comma separated):</b></label
			>
			<input
				type="text"
				id="control-columns"
				bind:value={controlColumns}
				disabled={$isFileUploaded === false}
				class="block w-full mb-4 px-3 py-2 border rounded"
				placeholder="Name of control columns"
			/>

			<label for="event-type" class="block mb-2"><b> Event Type:</b></label>

			<select
				id="event-type"
				bind:value={eventType}
				disabled={$isFileUploaded === false}
				class="block w-full mb-4 px-3 py-2 border rounded"
			>
				<option value="" disabled>Select event type</option>
				<option value="Publicidad">Publicidad</option>
				<option value="Cambio de politica control">Cambio de política de control</option>
				<option value="Evento adverso COVID-19">Evento adverso COVID-19</option>
				<option value="Tratamiento">Tratamiento</option>
				<option value={newEventType}>{newEventType}</option>
				<!-- Opción para el nuevo tipo de evento -->

				<!-- Añadir más opciones según sea necesario -->
			</select>
			{#if $isFileUploaded}
				<p class="small-text">
					¿No encuentras el tipo de evento que buscas? <button on:click={openModal}
						><b style="color: #d6361f;"> ¡Crea uno nuevo!</b></button
					>
				</p>
				<br />
			{/if}
			<button class="button" on:click={validateInputs}>Visualize</button>
			<button
				class="button mt-4"
				on:click={sendDataToBackend}
				style="display: {$showGenerateButton ? 'inline-block' : 'none'}">Model Generate</button
			>
		</div>
	</div>
</section>

<!-- Modal para agregar un nuevo tipo de evento -->
{#if $isModalOpen}
	<div class="modal">
		<div class="modal-content">
			<h2>Tipo de evento</h2>
			<input type="text" bind:value={newEventType} placeholder="Escriba el nuevo tipo de evento" />
			<button on:click={addEventType}>Aceptar</button>
			<button on:click={closeModal}>Cancelar</button>
		</div>
	</div>
{/if}

<!-- Resumen de datos seleccionados -->
<section class="container mx-auto p-4">
	{#if $isFileUploaded && originalColumn && interventionDate && controlColumns && eventType}
		<div class="bg-gray-100 p-4 mt-6 rounded-md">
			<h2 class="text-xl font-semibold mb-4">Resumen de Selección</h2>
			<p><strong>Columna Original:</strong> {originalColumn}</p>
			<p><strong>Fecha de Intervención:</strong> {interventionDate}</p>
			<p><strong>Columnas de Control:</strong> {controlColumns}</p>
			<p><strong>Tipo de Evento:</strong> {eventType}</p>
		</div>
	{/if}
</section>

<!-- Sección para mostrar el gráfico -->
<section class="container mx-auto p-4">
	{#if data.length > 0 && originalColumn && controlColumns && interventionDate && eventType}
		<section class="mt-6">
			<div class="w-full h-96">
				<canvas bind:this={chartCanvas} class="w-full h-full"></canvas>
			</div>
		</section>
	{/if}
</section>

<!-- Tabla de Impactos -->
<section class="container mx-auto p-4">
	<div class="mb-8">
		<table class="min-w-full bg-white border border-gray-200">
			<thead>
				<tr class="w-full bg-gray-200 text-gray-600 uppercase text-sm leading-normal">
					<th class="py-3 px-6 text-center">Descripción</th>
					<th class="py-3 px-6 text-center">Valor</th>
				</tr>
			</thead>
			<tbody id="summaryTableBody" class="text-gray-600 text-sm font-light"></tbody>
		</table>
	</div>

	<!-- Gráficos de la causa y efecto -->
	<div class="flex justify-center space-x-4">
		<div class="w-1/2">
			<canvas id="barChart"></canvas>
		</div>
		<div class="w-1/2">
			<canvas id="pieChart"></canvas>
		</div>
	</div>
</section>

<!-- Seccion de la respuesta del backend -->
<section class="container mx-auto p-4">
	<!-- Mostrar resultados de la API -->
	{#if $apiResults}
		<h1 class="text-2xl font-bold mb-4">Results</h1>

		<div class="mt-6">
			<!-- Card de la descripción del evento -->
			<div
				class="bg-gradient-to-l from-slate-300 to-slate-100 text-slate-600 border border-slate-300 grid grid-col-2 p-4 gap-4 rounded-lg shadow-md"
			>
				<div class="text-lg font-bold capitalize rounded-md">Technical report:</div>
				<div class="rounded-md">
					<details class="mb-4">
						<summary class="cursor-pointer">View full report</summary>
						<p class="italic mt-2">
							<!-- Mostrar el reporte completo -->
							{$apiResults.report}
						</p>
						<div class="mb-6">
							<h2 class="text-xl font-semibold mb-4 text-center">Causal-Event</h2>
							<!-- Sección para mostrar la imagen -->
							{#if imageUrl}
								<img
									src={imageUrl}
									alt="Graph illustrating the impact of the event on the economic indicator"
									class="w-full h-auto border rounded"
								/>
							{:else}
								<p>No image available.</p>
							{/if}
						</div>
					</details>
				</div>
			</div>

			<!-- Card de la explicación del evento con llama 3 -->
			<div class="relative rounded-lg bg-slate-900 p-2">
				<div class="relative flex text-center">
					<div class="flex pl-3.5 pt-3">
						<svg
							viewBox="0 0 24 24"
							fill="currentColor"
							class="-ml-0.5 mr-1.5 h-3 w-3 text-red-500/20"
						>
							<circle r="12" cy="12" cx="12"></circle>
						</svg>
						<svg
							viewBox="0 0 24 24"
							fill="currentColor"
							class="-ml-0.75 mr-1.5 h-3 w-3 text-yellow-500/20"
						>
							<circle r="12" cy="12" cx="12"></circle>
						</svg>
						<svg
							viewBox="0 0 24 24"
							fill="currentColor"
							class="-ml-0.75 mr-1.5 h-3 w-3 text-green-500/20"
						>
							<circle r="12" cy="12" cx="12"></circle>
						</svg>
					</div>
					<span class="absolute inset-x-0 top-2 text-xs text-slate-500">
						<h5>llama3-8b-8192 Explanation</h5>
					</span>
				</div>
				<div class="mt-5 space-y-1.5 px-5 pb-10">
					<!-- Chat de llama 3 -->
					<div>
						<p class=" text-white">{@html $loadingExplanationGroq}</p>
					</div>
				</div>
			</div>

			<br />
			<br />
			<!-- Card de la explicación del evento con OpenAI -->
			<div class="relative rounded-lg bg-slate-900 p-2">
				<div class="relative flex text-center">
					<div class="flex pl-3.5 pt-3">
						<svg
							viewBox="0 0 24 24"
							fill="currentColor"
							class="-ml-0.5 mr-1.5 h-3 w-3 text-red-500/20"
						>
							<circle r="12" cy="12" cx="12"></circle>
						</svg>
						<svg
							viewBox="0 0 24 24"
							fill="currentColor"
							class="-ml-0.75 mr-1.5 h-3 w-3 text-yellow-500/20"
						>
							<circle r="12" cy="12" cx="12"></circle>
						</svg>
						<svg
							viewBox="0 0 24 24"
							fill="currentColor"
							class="-ml-0.75 mr-1.5 h-3 w-3 text-green-500/20"
						>
							<circle r="12" cy="12" cx="12"></circle>
						</svg>
					</div>
					<span class="absolute inset-x-0 top-2 text-xs text-slate-500">
						<h5>gpt-3.5-turbo Explanation</h5>
					</span>
				</div>
				<div class="mt-5 space-y-1.5 px-5 pb-10">
					<!-- Chat de OpenAI -->
					<div>
						<p class=" text-white">{@html $loadingExplanationOpenAI}</p>
					</div>
				</div>
			</div>
		</div>
	{/if}
</section>

<!--Spinner-->
{#if $isLoading}
	<div class="spinner-overlay">
		<div class="spinner"></div>
		<p class="ml-2 text-white">Procesando, por favor espere...</p>
	</div>
{/if}

<!-- Estilos -->
<style>

	/* Estilos para el botón */
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
		margin: auto;
	}
	/* Estilos para el botón hover */
	.button:hover {
		background:
			linear-gradient(140.14deg, #d6361f 15.05%, #ec540e 114.99%) padding-box,
			linear-gradient(142.51deg, #af1905 8.65%, #ff9465 88.82%) border-box;
		transform: scale(1.05);
	}
	/* Estilos para el spinner overlay */
	.spinner-overlay {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: rgba(0, 0, 0, 0.5);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
	}

	/* Estilos para el spinner */
	.spinner {
		border: 4px solid rgba(0, 0, 0, 0.1);
		border-radius: 50%;
		border-top: 4px solid #d6361f;
		width: 40px;
		height: 40px;
		animation: spin 1s linear infinite;
	}
	/* Estilos para el spinner animation */
	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	/* Estilos para el modal */
	.modal {
		position: fixed;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-color: rgba(0, 0, 0, 0.7); /* Más oscuro para mayor contraste */
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 1000; /* Asegura que el modal esté sobre otros elementos */
		animation: fadeIn 0.3s ease-in-out; /* Animación de aparición */
	}

	.modal-content {
		background-color: #f9f9f9; /* Color de fondo suave */
		padding: 30px; /* Más espacio interior */
		border-radius: 10px; /* Bordes más redondeados */
		width: 400px; /* Ancho más amplio */
		max-width: 90%; /* Responsivo para pantallas pequeñas */
		text-align: left; /* Alineación de texto a la izquierda */
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Sombra sutil */
		position: relative; /* Para posicionar elementos dentro */
		animation: slideDown 0.3s ease-in-out; /* Animación de entrada */
	}

	.modal-content h2 {
		margin-top: 0;
		color: #333; /* Color de texto oscuro */
		font-size: 1.5em; /* Tamaño de fuente más grande */
	}

	.modal-content input {
		width: calc(100% - 20px); /* Ancho completo menos padding */
		padding: 12px; /* Más padding */
		margin-bottom: 15px; /* Más espacio debajo */
		border: 1px solid #ddd; /* Borde sutil */
		border-radius: 5px; /* Bordes redondeados */
		font-size: 1em; /* Tamaño de fuente normal */
	}

	.modal-content button {
		padding: 12px 20px; /* Más padding y ancho mayor */
		margin: 5px;
		border: none; /* Sin borde */
		border-radius: 5px; /* Bordes redondeados */
		background-color: #d6361f; /* Azul llamativo */
		color: white; /* Texto blanco */
		font-size: 1em; /* Tamaño de fuente normal */
		cursor: pointer; /* Manito en hover */
		transition: background-color 0.3s ease; /* Transición suave */
	}

	.modal-content button:hover {
		background-color: #861403; /* Azul más oscuro en hover */
	}

	/* Estilos para el botón de cierre */
	@keyframes fadeIn {
		from {
			opacity: 0;
		}
		to {
			opacity: 1;
		}
	}
	/* Estilos para el botón de cierre */
	@keyframes slideDown {
		from {
			transform: translateY(-20%);
		}
		to {
			transform: translateY(0);
		}
	}
	/* Estilos para el texto pequeño */
	.small-text {
		font-size: 14px; /* Ajusta este valor para cambiar el tamaño de la letra */
	}
</style>
