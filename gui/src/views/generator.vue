<template>
	<div class="app-container" ref="containerRef">
		<!-- 窗口边缘缩放区域 -->
		<div class="resize-edge resize-bottom" @mousedown="startResize('bottom', $event)"></div>
		<div class="resize-edge resize-left" @mousedown="startResize('left', $event)"></div>
		<div class="resize-edge resize-right" @mousedown="startResize('right', $event)"></div>
		<div class="resize-corner resize-tl" @mousedown="startResize('top-left', $event)"></div>
		<div class="resize-corner resize-tr" @mousedown="startResize('top-right', $event)"></div>
		<div class="resize-corner resize-bl" @mousedown="startResize('bottom-left', $event)"></div>
		<div class="resize-corner resize-br" @mousedown="startResize('bottom-right', $event)"></div>

		<!-- 固定顶部 -->
		<div class="app-header">
			<div class="header-left">
				<img src="@/assets/icons/logo.svg" @click.stop="appStore.winSetUp = true" style="width: 24px; height: 24px; -webkit-user-drag: none" />
				<span class="app-title">开心果</span>
			</div>
			<div class="header-right">
				<q-toggle
					:model-value="isDark"
					checked-icon="dark_mode"
					unchecked-icon="light_mode"
					size="sm"
					class="q-mr-sm dark-toggle"
					@click.stop="toggleDarkClick"
				/>
				<q-btn flat round dense icon="push_pin" :color="appStore.alwaysOnTop ? 'primary' : 'grey-6'" @click="toggleAlwaysOnTop" size="sm" :style="{ opacity: appStore.alwaysOnTop ? 1 : 0.5 }" />
				<q-btn flat round dense icon="remove" color="grey-7" @click="minimize" size="sm" />
				<q-btn flat round dense :icon="appStore.restoreWindow ? 'filter_none' : 'fullscreen'" color="warning" @click="toggleMaximize" size="sm" />
				<q-btn flat round dense icon="close" color="negative" @click="exitAppTip = true" size="sm" />
			</div>
		</div>

		<!-- 可滚动内容区 -->
		<div class="app-body">
			<q-form class="app-form" ref="formRef">
				<q-tabs v-model="activeTab" dense class="tab-header" active-color="primary" indicator-color="primary" align="justify">
					<q-tab name="basic" label="基础信息" />
					<q-tab name="vehicle" label="车辆信息" />
				</q-tabs>

				<q-tab-panels v-model="activeTab" animated class="tab-panels">
					<q-tab-panel name="basic" class="q-pa-sm">
						<BasicInfoGenerator />
					</q-tab-panel>
					<q-tab-panel name="vehicle" class="q-pa-sm">
						<VehicleInfoGenerator />
					</q-tab-panel>
				</q-tab-panels>
			</q-form>

			<!-- 加载状态 -->
			<q-inner-loading :showing="appStore.loading">
				<q-spinner-gears size="50px" color="primary" />
			</q-inner-loading>
		</div>

		<!-- 退出提示 -->
		<q-dialog v-model="exitAppTip">
			<q-card class="exit-dialog">
				<q-card-section class="q-pa-md text-center">
					<div class="text-body1">{{ appStore.exitTipText }}</div>
				</q-card-section>
				<q-card-actions align="right" class="q-px-md q-pb-sm">
					<q-btn flat color="primary" label="确定" size="sm" @click="destroy" />
				</q-card-actions>
			</q-card>
		</q-dialog>

		<!-- 设置抽屉 -->
		<SettingsDrawer
			v-model:visible="appStore.winSetUp"
			:config="appStore.windowConfig"
			:changeDirectory="appStore.changeDirectory"
			:changePath="appStore.updateDirectoryPath"
			:checkPath="handleCheckPath"
			:beforeClose="winSetUpBeforeClose"
		/>
	</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useQuasar, Dark } from 'quasar';
import { useAppStore } from '@/stores';
import { useWindow } from '@/composables/useWindow';
import { windowApi } from '@/api';
import SettingsDrawer from '@/components/SettingsDrawer.vue';
import BasicInfoGenerator from '@/components/BasicInfoGenerator.vue';
import VehicleInfoGenerator from '@/components/VehicleInfoGenerator.vue';

const $q = useQuasar();
const appStore = useAppStore();
const { minimize, toggleMaximize, destroy } = useWindow();

const exitAppTip = ref(false);
const activeTab = ref('basic');

// 深色模式
const isDark = ref(Dark.isActive);

async function toggleDark(event) {
	// 获取点击位置
	const x = event?.clientX ?? window.innerWidth / 2;
	const y = event?.clientY ?? window.innerHeight / 2;

	// 兼容性检查
	if (!document.startViewTransition) {
		Dark.toggle();
		isDark.value = Dark.isActive;
		localStorage.setItem('darkMode', Dark.isActive);
		return;
	}

	const wasDark = isDark.value;
	const endRadius = Math.hypot(
		Math.max(x, window.innerWidth - x),
		Math.max(y, window.innerHeight - y)
	);

	// 动态设置层级样式
	const styleId = 'dark-transition-override';
	let style = document.getElementById(styleId);
	if (!style) {
		style = document.createElement('style');
		style.id = styleId;
		document.head.appendChild(style);
	}

	// 根据切换方向设置不同的 z-index
	style.textContent = wasDark
		? `::view-transition-old(root) { z-index: 999; animation: none; }
		   ::view-transition-new(root) { z-index: 1; animation: none; }`
		: `::view-transition-old(root) { z-index: 1; animation: none; }
		   ::view-transition-new(root) { z-index: 999; animation: none; }`;

	const transition = document.startViewTransition(() => {
		Dark.toggle();
		isDark.value = Dark.isActive;
		localStorage.setItem('darkMode', Dark.isActive);
	});

	await transition.ready;

	const animation = document.documentElement.animate(
		{
			clipPath: wasDark
				? [`circle(${endRadius}px at ${x}px ${y}px)`, `circle(0px at ${x}px ${y}px)`]
				: [`circle(0px at ${x}px ${y}px)`, `circle(${endRadius}px at ${x}px ${y}px)`]
		},
		{
			duration: 400,
			easing: 'ease-out',
			pseudoElement: wasDark
				? '::view-transition-old(root)'
				: '::view-transition-new(root)'
		}
	);

	await animation.finished;
	style.textContent = '';
}

// 点击切换按钮的处理函数
function toggleDarkClick(event) {
	toggleDark(event);
}

// 初始化深色模式
const savedDark = localStorage.getItem('darkMode');
if (savedDark !== null) {
	Dark.set(savedDark === 'true');
	isDark.value = Dark.isActive;
}

// 窗口置顶
async function toggleAlwaysOnTop() {
	await appStore.toggleAlwaysOnTop();
	$q.notify({
		message: appStore.alwaysOnTop ? '已置顶' : '已取消置顶',
		color: 'grey-7',
		textColor: 'white',
		position: 'top',
		timeout: 800,
		classes: 'compact-notify'
	});
}

// ==================== 窗口缩放 ====================
const resizeState = ref({
	isResizing: false,
	direction: '',
	startX: 0,
	startY: 0,
	startWidth: 0,
	startHeight: 0,
});

const MIN_WIDTH = 750;
const MIN_HEIGHT = 385;

function startResize(direction, event) {
	if (!window.pywebview) return;

	event.preventDefault();
	resizeState.value = {
		isResizing: true,
		direction,
		startX: event.screenX,
		startY: event.screenY,
		startWidth: appStore.screenWidth,
		startHeight: appStore.screenHeight,
	};

	document.addEventListener('mousemove', handleResize);
	document.addEventListener('mouseup', stopResize);
}

function handleResize(event) {
	if (!resizeState.value.isResizing) return;

	const { direction, startX, startY, startWidth, startHeight } = resizeState.value;
	const deltaX = event.screenX - startX;
	const deltaY = event.screenY - startY;

	let newWidth = startWidth;
	let newHeight = startHeight;

	if (direction.includes('right')) {
		newWidth = Math.max(MIN_WIDTH, startWidth + deltaX);
	}
	if (direction.includes('left')) {
		newWidth = Math.max(MIN_WIDTH, startWidth - deltaX);
	}
	if (direction.includes('bottom')) {
		newHeight = Math.max(MIN_HEIGHT, startHeight + deltaY);
	}
	if (direction.includes('top')) {
		newHeight = Math.max(MIN_HEIGHT, startHeight - deltaY);
	}

	newWidth = Math.min(newWidth, appStore.maxScreenWidth);
	newHeight = Math.min(newHeight, appStore.maxscreenHeight);

	appStore.screenWidth = newWidth;
	appStore.screenHeight = newHeight;
	windowApi.resize(newWidth, newHeight);
}

function stopResize() {
	if (resizeState.value.isResizing) {
		resizeState.value.isResizing = false;
		appStore.saveWindowSize();
	}
	document.removeEventListener('mousemove', handleResize);
	document.removeEventListener('mouseup', stopResize);
}

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

onMounted(async () => {
	try {
		await waitForPywebview();
		windowApi.resize(appStore.screenWidth, appStore.screenHeight);
		const alwaysOnTop = await windowApi.getAlwaysOnTop();
		appStore.initAlwaysOnTop(alwaysOnTop);
		await appStore.changeDirectory(appStore.directoryType, true);
	} catch (e) {
		console.error('pywebview 初始化超时:', e);
	}
});

onUnmounted(() => {
	document.removeEventListener('mousemove', handleResize);
	document.removeEventListener('mouseup', stopResize);
});

async function handleCheckPath(isInit = false) {
	const isValid = await appStore.checkPath(isInit);
	if (isValid && !isInit) {
		$q.notify({
			message: '修改目录成功',
			color: 'grey-7',
			textColor: 'white',
			position: 'top',
			timeout: 800,
			classes: 'compact-notify'
		});
	} else if (!isValid) {
		$q.notify({
			message: '目录不存在，应用目录失败',
			color: 'grey-7',
			textColor: 'white',
			position: 'top',
			timeout: 800,
			classes: 'compact-notify'
		});
	}
}

function winSetUpBeforeClose(done) {
	if (appStore.directoryType === 'diy' && !appStore.enablePath) {
		$q.notify({
			message: '请先检测自定义目录是否可用',
			color: 'grey-7',
			textColor: 'white',
			position: 'top',
			timeout: 800,
			classes: 'compact-notify'
		});
		return;
	}
	done();
}
</script>

<style lang="css" scoped>
.app-container {
	height: 100vh;
	width: 100%;
	display: flex;
	flex-direction: column;
	overflow: hidden;
}

/* 边缘缩放区域 */
.resize-edge {
	position: fixed;
	z-index: 9998;
	background: transparent;
}

.resize-bottom {
	bottom: 0;
	left: 12px;
	right: 12px;
	height: 4px;
	cursor: s-resize;
}

.resize-left {
	left: 0;
	top: 36px;
	bottom: 12px;
	width: 4px;
	cursor: w-resize;
}

.resize-right {
	right: 0;
	top: 36px;
	bottom: 12px;
	width: 4px;
	cursor: e-resize;
}

/* 角落缩放区域 */
.resize-corner {
	position: fixed;
	z-index: 9999;
	background: transparent;
	width: 16px;
	height: 16px;
}

.resize-tl {
	top: 0;
	left: 0;
	cursor: nw-resize;
}

.resize-tr {
	top: 0;
	right: 0;
	cursor: ne-resize;
}

.resize-bl {
	bottom: 0;
	left: 0;
	cursor: sw-resize;
}

.resize-br {
	bottom: 0;
	right: 0;
	cursor: se-resize;
}

/* 固定顶部 */
.app-header {
	flex-shrink: 0;
	display: flex;
	align-items: center;
	justify-content: space-between;
	padding: 4px 10px;
	font-size: 12px;
	min-height: 32px;
}

.header-left {
	display: flex;
	align-items: center;
	padding: 0 8px;
}

.header-right {
	display: flex;
	align-items: center;
}

/* 可滚动内容区 */
.app-body {
	flex: 1;
	min-height: 0;
	overflow: hidden;
	display: flex;
	flex-direction: column;
}

.app-form {
	padding: 0;
	flex: 1;
	display: flex;
	flex-direction: column;
	min-height: 0;
}

/* Tab 填满高度 */
.tab-panels {
	flex: 1;
	display: flex;
	flex-direction: column;
	min-height: 0;
	background: transparent;
}

.tab-panels :deep(.q-tab-panel) {
	flex: 1;
	overflow: hidden;
	display: flex;
	flex-direction: column;
	min-height: 0;
}

.app-title {
	font-size: 14px;
	font-weight: bold;
	margin-left: 8px;
}

.tab-header {
	background: rgba(0, 0, 0, 0.05);
	flex-shrink: 0;
}

.body--dark .tab-header {
	background: rgba(255, 255, 255, 0.05);
}

/* 退出弹窗样式 */
.exit-dialog {
	min-width: 200px;
	max-width: 280px;
	border-radius: 8px;
}
</style>
