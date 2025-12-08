<template>
	<el-row :gutter="15">
		<el-col :span="8">
			<el-card style="height: 500px">
				<template #header>
					<div class="card-header">
						<span>车辆信息</span>
					</div>
				</template>
				<el-row :gutter="10" v-for="(label, field) in vehicleInfoFields" :key="field">
					<el-col :span="24">
						<el-form-item :label="label">
							<el-col :span="24">
								<el-input v-model="formData[field]" readonly @click="copy(field)" style="cursor: pointer">
									<template #append>
										<el-button :icon="Pointer" @click="generator(field)"></el-button>
									</template>
								</el-input>
							</el-col>
						</el-form-item>
					</el-col>
				</el-row>
			</el-card>
		</el-col>
	</el-row>
	<!-- 按钮 -->
	<el-row :gutter="15" style="padding-top: 10px">
		<el-col :span="24">
			<el-form-item>
				<div class="mb-4">
					<el-button type="primary" :icon="Pointer" @click="generator('all')"> 生成 </el-button>
					<el-button type="info" :icon="Refresh" @click="resetForm">重置</el-button>
				</div>
			</el-form-item>
		</el-col>
	</el-row>
</template>

<script setup>
	import { ref, onMounted } from 'vue';
	import { CopyDocument, Pointer, Refresh } from '@element-plus/icons-vue';
	import { copyToClipboard } from '@/utils';

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
			window.addEventListener('pywebviewready', () => {
				generator('all', true);
			});
		}
	});

	function generator(type, isInit = false) {
		if (props.checkNbBalance(isInit)) {
			return;
		}

		props.setFormLoading(true);

		try {
			if (type === 'licensePlate') {
				window.pywebview.api.randomLicensePlate().then(val => {
					formData.value.licensePlate = val;
				});
			} else if (type === 'vin') {
				window.pywebview.api.randomVIN().then(val => {
					formData.value.vin = val;
				});
			} else if (type === 'engineNo') {
				window.pywebview.api.randomEngineNo().then(val => {
					formData.value.engineNo = val;
				});
			} else if (type === 'address') {
				window.pywebview.api.randomAddress().then(val => {
					formData.value.address = val;
				});
			} else if (type === 'all') {
				Object.keys(vehicleInfoFields).forEach(field => {
					generator(field);
				});
			}
		} catch (error) {
			console.error('generator');
			return;
		}

		setTimeout(async () => {
			props.setFormLoading(false);
			if (!isInit && type === 'all') {
				props.consumeNb(1);
			}
		}, 500);
	}

	function copy(field) {
		const text = formData.value[field];
		copyToClipboard(text);
	}

	function resetForm() {
		formData.value = {
			licensePlate: '',
			vin: '',
			engineNo: '',
			address: '',
		};
	}
</script>

<style lang="css" scoped>
	.card-header {
		font-weight: bold;
	}

	:deep(label) {
		font-weight: 500;
	}

	.el-button {
		transition: all 0.5s ease;
	}
</style>
