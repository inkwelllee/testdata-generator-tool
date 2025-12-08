<template>
	<el-row :gutter="15">
		<el-col :span="8">
			<el-card style="height: 500px">
				<template #header>
					<div class="card-header">
						<span>身份信息</span>
					</div>
				</template>
				<el-row :gutter="10">
					<el-col :span="12">
						<el-form-item label="性别">
							<el-radio-group v-model="formData.gender">
								<el-radio :value="1">男</el-radio>
								<el-radio :value="0">女</el-radio>
							</el-radio-group>
						</el-form-item>
					</el-col>
					<el-col :span="12">
						<el-form-item label="出生日期">
							<el-date-picker v-model="formData.birthday" type="date" format="YYYY-MM-DD" value-format="YYYY-MM-DD"></el-date-picker>
						</el-form-item>
					</el-col>
				</el-row>
				<el-row :gutter="10" v-for="(label, field) in personalInfoFields" :key="field">
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
		<el-col :span="8">
			<el-card style="height: 500px">
				<template #header>
					<div class="card-header">
						<span>企业信息</span>
					</div>
				</template>
				<el-row :gutter="10" v-for="(label, field) in companyInfoFields" :key="field">
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
		<el-col :span="8">
			<el-card style="height: 500px">
				<template #header>
					<div class="card-header">
						<span>账号信息</span>
					</div>
				</template>
				<el-row :gutter="10" v-for="(label, field) in accountInfoFields" :key="field">
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
					<el-button plain type="primary" :icon="User" @click="generateIdCardImage">身份证</el-button>
					<el-button plain type="primary" :icon="Postcard" @click="generateBusinessImage">营业执照</el-button>
				</div>
			</el-form-item>
		</el-col>
	</el-row>
</template>

<script setup>
	import { ref, onMounted } from 'vue';
	import { ElMessage } from 'element-plus';
	import { CopyDocument, User, Pointer, Postcard, Refresh } from '@element-plus/icons-vue';
	import { copyToClipboard } from '@/utils';
	import moment from 'moment';

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

	const personalInfoFields = {
		name: '姓名',
		idCard: '身份证号',
		phone: '手机号',
		email: '邮箱',
	};

	const companyInfoFields = {
		company: '公司名称',
		name: '法定代表人',
		socialCreditCode: '统一社会信用代码',
		organizationCode: '组织机构代码',
		zhongzhengCode: '中征码',
	};

	const accountInfoFields = {
		BOC: '中国银行账号',
		CCB: '建设银行账号',
		ABC: '农业银行账号',
		ICBC: '工商银行账号',
		PSBC: '邮储银行账号',
	};

	onMounted(() => {
		formData.value.gender = Math.random() > 0.5 ? 1 : 0;
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
			if (type === 'name') {
				window.pywebview.api.randomName(formData.value.gender).then(name => {
					formData.value.name = name;
				});
			} else if (type === 'idCard') {
				window.pywebview.api.randomIdCard(formData.value.gender, formData.value.birthday).then(idCard => {
					formData.value.idCard = idCard;
				});
			} else if (type === 'phone') {
				window.pywebview.api.randomPhoneNumber().then(phone => {
					formData.value.phone = phone;
				});
			} else if (type === 'email') {
				window.pywebview.api.randomEmail().then(email => {
					formData.value.email = email;
				});
			} else if (type === 'company') {
				window.pywebview.api.randomCompanyName().then(company => {
					formData.value.company = company;
				});
			} else if (type === 'socialCreditCode') {
				window.pywebview.api.randomSocialCreditCode().then(socialCreditCode => {
					formData.value.socialCreditCode = socialCreditCode;
				});
			} else if (type === 'organizationCode') {
				window.pywebview.api.randomOrganizationCode().then(organizationCode => {
					formData.value.organizationCode = organizationCode;
				});
			} else if (type === 'zhongzhengCode') {
				window.pywebview.api.randomZhongzhengCode().then(zhongzhengCode => {
					formData.value.zhongzhengCode = zhongzhengCode;
				});
			} else if (type === 'BOC') {
				window.pywebview.api.randomBankAccount(type).then(bankAccount => {
					formData.value.BOC = bankAccount;
				});
			} else if (type === 'CCB') {
				window.pywebview.api.randomBankAccount(type).then(bankAccount => {
					formData.value.CCB = bankAccount;
				});
			} else if (type === 'ABC') {
				window.pywebview.api.randomBankAccount(type).then(bankAccount => {
					formData.value.ABC = bankAccount;
				});
			} else if (type === 'ICBC') {
				window.pywebview.api.randomBankAccount(type).then(bankAccount => {
					formData.value.ICBC = bankAccount;
				});
			} else if (type === 'PSBC') {
				window.pywebview.api.randomBankAccount(type).then(bankAccount => {
					formData.value.PSBC = bankAccount;
				});
			} else if (type === 'all') {
				Object.keys(personalInfoFields).forEach(field => {
					generator(field);
				});
				Object.keys(companyInfoFields).forEach(field => {
					generator(field);
				});
				Object.keys(accountInfoFields).forEach(field => {
					generator(field);
				});

				//随机生日
				formData.value.birthday = moment()
					.year(Math.floor(Math.random() * (2000 - 1960 + 1)) + 1960)
					.dayOfYear(Math.floor(Math.random() * 365) + 1)
					.format('YYYY-MM-DD');
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
			gender: Math.random() > 0.5 ? 1 : 0,
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
		};
	}

	function generateIdCardImage() {
		if (props.checkNbBalance(false, 1)) {
			return;
		}

		props.setFormLoading(true);
		setTimeout(() => {
			try {
				window.pywebview.api
					.generateIdCardImage(formData.value.name, formData.value.gender, formData.value.birthday, formData.value.idCard, props.windowConfig.directoryPath)
					.then(idCardImage => {
						ElMessage({
							message: idCardImage,
							type: 'success',
						});
					})
					.catch(error => {
						ElMessage({
							message: error,
							type: 'error',
						});
					});

				props.consumeNb(2);
			} catch (error) {
				console.error('generateIdCardImage');
			}

			props.setFormLoading(false);
		}, 1000);
	}

	function generateBusinessImage() {
		if (props.checkNbBalance(false, 1)) {
			return;
		}

		props.setFormLoading(true);
		setTimeout(() => {
			try {
				window.pywebview.api
					.generateBusinessImage(formData.value.company, formData.value.socialCreditCode, formData.value.name, props.windowConfig.directoryPath)
					.then(businessImage => {
						ElMessage({
							message: businessImage,
							type: 'success',
						});
					})
					.catch(error => {
						ElMessage({
							message: error,
							type: 'error',
						});
					});
				props.consumeNb(2);
			} catch (error) {
				console.error('generateBusinessImage');
			}

			props.setFormLoading(false);
		}, 1000);
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
