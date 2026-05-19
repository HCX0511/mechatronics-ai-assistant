import os
from pathlib import Path

import requests
from dotenv import dotenv_values
from flask import Flask, Response, jsonify, render_template, request


BASE_DIR = Path(__file__).resolve().parent
env_values = dotenv_values(BASE_DIR / "1.env")

API_BASE = (os.getenv("API_BASE") or env_values.get("API_BASE") or "https://api.deepseek.com").rstrip("/")
API_KEY = (os.getenv("API_KEY") or env_values.get("API_KEY") or "").strip()
MODEL_NAME = (os.getenv("MODEL_NAME") or env_values.get("MODEL_NAME") or "deepseek-chat").strip()

print("API_BASE:", API_BASE)
print("MODEL_NAME:", MODEL_NAME)
print("API_KEY loaded:", bool(API_KEY))
print("API_KEY preview:", API_KEY[:6] + "****" if API_KEY else "EMPTY")

app = Flask(__name__)

EXPERIMENTS = {
    "led_flow": {
        "name": "LED 流水灯",
        "subtitle": "GPIO 输出与时序控制基础实验",
        "knowledge_file": "led_experiment.md",
        "summary": "适合入门 GPIO 输出控制、延时、位操作和实验现象观察。",
        "quick_prompts": [
            {
                "title": "实验预习",
                "description": "了解实验目标、原理和器材。",
                "prompt": "请介绍 LED 流水灯实验的实验目标、实验原理和所需器材。",
            },
            {
                "title": "操作指导",
                "description": "获取接线、编译、烧录与观察流程。",
                "prompt": "请一步一步指导我完成 LED 流水灯实验，包括接线、代码编写和烧录。",
            },
            {
                "title": "故障排查",
                "description": "定位 LED 不亮、全亮或不按顺序闪烁的问题。",
                "prompt": "程序烧录成功了，但是 LED 不亮或者全亮不流水，应该怎么排查？",
            },
            {
                "title": "报告辅助",
                "description": "生成实验现象、误差分析和改进建议。",
                "prompt": "帮我生成一段 LED 流水灯实验报告中的实验现象、误差分析和改进建议。",
            },
        ],
    },
    "key_input": {
        "name": "独立按键",
        "subtitle": "GPIO 输入、消抖与人机交互基础实验",
        "knowledge_file": "key_input.md",
        "summary": "适合入门按键输入、电平采样、软件消抖和状态切换。",
        "quick_prompts": [
            {
                "title": "实验预习",
                "description": "理解按键输入原理和上拉下拉方式。",
                "prompt": "请介绍独立按键实验的目标、输入原理，以及上拉和下拉的区别。",
            },
            {
                "title": "操作指导",
                "description": "学习按键接线和消抖程序设计。",
                "prompt": "请一步一步指导我完成独立按键实验，并解释软件消抖该怎么写。",
            },
            {
                "title": "故障排查",
                "description": "排查误触发、连按、按下无反应等问题。",
                "prompt": "按键按下后程序经常误触发或没反应，我该如何排查接线和消抖问题？",
            },
            {
                "title": "报告辅助",
                "description": "整理按键实验现象与分析。",
                "prompt": "帮我写一段独立按键实验的实验现象、问题分析和结论。",
            },
        ],
    },
    "timer_interrupt": {
        "name": "定时器中断",
        "subtitle": "周期任务、定时与中断机制基础实验",
        "knowledge_file": "timer_interrupt.md",
        "summary": "适合入门定时器装载值、中断服务函数和周期任务调度。",
        "quick_prompts": [
            {
                "title": "实验预习",
                "description": "理解定时器中断的工作机制。",
                "prompt": "请介绍定时器中断实验的原理、装载值计算思路和应用场景。",
            },
            {
                "title": "操作指导",
                "description": "学习如何配置定时器和编写中断服务函数。",
                "prompt": "请一步一步指导我完成定时器中断实验，并说明中断服务函数怎么写。",
            },
            {
                "title": "故障排查",
                "description": "排查不进中断、频率不准等问题。",
                "prompt": "我的定时器中断没有进入或者中断频率不准，应该怎么排查？",
            },
            {
                "title": "报告辅助",
                "description": "总结定时误差与实验结论。",
                "prompt": "帮我写一段定时器中断实验的实验现象、误差来源和改进建议。",
            },
        ],
    },
    "uart": {
        "name": "串口通信 UART",
        "subtitle": "异步串行通信基础实验",
        "knowledge_file": "uart.md",
        "summary": "适合入门波特率、收发流程、串口助手联调和调试输出。",
        "quick_prompts": [
            {
                "title": "实验预习",
                "description": "理解 UART 帧格式和波特率概念。",
                "prompt": "请介绍 UART 串口通信实验的基本原理、帧格式和波特率含义。",
            },
            {
                "title": "操作指导",
                "description": "学习串口初始化、发送和接收。",
                "prompt": "请一步一步指导我完成 UART 串口通信实验，包括初始化、发送和接收。",
            },
            {
                "title": "故障排查",
                "description": "排查乱码、收不到数据、回传异常。",
                "prompt": "串口助手出现乱码或者单片机收不到数据，我该怎么排查？",
            },
            {
                "title": "报告辅助",
                "description": "整理串口联调现象与分析。",
                "prompt": "帮我写一段 UART 串口通信实验的实验现象、问题分析和实验结论。",
            },
        ],
    },
    "i2c": {
        "name": "I2C 通信",
        "subtitle": "双线同步总线基础实验",
        "knowledge_file": "i2c.md",
        "summary": "适合入门主从通信、器件地址、应答位和总线时序。",
        "quick_prompts": [
            {
                "title": "实验预习",
                "description": "理解起始、停止、应答和地址机制。",
                "prompt": "请介绍 I2C 通信实验的原理，包括起始位、停止位、应答位和器件地址。",
            },
            {
                "title": "操作指导",
                "description": "学习 I2C 读写流程和典型接线。",
                "prompt": "请一步一步指导我完成 I2C 通信实验，并讲清楚主机读写从机的流程。",
            },
            {
                "title": "故障排查",
                "description": "排查无应答、总线占用和读写失败。",
                "prompt": "I2C 设备没有应答或者读写失败，应该从哪些方面排查？",
            },
            {
                "title": "报告辅助",
                "description": "总结总线通信现象与问题分析。",
                "prompt": "帮我写一段 I2C 通信实验的实验现象、常见问题和改进建议。",
            },
        ],
    },
    "spi": {
        "name": "SPI 通信",
        "subtitle": "高速同步串行接口基础实验",
        "knowledge_file": "spi.md",
        "summary": "适合入门主从时钟、片选、全双工传输和模式配置。",
        "quick_prompts": [
            {
                "title": "实验预习",
                "description": "理解 SPI 四线接口和工作模式。",
                "prompt": "请介绍 SPI 通信实验的工作原理、四根信号线含义以及 CPOL/CPHA。",
            },
            {
                "title": "操作指导",
                "description": "学习 SPI 初始化和主从收发流程。",
                "prompt": "请一步一步指导我完成 SPI 通信实验，并说明主机如何与从机收发数据。",
            },
            {
                "title": "故障排查",
                "description": "排查片选错误、时序不匹配和数据错位。",
                "prompt": "SPI 通信时读到的数据不对或者没有响应，我该怎么排查时序和片选？",
            },
            {
                "title": "报告辅助",
                "description": "整理 SPI 通信实验记录。",
                "prompt": "帮我写一段 SPI 通信实验的实验现象、错误原因和实验总结。",
            },
        ],
    },
    "adc": {
        "name": "ADC 采样",
        "subtitle": "模拟量采集基础实验",
        "knowledge_file": "adc.md",
        "summary": "适合入门采样分辨率、参考电压、传感器输入和数据换算。",
        "quick_prompts": [
            {
                "title": "实验预习",
                "description": "理解 ADC 采样原理和分辨率。",
                "prompt": "请介绍 ADC 采样实验的原理、分辨率、参考电压和数值换算关系。",
            },
            {
                "title": "操作指导",
                "description": "学习 ADC 初始化与采样流程。",
                "prompt": "请一步一步指导我完成 ADC 采样实验，包括初始化、启动采样和结果处理。",
            },
            {
                "title": "故障排查",
                "description": "排查采样值跳变、偏差大和不稳定。",
                "prompt": "ADC 采样值不稳定或者偏差很大，我应该如何排查硬件和软件配置？",
            },
            {
                "title": "报告辅助",
                "description": "整理采样结果和误差分析。",
                "prompt": "帮我写一段 ADC 采样实验的实验现象、误差来源和改进建议。",
            },
        ],
    },
    "pwm_motor": {
        "name": "PWM 电机控制",
        "subtitle": "脉宽调制与执行器控制基础实验",
        "knowledge_file": "pwm_motor.md",
        "summary": "适合入门占空比、频率设置、驱动电路和速度控制。",
        "quick_prompts": [
            {
                "title": "实验预习",
                "description": "理解 PWM 原理和电机驱动基本结构。",
                "prompt": "请介绍 PWM 电机控制实验的原理、占空比作用以及驱动电路的基本要求。",
            },
            {
                "title": "操作指导",
                "description": "学习 PWM 输出配置与电机调速。",
                "prompt": "请一步一步指导我完成 PWM 电机控制实验，并说明如何调节占空比实现调速。",
            },
            {
                "title": "故障排查",
                "description": "排查电机不转、抖动或速度异常。",
                "prompt": "PWM 输出正常但电机不转或者抖动严重，我应该怎么排查？",
            },
            {
                "title": "报告辅助",
                "description": "整理电机控制现象与分析。",
                "prompt": "帮我写一段 PWM 电机控制实验的实验现象、问题分析和优化建议。",
            },
        ],
    },
}

DEFAULT_EXPERIMENT_ID = "led_flow"


def get_experiment(experiment_id: str | None) -> dict:
    return EXPERIMENTS.get(experiment_id or "", EXPERIMENTS[DEFAULT_EXPERIMENT_ID])


def load_knowledge_base(experiment_id: str) -> str:
    experiment = get_experiment(experiment_id)
    knowledge_path = BASE_DIR / "knowledge" / experiment["knowledge_file"]
    if not knowledge_path.exists():
        return f"当前实验“{experiment['name']}”的知识库文件不存在，请检查 knowledge/{experiment['knowledge_file']}。"
    return knowledge_path.read_text(encoding="utf-8")


def generate_local_demo_reply(user_question: str, experiment_id: str) -> str:
    experiment = get_experiment(experiment_id)
    question = user_question.lower()

    study_keywords = ["目标", "目的", "原理", "预习", "介绍"]
    guide_keywords = ["步骤", "怎么做", "操作", "接线", "烧录", "指导", "配置"]
    troubleshoot_keywords = ["不亮", "失败", "报错", "故障", "乱码", "不转", "没反应", "异常"]
    report_keywords = ["报告", "现象", "误差", "分析", "总结", "结论"]

    if any(keyword in question for keyword in study_keywords):
        return (
            f"1. 实验名称\n当前实验为“{experiment['name']}”，它属于嵌入式基础实验中的{experiment['subtitle']}。\n\n"
            "2. 学习目标\n"
            "建议重点掌握该实验涉及的硬件接口作用、基本时序、关键寄存器或配置项，以及程序流程如何驱动硬件产生实验现象。\n\n"
            "3. 预习重点\n"
            "预习时优先看清楚引脚连接关系、输入输出电平逻辑、初始化步骤、主要函数调用顺序，以及实验中最容易出错的参数配置。\n\n"
            "4. 建议做法\n"
            "先用最小功能验证硬件和程序是否正常，再逐步扩展完整功能，这样更容易定位问题。\n\n"
            "当前由于在线接口不可用，以上内容为本地演示模式生成。"
        )

    if any(keyword in question for keyword in guide_keywords):
        return (
            f"1. 实验准备\n请先明确当前实验是“{experiment['name']}”，准备好开发板、供电、连接线、下载器和对应外设模块。\n\n"
            "2. 接线与配置\n根据原理图确认电源、地线、信号线连接无误，再完成 GPIO 或外设模块初始化，确保时钟、模式、波特率或采样参数配置正确。\n\n"
            "3. 最小功能验证\n建议先验证一个最核心的功能点，例如是否能点亮一个灯、是否能收到一帧数据、是否能读到一个稳定采样值。\n\n"
            "4. 完整实验执行\n在最小功能通过后，再补充完整流程、显示逻辑、异常处理和实验现象记录。\n\n"
            "当前由于在线接口不可用，以上内容为本地演示模式生成。"
        )

    if any(keyword in question for keyword in troubleshoot_keywords):
        return (
            f"1. 先确认实验对象\n当前实验为“{experiment['name']}”，排查时先不要同时怀疑所有环节，建议从供电、接线、初始化配置和核心时序四部分逐项检查。\n\n"
            "2. 常见原因\n"
            "常见问题包括引脚接错、地线未共地、外设模式配置不匹配、时钟或波特率设置错误、采样参数不合适，以及程序没有真正执行到目标流程。\n\n"
            "3. 排查顺序\n"
            "先查硬件连接，再查最小测试程序，再查关键参数，最后查完整业务逻辑。每次只改一个变量，避免把问题越调越乱。\n\n"
            "4. 记录结论\n"
            "把每一步现象和修改结果记录下来，后面写实验报告和答辩时会很有帮助。\n\n"
            "当前由于在线接口不可用，以上内容为本地演示模式生成。"
        )

    if any(keyword in question for keyword in report_keywords):
        return (
            f"1. 实验现象\n在“{experiment['name']}”实验中，应先客观描述程序运行后的实际现象，包括功能是否实现、结果是否稳定、是否出现异常。\n\n"
            "2. 原因分析\n从硬件连接、参数配置、时序逻辑、外设初始化和环境干扰几个角度分析实验结果产生的原因。\n\n"
            "3. 误差与问题\n如果结果和理论不完全一致，可以从定时精度、信号干扰、采样偏差、通信配置差异等方面写误差来源。\n\n"
            "4. 改进建议\n可从优化接线、完善程序结构、增加调试输出、提升参数配置准确性等方向提出改进建议。\n\n"
            "当前由于在线接口不可用，以上内容为本地演示模式生成。"
        )

    return (
        f"当前实验为“{experiment['name']}”。你可以围绕实验原理、操作步骤、故障排查或实验报告继续提问。\n\n"
        "为了让我回答得更准确，建议在问题里明确写出你关心的是原理、接线、程序配置、通信异常、采样偏差还是报告分析。\n\n"
        "当前由于在线接口不可用，以上内容为本地演示模式生成。"
    )


def call_llm_api(user_question: str, knowledge: str, experiment_id: str) -> str:
    experiment = get_experiment(experiment_id)

    if API_KEY == "":
        return generate_local_demo_reply(user_question, experiment_id)

    url = f"{API_BASE}/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "你是一名嵌入式基础实验智能助教，面向高校机电、电子、自动化相关实验教学。"
                    f"当前实验主题是“{experiment['name']}”。"
                    "回答时要优先参考给定知识库，结构清晰，适合学生理解。"
                    "如果是故障排查问题，要给出可能原因和逐步排查方法；"
                    "如果是实验报告问题，要给出实验现象、原因分析、误差来源和改进建议；"
                    "涉及硬件操作时，要提醒先断电检查接线，避免短路和错误供电。"
                ),
            },
            {
                "role": "user",
                "content": (
                    f"以下是当前实验“{experiment['name']}”的本地知识库内容：\n{knowledge}\n\n"
                    f"学生问题：{user_question}"
                ),
            },
        ],
        "temperature": 0.4,
        "stream": False,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as error:
        print("DeepSeek API error:", error)
        fallback_reply = generate_local_demo_reply(user_question, experiment_id)
        return f"DeepSeek API 调用失败，已切换为本地演示模式。\n\n{fallback_reply}"


@app.route("/")
def index():
    return render_template(
        "index.html",
        experiments=EXPERIMENTS,
        default_experiment_id=DEFAULT_EXPERIMENT_ID,
    )


@app.route("/favicon.ico")
def favicon():
    return Response(status=204)


@app.route("/api/experiments")
def experiments():
    return jsonify(
        {
            "defaultExperimentId": DEFAULT_EXPERIMENT_ID,
            "experiments": EXPERIMENTS,
        }
    )


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_question = (data.get("message") or "").strip()
    experiment_id = data.get("experimentId") or DEFAULT_EXPERIMENT_ID

    if not user_question:
        return jsonify({"reply": "请输入你的实验问题后再发送。"}), 400

    knowledge = load_knowledge_base(experiment_id)
    reply = call_llm_api(user_question, knowledge, experiment_id)
    return jsonify({"reply": reply})


if __name__ == "__main__":
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    app.run(host=host, port=port, debug=debug)
