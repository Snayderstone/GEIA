import base64
import re
import warnings
from io import BytesIO

import pandas as pd
from causalimpact import CausalImpact
from flask import Flask, request, jsonify
from flask_cors import CORS

import groq_utils
import openai_utils
from plot_utils import plot2

# Suprimir todas las advertencias
warnings.filterwarnings('ignore')
app = Flask(__name__)
CORS(app)


@app.route('/api/impact', methods=['POST'])
def analyze_impact():
    try:
        # Obtener datos del cuerpo de la solicitud
        data = request.json

        # Extraer columnas relevantes
        date_column = data['dateColumn']
        original_column = data['originalColumn']
        control_columns = data['controlColumns']
        intervention_date = pd.to_datetime(data['interventionDate'], errors='coerce')
        event_type = data['eventType']
        original_column_name = original_column['name']

        # Crear un DataFrame a partir de los datos recibidos
        try:
            df = pd.DataFrame({
                date_column['name']: pd.to_datetime(date_column['data']),
                original_column['name']: pd.to_numeric(original_column['data']),
                **{col['name']: pd.to_numeric(col['data']) for col in control_columns}
            })
        except Exception as e:
            return jsonify({'error': f'Error al crear DataFrame: {str(e)}'}), 400

        # Establecer la columna de fecha como índice del DataFrame
        df.set_index(date_column['name'], inplace=True)

        # Asegurarse de que el DataFrame esté ordenado por fecha
        df.sort_index(inplace=True)

        # Verificar si la fecha de intervención está en el índice del DataFrame
        if intervention_date not in df.index:
            return jsonify({'error': 'Fecha de intervención no encontrada en los datos'}), 400

        intervention_index = df.index.get_loc(intervention_date)  # Índice de la fecha de intervención

        # Definir los períodos
        pre_period = [df.index[0], df.index[intervention_index]]
        post_period = [df.index[intervention_index + 1], df.index[-1]]

        # Imprimir el DataFrame para verificación
        print("DataFrame creado:")
        print(df)

        # Imprimir el evento y la fecha de intervención
        print(f"Evento: {event_type}")
        print(f"Columna original: {original_column_name}")
        print(f"Fecha de intervención: {intervention_date}")
        print(f"Índice de la fecha de intervención: {intervention_index}")
        print(f"Período Pre-intervención: {pre_period}")
        print(f"Período Post-intervención: {post_period}")

        # Realizar el análisis
        try:
            ci = CausalImpact(df, pre_period, post_period)
        except Exception as e:
            return jsonify({'error': f'Error en el análisis de causalidad: {str(e)}'}), 500

        # Obtener el gráfico de causal impact
        try:
            buffer = BytesIO()
            plot2(ci, buffer)  # Asegúrate de que la función plot2 acepte un buffer
            buffer.seek(0)

            # Convertir la imagen a base64
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        except Exception as e:
            return jsonify({'error': f'Error al generar el gráfico: {str(e)}'}), 500

        # Obtener el resumen del análisis
        try:
            summary = ci.summary()
        except Exception as e:
            return jsonify({'error': f'Error al obtener el resumen: {str(e)}'}), 500

        print("Resumen del análisis:")
        print(summary)

        # Patrones de regex para extraer los datos específicos
        patterns = {
            'Actual Average': re.compile(r'Actual\s+(\S+)'),
            'Actual Cumulative': re.compile(r'Actual\s+(\S+)\s+(\S+)'),
            'Prediction (s.d.) Average': re.compile(r'Prediction \(s\.d\.\)\s+(\S+ \(\S+\))'),
            'Prediction (s.d.) Cumulative': re.compile(r'Prediction \(s\.d\.\)\s+(\S+ \(\S+\))\s+(\S+ \(\S+\))'),
            'Absolute effect (s.d.) Average': re.compile(r'Absolute effect \(s\.d\.\)\s+(\S+ \(\S+\))'),
            'Absolute effect (s.d.) Cumulative': re.compile(r'Absolute effect \(s\.d\.\)\s+(\S+ \(\S+\))\s+(\S+ \(\S+\))'),
            'Relative effect (s.d.) Average': re.compile(r'Relative effect \(s\.d\.\)\s+(\S+ \(\S+\))'),
            'Relative effect (s.d.) Cumulative': re.compile(r'Relative effect \(s\.d\.\)\s+(\S+ \(\S+\))\s+(\S+ \(\S+\))')
        }

        # Extraer valores usando regex
        extracted_data = {}
        for key, pattern in patterns.items():
            match = pattern.search(summary)
            if match:
                extracted_data[key] = match.groups()

        # Imprimir los valores extraídos
        print("Valores extraídos del resumen:")
        for key, value in extracted_data.items():
            print(f"{key}: {value}")

        extracted_values = {
            'Promedio Actual': extracted_data.get('Actual Average', ('N/A',))[0],
            'Acumulado Actual': extracted_data.get('Actual Cumulative', ('N/A', 'N/A'))[1],
            'Predicción Promedio': extracted_data.get('Prediction (s.d.) Average', ('N/A',))[0],
            'Predicción Acumulada': extracted_data.get('Prediction (s.d.) Cumulative', ('N/A', 'N/A'))[1],
            'Efecto Absoluto Promedio': extracted_data.get('Absolute effect (s.d.) Average', ('N/A',))[0],
            'Efecto Absoluto Acumulado': extracted_data.get('Absolute effect (s.d.) Cumulative', ('N/A', 'N/A'))[1],
            'Efecto Relativo Promedio': extracted_data.get('Relative effect (s.d.) Average', ('N/A',))[0],
            'Efecto Relativo Acumulado': extracted_data.get('Relative effect (s.d.) Cumulative', ('N/A', 'N/A'))[1]
        }

        # Obtener el reporte del análisis
        try:
            report = ci.summary(output='report')
        except Exception as e:
            return jsonify({'error': f'Error al obtener el reporte: {str(e)}'}), 500

        print("Reporte del análisis:")
        print(report)

        # Preparar el prompt para OpenAI
        prompt_openai = f"""
        En un análisis de series de tiempo interrumpidas sobre la medición del efecto causal se obtiene la siguiente información:
        Tipo de intervención: {event_type},
        Tipo de datos: {original_column_name},
        Fecha de intervención: {intervention_date},
        definidos en el pre-periodo: {pre_period},
        y el post-periodo: {post_period}.
        En formato markdown y en español devuélveme una explicación del siguiente reporte el cual debe tener como 
        título: “Informe sobre el impacto de la intervención” seguido de un párrafo de nomas de 10 líneas, 
        en forma sencilla, clara y precisa para usuarios que no saben nada.
        Luego, si el valor promedio actual es mayor que el valor promedio predicho escribe el 
        título “Estrategias para potenciar el éxito del impacto” seguido de una lista ordenada con 3 subtítulos con un párrafo cada uno que no supere más de 5 líneas sobre 
        las estrategias para potenciar el éxito del impacto.
        Por lo contrario, si el valor promedio actual es menor que el valorpromedio predicho escribe el título “Estrategias de acción del fracaso del impacto” 
        seguido de una lista ordenada con 5 subtítulos con un párrafo cada uno que no supere más de 10 líneas de texto, 
        escribiendo sobre estrategias de acción para no volver a caer en el impacto negativo de forma específica y clara.
        Reporte dado en dólares: {report}
        """

        # Preparar el prompt para Groq
        prompt_groq = f"""
        En un análisis de series de tiempo interrumpidas sobre la medición del efecto causal se obtiene la siguiente información: 
        Tipo de intervención: {event_type}, 
        Tipo de datos: {original_column_name}, 
        Fecha de intervención: {intervention_date},
        definidos en el pre-periodo: {pre_period},
        y el post-periodo: {post_period}.
        En formato markdown y en español devuélveme una explicación del siguiente reporte el cual debe tener como 
        título: “Informe sobre el impacto de la intervención” seguido de un párrafo de nomas de 5 líneas, 
        en forma sencilla, clara y precisa para usuarios que no saben nada, sin incluir más palabras. 
        Luego en un título: “Explicación” seguido de un párrafo de nomas de 5 líneas, en forma sencilla, 
        clara y precisa para usuarios que no saben nada explica las posibles causas de esos resultados, 
        sin incluir más palabras.
        Reporte dado en dólares: {report}
        """

        # Obtener las explicaciones de OpenAI y Groq
        openai_explanation, openai_duration, openai_tokens, openai_cost = openai_utils.get_openai_completion(prompt_openai)
        groq_explanation, groq_duration, groq_tokens, groq_cost = groq_utils.get_groq_completion(prompt_groq)


        # Retornar los resultados
        return jsonify({
            'message': 'Datos procesados y guardados con éxito',
            'originalColumn': original_column_name,  # Nombre de la columna original
            'eventType': event_type,  # Tipo de evento
            'interventionDate': intervention_date.strftime('%Y-%m-%d'),  # Fecha de intervención
            'summary': extracted_values,  # Resumen del análisis
            'report': report,  # Reporte del análisis
            'image': img_base64,  # Imagen del gráfico de causal impact
            #"simpleExplanation": simple_explanation  # Explicación sencilla del reporte
            'openai': {
                'explanation': openai_explanation if openai_explanation else "No se recibió respuesta de OpenAI",
                'duration': openai_duration,
                'tokens': openai_tokens,
                'cost': openai_cost
            },
            'groq': {
                'explanation': groq_explanation if groq_explanation else "No se recibió respuesta de Groq",
                'duration': groq_duration,
                'tokens': groq_tokens,
                'cost': groq_cost
            }
        })

    except Exception as e:
        print(f"Error inesperado: {str(e)}")  # Imprimir el error en caso de excepción
        return jsonify({'error': 'Error inesperado en el servidor'}), 500


if __name__ == '__main__':
    app.run(port=5000, debug=True)  # Puedes usar otro puerto si prefieres
