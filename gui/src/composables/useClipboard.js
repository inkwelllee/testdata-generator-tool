import { useAppStore } from '@/stores';
import { copyToClipboard } from '@/utils';

/**
 * 剪贴板组合式函数
 */
export function useClipboard() {
	function copy(text) {
		copyToClipboard(text);
	}

	return { copy };
}
