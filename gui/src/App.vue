<template>
	<n-config-provider :theme="isDark ? darkTheme : null" :locale="zhCN" :date-locale="dateZhCN">
		<n-message-provider>
			<n-dialog-provider>
				<n-notification-provider>
					<n-watermark
						content="Inkwell"
						:font-size="16"
						:font-color="isDark ? 'rgba(255,255,255,0.15)' : 'rgba(0,0,0,0.15)'"
						:width="150"
						:height="120"
						:line-height="80"
						:x-gap="100"
						:y-gap="100"
						:rotate="-22"
						cross
					>
						<RouterView />
					</n-watermark>
				</n-notification-provider>
			</n-dialog-provider>
		</n-message-provider>
	</n-config-provider>
</template>

<script setup>
import { RouterView } from 'vue-router';
import { darkTheme, zhCN, dateZhCN } from 'naive-ui';
import { useDark } from '@vueuse/core';

const isDark = useDark();
</script>

<style>
/* View Transitions 深色模式切换动画 */
::view-transition-old(root),
::view-transition-new(root) {
	animation: none !important;
}
</style>
