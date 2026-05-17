<template>
		<n-config-provider :theme="isDark ? darkTheme : null" :locale="zhCN" :date-locale="dateZhCN">
			<n-message-provider>
				<n-dialog-provider>
					<n-notification-provider>
						<n-watermark
							content="不娇虑"
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
	import { onMounted } from 'vue';
	import { useRouter, RouterView } from 'vue-router';
	import { darkTheme, zhCN, dateZhCN } from 'naive-ui';
	import { useDark } from '@vueuse/core';

	const isDark = useDark();
	const router = useRouter();

	// 等待 pywebview 就绪（增加超时时间）
	function waitForPywebview(timeout = 30000) {
		return new Promise((resolve, reject) => {
			if (window.pywebview && window.pywebview.api) {
				resolve();
				return;
			}

			const startTime = Date.now();
			const checkInterval = setInterval(() => {
				if (window.pywebview && window.pywebview.api) {
					clearInterval(checkInterval);
					resolve();
				} else if (Date.now() - startTime > timeout) {
					clearInterval(checkInterval);
					reject(new Error('pywebview timeout'));
				}
			}, 100);
		});
	}

	// 检查验证状态
	async function checkVerification() {
		try {
			await waitForPywebview();
			const status = await window.pywebview.api.getVerificationStatus();

			// 如果未验证，跳转到验证页面
			if (!status.isVerified) {
				router.replace('/verify');
			}
		} catch (error) {
			console.error('pywebview not ready:', error);
			// 超时后仍跳转到验证页面，确保安全
			router.replace('/verify');
		}
	}

	onMounted(() => {
		checkVerification();
	});
	</script>

	<style>
	/* View Transitions 深色模式切换动画 */
	::view-transition-old(root),
	::view-transition-new(root) {
		animation: none !important;
	}
	</style>