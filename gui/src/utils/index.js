import { Notify } from 'quasar';

export function copyToClipboard(text) {
	if (navigator.clipboard) {
		navigator.clipboard
			.writeText(text)
			.then(() => {
				Notify.create({
					message: '复制成功',
					icon: 'content_copy',
					position: 'top',
					timeout: 1500,
					classes: 'notify-toast',
				});
			})
			.catch(err => {
				Notify.create({
					message: '复制失败',
					icon: 'error',
					position: 'top',
					color: 'negative',
					timeout: 2000,
				});
			});
	} else {
		const textArea = document.createElement('textarea');
		textArea.value = text;
		document.body.appendChild(textArea);
		textArea.select();
		try {
			document.execCommand('copy');
			Notify.create({
				message: '复制成功',
				icon: 'content_copy',
				position: 'top',
				timeout: 1500,
				classes: 'notify-toast',
			});
		} catch (err) {
			Notify.create({
				message: '复制失败',
				icon: 'error',
				position: 'top',
				color: 'negative',
				timeout: 2000,
			});
		}
		document.body.removeChild(textArea);
	}
}
