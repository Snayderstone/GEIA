# Proyecto Generative AI-Powered Economic Impact Analysis System"

GEIA es una plataforma web para analizar el impacto de eventos significativos en series de tiempo. Ideal para:

- **Investigación de Mercados:** Evaluar el efecto de campañas de marketing en las ventas.
- **Ciencias Políticas:** Analizar cómo los cambios legislativos afectan el comportamiento de la población.
- **Economía:** Estudiar el impacto de nuevos controles crediticios en el endeudamiento.
- **Eventos Económicos:** Investigar cómo eventos como crisis o elecciones influyen en indicadores económicos.
- **Medicina:** Medir la eficacia de tratamientos comparando datos de salud antes y después del tratamiento.

GEIA permite a los usuarios comparar datos antes y después de eventos clave para obtener insights valiosos y tomar decisiones basadas en datos.

Este proyecto consiste en un frontend desarrollado con SvelteKit y un backend en Flask. Ambos componentes están dockerizados y pueden ser desplegados juntos usando Docker Compose.

## Arquitectura

![App Screenshot](./architecture.png)

## Requisitos

Antes de comenzar, asegúrate de tener instalado:
- [Docker](https://www.docker.com/) o [Docker Desktop](https://www.docker.com/products/docker-desktop/)
Y conocimientos de:
- [Docker Compose](https://docs.docker.com/compose/)

## Pasos Para Ejecutar el Proyecto Localmente

### 1. Clonar el Repositorio 
Primero, clona el repositorio en tu máquina local:

```bash
git clone https://github.com/Snayderstone/GEIA.git
cd GEIA
```
### 2. Configurar las API Keys

Accede al archivo `docker-compose.yml` y asegúrate de definir las API keys para tus modelos LLM (opcional).

Reemplaza los valores en las siguientes variables de entorno:

- `GROQ_API_KEY=your-groq-api-key-here`
- `OPENAI_API_KEY=your-openai-api-key-here`

### 3: Ejecutar Docker Compose
En la raíz del proyecto, ejecuta el siguiente comando para iniciar los contenedores:
```bash
docker-compose up -d
```
### 4: Acceder a la Aplicación
Una vez que los contenedores estén corriendo:
Accede: 
- Al frontend en tu navegador en http://localhost:4173.
- El backend estará disponible en http://localhost:5000.

### 5: Detener los Contenedores
Para detener los contenedores, ejecuta:
```bash
docker-compose down
```


## Licensia

[MIT](https://choosealicense.com/licenses/mit/)

