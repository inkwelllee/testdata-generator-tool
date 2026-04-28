import { createRouter, createWebHashHistory } from 'vue-router';

const routes = [
	{
		path: '/',
		component: () => import('@/views/generator.vue'),
	},
	{
		path: '/verify',
		component: () => import('@/views/Verification.vue'),
	},
];

export const router = createRouter({
	history: createWebHashHistory(),
	routes,
});
