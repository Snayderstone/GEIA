<script>
	import Counter from './Counter.svelte';
	import welcome from '$lib/images/svelte-welcome.webp';
	import welcome_fallback from '$lib/images/svelte-welcome.png';
	import { goto } from '$app/navigation';

	function handleClick() {
		goto('/causal-impact'); // Redirige a la URL deseada
	}
</script>

<svelte:head>
	<title>Home</title>
	<meta name="description" content="Svelte app GEIA" />
</svelte:head>

<section>
	<h1>
		<span class="welcome">
			<picture>
				<source srcset={welcome} type="image/webp" />
				<img src={welcome_fallback} alt="Welcome" />
			</picture>
		</span>

		Generative AI-Powered Economic Impact Analysis System <br /> <b>(GEIA)</b>
	</h1>

	<br />
	<br />

	<button class="button" on:click={handleClick}>Get Started</button>

	<!-- <Counter /> -->
</section>

<style>
	.button {
		background:
			linear-gradient(140.14deg, #ec540e 15.05%, #d6361f 114.99%) padding-box,
			linear-gradient(142.51deg, #ff9465 8.65%, #af1905 88.82%) border-box;
		border-radius: 7px;
		border: 2px solid transparent;

		text-shadow: 1px 1px 1px #00000040;
		box-shadow: 8px 8px 20px 0px #45090059;

		padding: 20px 140px;
		line-height: 20px;
		cursor: pointer;
		transition: all 0.3s;
		color: white;
		font-size: 40px;
		font-weight: 500;
	}

	.button:hover {
		box-shadow: none;
		opacity: 80%;
	}

	section {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		flex: 0.6;
	}

	h1 {
		width: 100%;
	}

	.welcome {
		display: block;
		position: relative;
		width: 100%;
		height: 0;
		padding: 0 0 calc(100% * 495 / 2048) 0;
	}

	.welcome img {
		position: absolute;
		width: 100%;
		height: 100%;
		top: 0;
		display: block;
	}
</style>
