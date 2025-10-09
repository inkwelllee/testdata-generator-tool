import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

// https://vite.dev/config/
export default defineConfig({
	publicPath: './',
	base: './',
	plugins: [vue()],
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
