import { createApp } from 'vue';
import { createPinia } from 'pinia';
import { Quasar, Notify, Dark, Dialog } from 'quasar';

// Quasar 样式
import '@quasar/extras/material-icons/material-icons.css';
import 'quasar/src/css/index.sass';

import App from './App.vue';
import { router } from './router/index';

const app = createApp(App);

const pinia = createPinia();

app.use(pinia);
app.use(Quasar, {
	plugins: { Notify, Dark, Dialog },
	config: {
		dark: 'auto', // 跟随系统
		notify: {
			position: 'top',
			timeout: 2500,
		}
	}
});
app.use(router);

app.mount('#app');
