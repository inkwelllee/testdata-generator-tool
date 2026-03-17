<template>
	<q-dialog
		:model-value="visible"
		@update:model-value="$emit('update:visible', $event)"
		position="left"
		:before-hide="beforeClose"
	>
		<q-card class="settings-card">
			<q-card-section class="q-pa-sm">
				<div class="text-subtitle1 text-weight-medium">设置</div>
			</q-card-section>

			<q-separator />

			<q-card-section class="q-pa-sm">
				<div class="setting-section">
					<div class="text-body2 text-weight-medium q-mb-xs">窗口设置</div>
					<p class="text-caption text-grey q-mb-xs">拖动窗口边缘可调整大小</p>
					<q-btn outline color="primary" icon="aspect_ratio" label="还原默认大小" size="sm" @click="resetSize" />
				</div>

				<div class="setting-section">
					<div class="text-body2 text-weight-medium q-mb-xs">生成目录</div>
					<q-btn-toggle
						v-model="config.directoryType"
						toggle-color="primary"
						:options="directoryOptions"
						dense
						outline
						size="sm"
						@update:model-value="changeDirectory"
					/>
					<div class="q-mt-xs">
						<q-input
							v-model="config.directoryPath"
							dense
							borderless
							class="input-field"
							placeholder="例：D:\下载，点击后方按钮检测"
							:disable="config.directoryType !== 'diy'"
							@update:model-value="changePath"
						>
							<template v-slot:append>
								<q-btn
									flat
									round
									dense
									size="sm"
									:disable="config.directoryType !== 'diy'"
									@click="checkPath()"
								>
									<q-icon :name="config.enablePath || config.directoryType !== 'diy' ? 'check' : 'autorenew'" :color="config.enablePath || config.directoryType !== 'diy' ? 'positive' : 'warning'" size="18px" />
								</q-btn>
							</template>
						</q-input>
					</div>
				</div>
			</q-card-section>

			<q-card-actions align="right" class="q-px-sm q-pb-sm">
				<div class="text-caption text-grey" @click="handleVersionClick" style="cursor: pointer; user-select: none;">
					版本：0.6.3.17
				</div>
			</q-card-actions>
		</q-card>
	</q-dialog>
</template>

<script setup>
import { ref } from 'vue';
import { useQuasar } from 'quasar';
import { useAppStore } from '@/stores';
import { windowApi } from '@/api';

const $q = useQuasar();

const props = defineProps({
	visible: Boolean,
	config: Object,
	changeDirectory: Function,
	changePath: Function,
	checkPath: Function,
	beforeClose: Function,
});

const emit = defineEmits(['update:visible']);

const appStore = useAppStore();

const directoryOptions = [
	{ label: '桌面', value: 'desktop' },
	{ label: '跟随应用', value: 'follow' },
	{ label: '自定义', value: 'diy' }
];

const clickCount = ref(0);
const lastClickTime = ref(0);

function resetSize() {
	appStore.screenWidth = 750;
	appStore.screenHeight = 385;
	appStore.saveWindowSize();
	windowApi.resize(750, 385);
	$q.notify({ message: '已还原默认大小', color: 'positive', position: 'top' });
}

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
					$q.notify({ message: res, color: 'positive', position: 'top' });
				});
			}
		} catch (e) {
			console.error(e);
		}
	}
}
</script>

<style scoped>
.settings-card {
	width: 320px;
	max-width: 90vw;
	max-height: 90vh;
	overflow: hidden;
}

/* 隐藏滚动条 */
.settings-card :deep(.q-card__section) {
	overflow-y: auto;
	scrollbar-width: none;
	-ms-overflow-style: none;
}

.settings-card :deep(.q-card__section::-webkit-scrollbar) {
	display: none;
}

.setting-section {
	margin-bottom: 12px;
}

/* 输入框样式 */
.input-field {
	border-bottom: 1px solid rgba(0, 0, 0, 0.12);
	border-radius: 0;
}

.input-field:hover {
	border-bottom-color: rgba(0, 0, 0, 0.24);
}

.body--dark .input-field {
	border-bottom-color: rgba(255, 255, 255, 0.12);
}

.body--dark .input-field:hover {
	border-bottom-color: rgba(255, 255, 255, 0.24);
}

.input-field.q-field--focused {
	border-bottom-color: var(--q-primary);
}

.input-field :deep(.q-field__control) {
	background: transparent !important;
	padding: 0 4px;
	height: 28px;
}

.input-field :deep(.q-field__label) {
	font-size: 13px;
	top: 5px;
}

/* 浮动后的标签样式 - 保持可读大小 */
.input-field.q-field--float :deep(.q-field__label) {
	font-size: 12px;
	transform: translateY(-60%) scale(1);
	max-width: 100%;
}

.input-field :deep(.q-field__native) {
	padding-top: 12px;
	font-size: 13px;
}
</style>
