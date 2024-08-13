<script>

import logouce from '$lib/images/uce-logo.png';

</script>


<svelte:head>
	<title>About</title>
	<meta name="description" content="About this app" />
</svelte:head>

<div class="about-container">
	<section class="hero">
		<div class="hero-content">
			<h1>Sobre Nosotros</h1>
			<p>Descubre nuestra educación y compromiso con la excelencia educativa.</p>
		</div>
		<img src={logouce} alt="UCE Logo" class="logo" />
	</section>

	<section class="content">
		<h2>Universidad Central del Ecuador</h2>
		<p>
			Fundada en 1826, la <strong>Universidad Central del Ecuador (UCE)</strong> es la universidad pública más antigua y una de las más prestigiosas del país. Ubicada en Quito, la capital de Ecuador, la UCE ha jugado un papel fundamental en la formación de líderes en diversas áreas del conocimiento.
		</p>

		<h2>Facultad de Ingeniería y Ciencias Aplicadas (FICA)</h2>
		<p>
			La <strong>Facultad de Ingeniería y Ciencias Aplicadas</strong> ofrece programas académicos de alta calidad en diversas disciplinas de ingeniería. Con una infraestructura moderna y un cuerpo docente altamente calificado, la FICA se dedica a la formación integral de profesionales que contribuyan al desarrollo tecnológico y científico del país.
		</p>

		<h2>Carrera de Ingeniería en Sistemas de Información</h2>
		<p>
			La <strong>Carrera de Ingeniería en Sistemas de Información</strong> se enfoca en el diseño, desarrollo y gestión de sistemas informáticos. Los estudiantes reciben una formación sólida en áreas clave como programación, bases de datos, redes, inteligencia artificial y seguridad informática, preparándolos para enfrentar los desafíos tecnológicos del futuro.
		</p>

		<p>
			Su misión es formar ingenieros capaces de innovar y liderar proyectos tecnológicos con un enfoque ético y sostenible, contribuyendo al avance de la sociedad y la industria.
		</p>

		<a href="https://www.uce.edu.ec/web/fing" class="button">Conoce más</a>
	</section>
</div>

<style>
	.about-container {
		font-family: 'Roboto', sans-serif;
		color: #333;
		line-height: 1.6;
	}

	.hero {
		display: flex;
		align-items: center;
		justify-content: space-between;
		background-color: #0056a3;
		color: white;
		padding: 2rem;
		border-radius: 8px;
		margin-bottom: 2rem;
	}

	.hero-content h1 {
		font-size: 2.5rem;
		margin-bottom: 0.5rem;
	}

	.hero-content p {
		font-size: 1.2rem;
	}

	.logo {
		max-width: 150px;
		height: auto;
	}

	.content {
		background-color: #f9f9f9;
		padding: 2rem;
		border-radius: 8px;
		box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
	}

	h2 {
		color: #d6361f;
		font-size: 1.8rem;
		margin-top: 1.5rem;
	}

	p {
		margin-bottom: 1rem;
		font-size: 1.1rem;
	}

	.button {
		display: inline-block;
		margin-top: 1.5rem;
		padding: 0.75rem 1.5rem;
		background-color: #d6361f;
		color: white;
		border-radius: 5px;
		text-decoration: none;
		font-size: 1rem;
		transition: background-color 0.3s ease;
	}

	.button:hover {
		background-color: #d6361f;
	}
</style>
