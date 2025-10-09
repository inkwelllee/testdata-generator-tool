import { ElMessage } from 'element-plus';

export function copyToClipboard(text) {
	if (navigator.clipboard) {
		navigator.clipboard
			.writeText(text)
			.then(() => {
				ElMessage.success('复制成功');
			})
			.catch(err => {
				ElMessage.error('复制失败: ' + err);
			});
	} else {
		const textArea = document.createElement('textarea');
		textArea.value = text;
		document.body.appendChild(textArea);
		textArea.select();
		try {
			document.execCommand('copy');
			ElMessage.success('复制成功');
		} catch (err) {
			ElMessage.error('复制失败: ' + err);
		}
		document.body.removeChild(textArea);
	}
}
