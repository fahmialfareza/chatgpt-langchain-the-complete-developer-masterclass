<script lang="ts">
	import '../app.css';
	import 'material-icons/iconfont/material-icons.css';
	import { onMount } from 'svelte';
	import Navbar from '$c/Navbar.svelte';
	import ErrorModal from '$c/ErrorModal.svelte';
	import { getUser, auth } from '$s/auth';

	export const ssr = false;

	$: user = $auth.user;

	onMount(() => {
		if (user === null) {
			getUser();
		}
	});
</script>

<ErrorModal />
<div class="h-screen">
	<Navbar />
	<div class="container mx-auto">
		<slot />
	</div>
</div>
