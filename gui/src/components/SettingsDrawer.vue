<template>
	<el-drawer :model-value="visible" @update:model-value="$emit('update:visible', $event)" :before-close="beforeClose" direction="ltr" size="400px">
		<template #header>
			<h4>设置</h4>
		</template>
		<template #default>
			<div>
				<h5>窗口设置</h5>
				<el-button plain type="primary" :icon="Menu" size="small" @click="resizeApp('resize')">还原默认大小</el-button>
			</div>
			<div class="slider-demo-block">
				<span class="demonstration">窗口宽度</span>
				<el-slider v-model="config.screenWidth" @input="resizeApp" @change="saveWinSizeItem" :min="700" :max="config.maxScreenWidth" :step="1" show-input size="small" />
			</div>
			<div class="slider-demo-block">
				<span class="demonstration">窗口高度</span>
				<el-slider v-model="config.screenHeight" @input="resizeApp" @change="saveWinSizeItem" :min="300" :max="config.maxscreenHeight" :step="1" show-input size="small" />
			</div>
			<div>
				<h5>生成目录</h5>
				<el-radio-group v-model="config.directoryType" @change="changeDirectory" size="small">
					<el-radio-button label="桌面" value="desktop" />
					<el-radio-button label="跟随应用" value="follow" />
					<el-radio-button label="自定义" value="diy" />
				</el-radio-group>
				<div>
					<el-input
						v-model="config.directoryPath"
						placeholder="例：D:\下载 ，输入完请点击后方按钮检测是否可用"
						:disabled="config.directoryType !== 'diy'"
						@change="changePath"
						size="small"
					>
						<!-- <template #prepend>目录</template> -->
						<template #append>
							<el-button :disabled="config.directoryType !== 'diy'" @click="checkPath()">
								<el-icon v-if="config.enablePath || config.directoryType !== 'diy'" color="#69ffb4"><Select /></el-icon>
								<el-icon v-else color="#d8e510"><RefreshRight /></el-icon>
							</el-button>
						</template>
					</el-input>
				</div>
			</div>
		</template>
		<template #footer>
			<div style="flex: auto">
				<h6 @click="handleVersionClick" style="cursor: pointer; user-select: none;">版本：0.5.11.5</h6>
			</div>
		</template>
	</el-drawer>
</template>

<script setup>
	import { ref } from 'vue';
	import { Menu, Select, RefreshRight } from '@element-plus/icons-vue';
	import { ElMessage } from 'element-plus';

	defineProps({
		visible: Boolean,
		config: Object,
		resizeApp: Function,
		saveWinSizeItem: Function,
		changeDirectory: Function,
		changePath: Function,
		checkPath: Function,
		beforeClose: Function,
	});

	defineEmits(['update:visible']);

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
						ElMessage.success(res);
					});
				}
			} catch (e) {
				console.error(e);
			}
		}
	}
</script>

<style scoped>
	.slider-demo-block {
		max-width: 600px;
		display: flex;
		align-items: center;
	}
	.slider-demo-block .el-slider {
		margin-top: 0;
		margin-left: 12px;
	}
	.slider-demo-block .demonstration {
		font-size: 14px;
		color: var(--el-text-color-secondary);
		line-height: 44px;
		flex: 1;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		margin-bottom: 0;
	}
	.slider-demo-block .demonstration + .el-slider {
		flex: 0 0 80%;
	}
</style>
