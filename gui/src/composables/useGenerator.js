import { useAppStore, useGeneratorStore } from '@/stores';

/**
 * 通用生成器组合式函数
 * @param {string} type - 生成器类型: 'basic' | 'company' | 'account' | 'vehicle'
 */
export function useGenerator(type) {
	const appStore = useAppStore();
	const generatorStore = useGeneratorStore();

	// 根据类型获取对应的配置
	const getConfig = () => {
		switch (type) {
			case 'basic':
				return {
					state: generatorStore.basicInfo,
					fields: generatorStore.personalInfoFields,
					apiMap: generatorStore.basicApiMap,
					updateField: generatorStore.updateBasicField,
					reset: generatorStore.resetBasicInfo,
				};
			case 'company':
				return {
					state: generatorStore.companyInfo,
					fields: generatorStore.companyInfoFields,
					apiMap: generatorStore.companyApiMap,
					updateField: generatorStore.updateCompanyField,
					reset: generatorStore.resetCompanyInfo,
				};
			case 'account':
				return {
					state: generatorStore.accountInfo,
					fields: generatorStore.accountInfoFields,
					apiMap: generatorStore.accountApiMap,
					updateField: generatorStore.updateAccountField,
					reset: generatorStore.resetAccountInfo,
				};
			case 'vehicle':
				return {
					state: generatorStore.vehicleInfo,
					fields: generatorStore.vehicleInfoFields,
					apiMap: generatorStore.vehicleApiMap,
					updateField: generatorStore.updateVehicleField,
					reset: generatorStore.resetVehicleInfo,
				};
			default:
				return null;
		}
	};

	// 生成单个字段
	async function generateField(field, isInit = false) {
		appStore.setLoading(true);

		try {
			const config = getConfig();
			if (config && config.apiMap[field]) {
				const value = await config.apiMap[field]();
				config.updateField(field, value);
			}
		} catch (error) {
			console.error(`generateField ${field}:`, error);
		} finally {
			setTimeout(() => {
				appStore.setLoading(false);
			}, 100);
		}
	}

	// 生成所有字段
	async function generateAll(isInit = false) {
		const config = getConfig();
		if (!config) return;

		appStore.setLoading(true);

		try {
			// 并行生成所有字段
			const promises = Object.keys(config.fields).map(field => {
				if (config.apiMap[field]) {
					return config.apiMap[field]().then(value => {
						config.updateField(field, value);
					});
				}
				return Promise.resolve();
			});

			await Promise.all(promises);

			// 基础信息生成时随机生日
			if (type === 'basic') {
				generatorStore.randomizeBirthday();
			}
		} catch (error) {
			console.error('generateAll:', error);
		} finally {
			setTimeout(() => {
				appStore.setLoading(false);
			}, 500);
		}
	}

	// 统一生成方法
	function generate(field, isInit = false) {
		if (field === 'all') {
			return generateAll(isInit);
		}
		return generateField(field, isInit);
	}

	// 重置
	function reset() {
		const config = getConfig();
		if (config) {
			config.reset();
		}
	}

	return {
		generate,
		generateField,
		generateAll,
		reset,
	};
}

/**
 * 完整生成器组合式函数（包含所有类型）
 */
export function useFullGenerator() {
	const appStore = useAppStore();
	const generatorStore = useGeneratorStore();

	// 生成基础信息
	async function generateBasic(field, isInit = false) {
		appStore.setLoading(true);

		try {
			if (field === 'all') {
				const promises = Object.keys(generatorStore.personalInfoFields).map(f => {
					if (generatorStore.basicApiMap[f]) {
						return generatorStore.basicApiMap[f]().then(value => {
							generatorStore.updateBasicField(f, value);
						});
					}
					return Promise.resolve();
				});
				await Promise.all(promises);
				generatorStore.randomizeBirthday();
			} else if (generatorStore.basicApiMap[field]) {
				const value = await generatorStore.basicApiMap[field]();
				generatorStore.updateBasicField(field, value);
			}
		} catch (error) {
			console.error('generateBasic:', error);
		} finally {
			setTimeout(() => {
				appStore.setLoading(false);
			}, 100);
		}
	}

	// 生成企业信息
	async function generateCompany(field, isInit = false) {
		appStore.setLoading(true);

		try {
			if (field === 'all') {
				// 生成所有企业信息字段（包括 company）
				const allFields = ['company', ...Object.keys(generatorStore.companyInfoFields)];
				const promises = allFields.map(f => {
					if (generatorStore.companyApiMap[f]) {
						return generatorStore.companyApiMap[f]().then(value => {
							generatorStore.updateCompanyField(f, value);
						});
					}
					return Promise.resolve();
				});
				await Promise.all(promises);
			} else if (generatorStore.companyApiMap[field]) {
				const value = await generatorStore.companyApiMap[field]();
				generatorStore.updateCompanyField(field, value);
			}
		} catch (error) {
			console.error('generateCompany:', error);
		} finally {
			setTimeout(() => {
				appStore.setLoading(false);
			}, 100);
		}
	}

	// 生成账号信息
	async function generateAccount(field, isInit = false) {
		appStore.setLoading(true);

		try {
			if (field === 'all') {
				const promises = Object.keys(generatorStore.accountInfoFields).map(f => {
					if (generatorStore.accountApiMap[f]) {
						return generatorStore.accountApiMap[f]().then(value => {
							generatorStore.updateAccountField(f, value);
						});
					}
					return Promise.resolve();
				});
				await Promise.all(promises);
			} else if (generatorStore.accountApiMap[field]) {
				const value = await generatorStore.accountApiMap[field]();
				generatorStore.updateAccountField(field, value);
			}
		} catch (error) {
			console.error('generateAccount:', error);
		} finally {
			setTimeout(() => {
				appStore.setLoading(false);
			}, 100);
		}
	}

	// 生成车辆信息
	async function generateVehicle(field, isInit = false) {
		appStore.setLoading(true);

		try {
			if (field === 'all') {
				const promises = Object.keys(generatorStore.vehicleInfoFields).map(f => {
					if (generatorStore.vehicleApiMap[f]) {
						return generatorStore.vehicleApiMap[f]().then(value => {
							generatorStore.updateVehicleField(f, value);
						});
					}
					return Promise.resolve();
				});
				await Promise.all(promises);
			} else if (generatorStore.vehicleApiMap[field]) {
				const value = await generatorStore.vehicleApiMap[field]();
				generatorStore.updateVehicleField(field, value);
			}
		} catch (error) {
			console.error('generateVehicle:', error);
		} finally {
			setTimeout(() => {
				appStore.setLoading(false);
			}, 100);
		}
	}

	// 生成所有信息
	async function generateAll(isInit = false) {
		appStore.setLoading(true);

		try {
			// 并行生成所有类型
			await Promise.all([
				generateBasic('all', true),
				generateCompany('all', true),
				generateAccount('all', true),
				generateVehicle('all', true),
			]);
		} catch (error) {
			console.error('generateAll:', error);
		} finally {
			setTimeout(() => {
				appStore.setLoading(false);
			}, 500);
		}
	}

	return {
		generateBasic,
		generateCompany,
		generateAccount,
		generateVehicle,
		generateAll,
	};
}
