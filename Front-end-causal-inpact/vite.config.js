import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	server: {
		host: '0.0.0.0', // Permitir conexiones desde fuera del contenedor
		port: 4173 // Asegúrate de que el puerto coincide con el expuesto en Dockerfile
	},
	plugins: [sveltekit()]
});
