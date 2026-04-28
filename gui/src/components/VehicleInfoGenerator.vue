<template>
	<div class="generator-container">
		<n-grid :cols="3" :x-gap="12" :y-gap="8">
			<n-gi>
				<n-card title="车辆信息" size="small" :bordered="true">
					<n-form-item v-for="(label, field) in vehicleInfoFields" :key="field" :label="label" label-placement="left" label-width="80">
						<n-input-group>
							<n-input v-model:value="formData[field]" readonly @click="copy(field)" size="small" style="cursor: pointer" />
							<n-button size="small" @click="generator(field)">
								<template #icon><n-icon><FingerPrintOutline /></n-icon></template>
							</n-button>
						</n-input-group>
					</n-form-item>
				</n-card>
			</n-gi>
		</n-grid>

		<!-- 按钮 -->
		<n-space style="padding-top: 12px; justify-content: flex-start">
			<n-button type="primary" size="small" @click="generator('all')">
				<template #icon><n-icon><FingerPrintOutline /></n-icon></template>
				生成
			</n-button>
			<n-button size="small" @click="resetForm">
				<template #icon><n-icon><RefreshOutline /></n-icon></template>
				重置
			</n-button>
		</n-space>
	</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useMessage } from 'naive-ui';
import { RefreshOutline, FingerPrintOutline } from '@vicons/ionicons5';
import { copyToClipboard } from '@/utils';

const message = useMessage();

const props = defineProps({
	checkNbBalance: Function,
	setFormLoading: Function,
	consumeNb: Function,
});

const formData = ref({
	licensePlate: '',
	vin: '',
	engineNo: '',
	address: '',
});

const vehicleInfoFields = {
	licensePlate: '车牌号',
	vin: '车架号',
	engineNo: '发动机号',
	address: '所在位置',
};

onMounted(() => {
	if (window.pywebview) {
		generator('all', true);
	} else {
		window.addEventListener('pywebviewready', () => generator('all', true));
	}
});

function generator(type, isInit = false) {
	if (props.checkNbBalance(isInit)) return;
	props.setFormLoading(true);

	try {
		const api = window.pywebview?.api;
		if (!api) return;

		const actions = {
			licensePlate: () => api.randomLicensePlate().then(v => formData.value.licensePlate = v),
			vin: () => api.randomVIN().then(v => formData.value.vin = v),
			engineNo: () => api.randomEngineNo().then(v => formData.value.engineNo = v),
			address: () => api.randomAddress().then(v => formData.value.address = v),
			all: () => Object.keys(vehicleInfoFields).forEach(generator)
		};

		if (actions[type]) actions[type]();
	} catch (error) {
		console.error('generator', error);
	}

	setTimeout(() => {
		props.setFormLoading(false);
		if (!isInit && type === 'all') props.consumeNb(1);
	}, 500);
}

function copy(field) {
	copyToClipboard(formData.value[field])
		.then(() => message.success('复制成功'))
		.catch(() => message.error('复制失败'));
}

function resetForm() {
	formData.value = { licensePlate: '', vin: '', engineNo: '', address: '' };
}
</script>

<style scoped>
.generator-container {
	display: flex;
	flex-direction: column;
}
</style>
