<template>
	<el-scrollbar>
		<el-header class="app-header">
			<el-row>
				<el-col :span="12">
					<img src="@/assets/icons/jiaoayi.ico" @click="windowConfig.winSetUp = true" style="width: 30px; height: 30px; -webkit-user-drag: none" />
					<span class="app-title">测试数据生成器</span>
				</el-col>
				<el-col :span="12">
					<!-- 余额进度条 -->
					<div style="text-align: right">
						<el-progress class="demo-progress" type="dashboard" :percentage="residuePercent" :color="customColors" :width="32" :stroke-width="4">
							<template #default="{ percentage }">
								<span class="percentage-value">{{ percentage }}%</span>
							</template>
						</el-progress>
						<!-- 切换主题 -->
						<el-switch
							style="margin-right: 12px; --el-switch-on-color: #2c2c2c; --el-switch-off-color: #f2f2f2"
							v-model="isDark"
							inline-prompt
							:active-action-icon="Moon"
							:inactive-action-icon="Sun"
							@change="toggleDark"
						>
						</el-switch>
						<!-- 窗口按钮 -->
						<el-button type="info" :icon="Minus" @click="minimizeApp" plain></el-button>
						<el-button type="warning" :icon="windowConfig.restoreWindow ? CopyDocument : FullScreen" @click="restoreApp" plain></el-button>
						<el-button type="danger" :icon="Close" @click="exitAppTip = true" plain></el-button>
					</div>
				</el-col>
			</el-row>
		</el-header>
		<el-form class="app-from" ref="formRef" v-loading="formLoading" :model="formData" label-width="120px" label-position="top">
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
									<el-col :span="20">
										<el-input v-model="formData[field]" disabled>
											<template #append>
												<el-button :icon="CopyDocument" @click="copy(field)"></el-button>
											</template>
										</el-input>
									</el-col>
									<el-col :span="4">
										<el-button :icon="Pointer" @click="generator(field)"></el-button>
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
									<el-col :span="20">
										<el-input v-model="formData[field]" disabled>
											<template #append>
												<el-button :icon="CopyDocument" @click="copy(field)"></el-button>
											</template>
										</el-input>
									</el-col>
									<el-col :span="4">
										<el-button :icon="Pointer" @click="generator(field)"></el-button>
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
									<el-col :span="20">
										<el-input v-model="formData[field]" disabled>
											<template #append>
												<el-button :icon="CopyDocument" @click="copy(field)"></el-button>
											</template>
										</el-input>
									</el-col>
									<el-col :span="4">
										<el-button :icon="Pointer" @click="generator(field)"></el-button>
									</el-col>
								</el-form-item>
							</el-col>
						</el-row>
					</el-card>
				</el-col>
			</el-row>
			<!-- 鸡汤 -->
			<!-- <el-row :gutter="15" style="padding-top: 10px">
				<el-col>
					<el-button plain type="primary" size="small" @click="getTangDaren">汤达人：{{ windowConfig.tangDaren }}</el-button>
				</el-col>
			</el-row> -->
			<!-- 按钮 -->
			<el-row :gutter="15" style="padding-top: 10px">
				<el-col :span="24">
					<el-form-item>
						<div class="mb-4">
							<el-button type="primary" :icon="Pointer" @click="generator('all')"> 生成 </el-button>
							<el-button type="info" :icon="Refresh" @click="resetForm">重置</el-button>
							<el-button plain type="primary" :icon="User" @click="generateIdCardImage">身份证</el-button>
							<el-button plain type="primary" :icon="Postcard" @click="generateBusinessImage">营业执照</el-button>
							<!-- <el-button plain type="primary" :icon="Postcard" @click="test">test</el-button> -->
						</div>
					</el-form-item>
				</el-col>
			</el-row>
			<!-- 投币 -->
			<el-dialog v-model="dialogVisible" title="这是另外的价钱" width="500" :close-on-click-modal="false" :show-close="false">
				<div class="block text-center" style="height: 280px">
					<span class="demonstration">牛币不足，请投币</span>
					<el-button class="butou-btn" type="danger" @click="windowConfig.zaishuoyibian = true" :disabled="dialogBtnDisabled" text> 我就不投 </el-button>

					<el-dialog v-model="windowConfig.zaishuoyibian" width="500" title="" append-to-body>
						<img src="@/assets/img/zaishuoyibian.jpg" alt="直视我" />
					</el-dialog>

					<el-carousel height="auto" :autoplay="false">
						<el-carousel-item style="height: 260px">
							<el-button class="countdown-btn" type="primary" @click="putCoins" :disabled="dialogBtnDisabled" text> 投币 </el-button>
							<video autoplay loop muted playsinline id="bgvid" style="width: 100%">
								<source src="@/assets/video/WeChat_20241219111716.mp4" type="video/webm" />
							</video>
						</el-carousel-item>
						<el-carousel-item style="height: 260px; background-color: #fff">
							<el-button class="countdown-btn" type="primary" @click="putCoins" :disabled="dialogBtnDisabled" text> 投币 </el-button>
							<div v-if="windowConfig.getQRStatus" id="imgid" style="text-align: center; background-color: #000"></div>
							<div v-if="!windowConfig.getQRStatus" style="text-align: center; background-color: #000"><img src="@/assets/img/inkwell_web.png" alt="二维码" /></div>
						</el-carousel-item>
					</el-carousel>
				</div>
			</el-dialog>
			<!-- 退出提示 -->
			<el-dialog v-model="exitAppTip" title="提示" :align-center="true" :width="500" draggable>
				<h2 style="text-align: center">{{ windowConfig.exitTipText }}</h2>
				<template #footer>
					<div class="dialog-footer">
						<el-button plain type="primary" @click="destroyApp"> 确定 </el-button>
					</div>
				</template>
			</el-dialog>

			<!-- 节日信息 -->
			<el-dialog v-model="windowConfig.festivalInfo" title="节日快乐" :align-center="true" :width="1150" :height="550" draggable>
				<FestivalAnimation v-if="windowConfig.festivalInfo" />
			</el-dialog>
			<!-- 设置按钮 -->
			<el-drawer v-model="windowConfig.winSetUp" :before-close="winSetUpBeforeClose" direction="ltr" size="400px">
				<template #header>
					<h4>设置</h4>
				</template>
				<template #default>
					<div>
						<h5>窗口设置</h5>
						<el-button plain type="primary" :icon="Menu" size="small" @click="resizeApp('resize')">还原默认大小</el-button>
					</div>
					<div class="slider-demo-block">
						<span class="demonstration">窗口宽度</span>
						<el-slider v-model="windowConfig.screenWidth" @input="resizeApp" @change="saveWinSizeItem" :min="700" :max="windowConfig.maxScreenWidth" :step="1" show-input size="small" />
					</div>
					<div class="slider-demo-block">
						<span class="demonstration">窗口高度</span>
						<el-slider v-model="windowConfig.screenHeight" @input="resizeApp" @change="saveWinSizeItem" :min="300" :max="windowConfig.maxscreenHeight" :step="1" show-input size="small" />
					</div>
					<div>
						<h5>生成目录</h5>
						<el-radio-group v-model="windowConfig.directoryType" @change="changeDirectory" size="small">
							<el-radio-button label="桌面" value="desktop" />
							<el-radio-button label="跟随应用" value="follow" />
							<el-radio-button label="自定义" value="diy" />
						</el-radio-group>
						<div>
							<el-input
								v-model="windowConfig.directoryPath"
								placeholder="例：D:\下载 ，输入完请点击后方按钮检测是否可用"
								:disabled="windowConfig.directoryType !== 'diy'"
								@change="changePath"
								size="small"
							>
								<!-- <template #prepend>目录</template> -->
								<template #append>
									<el-button :disabled="windowConfig.directoryType !== 'diy'" @click="checkPath()">
										<el-icon v-if="windowConfig.enablePath || windowConfig.directoryType !== 'diy'" color="#69ffb4"><Select /></el-icon>
										<el-icon v-else color="#d8e510"><RefreshRight /></el-icon>
									</el-button>
								</template>
							</el-input>
						</div>
					</div>
				</template>
				<template #footer>
					<div style="flex: auto">
						<h6>版本：0.5.11.5</h6>
					</div>
				</template>
			</el-drawer>
		</el-form>
	</el-scrollbar>
</template>

<script setup>
	import { ref, onMounted } from 'vue';
	import { ElMessage } from 'element-plus';
	import { CopyDocument, User, Pointer, Postcard, Refresh, Close, Minus, Select, RefreshRight, FullScreen, Menu } from '@element-plus/icons-vue';
	import { copyToClipboard } from '@/utils';
	import moment from 'moment';
	import axios from 'axios';
	import { useDark, useToggle } from '@vueuse/core';
	import Sun from '@/assets/icons/sun.vue';
	import Moon from '@/assets/icons/moon.vue';
	import FestivalAnimation from '@/components/FestivalAnimation.vue';

	// 深色模式
	const isDark = useDark();
	const toggleDark = useToggle(isDark);

	const formLoading = ref(false);
	const dialogVisible = ref();
	const exitAppTip = ref(false);
	const dialogBtnDisabled = ref(true);
	const residuePercent = ref(100);
	const windowConfig = ref({
		//窗口配置
		winSetUp: false, //窗口设置是否展示
		restoreWindow: false, //窗口放大或恢复
		screenWidth: (localStorage.getItem('screenWidth') || 1200) * 1, //窗口宽度
		screenHeight: (localStorage.getItem('screenHeight') || 660) * 1, //窗口高度
		maxScreenWidth: window.screen.width * window.devicePixelRatio || 1920, //最大窗口宽度(屏幕宽度 * 缩放比例)
		maxscreenHeight: window.screen.height * window.devicePixelRatio || 1080, //最大窗口高度
		exitTipText: '暂别勿思念，转瞬与亲见', //退出提示语
		tangDaren: '', //汤达人
		getQRStatus: false, //二维码获取成功状态
		zaishuoyibian: false, //不投币展示框
		festivalInfo: false, //节日信息
		directoryType: localStorage.getItem('directoryType') || 'desktop', //目录设置 desktop,桌面,follow,跟随应用,diy,自定义
		enablePath: localStorage.getItem('enablePath') || false, //diy目录是否生效
		directoryPath: localStorage.getItem('directoryPath') || '', //生成目录路径
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

	const customColors = ref([
		{ color: '#f56c6c', percentage: 20 },
		{ color: '#e6a23c', percentage: 40 },
		{ color: '#5cb87a', percentage: 60 },
		{ color: '#1989fa', percentage: 80 },
		{ color: '#6f7ad3', percentage: 100 },
	]);

	const exitTip = [
		'暂别勿思念，转瞬与亲见',
		'暂别莫惆怅，不久再相逢',
		'离别有时，重逢有期',
		'暂别且安心，相逢终有时',
		'暂时的离别，是为了更好的相遇',
		'离别只是短暂，期待再次相遇',
		'离别之刻，重逢在望',
		'此刻虽离别，相逢在眼前',
		'这就走了？',
		'好吧，再见',
		'好吧，记得想我',
	];

	onMounted(() => {
		formData.value.gender = Math.random() > 0.5 ? 1 : 0;
		//getTangDaren();
		windowConfig.value.exitTipText = exitTip[Math.floor(Math.random() * exitTip.length)];
		residuePercent.value = (localStorage.getItem('nbBalance') || 100) * 1;
		setTimeout(() => {
			resizeApp();
			saveWinSizeItem(); // 初始化窗口大小
			changeDirectory(windowConfig.value.directoryType, true); //初始化生成路径
			generator('all', true);
		}, 100);

		showFestivalInfo();
	});

	function showFestivalInfo() {
		const today = new Date();
		const month = today.getMonth() + 1; // 注意月份是从 0 开始的，要加 1
		const day = today.getDate();
		console.log('加载节日', today, month, day);

		// 检查是否为特定节日日期
		if (month === 1 && day >= 1 && day <= 7) {
			console.log('######## 欢度元旦 ########');
			windowConfig.value.festivalInfo = true;

			// 91.5秒后自动关闭
			setTimeout(() => {
				windowConfig.value.festivalInfo = false;
			}, 91500);
		}
	}

	function generator(type, isInit = false) {
		if (checkNbBalance(isInit)) {
			return;
		}

		formLoading.value = true;

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
			formLoading.value = false;
			if (!isInit && type === 'all') {
				residuePercent.value = Math.max(residuePercent.value - 1, 0);
				//residuePercent.value = Math.max(residuePercent.value - residuePercent.value, 0);	// 测试用一次扣完
				localStorage.setItem('nbBalance', residuePercent.value);
				//getTangDaren();
			}
		}, 500);
	}

	function copy(field) {
		const text = formData.value[field];
		copyToClipboard(text);
	}

	// 检查余额
	function checkNbBalance(isInit = false, consume = 0) {
		if (!isInit && residuePercent.value <= consume) {
			dialogBtnDisabled.value = true;
			dialogVisible.value = true;
			getQRCode();
			setTimeout(() => {
				dialogBtnDisabled.value = false;
			}, 3000); //3秒广告倒计时

			return true;
		}

		return false;
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
		if (checkNbBalance(false, 1)) {
			return;
		}

		formLoading.value = true;
		setTimeout(() => {
			try {
				window.pywebview.api
					.generateIdCardImage(formData.value.name, formData.value.gender, formData.value.birthday, formData.value.idCard, windowConfig.value.directoryPath)
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

				residuePercent.value = residuePercent.value - 2;
				localStorage.setItem('nbBalance', residuePercent.value);
			} catch (error) {
				console.error('generateIdCardImage');
			}

			formLoading.value = false;
		}, 1000);
	}

	function generateBusinessImage() {
		if (checkNbBalance(false, 1)) {
			return;
		}

		formLoading.value = true;
		setTimeout(() => {
			try {
				window.pywebview.api
					.generateBusinessImage(formData.value.company, formData.value.socialCreditCode, formData.value.name, windowConfig.value.directoryPath)
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
				residuePercent.value = residuePercent.value - 2;
				localStorage.setItem('nbBalance', residuePercent.value);
			} catch (error) {
				console.error('generateBusinessImage');
			}

			formLoading.value = false;
		}, 1000);
	}

	function putCoins() {
		let nb = Math.floor(Math.random() * 100);
		if (residuePercent.value + nb >= 100) {
			nb = 100 - residuePercent.value;
			ElMessage({
				message: '哇~，牛币爆表了！！！！',
				type: 'success',
			});
		} else {
			ElMessage({
				message: '恭喜你，获得' + nb + '个牛币',
				type: 'success',
			});
		}

		residuePercent.value = residuePercent.value + nb;
		localStorage.setItem('nbBalance', residuePercent.value);
		dialogVisible.value = false;
	}

	function getTangDaren() {
		try {
			axios
				.get('https://api.oick.cn/dutang/api.php')
				.then(Response => {
					windowConfig.value.tangDaren = Response.data;
				})
				.catch(error => {
					windowConfig.value.tangDaren = '接口好像罢工了，请稍后再试';
					console.error('There was an error!', error);
				});
		} catch (error) {
			console.error('getTangDaren');
		}
	}

	function getQRCode() {
		try {
			const getImageUrl = 'https://oneapi.coderbox.cn/openapi/public/qrcode/simple?lightColor=Black&darkColor=rgb(180,180,180)&text=' + encodeURIComponent('https://inkwell.top/');
			axios({ url: getImageUrl, method: 'get', responseType: 'blob' })
				.then(Response => {
					// 将blob数据转换为可以在浏览器中显示的URL
					const imageUrl = URL.createObjectURL(new Blob([Response.data]));
					// 创建一个img标签并设置其src属性为转换后的URL
					const img = document.createElement('img');
					img.src = imageUrl;
					img.height = 260;
					img.width = 260;

					// 清空容器后再添加新图片，避免重复
					const container = document.getElementById('imgid');
					container.innerHTML = '';
					container.appendChild(img);
					windowConfig.value.getQRStatus = true;
				})
				.catch(error => {
					windowConfig.value.getQRStatus = false;
					console.error('There was an error!', error);
				});
		} catch (error) {
			windowConfig.value.getQRStatus = false;
			console.error('getQRCode');
		}
	}

	// 切换目录
	function changeDirectory(data, isInit = false) {
		try {
			localStorage.setItem('directoryType', data);
			if ('diy' === data) {
				windowConfig.value.directoryPath = localStorage.getItem('directoryPath') || '';
				if (windowConfig.value.directoryPath !== '') {
					checkPath(isInit);
				}
				return;
			}
			window.pywebview.api.changeDirectory(data).then(directoryPath => {
				windowConfig.value.enablePath = false;
				windowConfig.value.directoryPath = directoryPath;
			});
		} catch (error) {
			console.error('changeDirectory');
		}
	}

	function changePath() {
		windowConfig.value.enablePath = false;
	}

	function checkPath(isInit = false) {
		let directoryPath = windowConfig.value.directoryPath;
		if (!directoryPath) {
			ElMessage({
				message: '请先输入目录',
				type: 'warning',
			});
			return;
		}
		window.pywebview.api.checkPath(directoryPath).then(checkPath => {
			if (checkPath) {
				windowConfig.value.enablePath = true;
				localStorage.setItem('enablePath', true);
				localStorage.setItem('directoryPath', directoryPath);
				if (!isInit) {
					ElMessage({
						message: '修改目录成功',
						type: 'success',
					});
				}
			} else {
				windowConfig.value.enablePath = false;
				ElMessage({
					message: '目录不存在，应用目录失败',
					type: 'error',
				});
			}
		});
	}

	function winSetUpBeforeClose(done) {
		if (windowConfig.value.directoryType === 'diy' && !windowConfig.value.enablePath) {
			ElMessage({
				message: '请先检测自定义目录是否可用',
				type: 'warning',
			});
			return;
		}
		done();
	}

	//关闭窗口
	function destroyApp() {
		try {
			window.pywebview.api.destroyApp();
		} catch (error) {
			console.error('destroyApp');
		}
	}

	//最小化窗口
	function minimizeApp() {
		try {
			window.pywebview.api.minimizeApp();
		} catch (error) {
			console.error('minimizeApp');
		}
	}
	//最大化/还原窗口
	function restoreApp() {
		windowConfig.value.restoreWindow = !windowConfig.value.restoreWindow;
		try {
			if (windowConfig.value.restoreWindow) {
				window.pywebview.api.maximizeApp(); //最大化
			} else {
				window.pywebview.api.restoreApp(); //还原
			}
		} catch (error) {
			console.error('restoreApp');
		}
	}

	// 设置窗口大小
	function resizeApp(resizeApp) {
		try {
			if ('resize' == resizeApp) {
				windowConfig.value.screenWidth = 1200;
				windowConfig.value.screenHeight = 660;
				saveWinSizeItem();
				window.pywebview.api.resizeApp(1200, 660);
			} else {
				window.pywebview.api.resizeApp(windowConfig.value.screenWidth, windowConfig.value.screenHeight);
			}
		} catch (error) {
			console.error('resizeApp');
		}
	}

	function saveWinSizeItem() {
		try {
			//保存窗口大小
			localStorage.setItem('screenWidth', windowConfig.value.screenWidth);
			localStorage.setItem('screenHeight', windowConfig.value.screenHeight);
		} catch (error) {
			console.error('saveWinSizeItem');
		}
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

	.carousel-item {
		color: #475669;
		opacity: 0.75;
		margin: 0;
		text-align: center;
	}

	.el-carousel__item h3 {
		color: #475669;
		opacity: 0.75;
		display: flex;
		align-items: center;
		margin: 0;
		text-align: center;
		height: 100%;
	}

	.el-carousel__item:nth-child(2n) {
		background-color: #99a9bf;
	}

	.el-carousel__item:nth-child(2n + 1) {
		background-color: #d3dce6;
	}

	.countdown-btn {
		position: absolute;
		top: 10%;
		left: 90%;
		transform: translate(-50%, -50%);
		background-color: #4caf50;
		color: white;
		padding: 10px 20px;
		border: none;
		cursor: pointer;
		z-index: 1;
	}

	.butou-btn {
		position: absolute;
		top: 10%;
		left: 90%;
		transform: translate(-50%, -50%);
		/*color: white;
		 padding: 10px 20px;*/
		border: none;
		cursor: pointer;
		z-index: 1;
	}

	.demo-progress {
		position: absolute;
		top: 0px;
		right: 226px;
	}

	.percentage-value {
		display: block;
		margin-right: 18px;
		font-size: 9px;
	}

	.app-title {
		position: absolute;
		font-size: 16px;
		font-weight: 'bold';
		top: 5px;
		left: 40px;
	}

	/* 不加padding会有滚动条 */
	.app-header {
		padding: 0 10px;
		font-size: 12px;
		height: 40px;
	}

	.app-from {
		overflow: hidden;
		/* padding: 0 15px; */
	}

	.slider-demo-block {
		max-width: 600px;
		display: flex;
		align-items: center;
	}
	.slider-demo-block .el-slider {
		margin-top: 0;
		margin-left: 12px;
	}
	.slider-demo-block .demonstration {
		font-size: 14px;
		color: var(--el-text-color-secondary);
		line-height: 44px;
		flex: 1;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		margin-bottom: 0;
	}
	.slider-demo-block .demonstration + .el-slider {
		flex: 0 0 80%;
	}
</style>
