<template>
	<div>
		<h1>这是主页</h1>
		<button @click="to">前往</button>
	</div>
</template>

<script setup>
	import { router } from '@/router';

	function to() {
		router.push('/generator');
	}
</script>
