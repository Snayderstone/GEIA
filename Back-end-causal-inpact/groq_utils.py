import os
import time

from groq import Groq

# Configura tu clave de API de Groq
api_key = os.getenv('GROQ_API_KEY')
groq_client = Groq(api_key=api_key)

def get_groq_completion(prompt):
    print("Prompt Groq:", prompt)

    # Inicia el temporizador para medir la duración de la solicitud
    start_time = time.time()

    try:
        # Realiza la solicitud a la API de Groq
        completion = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None
        )

        # Extrae la respuesta y el uso de tokens
        response_content = completion.choices[0].message.content
        usage = completion.usage
        total_tokens = usage.total_tokens

        # Calcula el costo estimado
        # Suponiendo un costo de $0.002 por 1000 tokens
        cost_per_token = 0.002 / 1000
        cost = total_tokens * cost_per_token

    except Exception as e:
        response_content = ""
        total_tokens = 0
        cost = 0.0
        print(f"Error al obtener la respuesta de Groq: {str(e)}")

    # Calcula el tiempo de duración de la solicitud
    duration = time.time() - start_time

    # Imprime la respuesta y las métricas
    print("Response Groq:", response_content)
    print(f"Total tokens used (input + output): {total_tokens}")
    print(f"Request duration: {duration:.2f} seconds")
    print(f"Estimated cost: ${cost:.6f}")


    return response_content, duration, total_tokens, cost
