<template>
	<n-drawer :show="visible" :width="360" placement="left" @update:show="handleUpdateShow">
		<n-drawer-content title="设置" closable>
			<div class="settings-section">
				<n-text depth="3" style="font-weight: 500; margin-bottom: 8px; display: block">窗口设置</n-text>
				<n-button size="small" @click="resetToDefault">还原默认大小</n-button>
			</div>

			<div class="settings-section">
				<n-text depth="3" style="font-weight: 500; margin-bottom: 12px; display: block">生成目录</n-text>
				<n-radio-group v-model:value="config.directoryType" @update:value="changeDirectory" size="small">
					<n-radio-button value="desktop">桌面</n-radio-button>
					<n-radio-button value="follow">跟随应用</n-radio-button>
					<n-radio-button value="diy">自定义</n-radio-button>
				</n-radio-group>
				<div style="margin-top: 12px">
					<n-input-group>
						<n-input
							v-model:value="config.directoryPath"
							placeholder="例：D:\下载，输入完请点击后方按钮检测"
							:disabled="config.directoryType !== 'diy'"
							@update:value="changePath"
							size="small"
						/>
						<n-button size="small" :disabled="config.directoryType !== 'diy'" @click="checkPath()">
							<template #icon>
								<n-icon :color="config.enablePath || config.directoryType !== 'diy' ? '#18a058' : '#f0a020'">
									<CheckmarkCircleOutline v-if="config.enablePath || config.directoryType !== 'diy'" />
									<RefreshOutline v-else />
								</n-icon>
							</template>
						</n-button>
					</n-input-group>
				</div>
			</div>

			<template #footer>
				<n-text depth="3" style="cursor: pointer; user-select: none" @click="handleVersionClick">
					版本：0.6.5.11
				</n-text>
			</template>
		</n-drawer-content>
	</n-drawer>
</template>

<script setup>
import { ref } from 'vue';
import { useMessage } from 'naive-ui';
import { CheckmarkCircleOutline, RefreshOutline } from '@vicons/ionicons5';

const message = useMessage();

const props = defineProps({
	visible: Boolean,
	config: Object,
	resetToDefault: Function,
	changeDirectory: Function,
	changePath: Function,
	checkPath: Function,
	beforeClose: Function,
});

const emit = defineEmits(['update:visible']);

function handleUpdateShow(val) {
	if (!val && props.beforeClose) {
		props.beforeClose(() => {
			emit('update:visible', false);
		});
	} else {
		emit('update:visible', val);
	}
}

const clickCount = ref(0);
const lastClickTime = ref(0);

function handleVersionClick() {
	const currentTime = new Date().getTime();
	if (currentTime - lastClickTime.value > 1000) {
		clickCount.value = 0;
	}

	clickCount.value++;
	lastClickTime.value = currentTime;

	if (clickCount.value >= 5) {
		clickCount.value = 0;
		try {
			if (window.pywebview) {
				window.pywebview.api.clearCache().then(res => {
					message.success(res);
				});
			}
		} catch (e) {
			console.error(e);
		}
	}
}
</script>

<style scoped>
.settings-section {
	margin-bottom: 20px;
}
</style>
