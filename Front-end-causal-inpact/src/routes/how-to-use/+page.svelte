<script>
    import Data_use from '$lib/images/data_use.png';

</script>

<div class="container">
    <h1>¿Cómo Usar <code>GEIA</code> para Evaluar Efectos en Tus Datos?</h1>
    
    <p>¿Alguna vez te has preguntado si un evento o cambio ha tenido un efecto en tus datos? Aquí te presentamos cómo puedes utilizar <code>GEIA</code> para responder a esta pregunta en distintos contextos.</p>
  
    <h2>Casos de Uso de <code>GEIA</code></h2>
    
    <table>
        <thead>
            <tr>
                <th>Área</th>
                <th>Ejemplo de Uso</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Investigación de Mercados</td>
                <td>¿Cómo afectó una campaña de marketing a las ventas? Puedes usar <code>GEIA</code> para comparar las ventas antes y después de la campaña, y ver si hubo un aumento significativo que se puede atribuir a la campaña.</td>
            </tr>
            <tr>
                <td>Ciencias Políticas</td>
                <td>¿Cómo influyeron los cambios en las leyes en el comportamiento de las personas en un país? <code>GEIA</code> puede ayudarte a evaluar si el comportamiento de la población cambió significativamente después de una reforma legislativa.</td>
            </tr>
            <tr>
                <td>Economía</td>
                <td>¿Cómo impactaron los cambios en los controles crediticios en el comportamiento de endeudamiento? Puedes analizar los datos de endeudamiento antes y después de la implementación de nuevos controles para ver si hubo un cambio notable.</td>
            </tr>
            <tr>
                <td>Eventos Económicos</td>
                <td>¿Cómo afectaron eventos como manifestaciones, crisis o elecciones a la economía de un país? Utiliza <code>GEIA</code> para comparar los indicadores económicos antes y después del evento para entender su impacto.</td>
            </tr>
            <tr>
                <td>Medicina</td>
                <td>¿Cómo influyó el tratamiento de un medicamento en la salud de los pacientes? <code>GEIA</code> puede ayudarte a medir la eficacia de un tratamiento al comparar los resultados de salud antes y después de iniciar el tratamiento.</td>
            </tr>
        </tbody>
    </table>

    <h2>1. Preparando tus Datos</h2>

    <p>Para usar <code>GEIA</code>, organiza tus datos en una tabla (dataframe) con el siguiente formato:</p>
  
    <ol>
      <li><strong>Columna de Fecha:</strong> La fecha para cada dato.</li>
      <li><strong>Columna de la Serie de Tiempo:</strong> La serie que quieres analizar (por ejemplo, ventas, comportamiento de deuda, indicadores económicos).</li>
      <li><strong>Columnas de Variables de Control:</strong> Datos adicionales que podrían influir en la serie (por ejemplo, presupuesto de marketing, cambios legislativos, controles crediticios).</li>
    </ol>
  
    <h2>Ejemplo de Datos</h2>
    
    <img src={Data_use} alt="Data Use Example" />
  
    <h2>2. Ejecuta el Análisis</h2>
  
    <h2>3. Interpretación de Resultados</h2>
  
    <p><strong>Impacto Causal:</strong> Si el <i>número promedio real es <b>mayor que</b> el número 
        promedio predicho</i> indica que el evento tuvo un efecto positivo (ej. como más ventas), 
        mientras que si el <i> número promedio real es <b>menor que</b> el número promedio predicho </i> indica
        que el evento tuvo un efecto negativo (ej. como menos ventas).</p>
  
    <h2 class="text-center"> Empieza ahora a usar <a href="/causal-impact"> GEIA </a></h2>
</div>

<style>

    .container {
        max-width: 900px;
        margin: 2em auto;
        padding: 2em;
        background-color: #fff;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }



    h2 {
        font-size: 1.5em;
        margin-top: 1em;
        margin-bottom: 0.5em;
        font-weight: bold;
        
    }

    p {
        line-height: 1.6;
        margin-bottom: 1em;
    }

    code {
        background: #f8f9fa;
        padding: 0.4em 0.6em;
        border-radius: 4px;
        color: #d6361f;
    }

    ol {
        margin: 0 0 1em 1.5em;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        margin: 1em 0;
    }

    table, th, td {
        border: 1px solid #ddd;
    }

    th, td {
        padding: 0.8em;
        text-align: left;
    }

    th {
        background-color: #d6361f;
        color: #fff;
    }

    img {
        max-width: 100%;
        height: auto;
        display: block;
        margin: 1em auto;
    }
</style>