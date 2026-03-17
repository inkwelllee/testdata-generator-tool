import { useAppStore } from '@/stores';
import { windowApi } from '@/api';

/**
 * 窗口控制组合式函数
 */
export function useWindow() {
	const appStore = useAppStore();

	function minimize() {
		windowApi.minimize();
	}

	function toggleMaximize() {
		appStore.restoreWindow = !appStore.restoreWindow;
		if (appStore.restoreWindow) {
			windowApi.maximize();
		} else {
			windowApi.restore();
		}
	}

	function resize(width, height) {
		if (width && height) {
			appStore.screenWidth = width;
			appStore.screenHeight = height;
		}
		windowApi.resize(appStore.screenWidth, appStore.screenHeight);
		appStore.saveWindowSize();
	}

	function destroy() {
		windowApi.destroy();
	}

	function resizeToDefault() {
		appStore.screenWidth = 1200;
		appStore.screenHeight = 700;
		appStore.saveWindowSize();
		windowApi.resize(1200, 700);
	}

	return {
		minimize,
		toggleMaximize,
		resize,
		destroy,
		resizeToDefault,
	};
}
