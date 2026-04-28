export function copyToClipboard(text) {
	return new Promise((resolve, reject) => {
		if (navigator.clipboard) {
			navigator.clipboard
				.writeText(text)
				.then(() => {
					resolve(true);
				})
				.catch(err => {
					reject(err);
				});
		} else {
			const textArea = document.createElement('textarea');
			textArea.value = text;
			document.body.appendChild(textArea);
			textArea.select();
			try {
				document.execCommand('copy');
				resolve(true);
			} catch (err) {
				reject(err);
			}
			document.body.removeChild(textArea);
		}
	});
}
