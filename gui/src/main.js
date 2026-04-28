import { createApp } from 'vue';
import naive from 'naive-ui';
import VueClipboard from 'vue-clipboard2';

import './style.css';
import App from './App.vue';
import { router } from './router/index';

const app = createApp(App);

app.use(naive);
app.use(VueClipboard);
app.use(router);

app.mount('#app');