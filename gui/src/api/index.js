/**
 * API 封装层
 * 与后端 src/utils/api.py 对齐
 */

// 数据生成 API
export const generatorApi = {
	randomName: sex => window.pywebview.api.randomName(sex),
	randomIdCard: (sex, birthDate) => window.pywebview.api.randomIdCard(sex, birthDate),
	randomPhoneNumber: () => window.pywebview.api.randomPhoneNumber(),
	randomEmail: () => window.pywebview.api.randomEmail(),
	randomCompanyName: () => window.pywebview.api.randomCompanyName(),
	randomSocialCreditCode: () => window.pywebview.api.randomSocialCreditCode(),
	randomOrganizationCode: () => window.pywebview.api.randomOrganizationCode(),
	randomZhongzhengCode: () => window.pywebview.api.randomZhongzhengCode(),
	randomBankAccount: bankType => window.pywebview.api.randomBankAccount(bankType),
	randomLicensePlate: () => window.pywebview.api.randomLicensePlate(),
	randomVIN: () => window.pywebview.api.randomVIN(),
	randomEngineNo: () => window.pywebview.api.randomEngineNo(),
	randomAddress: () => window.pywebview.api.randomAddress(),
};

// 图片生成 API
export const imageApi = {
	generateIdCardImage: (name, sex, birthDate, idCard, directoryPath) => window.pywebview.api.generateIdCardImage(name, sex, birthDate, idCard, directoryPath),
	generateBusinessImage: (companyName, creditCode, name, directoryPath) => window.pywebview.api.generateBusinessImage(companyName, creditCode, name, directoryPath),
};

// 窗口控制 API
export const windowApi = {
	destroy: () => window.pywebview.api.destroyApp(),
	minimize: () => window.pywebview.api.minimizeApp(),
	maximize: () => window.pywebview.api.maximizeApp(),
	restore: () => window.pywebview.api.restoreApp(),
	resize: (width, height) => window.pywebview.api.resizeApp(width, height),
	toggleAlwaysOnTop: () => window.pywebview.api.toggleAlwaysOnTop(),
	getAlwaysOnTop: () => window.pywebview.api.getAlwaysOnTop(),
};

// 路径 API
export const pathApi = {
	changeDirectory: type => window.pywebview.api.changeDirectory(type),
	checkPath: path => window.pywebview.api.checkPath(path),
};

// 缓存 API
export const cacheApi = {
	clear: () => window.pywebview.api.clearCache(),
	clearSystem: () => window.pywebview.api.clearSystemCache(),
	getInfo: () => window.pywebview.api.getCacheInfo(),
};
