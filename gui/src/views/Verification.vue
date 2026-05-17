<template>
	<div class="verification-container" :class="{ 'is-dark': isDark, 'success-fade': isSuccess }">
		<div class="verification-card">
			<h2 class="verification-title">请输入密码</h2>

			<!-- 锁定提示 -->
			<div v-if="isLocked" class="lock-message">
				<n-alert type="warning" title="已锁定">
					请等待 {{ lockRemainingSeconds }} 秒后重试
				</n-alert>
				<n-button type="error" size="large" class="exit-btn" @click="exitApp">
					退出程序
				</n-button>
			</div>

			<!-- 验证码输入框 -->
			<div v-else class="code-input-wrapper">
				<div class="code-inputs">
					<n-input
						v-for="(_, index) in 7"
						:key="index"
						:ref="(el) => setInputRef(el, index)"
						v-model:value="codeChars[index]"
						:maxlength="1"
						size="large"
						placeholder=""
						:type="showPassword ? 'text' : 'password'"
						@update:value="handleInput(index)"
						@keydown="handleKeydown(index, $event)"
						@paste="handlePaste($event, index)"
						class="code-input"
					/>
				</div>

				<!-- 显示/隐藏密码 -->
				<div class="show-password-toggle">
					<n-switch v-model:value="showPassword" size="small">
						<template #checked>显示</template>
						<template #unchecked>隐藏</template>
					</n-switch>
				</div>
			</div>

			<!-- 错误提示 -->
			<n-text v-if="errorMessage" type="error" class="error-message">
				{{ errorMessage }}
			</n-text>

			<!-- 提交按钮 -->
			<n-button
				v-if="!isLocked"
				type="primary"
				size="large"
				:loading="isLoading"
				:disabled="isCodeEmpty"
				@click="submitVerification"
				class="submit-btn"
			>
				验证
			</n-button>

			<!-- 退出按钮 -->
			<n-button
				v-if="!isLocked"
				type="default"
				size="large"
				@click="exitApp"
				class="exit-btn"
			>
				退出程序
			</n-button>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { useMessage } from 'naive-ui';
import { useDark } from '@vueuse/core';

const router = useRouter();
const message = useMessage();
const isDark = useDark();

const codeChars = ref(['', '', '', '', '', '', '']);
const inputRefs = ref({});
const showPassword = ref(false);
const isLoading = ref(false);
const errorMessage = ref('');
const isLocked = ref(false);
const lockRemainingSeconds = ref(0);
const failedAttempts = ref(0);
const isSuccess = ref(false);

// 设置输入框引用
function setInputRef(el, index) {
	if (el) {
		inputRefs.value[index] = el;
	}
}

const isCodeEmpty = computed(() => {
	return codeChars.value.some((char) => !char);
});

const fullCode = computed(() => {
	return codeChars.value.join('');
});

// 等待 pywebview 就绪
function waitForPywebview(timeout = 5000) {
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
		}, 50);
	});
}

// 检查验证状态
async function checkVerificationStatus() {
	try {
		await waitForPywebview();
		const status = await window.pywebview.api.getVerificationStatus();
		isLocked.value = status.isLocked;
		lockRemainingSeconds.value = status.lockRemainingSeconds;
		failedAttempts.value = status.failedAttempts;

		// 如果已验证，直接跳转
		if (status.isVerified) {
			router.push('/');
		} else if (status.isLocked) {
			startLockTimer();
		}
	} catch (error) {
		console.error('checkVerificationStatus', error);
		// pywebview 未就绪时，显示输入框
	}
}

// 锁定倒计时
function startLockTimer() {
	if (lockRemainingSeconds.value <= 0) return;

	const timer = setInterval(() => {
		lockRemainingSeconds.value--;
		if (lockRemainingSeconds.value <= 0) {
			clearInterval(timer);
			isLocked.value = false;
			errorMessage.value = '';
			clearCode();
			focusFirstInput();
		}
	}, 1000);
}

// 处理输入
function handleInput(index) {
	const char = codeChars.value[index];
	if (char && index < 6) {
		// 自动跳转到下一个输入框
		nextTick(() => {
			inputRefs.value[index + 1]?.focus();
		});
	}
}

// 处理按键
function handleKeydown(index, event) {
	if (event.key === 'Backspace' && !codeChars.value[index] && index > 0) {
		// 当前框为空时，退格跳转到上一个框
		event.preventDefault();
		nextTick(() => {
			inputRefs.value[index - 1]?.focus();
		});
	} else if (event.key === 'Enter' && !isCodeEmpty.value) {
		// 回车提交
		event.preventDefault();
		submitVerification();
	}
}

// 处理粘贴
function handlePaste(event, index) {
	event.preventDefault();
	const pastedText = (event.clipboardData || window.clipboardData).getData('text');
	const chars = pastedText.slice(0, 7).split('');

	for (let i = 0; i < chars.length; i++) {
		const targetIndex = index + i;
		if (targetIndex < 7) {
			codeChars.value[targetIndex] = chars[i];
		}
	}

	// 聚焦到最后一个填充的框或第 6 个框
	const lastIndex = Math.min(index + chars.length - 1, 6);
	nextTick(() => {
		inputRefs.value[lastIndex]?.focus();
	});
}

// 清空输入
function clearCode() {
	codeChars.value = ['', '', '', '', '', '', ''];
}

// 退出程序
async function exitApp() {
	try {
		await waitForPywebview();
		window.pywebview.api.destroyApp();
	} catch (error) {
		console.error('exitApp', error);
	}
}

// 聚焦第一个输入框
function focusFirstInput() {
	nextTick(() => {
		inputRefs.value[0]?.focus();
	});
}

// 提交验证
async function submitVerification() {
	if (isCodeEmpty.value) return;

	isLoading.value = true;
	errorMessage.value = '';

	try {
		await waitForPywebview();
		const result = await window.pywebview.api.verifyPassword(fullCode.value);

		if (result.success) {
			message.success('验证成功', { duration: 1500 });
			isSuccess.value = true;
			setTimeout(() => {
				router.push('/');
			}, 400);
		} else {
			errorMessage.value = result.message;
			clearCode();
			focusFirstInput();

			if (result.isLocked) {
				isLocked.value = true;
				lockRemainingSeconds.value = result.lockRemainingSeconds;
				startLockTimer();
			}

			failedAttempts.value = await window.pywebview.api.getVerificationStatus().failedAttempts;
		}
	} catch (error) {
		console.error('submitVerification', error);
		errorMessage.value = '验证请求失败';
	} finally {
		isLoading.value = false;
	}
}

onMounted(async () => {
	await checkVerificationStatus();
	focusFirstInput();
});
</script>

<style lang="css" scoped>
.verification-container {
	height: 100vh;
	width: 100%;
	display: flex;
	align-items: center;
	justify-content: center;
	transition: opacity 0.4s ease, transform 0.4s ease;
}

.success-fade {
	opacity: 0;
	transform: scale(0.95);
}

.verification-card {
	padding: 40px;
	border-radius: 12px;
	text-align: center;
}

.is-dark .verification-card {
	background: rgba(255, 255, 255, 0.08);
}

.verification-container:not(.is-dark) .verification-card {
	background: rgba(255, 255, 255, 0.9);
	box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.verification-title {
	font-size: 24px;
	font-weight: 500;
	margin-bottom: 24px;
}

.is-dark .verification-title {
	color: rgba(255, 255, 255, 0.85);
}

.verification-container:not(.is-dark) .verification-title {
	color: rgba(0, 0, 0, 0.85);
}

.code-input-wrapper {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 16px;
}

.code-inputs {
	display: flex;
	gap: 12px;
}

.code-input {
	width: 48px;
	text-align: center;
	font-size: 20px;
}

.code-input :deep(.n-input__input-el) {
	text-align: center;
}

.show-password-toggle {
	margin-top: 8px;
}

.lock-message {
	margin-bottom: 20px;
}

.exit-btn {
	margin-top: 20px;
	min-width: 120px;
}

.error-message {
	margin-top: 16px;
	font-size: 14px;
}

.submit-btn {
	margin-top: 24px;
	min-width: 120px;
	margin-right: 16px;
}
</style>
