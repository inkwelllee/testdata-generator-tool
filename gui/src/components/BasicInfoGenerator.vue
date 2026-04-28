<template>
	<div class="generator-container">
		<n-grid :cols="3" :x-gap="12" :y-gap="8">
			<!-- 身份信息 -->
			<n-gi>
				<n-card title="身份信息" size="small" :bordered="true">
					<n-grid :cols="2" :x-gap="8">
						<n-gi>
							<n-form-item label="性别" label-placement="top">
								<n-radio-group v-model:value="formData.gender" size="small">
									<n-radio-button :value="1">男</n-radio-button>
									<n-radio-button :value="0">女</n-radio-button>
								</n-radio-group>
							</n-form-item>
						</n-gi>
						<n-gi>
							<n-form-item label="出生日期" label-placement="top">
								<n-date-picker
									v-model:formatted-value="formData.birthday"
									type="date"
									format="yyyy-MM-dd"
									value-format="yyyy-MM-dd"
									size="small"
									style="width: 100%"
								/>
							</n-form-item>
						</n-gi>
					</n-grid>
					<n-form-item v-for="(label, field) in personalInfoFields" :key="field" :label="label" label-placement="top">
						<n-input-group>
							<n-input v-model:value="formData[field]" readonly @click="copy(field)" size="small" style="cursor: pointer" />
							<n-button size="tiny" @click="generator(field)">
								<template #icon><n-icon><FingerPrintOutline /></n-icon></template>
							</n-button>
						</n-input-group>
					</n-form-item>
				</n-card>
			</n-gi>

			<!-- 企业信息 -->
			<n-gi>
				<n-card title="企业信息" size="small" :bordered="true">
					<n-form-item v-for="(label, field) in companyInfoFields" :key="field" :label="label" label-placement="top">
						<n-input-group>
							<n-input v-model:value="formData[field]" readonly @click="copy(field)" size="small" style="cursor: pointer" />
							<n-button size="tiny" @click="generator(field)">
								<template #icon><n-icon><FingerPrintOutline /></n-icon></template>
							</n-button>
						</n-input-group>
					</n-form-item>
				</n-card>
			</n-gi>

			<!-- 账号信息 -->
			<n-gi>
				<n-card title="账号信息" size="small" :bordered="true">
					<n-form-item v-for="(label, field) in accountInfoFields" :key="field" :label="label" label-placement="top">
						<n-input-group>
							<n-input v-model:value="formData[field]" readonly @click="copy(field)" size="small" style="cursor: pointer" />
							<n-button size="tiny" @click="generator(field)">
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
			<n-button type="primary" ghost size="small" @click="generateIdCardImage">
				<template #icon><n-icon><PersonOutline /></n-icon></template>
				身份证
			</n-button>
			<n-button type="primary" ghost size="small" @click="generateBusinessImage">
				<template #icon><n-icon><CardOutline /></n-icon></template>
				营业执照
			</n-button>
		</n-space>
	</div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useMessage } from 'naive-ui';
import { RefreshOutline, PersonOutline, CardOutline, FingerPrintOutline } from '@vicons/ionicons5';
import moment from 'moment';
import { copyToClipboard } from '@/utils';

const message = useMessage();

const props = defineProps({
	checkNbBalance: Function,
	windowConfig: Object,
	setFormLoading: Function,
	consumeNb: Function,
});

const formData = ref({
	gender: 0,
	birthday: '1992-07-25',
	name: '',
	phone: '',
	email: '',
	idCard: '',
	company: '',
	socialCreditCode: '',
	organizationCode: '',
	zhongzhengCode: '',
	BOC: '',
	CCB: '',
	ABC: '',
	ICBC: '',
	PSBC: '',
});

const personalInfoFields = { name: '姓名', idCard: '身份证号', phone: '手机号', email: '邮箱' };
const companyInfoFields = { company: '公司名称', socialCreditCode: '统一社会信用代码', organizationCode: '组织机构代码', zhongzhengCode: '中征码' };
const accountInfoFields = { BOC: '中国银行', CCB: '建设银行', ABC: '农业银行', ICBC: '工商银行', PSBC: '邮储银行' };

onMounted(() => {
	formData.value.gender = Math.random() > 0.5 ? 1 : 0;
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
			name: () => api.randomName(formData.value.gender).then(v => formData.value.name = v),
			idCard: () => api.randomIdCard(formData.value.gender, formData.value.birthday).then(v => formData.value.idCard = v),
			phone: () => api.randomPhoneNumber().then(v => formData.value.phone = v),
			email: () => api.randomEmail().then(v => formData.value.email = v),
			company: () => api.randomCompanyName().then(v => formData.value.company = v),
			socialCreditCode: () => api.randomSocialCreditCode().then(v => formData.value.socialCreditCode = v),
			organizationCode: () => api.randomOrganizationCode().then(v => formData.value.organizationCode = v),
			zhongzhengCode: () => api.randomZhongzhengCode().then(v => formData.value.zhongzhengCode = v),
			BOC: () => api.randomBankAccount('BOC').then(v => formData.value.BOC = v),
			CCB: () => api.randomBankAccount('CCB').then(v => formData.value.CCB = v),
			ABC: () => api.randomBankAccount('ABC').then(v => formData.value.ABC = v),
			ICBC: () => api.randomBankAccount('ICBC').then(v => formData.value.ICBC = v),
			PSBC: () => api.randomBankAccount('PSBC').then(v => formData.value.PSBC = v),
			all: () => {
				[...Object.keys(personalInfoFields), ...Object.keys(companyInfoFields), ...Object.keys(accountInfoFields)].forEach(generator);
				formData.value.birthday = moment().year(Math.floor(Math.random() * 41) + 1960).dayOfYear(Math.floor(Math.random() * 365) + 1).format('YYYY-MM-DD');
			}
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
	formData.value = {
		gender: Math.random() > 0.5 ? 1 : 0,
		birthday: '1992-07-25',
		name: '', phone: '', email: '', idCard: '',
		company: '', socialCreditCode: '', organizationCode: '', zhongzhengCode: '',
		BOC: '', CCB: '', ABC: '', ICBC: '', PSBC: '',
	};
}

function generateIdCardImage() {
	if (props.checkNbBalance(false, 1)) return;
	props.setFormLoading(true);
	setTimeout(() => {
		try {
			window.pywebview.api.generateIdCardImage(formData.value.name, formData.value.gender, formData.value.birthday, formData.value.idCard, props.windowConfig.directoryPath)
				.then(msg => message.success(msg))
				.catch(err => message.error(err));
			props.consumeNb(2);
		} catch (error) {
			console.error('generateIdCardImage', error);
		}
		props.setFormLoading(false);
	}, 1000);
}

function generateBusinessImage() {
	if (props.checkNbBalance(false, 1)) return;
	props.setFormLoading(true);
	setTimeout(() => {
		try {
			window.pywebview.api.generateBusinessImage(formData.value.company, formData.value.socialCreditCode, formData.value.name, props.windowConfig.directoryPath)
				.then(msg => message.success(msg))
				.catch(err => message.error(err));
			props.consumeNb(2);
		} catch (error) {
			console.error('generateBusinessImage', error);
		}
		props.setFormLoading(false);
	}, 1000);
}
</script>

<style scoped>
.generator-container {
	display: flex;
	flex-direction: column;
}

.generator-container :deep(.n-form-item) {
	margin-bottom: 0;
}

.generator-container :deep(.n-form-item-label) {
	font-size: 11px;
	padding: 0;
	line-height: 1.2;
	height: 14px;
}

.generator-container :deep(.n-form-item-blank) {
	min-height: auto;
}

.generator-container :deep(.n-card__content) {
	padding: 4px 6px;
}

.generator-container :deep(.n-card-header) {
	padding: 3px 6px;
}

.generator-container :deep(.n-input) {
	font-size: 12px;
}

.generator-container :deep(.n-input .n-input__input-el) {
	height: 22px;
	line-height: 22px;
	padding-top: 0;
	padding-bottom: 0;
}

.generator-container :deep(.n-input-wrapper) {
	padding: 1px 4px;
}

.generator-container :deep(.n-form-item-feedback-wrapper) {
	min-height: 0;
	display: none;
}

.generator-container :deep(.n-button--tiny-type) {
	height: 24px;
	padding: 0 6px;
	min-width: 28px;
}
</style>