<template>
	<RouterView />
</template>

<script setup>
import { RouterView } from 'vue-router';
</script>

<style>
/* 禁用 pywebview 滚动条 */
html, body {
	margin: 0;
	padding: 0;
	overflow: hidden;
	height: 100%;
	width: 100%;
}

#app {
	height: 100%;
	width: 100%;
	overflow: hidden;
}

/* 通知弹窗样式 */
.notify-toast {
	background: rgba(0, 0, 0, 0.75) !important;
	color: white !important;
	border-radius: 6px !important;
	padding: 8px 16px !important;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
}

.notify-toast .q-icon {
	font-size: 18px;
	margin-right: 8px;
}

.notify-toast .q-notification__message {
	font-size: 13px;
}
</style>
