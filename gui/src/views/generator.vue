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
			<el-tabs type="border-card">
				<el-tab-pane label="基础信息">
					<BasicInfoGenerator
						:checkNbBalance="checkNbBalance"
						:windowConfig="windowConfig"
						:setFormLoading="setFormLoading"
						:consumeNb="consumeNb"
					/>
				</el-tab-pane>
				<el-tab-pane label="车辆信息">
					<VehicleInfoGenerator
						:checkNbBalance="checkNbBalance"
						:setFormLoading="setFormLoading"
						:consumeNb="consumeNb"
					/>
				</el-tab-pane>
			</el-tabs>
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
			<SettingsDrawer
				v-model:visible="windowConfig.winSetUp"
				:config="windowConfig"
				:resizeApp="resizeApp"
				:saveWinSizeItem="saveWinSizeItem"
				:changeDirectory="changeDirectory"
				:changePath="changePath"
				:checkPath="checkPath"
				:beforeClose="winSetUpBeforeClose"
			/>
		</el-form>
	</el-scrollbar>
</template>

<script setup>
	import { ref, onMounted } from 'vue';
	import { ElMessage } from 'element-plus';
	import { CopyDocument, User, Pointer, Postcard, Refresh, Close, Minus, FullScreen } from '@element-plus/icons-vue';
	import { copyToClipboard } from '@/utils';
	import moment from 'moment';
	import axios from 'axios';
	import { useDark, useToggle } from '@vueuse/core';
	import Sun from '@/assets/icons/sun.vue';
	import Moon from '@/assets/icons/moon.vue';
	import FestivalAnimation from '@/components/FestivalAnimation.vue';
	import SettingsDrawer from '@/components/SettingsDrawer.vue';
	import BasicInfoGenerator from '@/components/BasicInfoGenerator.vue';
	import VehicleInfoGenerator from '@/components/VehicleInfoGenerator.vue';

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
		screenHeight: (localStorage.getItem('screenHeight') || 700) * 1, //窗口高度
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
		//formData.value.gender = Math.random() > 0.5 ? 1 : 0;
		//getTangDaren();
		windowConfig.value.exitTipText = exitTip[Math.floor(Math.random() * exitTip.length)];
		residuePercent.value = (localStorage.getItem('nbBalance') || 100) * 1;
		setTimeout(() => {
			resizeApp();
			saveWinSizeItem(); // 初始化窗口大小
			changeDirectory(windowConfig.value.directoryType, true); //初始化生成路径
			//generator('all', true);
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

	function setFormLoading(val) {
		formLoading.value = val;
	}

	function consumeNb(val) {
		residuePercent.value = Math.max(residuePercent.value - val, 0);
		localStorage.setItem('nbBalance', residuePercent.value);
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
				windowConfig.value.screenHeight = 700;
				saveWinSizeItem();
				window.pywebview.api.resizeApp(1200, 700);
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
</style>
