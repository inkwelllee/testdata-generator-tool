<template>
	<el-watermark :font="font" :content="watermark" :gap="[200, 200]">
		<RouterView />
	</el-watermark>
</template>

<script setup>
	import { ref } from 'vue';
	import { RouterView } from 'vue-router';

	const font = ref({
		color: 'rgba(0, 0, 0, .15)',
	});

	const watermarkList = [
		'我不是水印，而是你眼里的一道痕',
		'我不是繁星，而是你心底的一抹幽光',
		'我不是尘埃，而是你记忆中的一粒微尘',
		'我不是幻影，而是你心中的一缕残像',
		'我不是雨滴，而是你眸中的一滴泪光',
		'我不是风声，而是你耳畔的一丝轻语',
		'我不是云朵，而是你视线中的一抹缥缈',
		'我不是灯火，而是你旅程中的一点微光',
		'我不是花瓣，而是你情感中的一缕芬芳',
		'我不是涟漪，而是你思绪中的一波微澜',
		'我不是梦境，而是你灵魂中的一抹虚幻'
	];
	const watermark = ref(watermarkList[Math.floor(Math.random() * watermarkList.length)]);

</script>

<style scoped></style>
