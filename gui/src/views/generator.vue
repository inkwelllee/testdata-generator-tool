<template>
	<div class="app-container" :class="{ 'is-dark': isDark }">
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
				<img src="@/assets/icons/jiaoayi.ico" @click.stop="windowConfig.winSetUp = true" style="width: 20px; height: 20px; -webkit-user-drag: none; cursor: pointer" />
				<span class="app-title">测试数据生成器</span>
			</div>
			<div class="header-right">
				<!-- 余额进度条 -->
				<n-progress type="dashboard" :percentage="residuePercent" :color="progressColor" :stroke-width="12" style="width: 28px; height: 28px; --n-font-size-circle: 10px" />
				<!-- 切换主题 -->
				<n-switch :value="isDark" @update:value="handleDarkClick" size="small">
					<template #checked-icon><moon-icon /></template>
					<template #unchecked-icon><sun-icon /></template>
				</n-switch>
				<!-- 窗口置顶按钮 -->
				<n-button :type="alwaysOnTop ? 'primary' : 'default'" size="tiny" @click="toggleAlwaysOnTop" circle>
					<template #icon><n-icon><top-icon /></n-icon></template>
				</n-button>
				<!-- 窗口按钮 -->
				<n-button size="tiny" quaternary @click="minimizeApp">
					<template #icon><n-icon><minus-icon /></n-icon></template>
				</n-button>
				<n-button size="tiny" quaternary @click="restoreApp">
					<template #icon>
						<n-icon><fullscreen-icon v-if="!windowConfig.restoreWindow" /><restore-icon v-else /></n-icon>
					</template>
				</n-button>
				<n-button size="tiny" quaternary type="error" @click="exitAppTip = true">
					<template #icon><n-icon><close-icon /></n-icon></template>
				</n-button>
			</div>
		</div>

		<!-- 可滚动内容区 -->
		<div class="app-body">
			<n-scrollbar>
				<div class="app-form" :class="{ 'loading-overlay': formLoading }">
					<n-tabs type="line" animated>
						<n-tab-pane name="basic" tab="基础信息">
							<BasicInfoGenerator
								:checkNbBalance="checkNbBalance"
								:windowConfig="windowConfig"
								:setFormLoading="setFormLoading"
								:consumeNb="consumeNb"
							/>
						</n-tab-pane>
						<n-tab-pane name="vehicle" tab="车辆信息">
							<VehicleInfoGenerator
								:checkNbBalance="checkNbBalance"
								:setFormLoading="setFormLoading"
								:consumeNb="consumeNb"
							/>
						</n-tab-pane>
					</n-tabs>
				</div>
			</n-scrollbar>
		</div>

		<!-- 投币 -->
		<n-modal v-model:show="dialogVisible" preset="card" title="这是另外的价钱" style="width: 450px" :mask-closable="false">
			<div class="block text-center" style="height: 260px">
				<span class="demonstration">牛币不足，请投币</span>
				<n-button text type="error" @click="windowConfig.zaishuoyibian = true" :disabled="dialogBtnDisabled" style="position: absolute; top: 10%; right: 5%">我就不投</n-button>

				<n-modal v-model:show="windowConfig.zaishuoyibian" preset="card" style="width: auto">
					<img src="@/assets/img/zaishuoyibian.jpg" alt="直视我" style="max-width: 400px" />
				</n-modal>

				<n-carousel autoplay :interval="3000" style="height: 220px; margin-top: 20px">
					<n-carousel-item style="display: flex; align-items: center; justify-content: center">
						<n-button text type="primary" @click="putCoins" :disabled="dialogBtnDisabled" style="position: absolute; top: 5%; right: 5%">投币</n-button>
						<video autoplay loop muted playsinline id="bgvid" style="width: 100%">
							<source src="@/assets/video/WeChat_20241219111716.mp4" type="video/webm" />
						</video>
					</n-carousel-item>
					<n-carousel-item style="display: flex; align-items: center; justify-content: center; background-color: #000">
						<n-button text type="primary" @click="putCoins" :disabled="dialogBtnDisabled" style="position: absolute; top: 5%; right: 5%">投币</n-button>
						<div v-if="windowConfig.getQRStatus" id="imgid" style="text-align: center"></div>
						<div v-if="!windowConfig.getQRStatus" style="text-align: center">
							<img src="@/assets/img/inkwell_web.png" alt="二维码" style="max-width: 260px" />
						</div>
					</n-carousel-item>
				</n-carousel>
			</div>
		</n-modal>

		<!-- 退出提示 -->
		<n-modal v-model:show="exitAppTip" preset="dialog" title="提示" :show-icon="false">
			<h2 style="text-align: center">{{ windowConfig.exitTipText }}</h2>
			<template #action>
				<n-button type="primary" @click="destroyApp">确定</n-button>
			</template>
		</n-modal>

		<!-- 节日信息 -->
		<n-modal v-model:show="windowConfig.festivalInfo" style="width: 1100px; height: 550px">
			<FestivalAnimation v-if="windowConfig.festivalInfo" />
		</n-modal>

		<!-- 设置按钮 -->
		<SettingsDrawer
			v-model:visible="windowConfig.winSetUp"
			:config="windowConfig"
			:resizeApp="resizeApp"
			:saveWinSizeItem="saveWinSizeItem"
			:changeDirectory="changeDirectory"
			:changePath="changePath"
			:checkPath="checkPath"
			:beforeClose="winSetUpBeforeClose"
		/>
	</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useMessage } from 'naive-ui';
import {
	RemoveOutline,
	CloseOutline,
	ArrowUpOutline,
	CopyOutline,
	ExpandOutline,
	ContractOutline,
} from '@vicons/ionicons5';
import axios from 'axios';
import { useDark } from '@vueuse/core';
import SunIcon from '@/assets/icons/sun.vue';
import MoonIcon from '@/assets/icons/moon.vue';
import FestivalAnimation from '@/components/FestivalAnimation.vue';
import SettingsDrawer from '@/components/SettingsDrawer.vue';
import BasicInfoGenerator from '@/components/BasicInfoGenerator.vue';
import VehicleInfoGenerator from '@/components/VehicleInfoGenerator.vue';

// 图标别名
const MinusIcon = RemoveOutline;
const CloseIcon = CloseOutline;
const TopIcon = ArrowUpOutline;
const CopyIcon = CopyOutline;
const FullscreenIcon = ExpandOutline;
const RestoreIcon = ContractOutline;

const message = useMessage();

// 进度条颜色
const progressColor = computed(() => {
	const p = residuePercent.value;
	if (p <= 20) return '#f56c6c';
	if (p <= 40) return '#e6a23c';
	if (p <= 60) return '#5cb87a';
	if (p <= 80) return '#1989fa';
	return '#6f7ad3';
});

// 深色模式
const isDark = useDark();

// 点击切换按钮时捕获位置并触发切换
function handleDarkClick(value) {
	const event = window.event || { clientX: window.innerWidth / 2, clientY: window.innerHeight / 2 };
	const x = event.clientX;
	const y = event.clientY;

	if (!document.startViewTransition) {
		isDark.value = value;
		return;
	}

	const wasDark = isDark.value;
	const endRadius = Math.hypot(
		Math.max(x, window.innerWidth - x),
		Math.max(y, window.innerHeight - y)
	);

	const styleId = 'dark-transition-override';
	let style = document.getElementById(styleId);
	if (!style) {
		style = document.createElement('style');
		style.id = styleId;
		document.head.appendChild(style);
	}

	style.textContent = wasDark
		? `::view-transition-old(root) { z-index: 999; animation: none; }
		   ::view-transition-new(root) { z-index: 1; animation: none; }`
		: `::view-transition-old(root) { z-index: 1; animation: none; }
		   ::view-transition-new(root) { z-index: 999; animation: none; }`;

	const transition = document.startViewTransition(() => {
		isDark.value = value;
	});

	transition.ready.then(() => {
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

		animation.finished.then(() => {
			style.textContent = '';
		});
	});
}

const formLoading = ref(false);
const dialogVisible = ref(false);
const exitAppTip = ref(false);
const dialogBtnDisabled = ref(true);
const residuePercent = ref(100);
const alwaysOnTop = ref(false);

const windowConfig = ref({
	winSetUp: false,
	restoreWindow: false,
	screenWidth: (localStorage.getItem('screenWidth') || 900) * 1,
	screenHeight: (localStorage.getItem('screenHeight') || 500) * 1,
	maxScreenWidth: window.screen.width * window.devicePixelRatio || 1920,
	maxscreenHeight: window.screen.height * window.devicePixelRatio || 1080,
	exitTipText: '暂别勿思念，转瞬与亲见',
	tangDaren: '',
	getQRStatus: false,
	zaishuoyibian: false,
	festivalInfo: false,
	directoryType: localStorage.getItem('directoryType') || 'desktop',
	enablePath: localStorage.getItem('enablePath') || false,
	directoryPath: localStorage.getItem('directoryPath') || '',
});

// 边缘缩放状态
const resizeState = ref({
	isResizing: false,
	direction: '',
	startX: 0,
	startY: 0,
	startWidth: 0,
	startHeight: 0,
});

const MIN_WIDTH = 900;
const MIN_HEIGHT = 500;

// pywebview 就绪检测
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

// 边缘缩放
function startResize(direction, event) {
	if (!window.pywebview) return;

	event.preventDefault();
	resizeState.value = {
		isResizing: true,
		direction,
		startX: event.screenX,
		startY: event.screenY,
		startWidth: windowConfig.value.screenWidth,
		startHeight: windowConfig.value.screenHeight,
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

	newWidth = Math.min(newWidth, windowConfig.value.maxScreenWidth);
	newHeight = Math.min(newHeight, windowConfig.value.maxscreenHeight);

	windowConfig.value.screenWidth = newWidth;
	windowConfig.value.screenHeight = newHeight;
	window.pywebview.api.resizeApp(newWidth, newHeight);
}

function stopResize() {
	if (resizeState.value.isResizing) {
		resizeState.value.isResizing = false;
		saveWinSizeItem();
	}
	document.removeEventListener('mousemove', handleResize);
	document.removeEventListener('mouseup', stopResize);
}

// 窗口置顶
async function toggleAlwaysOnTop() {
	try {
		const newState = await window.pywebview.api.toggleAlwaysOnTop();
		alwaysOnTop.value = newState;
		message.success(newState ? '已置顶' : '已取消置顶', { duration: 1000 });
	} catch (error) {
		console.error('toggleAlwaysOnTop', error);
	}
}

const exitTip = [
	'暂别勿思念，转瞬与亲见',
	'暂别莫惆怅，不久再相逢',
	'离别有时，重逢有期',
	'暂别且安心，相逢终有时',
	'暂时的离别，是为了更好的相遇',
	'离别只是短暂，期待再次相遇',
	'离别之刻，重逢在望',
	'此刻虽离别，相逢在眼前',
	'这就走了？',
	'好吧，再见',
	'好吧，记得想我',
];

onMounted(async () => {
	windowConfig.value.exitTipText = exitTip[Math.floor(Math.random() * exitTip.length)];
	residuePercent.value = (localStorage.getItem('nbBalance') || 100) * 1;

	try {
		await waitForPywebview();
		const topState = await window.pywebview.api.getAlwaysOnTop();
		alwaysOnTop.value = topState;
	} catch (error) {
		console.warn('pywebview not ready, skipping window controls init');
	}

	setTimeout(() => {
		resizeApp();
		saveWinSizeItem();
		changeDirectory(windowConfig.value.directoryType, true);
	}, 100);

	showFestivalInfo();
});

onUnmounted(() => {
	document.removeEventListener('mousemove', handleResize);
	document.removeEventListener('mouseup', stopResize);
});

function showFestivalInfo() {
	const today = new Date();
	const month = today.getMonth() + 1;
	const day = today.getDate();

	if (month === 1 && day >= 1 && day <= 7) {
		windowConfig.value.festivalInfo = true;
		setTimeout(() => {
			windowConfig.value.festivalInfo = false;
		}, 91500);
	}
}

function setFormLoading(val) {
	formLoading.value = val;
}

function consumeNb(val) {
	residuePercent.value = Math.max(residuePercent.value - val, 0);
	localStorage.setItem('nbBalance', residuePercent.value);
}

function checkNbBalance(isInit = false, consume = 0) {
	if (!isInit && residuePercent.value <= consume) {
		dialogBtnDisabled.value = true;
		dialogVisible.value = true;
		getQRCode();
		setTimeout(() => {
			dialogBtnDisabled.value = false;
		}, 3000);
		return true;
	}
	return false;
}

function putCoins() {
	let nb = Math.floor(Math.random() * 100);
	if (residuePercent.value + nb >= 100) {
		nb = 100 - residuePercent.value;
		message.success('哇~，牛币爆表了！！！！');
	} else {
		message.success('恭喜你，获得' + nb + '个牛币');
	}

	residuePercent.value = residuePercent.value + nb;
	localStorage.setItem('nbBalance', residuePercent.value);
	dialogVisible.value = false;
}

function getQRCode() {
	try {
		const getImageUrl = 'https://oneapi.coderbox.cn/openapi/public/qrcode/simple?lightColor=Black&darkColor=rgb(180,180,180)&text=' + encodeURIComponent('https://inkwell.top/');
		axios({ url: getImageUrl, method: 'get', responseType: 'blob' })
			.then(Response => {
				const imageUrl = URL.createObjectURL(new Blob([Response.data]));
				const img = document.createElement('img');
				img.src = imageUrl;
				img.height = 260;
				img.width = 260;

				const container = document.getElementById('imgid');
				container.innerHTML = '';
				container.appendChild(img);
				windowConfig.value.getQRStatus = true;
			})
			.catch(error => {
				windowConfig.value.getQRStatus = false;
				console.error('There was an error!', error);
			});
	} catch (error) {
		windowConfig.value.getQRStatus = false;
		console.error('getQRCode');
	}
}

function changeDirectory(data, isInit = false) {
	try {
		localStorage.setItem('directoryType', data);
		if ('diy' === data) {
			windowConfig.value.directoryPath = localStorage.getItem('directoryPath') || '';
			if (windowConfig.value.directoryPath !== '') {
				checkPath(isInit);
			}
			return;
		}
		window.pywebview.api.changeDirectory(data).then(directoryPath => {
			windowConfig.value.enablePath = false;
			windowConfig.value.directoryPath = directoryPath;
		});
	} catch (error) {
		console.error('changeDirectory');
	}
}

function changePath() {
	windowConfig.value.enablePath = false;
}

function checkPath(isInit = false) {
	let directoryPath = windowConfig.value.directoryPath;
	if (!directoryPath) {
		message.warning('请先输入目录');
		return;
	}
	window.pywebview.api.checkPath(directoryPath).then(checkPath => {
		if (checkPath) {
			windowConfig.value.enablePath = true;
			localStorage.setItem('enablePath', true);
			localStorage.setItem('directoryPath', directoryPath);
			if (!isInit) {
				message.success('修改目录成功');
			}
		} else {
			windowConfig.value.enablePath = false;
			message.error('目录不存在，应用目录失败');
		}
	});
}

function winSetUpBeforeClose(done) {
	if (windowConfig.value.directoryType === 'diy' && !windowConfig.value.enablePath) {
		message.warning('请先检测自定义目录是否可用');
		return;
	}
	done();
}

function destroyApp() {
	try {
		window.pywebview.api.destroyApp();
	} catch (error) {
		console.error('destroyApp');
	}
}

function minimizeApp() {
	try {
		window.pywebview.api.minimizeApp();
	} catch (error) {
		console.error('minimizeApp');
	}
}

function restoreApp() {
	windowConfig.value.restoreWindow = !windowConfig.value.restoreWindow;
	try {
		if (windowConfig.value.restoreWindow) {
			window.pywebview.api.maximizeApp();
		} else {
			window.pywebview.api.restoreApp();
		}
	} catch (error) {
		console.error('restoreApp');
	}
}

function resizeApp(resizeType) {
	try {
		if ('resize' == resizeType) {
			windowConfig.value.screenWidth = 900;
			windowConfig.value.screenHeight = 500;
			saveWinSizeItem();
			window.pywebview.api.resizeApp(900, 500);
		} else {
			window.pywebview.api.resizeApp(windowConfig.value.screenWidth, windowConfig.value.screenHeight);
		}
	} catch (error) {
		console.error('resizeApp');
	}
}

function saveWinSizeItem() {
	try {
		localStorage.setItem('screenWidth', windowConfig.value.screenWidth);
		localStorage.setItem('screenHeight', windowConfig.value.screenHeight);
	} catch (error) {
		console.error('saveWinSizeItem');
	}
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
	left: 10px;
	right: 10px;
	height: 4px;
	cursor: s-resize;
}

.resize-left {
	left: 0;
	top: 32px;
	bottom: 10px;
	width: 4px;
	cursor: w-resize;
}

.resize-right {
	right: 0;
	top: 32px;
	bottom: 10px;
	width: 4px;
	cursor: e-resize;
}

/* 角落缩放区域 */
.resize-corner {
	position: fixed;
	z-index: 9999;
	background: transparent;
	width: 14px;
	height: 14px;
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
	height: 32px;
}

.header-left {
	display: flex;
	align-items: center;
	padding: 0 6px;
}

.header-right {
	display: flex;
	align-items: center;
	gap: 6px;
}

.app-title {
	font-size: 13px;
	font-weight: 500;
	margin-left: 6px;
}

.is-dark .app-title {
	color: rgba(255, 255, 255, 0.85);
}

.app-container:not(.is-dark) .app-title {
	color: rgba(0, 0, 0, 0.85);
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
	padding: 0 8px 8px 8px;
}

.app-form :deep(.n-tabs-nav) {
	margin-top: 0;
	padding-top: 0;
}
</style>
