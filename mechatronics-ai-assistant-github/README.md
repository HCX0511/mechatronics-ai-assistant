# 嵌入式基础实验助手

这是一个面向高校机电、电子、自动化等方向的嵌入式基础实验问答项目。  
后端使用 `Flask`，前端使用原生 `HTML/CSS/JavaScript`，支持在页面中选择当前实验，并根据不同实验自动切换快捷提问与知识库内容。

## 项目特点

- 支持多种嵌入式基础实验切换
- 支持实验预习、操作指导、故障排查、报告辅助四类问答
- 支持本地 Markdown 知识库驱动回答
- 支持接入 DeepSeek API
- 当在线接口不可用时，自动回退到本地演示模式
- 支持局域网访问，适合课程演示和答辩展示

## 当前支持的实验

- LED 流水灯
- 独立按键
- 定时器中断
- UART 串口通信
- I2C 通信
- SPI 通信
- ADC 采样
- PWM 电机控制

## 项目结构

```text
mechatronics-ai-assistant/
├─ app.py
├─ README.md
├─ requirements.txt
├─ 1.env
├─ start_website.bat
├─ start_lan_share.ps1
├─ allow_port_5000.ps1
├─ knowledge/
│  ├─ led_experiment.md
│  ├─ key_input.md
│  ├─ timer_interrupt.md
│  ├─ uart.md
│  ├─ i2c.md
│  ├─ spi.md
│  ├─ adc.md
│  └─ pwm_motor.md
├─ templates/
│  └─ index.html
└─ static/
   ├─ style.css
   └─ main.js
```

## 环境要求

- Python 3.10 及以上

## 安装依赖

在项目根目录执行：

```bash
pip install -r requirements.txt
```

## 配置 API

项目通过 `1.env` 读取配置。

示例：

```env
API_BASE=https://api.deepseek.com
API_KEY=你的 DeepSeek API Key
MODEL_NAME=deepseek-chat
```

说明：

- `API_BASE` 默认使用 `https://api.deepseek.com`
- `MODEL_NAME` 默认使用 `deepseek-chat`
- 不要把真实 API Key 提交到仓库中

建议把 `1.env.example` 提供给其他人参考，再让他们自行复制为 `1.env` 并填写自己的密钥。

## 启动项目

直接启动：

```bash
python app.py
```

默认访问地址：

```text
http://127.0.0.1:5000
```

也可以通过环境变量指定监听地址、端口和调试模式：

```bash
APP_HOST=0.0.0.0
APP_PORT=5000
FLASK_DEBUG=false
python app.py
```

## 推荐启动方式

### 1. 本机直接启动

双击：

```text
start_website.bat
```

这个方式最适合你自己本机调试和演示。

### 2. 局域网共享启动

如果希望同一 Wi-Fi 或同一局域网里的其他设备访问你的网站：

1. 先以管理员身份运行 `allow_port_5000.ps1`
2. 再运行 `start_lan_share.ps1`
3. 保持服务窗口不要关闭
4. 让其他设备访问：

```text
http://你的局域网IP:5000
```

例如你之前检测到的地址是：

```text
http://10.87.120.219:5000
```

## 部署到 Render

这个项目可以直接部署到 Render 的免费 Web Service。

### 1. 上传代码到 GitHub

建议上传这些内容：

- `app.py`
- `requirements.txt`
- `render.yaml`
- `templates/`
- `static/`
- `knowledge/`
- `README.md`
- `1.env.example`

不建议上传这些内容：

- `1.env`
- `.venv/`
- `.tmp/`
- `__pycache__/`

### 2. 在 Render 创建服务

1. 登录 Render
2. 选择 `New +`
3. 选择 `Blueprint` 或 `Web Service`
4. 连接你的 GitHub 仓库

如果使用 `render.yaml`，Render 会自动识别这些配置：

- 构建命令：`pip install -r requirements.txt`
- 启动命令：`gunicorn app:app`
- 免费实例类型：`free`

### 3. 在 Render 设置环境变量

至少配置这些变量：

```text
API_BASE=https://api.deepseek.com
API_KEY=你的真实密钥
MODEL_NAME=deepseek-chat
```

说明：

- `API_KEY` 不要写进仓库
- Render 上应通过环境变量填写
- 现在 `app.py` 会优先读取 Render 环境变量，其次才读取本地 `1.env`

### 4. 部署完成后访问

部署完成后，Render 会给你一个公网地址，例如：

```text
https://mechatronics-ai-assistant.onrender.com
```

这个地址可以被不在同一局域网的人访问。

### 5. 免费版限制

- 免费实例空闲一段时间后会休眠
- 再次访问时会有冷启动等待
- 适合演示、课程展示、轻量使用
- 不适合高并发或正式生产长期服务

## 页面交互说明

当前页面支持：

- 选择当前实验
- 根据当前实验动态切换快捷提问
- 在同一问答区继续提问
- 将实验 ID 一起发送到后端
- 根据对应知识库生成回答

## 后端逻辑说明

`app.py` 中维护了实验配置表，包含：

- 实验名称
- 实验副标题
- 对应知识库文件
- 实验简介
- 快捷提问列表

前端切换实验时：

1. 页面更新实验标题和简介
2. 左侧快捷提问自动变化
3. 提问时把 `experimentId` 传给 `/api/chat`
4. 后端按对应实验读取知识库文件

## 知识库说明

每个实验对应 `knowledge/` 目录下一个 Markdown 文件。  
建议每个知识库至少包含这些部分：

- 实验目标
- 实验原理
- 器材与接线
- 配置或程序流程
- 常见问题
- 安全注意事项
- 报告写作建议

如果后续你要继续扩展实验，只需要：

1. 在 `knowledge/` 下新增一个 Markdown 文件
2. 在 `app.py` 的 `EXPERIMENTS` 中注册该实验
3. 配置快捷提问

## 回退逻辑

- 如果 `API_KEY` 为空，系统直接使用本地演示模式
- 如果 DeepSeek API 调用失败，系统会自动回退到本地演示模式
- 回退模式不会让网页报错，只是回答内容会更通用

## 技术栈

- Flask
- HTML / CSS / JavaScript
- python-dotenv
- requests
- 本地 Markdown 知识库
- DeepSeek Chat Completions API

## 适用场景

- 嵌入式基础实验课堂演示
- 课程设计原型展示
- 实验助教问答系统
- 比赛答辩演示页面

## 后续可扩展方向

- 增加更多实验类型，例如外部中断、数码管、CAN、传感器融合
- 增加实验分类页
- 按平台区分 51 / STM32 / Arduino 的回答风格
- 支持上传实验图片辅助诊断
- 支持实验报告模板自动生成
