import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { windowApi, pathApi } from '@/api';

export const useAppStore = defineStore('app', () => {
	// 窗口配置
	const winSetUp = ref(false);
	const restoreWindow = ref(false);
	const screenWidth = ref((localStorage.getItem('screenWidth') || 750) * 1);
	const screenHeight = ref((localStorage.getItem('screenHeight') || 385) * 1);
	const maxScreenWidth = ref(window.screen.width * window.devicePixelRatio || 1920);
	const maxscreenHeight = ref(window.screen.height * window.devicePixelRatio || 1080);

	// 目录配置
	const directoryType = ref(localStorage.getItem('directoryType') || 'desktop');
	const enablePath = ref(localStorage.getItem('enablePath') === 'true' || false);
	const directoryPath = ref(localStorage.getItem('directoryPath') || '');

	// 牛币余额
	const nbBalance = ref((localStorage.getItem('nbBalance') || 100) * 1);

	// 加载状态
	const loading = ref(false);

	// 对话框状态
	const showNbDialog = ref(false);
	const dialogBtnDisabled = ref(true);
	const zaishuoyibian = ref(false);
	const getQRStatus = ref(false);
	const festivalInfo = ref(false);

	// 退出提示
	const exitTipList = [
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
	const exitTipText = ref(exitTipList[Math.floor(Math.random() * exitTipList.length)]);

	// 计算属性
	const residuePercent = computed(() => nbBalance.value);

	// 窗口操作
	function minimize() {
		windowApi.minimize();
	}

	function toggleMaximize() {
		restoreWindow.value = !restoreWindow.value;
		if (restoreWindow.value) {
			windowApi.maximize();
		} else {
			windowApi.restore();
		}
	}

	function resize(width, height) {
		if (width && height) {
			screenWidth.value = width;
			screenHeight.value = height;
		}
		windowApi.resize(screenWidth.value, screenHeight.value);
		saveWindowSize();
	}

	function saveWindowSize() {
		localStorage.setItem('screenWidth', screenWidth.value);
		localStorage.setItem('screenHeight', screenHeight.value);
	}

	function destroy() {
		windowApi.destroy();
	}

	// 目录操作
	async function changeDirectory(type, isInit = false) {
		directoryType.value = type;
		localStorage.setItem('directoryType', type);

		if (type === 'diy') {
			directoryPath.value = localStorage.getItem('directoryPath') || '';
			if (directoryPath.value) {
				await checkPath(isInit);
			}
			return;
		}

		const path = await pathApi.changeDirectory(type);
		enablePath.value = false;
		directoryPath.value = path;
	}

	function updateDirectoryPath(path) {
		directoryPath.value = path;
		enablePath.value = false;
	}

	async function checkPath(isInit = false) {
		const path = directoryPath.value;
		if (!path) return false;

		const isValid = await pathApi.checkPath(path);
		enablePath.value = isValid;

		if (isValid) {
			localStorage.setItem('enablePath', 'true');
			localStorage.setItem('directoryPath', path);
		}

		return isValid;
	}

	// 余额管理
	function checkNbBalance(isInit = false, consume = 0) {
		if (!isInit && nbBalance.value <= consume) {
			showNbDialog.value = true;
			dialogBtnDisabled.value = true;
			setTimeout(() => {
				dialogBtnDisabled.value = false;
			}, 3000);
			return true;
		}
		return false;
	}

	function consumeNb(amount) {
		nbBalance.value = Math.max(nbBalance.value - amount, 0);
		localStorage.setItem('nbBalance', nbBalance.value);
	}

	function addNb(amount) {
		nbBalance.value = Math.min(nbBalance.value + amount, 100);
		localStorage.setItem('nbBalance', nbBalance.value);
	}

	// 加载状态
	function setLoading(val) {
		loading.value = val;
	}

	// 节日检查
	function checkFestival() {
		const today = new Date();
		const month = today.getMonth() + 1;
		const day = today.getDate();

		if (month === 1 && day >= 1 && day <= 7) {
			festivalInfo.value = true;
			setTimeout(() => {
				festivalInfo.value = false;
			}, 91500);
		}
	}

	// 窗口配置对象（用于传递给 SettingsDrawer）
	const windowConfig = computed(() => ({
		winSetUp: winSetUp.value,
		restoreWindow: restoreWindow.value,
		screenWidth: screenWidth.value,
		screenHeight: screenHeight.value,
		maxScreenWidth: maxScreenWidth.value,
		maxscreenHeight: maxscreenHeight.value,
		exitTipText: exitTipText.value,
		getQRStatus: getQRStatus.value,
		zaishuoyibian: zaishuoyibian.value,
		festivalInfo: festivalInfo.value,
		directoryType: directoryType.value,
		enablePath: enablePath.value,
		directoryPath: directoryPath.value,
	}));

	return {
		// 状态
		winSetUp,
		restoreWindow,
		screenWidth,
		screenHeight,
		maxScreenWidth,
		maxscreenHeight,
		directoryType,
		enablePath,
		directoryPath,
		nbBalance,
		loading,
		showNbDialog,
		dialogBtnDisabled,
		zaishuoyibian,
		getQRStatus,
		festivalInfo,
		exitTipText,
		residuePercent,
		windowConfig,

		// 方法
		minimize,
		toggleMaximize,
		resize,
		saveWindowSize,
		destroy,
		changeDirectory,
		updateDirectoryPath,
		checkPath,
		checkNbBalance,
		consumeNb,
		addNb,
		setLoading,
		checkFestival,
	};
});
