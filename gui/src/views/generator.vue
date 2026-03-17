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
				<img src="@/assets/icons/jiaoayi.ico" @click.stop="appStore.winSetUp = true" style="width: 24px; height: 24px; -webkit-user-drag: none" />
				<span class="app-title">测试数据生成器</span>
			</div>
			<div class="header-right">
				<q-circular-progress
					class="demo-progress"
					:value="appStore.residuePercent"
					size="28px"
					:thickness="0.2"
					:color="progressColor"
					track-color="grey-4"
					show-value
				>
					<span class="percentage-value">{{ appStore.residuePercent }}%</span>
				</q-circular-progress>
				<q-toggle
					v-model="isDark"
					@update:model-value="toggleDark"
					checked-icon="dark_mode"
					unchecked-icon="light_mode"
					size="sm"
					class="q-mr-sm"
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

		<!-- 投币对话框 -->
		<q-dialog v-model="appStore.showNbDialog" persistent>
			<q-card class="coin-dialog">
				<q-card-section class="q-pa-sm">
					<div class="text-subtitle1 text-weight-medium text-center">这是另外的价钱</div>
				</q-card-section>

				<q-card-section class="q-pa-sm text-center">
					<div class="text-body2 text-grey q-mb-sm">牛币不足，请投币</div>
					<div class="q-mb-sm">
						<q-btn outline color="grey-6" label="我就不投" :disable="appStore.dialogBtnDisabled" @click="appStore.zaishuoyibian = true" size="sm" />
					</div>

					<q-carousel v-model="carouselSlide" animated height="200px" class="bg-transparent">
						<q-carousel-slide name="video" class="q-pa-none">
							<q-btn unelevated color="primary" label="投币" :disable="appStore.dialogBtnDisabled" @click="putCoins" class="coin-btn" />
							<video autoplay loop muted playsinline id="bgvid" style="width: 100%">
								<source src="@/assets/video/WeChat_20241219111716.mp4" type="video/webm" />
							</video>
						</q-carousel-slide>
						<q-carousel-slide name="qrcode" class="q-pa-none bg-black">
							<q-btn unelevated color="primary" label="投币" :disable="appStore.dialogBtnDisabled" @click="putCoins" class="coin-btn" />
							<div v-if="appStore.getQRStatus" id="imgid" style="text-align: center;"></div>
							<div v-if="!appStore.getQRStatus" style="text-align: center;">
								<img src="@/assets/img/inkwell_web.png" alt="二维码" style="max-height: 180px;" />
							</div>
						</q-carousel-slide>
					</q-carousel>
				</q-card-section>

				<!-- 再说一遍对话框 -->
				<q-dialog v-model="appStore.zaishuoyibian">
					<q-card>
						<q-card-section class="q-pa-none">
							<img src="@/assets/img/zaishuoyibian.jpg" alt="直视我" style="max-width: 300px;" />
						</q-card-section>
					</q-card>
				</q-dialog>
			</q-card>
		</q-dialog>

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

		<!-- 节日信息 -->
		<q-dialog v-model="appStore.festivalInfo">
			<q-card style="width: 1150px; max-width: 90vw;">
				<q-card-section class="text-h6">节日快乐</q-card-section>
				<q-card-section>
					<FestivalAnimation v-if="appStore.festivalInfo" />
				</q-card-section>
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
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useQuasar, Dark } from 'quasar';
import { useAppStore } from '@/stores';
import { useWindow } from '@/composables/useWindow';
import { windowApi } from '@/api';
import FestivalAnimation from '@/components/FestivalAnimation.vue';
import SettingsDrawer from '@/components/SettingsDrawer.vue';
import BasicInfoGenerator from '@/components/BasicInfoGenerator.vue';
import VehicleInfoGenerator from '@/components/VehicleInfoGenerator.vue';

const $q = useQuasar();
const appStore = useAppStore();
const { minimize, toggleMaximize, destroy } = useWindow();

const exitAppTip = ref(false);
const activeTab = ref('basic');
const carouselSlide = ref('video');

// 进度条颜色
const progressColor = computed(() => {
	const val = appStore.residuePercent;
	if (val <= 20) return 'negative';
	if (val <= 40) return 'warning';
	if (val <= 60) return 'positive';
	if (val <= 80) return 'info';
	return 'primary';
});

// 深色模式
const isDark = ref(Dark.isActive);

function toggleDark() {
	Dark.toggle();
	isDark.value = Dark.isActive;
	localStorage.setItem('darkMode', Dark.isActive);
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
		message: appStore.alwaysOnTop ? '窗口已置顶' : '窗口已取消置顶',
		color: 'positive',
		position: 'top',
		timeout: 1000
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

onMounted(async () => {
	windowApi.resize(appStore.screenWidth, appStore.screenHeight);
	// 从后端获取置顶状态
	const alwaysOnTop = await windowApi.getAlwaysOnTop();
	appStore.initAlwaysOnTop(alwaysOnTop);
	appStore.changeDirectory(appStore.directoryType, true);
	appStore.checkFestival();
});

onUnmounted(() => {
	document.removeEventListener('mousemove', handleResize);
	document.removeEventListener('mouseup', stopResize);
});

function putCoins() {
	let nb = Math.floor(Math.random() * 100);
	if (appStore.nbBalance + nb >= 100) {
		nb = 100 - appStore.nbBalance;
		$q.notify({
			message: '哇~，牛币爆表了！！！！',
			color: 'positive',
			position: 'top',
		});
	} else {
		$q.notify({
			message: '恭喜你，获得' + nb + '个牛币',
			color: 'positive',
			position: 'top',
		});
	}

	appStore.addNb(nb);
	appStore.showNbDialog = false;
}

async function handleCheckPath(isInit = false) {
	const isValid = await appStore.checkPath(isInit);
	if (isValid && !isInit) {
		$q.notify({
			message: '修改目录成功',
			color: 'positive',
			position: 'top',
		});
	} else if (!isValid) {
		$q.notify({
			message: '目录不存在，应用目录失败',
			color: 'negative',
			position: 'top',
		});
	}
}

function winSetUpBeforeClose(done) {
	if (appStore.directoryType === 'diy' && !appStore.enablePath) {
		$q.notify({
			message: '请先检测自定义目录是否可用',
			color: 'warning',
			position: 'top',
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

/* 边缘缩放区域 - 避开拖拽区域 */
.resize-edge {
	position: fixed;
	z-index: 9998;
	background: transparent;
}

/* 顶部留给拖拽区域，通过角落缩放 */
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
}

.tab-panels :deep(.q-tab-panel) {
	flex: 1;
	overflow: hidden;
	display: flex;
	flex-direction: column;
	min-height: 0;
}

.demo-progress {
	margin-right: 6px;
}

.percentage-value {
	display: block;
	font-size: 8px;
}

.app-title {
	font-size: 14px;
	font-weight: bold;
	margin-left: 8px;
}

.countdown-btn {
	position: absolute;
	top: 10%;
	left: 90%;
	transform: translate(-50%, -50%);
	background-color: #4caf50;
	color: white;
	padding: 10px 20px;
	border: none;
	cursor: pointer;
	z-index: 1;
}

.tab-panels {
	background: transparent;
}

.tab-header {
	background: rgba(0, 0, 0, 0.05);
	flex-shrink: 0;
}

.body--dark .tab-header {
	background: rgba(255, 255, 255, 0.05);
}

/* 投币弹窗样式 */
.coin-dialog {
	width: 320px;
	max-width: 90vw;
}

.coin-dialog .coin-btn {
	position: absolute;
	top: 10px;
	right: 10px;
	z-index: 1;
	min-width: 60px;
}

/* 退出弹窗样式 */
.exit-dialog {
	min-width: 200px;
	max-width: 280px;
	border-radius: 8px;
}
</style>
