import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import { quasar, transformAssetUrls } from '@quasar/vite-plugin';
import path from 'path';
import copyToUiPlugin from './vite-plugin-copy-to-ui.js';

// https://vite.dev/config/
export default defineConfig({
	publicPath: './',
	base: './',
	plugins: [
		vue({
			template: { transformAssetUrls }
		}),
		quasar({
			sassVariables: path.resolve(__dirname, './src/quasar-variables.scss')
		}),
		copyToUiPlugin() // 自动复制到ui目录
	],
	resolve: {
		alias: {
			'~': path.resolve(__dirname, './'),
			'@': path.resolve(__dirname, 'src'),
		},
		extensions: ['.mjs', '.js', '.ts', '.jsx', '.tsx', '.json', '.vue'],
	},
	server: {
		port: '8098',
		host: '0.0.0.0',
		open: true,
		cors: true,
		proxy: {},
	},
	build: {
		rollupOptions: {
			input: {
				index: path.resolve(__dirname, 'index.html'),
			},
		},
	},
});
