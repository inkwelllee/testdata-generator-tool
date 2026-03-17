import { defineStore } from 'pinia';
import { ref } from 'vue';
import { generatorApi } from '@/api';

export const useGeneratorStore = defineStore('generator', () => {
	// 基础信息
	const basicInfo = ref({
		gender: Math.random() > 0.5 ? 1 : 0,
		birthday: '1992-07-25',
		name: '',
		idCard: '',
		phone: '',
		email: '',
	});

	// 企业信息
	const companyInfo = ref({
		company: '',
		socialCreditCode: '',
		organizationCode: '',
		zhongzhengCode: '',
	});

	// 账号信息
	const accountInfo = ref({
		BOC: '',
		CCB: '',
		ABC: '',
		ICBC: '',
		PSBC: '',
	});

	// 车辆信息
	const vehicleInfo = ref({
		licensePlate: '',
		vin: '',
		engineNo: '',
		address: '',
	});

	// 字段配置
	const personalInfoFields = {
		name: '姓名',
		idCard: '身份证号',
		phone: '手机号',
		email: '邮箱',
	};

	const companyInfoFields = {
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

	const vehicleInfoFields = {
		licensePlate: '车牌号',
		vin: '车架号',
		engineNo: '发动机号',
		address: '所在位置',
	};

	// API 映射
	const basicApiMap = {
		name: () => generatorApi.randomName(basicInfo.value.gender),
		idCard: () => generatorApi.randomIdCard(basicInfo.value.gender, basicInfo.value.birthday),
		phone: () => generatorApi.randomPhoneNumber(),
		email: () => generatorApi.randomEmail(),
	};

	const companyApiMap = {
		company: () => generatorApi.randomCompanyName(),
		socialCreditCode: () => generatorApi.randomSocialCreditCode(),
		organizationCode: () => generatorApi.randomOrganizationCode(),
		zhongzhengCode: () => generatorApi.randomZhongzhengCode(),
	};

	const accountApiMap = {
		BOC: () => generatorApi.randomBankAccount('BOC'),
		CCB: () => generatorApi.randomBankAccount('CCB'),
		ABC: () => generatorApi.randomBankAccount('ABC'),
		ICBC: () => generatorApi.randomBankAccount('ICBC'),
		PSBC: () => generatorApi.randomBankAccount('PSBC'),
	};

	const vehicleApiMap = {
		licensePlate: () => generatorApi.randomLicensePlate(),
		vin: () => generatorApi.randomVIN(),
		engineNo: () => generatorApi.randomEngineNo(),
		address: () => generatorApi.randomAddress(),
	};

	// 更新字段
	function updateBasicField(field, value) {
		if (field in basicInfo.value) {
			basicInfo.value[field] = value;
		}
	}

	function updateCompanyField(field, value) {
		if (field in companyInfo.value) {
			companyInfo.value[field] = value;
		}
	}

	function updateAccountField(field, value) {
		if (field in accountInfo.value) {
			accountInfo.value[field] = value;
		}
	}

	function updateVehicleField(field, value) {
		if (field in vehicleInfo.value) {
			vehicleInfo.value[field] = value;
		}
	}

	// 重置
	function resetBasicInfo() {
		basicInfo.value = {
			gender: Math.random() > 0.5 ? 1 : 0,
			birthday: '1992-07-25',
			name: '',
			idCard: '',
			phone: '',
			email: '',
		};
	}

	function resetCompanyInfo() {
		companyInfo.value = {
			company: '',
			socialCreditCode: '',
			organizationCode: '',
			zhongzhengCode: '',
		};
	}

	function resetAccountInfo() {
		accountInfo.value = {
			BOC: '',
			CCB: '',
			ABC: '',
			ICBC: '',
			PSBC: '',
		};
	}

	function resetVehicleInfo() {
		vehicleInfo.value = {
			licensePlate: '',
			vin: '',
			engineNo: '',
			address: '',
		};
	}

	// 随机生日
	function randomizeBirthday() {
		const year = Math.floor(Math.random() * (2000 - 1960 + 1)) + 1960;
		const dayOfYear = Math.floor(Math.random() * 365) + 1;
		const date = new Date(year, 0, dayOfYear);
		const month = String(date.getMonth() + 1).padStart(2, '0');
		const day = String(date.getDate()).padStart(2, '0');
		basicInfo.value.birthday = `${year}-${month}-${day}`;
	}

	return {
		// 状态
		basicInfo,
		companyInfo,
		accountInfo,
		vehicleInfo,

		// 字段配置
		personalInfoFields,
		companyInfoFields,
		accountInfoFields,
		vehicleInfoFields,

		// API 映射
		basicApiMap,
		companyApiMap,
		accountApiMap,
		vehicleApiMap,

		// 方法
		updateBasicField,
		updateCompanyField,
		updateAccountField,
		updateVehicleField,
		resetBasicInfo,
		resetCompanyInfo,
		resetAccountInfo,
		resetVehicleInfo,
		randomizeBirthday,
	};
});
