import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { windowApi, pathApi } from '@/api';

export const useAppStore = defineStore('app', () => {
	// 窗口配置
	const winSetUp = ref(false);
	const restoreWindow = ref(false);
	const alwaysOnTop = ref(false);
	const screenWidth = ref((localStorage.getItem('screenWidth') || 750) * 1);
	const screenHeight = ref((localStorage.getItem('screenHeight') || 385) * 1);
	const maxScreenWidth = ref(window.screen.width * window.devicePixelRatio || 1920);
	const maxscreenHeight = ref(window.screen.height * window.devicePixelRatio || 1080);

	// 目录配置
	const directoryType = ref(localStorage.getItem('directoryType') || 'desktop');
	const enablePath = ref(localStorage.getItem('enablePath') === 'true' || false);
	const directoryPath = ref(localStorage.getItem('directoryPath') || '');

	// 加载状态
	const loading = ref(false);

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

	async function toggleAlwaysOnTop() {
		const newState = await windowApi.toggleAlwaysOnTop();
		alwaysOnTop.value = newState;
	}

	function initAlwaysOnTop(state) {
		alwaysOnTop.value = state;
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

	// 加载状态
	function setLoading(val) {
		loading.value = val;
	}

	// 窗口配置对象
	const windowConfig = computed(() => ({
		winSetUp: winSetUp.value,
		restoreWindow: restoreWindow.value,
		screenWidth: screenWidth.value,
		screenHeight: screenHeight.value,
		maxScreenWidth: maxScreenWidth.value,
		maxscreenHeight: maxscreenHeight.value,
		exitTipText: exitTipText.value,
		directoryType: directoryType.value,
		enablePath: enablePath.value,
		directoryPath: directoryPath.value,
	}));

	return {
		// 状态
		winSetUp,
		restoreWindow,
		alwaysOnTop,
		screenWidth,
		screenHeight,
		maxScreenWidth,
		maxscreenHeight,
		directoryType,
		enablePath,
		directoryPath,
		loading,
		exitTipText,
		windowConfig,

		// 方法
		minimize,
		toggleMaximize,
		toggleAlwaysOnTop,
		initAlwaysOnTop,
		resize,
		saveWindowSize,
		destroy,
		changeDirectory,
		updateDirectoryPath,
		checkPath,
		setLoading,
	};
});
