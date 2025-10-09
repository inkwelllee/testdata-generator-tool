import { createApp } from 'vue';

import ElementPlus from 'element-plus';
import locale from 'element-plus/es/locale/lang/zh-cn';

import 'element-plus/dist/index.css';
import VueClipboard from 'vue-clipboard2';

// import "./style.css";
import 'element-plus/theme-chalk/dark/css-vars.css';
import App from './App.vue';
import { router } from './router/index';

const app = createApp(App);

app.use(ElementPlus, {
	locale: locale,
});
app.use(VueClipboard);
app.use(router);

app.mount('#app');
