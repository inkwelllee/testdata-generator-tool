<template>
	<div class="festival-container">
		<canvas ref="canvasRef" class="canvas"></canvas>
		<div class="overlay">
			<div class="tabs">
				<div class="tabs-labels">
					<span class="tabs-label">Commands</span>
					<span class="tabs-label">Info</span>
					<span class="tabs-label">Share</span>
				</div>
				<div class="tabs-panels">
					<ul class="tabs-panel commands">
						<li class="commands-item">
							<div class="commands-item-content">
								<span class="commands-item-title">Text</span>
								<span class="commands-item-info" data-demo="Hello :)">Type anything</span>
							</div>
							<span class="commands-item-action">Demo</span>
						</li>
						<li class="commands-item">
							<div class="commands-item-content">
								<span class="commands-item-title">Countdown</span>
								<span class="commands-item-info" data-demo="#countdown 10">#countdown<span class="commands-item-mode">number</span></span>
							</div>
							<span class="commands-item-action">Demo</span>
						</li>
						<li class="commands-item">
							<div class="commands-item-content">
								<span class="commands-item-title">Icon</span>
								<span class="commands-item-info" data-demo="#icon thumbs-up">#icon<span class="commands-item-mode">name</span>&nbsp;(using <a href="//fortawesome.github.io/Font-Awesome/#icons-new" target="_blank">Font Awesome</a>)</span>
							</div>
							<span class="commands-item-action">Demo</span>
						</li>
						<li class="commands-item">
							<div class="commands-item-content">
								<span class="commands-item-title">Time</span>
								<span class="commands-item-info" data-demo="#time">#time</span>
							</div>
							<span class="commands-item-action">Demo</span>
						</li>
						<li class="commands-item">
							<div class="commands-item-content">
								<span class="commands-item-title">Rectangle</span>
								<span class="commands-item-info" data-demo="#rectangle 30x15">#rectangle<span class="commands-item-mode">width x height</span></span>
							</div>
							<span class="commands-item-action">Demo</span>
						</li>
						<li class="commands-item">
							<div class="commands-item-content">
								<span class="commands-item-title">Circle</span>
								<span class="commands-item-info" data-demo="#circle 25">#circle<span class="commands-item-mode">diameter</span></span>
							</div>
							<span class="commands-item-action">Demo</span>
						</li>
						<li class="commands-item commands-item--gap">
							<div class="commands-item-content">
								<span class="commands-item-title">Animate</span>
								<span class="commands-item-info" data-demo="The time is|#time|#countdown 3|#icon thumbs-up">
									<span class="commands-item-mode">command1</span>&nbsp;|<span class="commands-item-mode">command2</span>
								</span>
							</div>
							<span class="commands-item-action">Demo</span>
						</li>
					</ul>
					<div class="tabs-panel ui-details">
						<div class="ui-details-content"></div>
					</div>
				</div>
			</div>
		</div>
		<audio ref="audioRef" autoplay loop>
			<source src="http://music.163.com/song/media/outer/url?id=1976115393.mp3" type="audio/mpeg">
		</audio>
	</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const canvasRef = ref(null);
const audioRef = ref(null);

let S = {};

onMounted(() => {
	initFestivalAnimation();
});

onUnmounted(() => {
	// 清理资源
	if (S.interval) {
		clearInterval(S.interval);
	}
});

function initFestivalAnimation() {
	// 创建一个Date对象，表示当前日期和时间
	const currentDate = new Date();
	// 获取当前年份
	const currentYear = currentDate.getFullYear();

	const str_text = 
		'HAPPY NEW YEAR|新年倒计时|5|4|3|2|1|' +
		currentYear +
		'|新的征程|新的希望|凡是过往|皆是序章|福启新岁|万事顺遂|梦想成真|' +
		currentYear +
		'|所遇皆所求|所行皆坦途|新年快乐|一切皆好|MIIYSOSU|INKWELL';

	S = {
		init: function () {
			S.Drawing.init(canvasRef.value);
			S.ShapeBuilder.init();
			S.UI.init();
			
			S.UI.simulate(str_text);

			S.Drawing.loop(function () {
				S.Shape.render();
			});
		},
	};

	S.Drawing = (function () {
		let canvas, context, renderFn;
		const requestFrame =
			window.requestAnimationFrame ||
			window.webkitRequestAnimationFrame ||
			window.mozRequestAnimationFrame ||
			window.oRequestAnimationFrame ||
			window.msRequestAnimationFrame ||
			function (callback) {
				window.setTimeout(callback, 1000 / 60);
			};

		return {
			init: function (el) {
				canvas = el;
				context = canvas.getContext('2d');
				this.adjustCanvas();

				window.addEventListener('resize', this.adjustCanvas);
			},

			loop: function (fn) {
				renderFn = !renderFn ? fn : renderFn;
				this.clearFrame();
				renderFn();
				requestFrame.call(window, this.loop.bind(this));
			},

			adjustCanvas: function () {
				canvas.width = 1100;
				canvas.height = 550;
			},

			clearFrame: function () {
				context.clearRect(0, 0, canvas.width, canvas.height);
			},

			getArea: function () {
				return { w: canvas.width, h: canvas.height };
			},

			drawCircle: function (p, c) {
				context.fillStyle = c.render();
				context.beginPath();
				context.arc(p.x, p.y, p.z, 0, 2 * Math.PI, true);
				context.closePath();
				context.fill();
			},
		};
	})();

	S.Point = function (args) {
		this.x = args.x;
		this.y = args.y;
		this.z = args.z;
		this.a = args.a;
		this.h = args.h;
	};

	S.Color = function (r, g, b, a) {
		this.r = r;
		this.g = g;
		this.b = b;
		this.a = a;
	};

	S.Color.prototype = {
		render: function () {
			return 'rgba(' + this.r + ',' + this.g + ',' + this.b + ',' + this.a + ')';
		},
	};

	S.UI = (function () {
		let interval, currentAction, sequence = [];
		const cmd = '#';

		function formatTime(date) {
			const h = date.getHours();
			let m = date.getMinutes();
			m = m < 10 ? '0' + m : m;
			return h + ':' + m;
		}

		function getValue(value) {
			return value && value.split(' ')[1];
		}

		function getAction(value) {
			value = value && value.split(' ')[0];
			return value && value[0] === cmd && value.substring(1);
		}

		function timedAction(fn, delay, max, reverse) {
			clearInterval(interval);
			currentAction = reverse ? max : 1;
			fn(currentAction);

			if (!max || (!reverse && currentAction < max) || (reverse && currentAction > 0)) {
				interval = setInterval(function () {
					currentAction = reverse ? currentAction - 1 : currentAction + 1;
					fn(currentAction);

					if ((!reverse && max && currentAction === max) || (reverse && currentAction === 0)) {
						clearInterval(interval);
					}
				}, delay);
			}
		}

		function performAction(value) {
			let action, current;
			sequence = typeof value === 'object' ? value : sequence.concat(value.split('|'));

			timedAction(
				function () {
					current = sequence.shift();
					action = getAction(current);
					value = getValue(current);

					switch (action) {
						case 'countdown':
							value = parseInt(value, 10) || 10;
							value = value > 0 ? value : 10;

							timedAction(
								function (index) {
									if (index === 0) {
										if (sequence.length === 0) {
											S.Shape.switchShape(S.ShapeBuilder.letter(''));
										} else {
											performAction(sequence);
										}
									} else {
										S.Shape.switchShape(S.ShapeBuilder.letter(index), true);
									}
								},
								1000,
								value,
								true
							);
							break;

						case 'rectangle':
							value = value && value.split('x');
							value = value && value.length === 2 ? value : [30, 15];
							S.Shape.switchShape(S.ShapeBuilder.rectangle(Math.min(30, parseInt(value[0], 10)), Math.min(30, parseInt(value[1], 10))));
							break;

						case 'circle':
							value = parseInt(value, 10) || 30;
							value = Math.min(value, 30);
							S.Shape.switchShape(S.ShapeBuilder.circle(value));
							break;

						case 'time':
							let t = formatTime(new Date());
							if (sequence.length > 0) {
								S.Shape.switchShape(S.ShapeBuilder.letter(t));
							} else {
								timedAction(function () {
									t = formatTime(new Date());
									S.Shape.switchShape(S.ShapeBuilder.letter(t));
								}, 1000);
							}
							break;

						default:
							S.Shape.switchShape(S.ShapeBuilder.letter(current[0] === cmd ? 'What?' : current));
					}
				},
				2500,
				sequence.length
			);
		}

		return {
			init: function () {
				// 初始化UI
			},
			simulate: function (action) {
				performAction(action);
			},
		};
	})();

	S.Dot = function (x, y) {
		this.p = new S.Point({
			x: x,
			y: y,
			z: 5,
			a: 1,
			h: 0,
		});

		this.e = 0.07;
		this.s = true;
		this.c = new S.Color(255, 255, 255, this.p.a);
		this.t = this.clone();
		this.q = [];
	};

	S.Dot.prototype = {
		clone: function () {
			return new S.Point({
				x: this.p.x,
				y: this.p.y,
				z: this.p.z,
				a: this.p.a,
				h: this.p.h,
			});
		},

		_draw: function () {
			this.c.a = this.p.a;
			S.Drawing.drawCircle(this.p, this.c);
		},

		_moveTowards: function (n) {
			const details = this.distanceTo(n, true);
			const dx = details[0];
			const dy = details[1];
			const d = details[2];
			const e = this.e * d;

			if (this.p.h === -1) {
				this.p.x = n.x;
				this.p.y = n.y;
				return true;
			}

			if (d > 1) {
				this.p.x -= (dx / d) * e;
				this.p.y -= (dy / d) * e;
			} else {
				if (this.p.h > 0) {
					this.p.h--;
				} else {
					return true;
				}
			}

			return false;
		},

		_update: function () {
			let p, d;

			if (this._moveTowards(this.t)) {
				p = this.q.shift();

				if (p) {
					this.t.x = p.x || this.p.x;
					this.t.y = p.y || this.p.y;
					this.t.z = p.z || this.p.z;
					this.t.a = p.a || this.p.a;
					this.p.h = p.h || 0;
				} else {
					if (this.s) {
						this.p.x -= Math.sin(Math.random() * 3.142);
						this.p.y -= Math.sin(Math.random() * 3.142);
					} else {
						this.move(
							new S.Point({
								x: this.p.x + Math.random() * 50 - 25,
								y: this.p.y + Math.random() * 50 - 25,
							})
						);
					}
				}
			}

			d = this.p.a - this.t.a;
			this.p.a = Math.max(0.1, this.p.a - d * 0.05);
			d = this.p.z - this.t.z;
			this.p.z = Math.max(1, this.p.z - d * 0.05);
		},

		distanceTo: function (n, details) {
			const dx = this.p.x - n.x;
			const dy = this.p.y - n.y;
			const d = Math.sqrt(dx * dx + dy * dy);
			return details ? [dx, dy, d] : d;
		},

		move: function (p, avoidStatic) {
			if (!avoidStatic || (avoidStatic && this.distanceTo(p) > 1)) {
				this.q.push(p);
			}
		},

		render: function () {
			this._update();
			this._draw();
		},
	};

	S.ShapeBuilder = (function () {
		const gap = 13;
		const shapeCanvas = document.createElement('canvas');
		const shapeContext = shapeCanvas.getContext('2d');
		const fontSize = 500;
		const fontFamily = 'Avenir, Helvetica Neue, Helvetica, Arial, sans-serif';

		function fit() {
			shapeCanvas.width = 1000;
			shapeCanvas.height = 550;
			shapeContext.fillStyle = 'red';
			shapeContext.textBaseline = 'middle';
			shapeContext.textAlign = 'center';
		}

		function processCanvas() {
			const pixels = shapeContext.getImageData(0, 0, shapeCanvas.width, shapeCanvas.height).data;
			const dots = [];
			let x = 0, y = 0, fx = shapeCanvas.width, fy = shapeCanvas.height, w = 0, h = 0;

			for (let p = 0; p < pixels.length; p += 4 * gap) {
				if (pixels[p + 3] > 0) {
					dots.push(new S.Point({ x: x, y: y }));
					w = x > w ? x : w;
					h = y > h ? y : h;
					fx = x < fx ? x : fx;
					fy = y < fy ? y : fy;
				}

				x += gap;
				if (x >= shapeCanvas.width) {
					x = 0;
					y += gap;
					p += gap * 4 * shapeCanvas.width;
				}
			}

			return { dots: dots, w: w + fx, h: h + fy };
		}

		function setFontSize(s) {
			shapeContext.font = 'bold ' + s + 'px ' + fontFamily;
		}

		function isNumber(n) {
			return !isNaN(parseFloat(n)) && isFinite(n);
		}

		return {
			init: function () {
				fit();
				window.addEventListener('resize', fit);
			},

			circle: function (d) {
				const r = Math.max(0, d) / 2;
				shapeContext.clearRect(0, 0, shapeCanvas.width, shapeCanvas.height);
				shapeContext.beginPath();
				shapeContext.arc(r * gap, r * gap, r * gap, 0, 2 * Math.PI, false);
				shapeContext.fill();
				shapeContext.closePath();
				return processCanvas();
			},

			letter: function (l) {
				let s = 0;
				setFontSize(fontSize);
				s = Math.min(fontSize, (shapeCanvas.width / shapeContext.measureText(l).width) * 0.8 * fontSize, (shapeCanvas.height / fontSize) * (isNumber(l) ? 1 : 0.45) * fontSize);
				setFontSize(s);

				shapeContext.clearRect(0, 0, shapeCanvas.width, shapeCanvas.height);
				shapeContext.fillText(l, shapeCanvas.width / 2, shapeCanvas.height / 2);
				return processCanvas();
			},

			rectangle: function (w, h) {
				const dots = [];
				const width = gap * w;
				const height = gap * h;

				for (let y = 0; y < height; y += gap) {
					for (let x = 0; x < width; x += gap) {
						dots.push(new S.Point({ x: x, y: y }));
					}
				}

				return { dots: dots, w: width, h: height };
			},
		};
	})();

	S.Shape = (function () {
		let dots = [], width = 0, height = 0, cx = 0, cy = 0;

		function compensate() {
			const a = S.Drawing.getArea();
			cx = a.w / 2 - width / 2;
			cy = a.h / 2 - height / 2;
		}

		return {
			switchShape: function (n, fast) {
				let size, a = S.Drawing.getArea(), d = 0, i = 0;

				width = n.w;
				height = n.h;
				compensate();

				if (n.dots.length > dots.length) {
					size = n.dots.length - dots.length;
					for (d = 1; d <= size; d++) {
						dots.push(new S.Dot(a.w / 2, a.h / 2));
					}
				}

				d = 0;
				while (n.dots.length > 0) {
					i = Math.floor(Math.random() * n.dots.length);
					dots[d].e = fast ? 0.25 : dots[d].s ? 0.14 : 0.11;

					if (dots[d].s) {
						dots[d].move(new S.Point({
							z: Math.random() * 20 + 10,
							a: Math.random(),
							h: 18,
						}));
					} else {
						dots[d].move(new S.Point({
							z: Math.random() * 5 + 5,
							h: fast ? 18 : 30,
						}));
					}

					dots[d].s = true;
					dots[d].move(new S.Point({
						x: n.dots[i].x + cx,
						y: n.dots[i].y + cy,
						a: 1,
						z: 5,
						h: 0,
					}));

					n.dots = n.dots.slice(0, i).concat(n.dots.slice(i + 1));
					d++;
				}

				for (i = d; i < dots.length; i++) {
					if (dots[i].s) {
						dots[i].move(new S.Point({
							z: Math.random() * 20 + 10,
							a: Math.random(),
							h: 20,
						}));

						dots[i].s = false;
						dots[i].e = 0.04;
						dots[i].move(new S.Point({
							x: Math.random() * a.w,
							y: Math.random() * a.h,
							a: 0.3,
							z: Math.random() * 4,
							h: 0,
						}));
					}
				}
			},

			render: function () {
				for (let d = 0; d < dots.length; d++) {
					dots[d].render();
				}
			},
		};
	})();

	// 初始化动画
	S.init();
}
</script>

<style scoped>
.festival-container {
	width: 1100px;
	height: 550px;
	overflow: hidden;
	background: #000000;
	position: relative;
}

.canvas {
	display: block;
}

/* 以下是从原HTML文件转换的样式 */
.overlay {
	position: absolute;
	top: 50%;
	left: 50%;
	width: 550px;
	height: 490px;
	margin: -260px 0 0 -275px;
	opacity: 0;
	transform: rotateY(90deg);
	transition: transform 0.7s cubic-bezier(0.694, 0.0482, 0.335, 1), opacity 0.7s cubic-bezier(0.694, 0.0482, 0.335, 1);
}

.overlay--visible {
	opacity: 1;
	transform: rotateY(0);
}

.tabs-labels {
	margin-bottom: 9px;
}

.tabs-label {
	display: inline-block;
	background: #fff;
	padding: 10px 20px;
	font-size: 12px;
	line-height: 22px;
	font-weight: 700;
	text-transform: uppercase;
	letter-spacing: 1px;
	color: #333;
	opacity: 0.5;
	cursor: pointer;
	margin-right: 2px;
	transition: opacity 0.1s cubic-bezier(0.694, 0.0482, 0.335, 1);
}

.tabs-label:hover {
	opacity: 0.9;
}

.tabs-label--active {
	opacity: 0.9;
}

.tabs-panel {
	display: none;
}

.tabs-panel--active {
	display: block;
}

.commands {
	margin: 0;
	padding: 0;
	list-style: none;
	cursor: pointer;
}

.commands-item {
	font-size: 12px;
	line-height: 22px;
	font-weight: 700;
	text-transform: uppercase;
	letter-spacing: 1px;
	padding: 20px;
	background: #fff;
	margin-top: 1px;
	color: #333;
	opacity: 0.9;
	transition: transform 0.1s cubic-bezier(0.694, 0.0482, 0.335, 1), opacity 0.1s cubic-bezier(0.694, 0.0482, 0.335, 1);
	display: flex;
	justify-content: space-between;
	align-items: center;
}

.commands-item--gap {
	margin-top: 9px;
}

.commands-item:hover {
	opacity: 1;
}

.commands-item:hover .commands-item-action {
	background: #333;
}

.commands-item a {
	display: inline-block;
}

.commands-item-mode {
	display: inline-block;
	margin-left: 3px;
	font-style: italic;
	color: #ccc;
}

.commands-item-content {
	display: flex;
	flex: 1;
	min-width: 0;
}

.commands-item-title {
	display: inline-block;
	width: 150px;
	flex-shrink: 0;
}

.commands-item-info {
	display: inline-block;
	flex: 1;
	font-size: 14px;
	text-transform: none;
	letter-spacing: 0;
	font-weight: 400;
	color: #aaa;
}

.commands-item-action {
	text-transform: uppercase;
	font-size: 10px;
	line-height: 10px;
	color: #fff;
	background: #90c9d1;
	padding: 5px 10px 4px;
	border-radius: 3px;
	flex-shrink: 0;
}

.commands-item:first-child {
	margin-top: 0;
}

.ui-details {
	opacity: 0.9;
	background: #fff;
	z-index: 2;
}

.ui-details-content {
	padding: 100px 50px;
}
</style>