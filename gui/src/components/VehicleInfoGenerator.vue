<template>
	<div class="generator-container">
		<div class="card-grid">
			<q-card flat bordered>
				<q-card-section class="card-header q-pa-sm">
					<div class="text-weight-bold text-body2">车辆信息</div>
				</q-card-section>
				<q-card-section class="q-pa-sm">
					<div class="row q-col-gutter-sm" v-for="(label, field) in generatorStore.vehicleInfoFields" :key="field">
						<div class="col-12">
							<q-input
								v-model="generatorStore.vehicleInfo[field]"
								dense
								borderless
								class="input-field"
								:label="label"
								readonly
								@click="copyToClipboard(generatorStore.vehicleInfo[field])"
							>
								<template v-slot:append>
									<q-btn flat round dense icon="touch_app" size="sm" @click.stop="generate(field)" />
								</template>
							</q-input>
						</div>
					</div>
				</q-card-section>
			</q-card>
		</div>
		<!-- 按钮 -->
		<div class="q-pt-sm">
			<div class="mb-4">
				<q-btn color="primary" icon="touch_app" label="生成" @click="generateAll" size="sm" />
				<q-btn color="grey-7" icon="refresh" label="重置" @click="resetAll" size="sm" class="q-ml-sm" />
			</div>
		</div>
	</div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useAppStore, useGeneratorStore } from '@/stores';
import { copyToClipboard } from '@/utils';

const appStore = useAppStore();
const generatorStore = useGeneratorStore();

async function generate(field) {
	if (appStore.checkNbBalance(false)) return;

	appStore.setLoading(true);
	try {
		if (generatorStore.vehicleApiMap[field]) {
			const value = await generatorStore.vehicleApiMap[field]();
			generatorStore.updateVehicleField(field, value);
		}
	} catch (error) {
		console.error(`generate ${field}:`, error);
	} finally {
		setTimeout(() => {
			appStore.setLoading(false);
		}, 100);
	}
}

async function generateAll(isInit = false) {
	const isInitFlag = isInit === true;

	if (appStore.checkNbBalance(isInitFlag)) return;

	appStore.setLoading(true);

	try {
		const promises = Object.keys(generatorStore.vehicleApiMap).map(field => {
			return generatorStore.vehicleApiMap[field]().then(value => {
				generatorStore.updateVehicleField(field, value);
			});
		});

		await Promise.all(promises);

		if (!isInitFlag) {
			appStore.consumeNb(1);
		}
	} catch (error) {
		console.error('generateAll:', error);
	} finally {
		setTimeout(() => {
			appStore.setLoading(false);
		}, 500);
	}
}

function resetAll() {
	generatorStore.resetVehicleInfo();
}

onMounted(() => {
	if (window.pywebview) {
		generateAll(true);
	} else {
		window.addEventListener('pywebviewready', () => {
			generateAll(true);
		});
	}
});
</script>

<style lang="css" scoped>
.generator-container {
	display: flex;
	flex-direction: column;
	height: 100%;
}

.card-header {
	border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.body--dark .card-header {
	border-bottom-color: rgba(255, 255, 255, 0.12);
}

.mb-4 {
	display: flex;
	gap: 8px;
	flex-shrink: 0;
}

/* CSS Grid 等高卡片布局 - 填满剩余高度 */
.card-grid {
	display: grid;
	grid-template-columns: repeat(3, 1fr);
	gap: 8px;
	align-items: stretch;
	flex: 1;
	min-height: 0;
}

.card-grid > .q-card {
	display: flex;
	flex-direction: column;
	min-height: 0;
}

.card-grid > .q-card > .q-card__section:last-child {
	flex: 1;
	overflow-y: auto;
	min-height: 0;
}

/* 隐藏卡片内滚动条 */
.card-grid > .q-card > .q-card__section:last-child::-webkit-scrollbar {
	display: none;
}

/* 增加字段行间距 */
.card-grid :deep(.row.q-col-gutter-sm) {
	margin-bottom: 8px;
}

.card-grid :deep(.row.q-col-gutter-sm:last-child) {
	margin-bottom: 0;
}

/* 输入框样式 - 简洁底部边框 */
.input-field {
	cursor: pointer;
	border-bottom: 1px solid rgba(0, 0, 0, 0.12);
	border-radius: 0;
}

.input-field:hover {
	border-bottom-color: rgba(0, 0, 0, 0.24);
}

.body--dark .input-field {
	border-bottom-color: rgba(255, 255, 255, 0.12);
}

.body--dark .input-field:hover {
	border-bottom-color: rgba(255, 255, 255, 0.24);
}

/* 输入框聚焦时的高亮 */
.input-field.q-field--focused {
	border-bottom-color: var(--q-primary);
}

.input-field :deep(.q-field__control) {
	background: transparent !important;
	padding: 0 4px;
	height: 32px;
}

.input-field :deep(.q-field__label) {
	font-size: 13px;
	top: 7px;
}

/* 浮动后的标签样式 - 保持可读大小 */
.input-field.q-field--float :deep(.q-field__label) {
	font-size: 12px;
	transform: translateY(-60%) scale(1);
	max-width: 100%;
}

.input-field :deep(.q-field__native) {
	padding-top: 14px;
	font-size: 13px;
}
</style>
