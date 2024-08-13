import os
import time

import openai

# Configura tu clave de API de OpenAI
openai.api_key = os.environ.get('OPENAI_API_KEY')

def get_openai_completion(prompt):
    print("Prompt OpenAI:", prompt)

    # Inicia el temporizador para medir la duración de la solicitud
    start_time = time.time()

    try:
        # Realiza la solicitud a la API de OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0.5
        )

        # Extrae el contenido de la respuesta
        response_content = response.choices[0].message['content'].strip()

        # Obtener el número de tokens utilizados
        total_tokens = response.usage['total_tokens']

        # Calcula el costo estimado
        # Suponiendo un costo de $0.03 por 1000 tokens
        cost_per_token = 0.03 / 1000
        cost = total_tokens * cost_per_token

    except Exception as e:
        response_content = ""
        total_tokens = 0
        cost = 0.0
        print(f"Error al obtener la respuesta de OpenAI: {str(e)}")

    # Calcula el tiempo de duración de la solicitud
    duration = time.time() - start_time

    # Imprime la respuesta y las métricas
    print("Response OpenAI:", response_content)
    print(f"Total tokens used (input + output): {total_tokens}")
    print(f"Request duration: {duration:.2f} seconds")
    print(f"Estimated cost: ${cost:.6f}")

    return response_content, duration, total_tokens, cost
