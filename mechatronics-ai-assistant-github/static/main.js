const appConfig = window.APP_CONFIG || { experiments: {}, defaultExperimentId: null };
const experiments = appConfig.experiments || {};
let currentExperimentId = appConfig.defaultExperimentId;

const replyPanel = document.getElementById("replyPanel");
const chatInput = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");
const clearBtn = document.getElementById("clearBtn");
const statusTag = document.getElementById("statusTag");
const experimentSelect = document.getElementById("experimentSelect");
const heroExperimentName = document.getElementById("heroExperimentName");
const heroExperimentSummary = document.getElementById("heroExperimentSummary");
const currentExperimentTag = document.getElementById("currentExperimentTag");
const experimentSubtitle = document.getElementById("experimentSubtitle");
const shortcutList = document.getElementById("shortcutList");
const chatExperimentName = document.getElementById("chatExperimentName");
const sideExperimentName = document.getElementById("sideExperimentName");

let thinkingMessage = null;

const UI_TEXT = {
    me: "\u6211",
    student: "\u5b66\u751f\u63d0\u95ee",
    aiTeacher: "AI \u52a9\u6559",
    thinking: "AI \u52a9\u6559\u6b63\u5728\u601d\u8003...",
    online: "\u5728\u7ebf",
    loading: "\u601d\u8003\u4e2d",
    emptyQuestion: "\u8bf7\u8f93\u5165\u5f53\u524d\u5b9e\u9a8c\u76f8\u5173\u7684\u95ee\u9898\u540e\u518d\u53d1\u9001\u3002",
    requestFailed: "\u8bf7\u6c42\u5931\u8d25\uff0c\u8bf7\u68c0\u67e5\u540e\u7aef\u670d\u52a1\u662f\u5426\u6b63\u5e38\u8fd0\u884c\u3002",
    currentExperiment: "\u5f53\u524d\u5b9e\u9a8c\uff1a",
    switchedPrefix: "\u5f53\u524d\u5df2\u5207\u6362\u5230\u201c",
    switchedSuffix: "\u201d\u3002\u4f60\u53ef\u4ee5\u70b9\u51fb\u5de6\u4fa7\u5feb\u6377\u63d0\u95ee\uff0c\u6216\u8005\u76f4\u63a5\u8f93\u5165\u8be5\u5b9e\u9a8c\u76f8\u5173\u7684\u95ee\u9898\u3002",
};

function scrollToBottom() {
    replyPanel.scrollTop = replyPanel.scrollHeight;
}

function getCurrentExperiment() {
    return experiments[currentExperimentId];
}

function createMessage(role, text) {
    const row = document.createElement("article");
    row.className = `message-row ${role === "user" ? "user-row" : "ai-row"}`;

    const avatar = document.createElement("div");
    avatar.className = `message-avatar ${role === "user" ? "message-avatar--user" : "message-avatar--ai"}`;
    avatar.textContent = role === "user" ? UI_TEXT.me : "AI";

    const stack = document.createElement("div");
    stack.className = "message-stack";

    const label = document.createElement("span");
    label.className = "message-role";
    label.textContent = role === "user" ? UI_TEXT.student : UI_TEXT.aiTeacher;

    const bubble = document.createElement("div");
    bubble.className = `message-bubble ${role === "user" ? "message-bubble--user" : "message-bubble--ai"}`;
    if (role === "ai") {
        bubble.innerHTML = formatAiText(text);
    } else {
        bubble.textContent = text;
    }

    stack.appendChild(label);
    stack.appendChild(bubble);
    row.appendChild(avatar);
    row.appendChild(stack);
    return row;
}

function escapeHtml(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#39;");
}

function formatAiText(text) {
    const escaped = escapeHtml(text);
    const blocks = escaped.split(/\n\s*\n/).filter(Boolean);

    return blocks.map((block) => {
        const lines = block.split("\n").filter(Boolean);
        const isListBlock = lines.every((line) => /^\d+\.\s/.test(line.trim()) || /^-\s/.test(line.trim()));

        if (isListBlock) {
            const items = lines.map((line) => `<li>${line.replace(/^\d+\.\s|^-\s/, "")}</li>`).join("");
            return `<ul class="message-rich-list">${items}</ul>`;
        }

        const headingMatch = block.trim().match(/^(\d+\.\s[^\n:：]+|[^\n]{2,20}[：:])$/);
        if (headingMatch) {
            return `<h4 class="message-rich-heading">${block.trim()}</h4>`;
        }

        return `<p>${lines.join("<br>")}</p>`;
    }).join("");
}

function appendMessage(role, text) {
    replyPanel.appendChild(createMessage(role, text));
    scrollToBottom();
}

function showThinkingMessage() {
    thinkingMessage = createMessage("ai", UI_TEXT.thinking);
    thinkingMessage.querySelector(".message-bubble").classList.add("message-bubble--thinking");
    replyPanel.appendChild(thinkingMessage);
    scrollToBottom();
}

function removeThinkingMessage() {
    if (thinkingMessage) {
        thinkingMessage.remove();
        thinkingMessage = null;
    }
}

function setLoading(isLoading) {
    sendBtn.disabled = isLoading;
    clearBtn.disabled = isLoading;
    chatInput.disabled = isLoading;
    experimentSelect.disabled = isLoading;
    statusTag.textContent = isLoading ? UI_TEXT.loading : UI_TEXT.online;
}

function renderExperimentOptions() {
    experimentSelect.innerHTML = Object.entries(experiments)
        .map(([id, experiment]) => `<option value="${id}">${experiment.name}</option>`)
        .join("");
    experimentSelect.value = currentExperimentId;
}

function createShortcutCard(item, index) {
    const button = document.createElement("button");
    button.className = "shortcut-card";
    button.type = "button";
    button.dataset.prompt = item.prompt;
    button.innerHTML = `
        <span class="shortcut-card__icon">${String(index + 1).padStart(2, "0")}</span>
        <div>
            <strong>${item.title}</strong>
            <p>${item.description}</p>
        </div>
    `;
    button.addEventListener("click", () => {
        const prompt = button.dataset.prompt || "";
        sendMessage(prompt);
    });
    return button;
}

function renderShortcuts() {
    const experiment = getCurrentExperiment();
    shortcutList.innerHTML = "";
    experiment.quick_prompts.forEach((item, index) => {
        shortcutList.appendChild(createShortcutCard(item, index));
    });
}

function renderExperimentView() {
    const experiment = getCurrentExperiment();
    heroExperimentName.textContent = experiment.name;
    heroExperimentSummary.textContent = experiment.summary;
    experimentSubtitle.textContent = experiment.subtitle;
    currentExperimentTag.textContent = `${UI_TEXT.currentExperiment}${experiment.name}`;
    chatExperimentName.textContent = experiment.name;
    sideExperimentName.textContent = experiment.name;
    renderShortcuts();
}

async function sendMessage(customMessage) {
    const message = (customMessage ?? chatInput.value).trim();

    if (!message) {
        appendMessage("ai", UI_TEXT.emptyQuestion);
        chatInput.focus();
        return;
    }

    appendMessage("user", message);

    chatInput.value = "";

    setLoading(true);
    showThinkingMessage();

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message,
                experimentId: currentExperimentId,
            }),
        });

        const data = await response.json();
        removeThinkingMessage();

        if (!response.ok) {
            throw new Error(data.reply || UI_TEXT.requestFailed);
        }

        appendMessage("ai", data.reply);
    } catch (error) {
        removeThinkingMessage();
        appendMessage("ai", error.message || UI_TEXT.requestFailed);
    } finally {
        setLoading(false);
        chatInput.focus();
        scrollToBottom();
    }
}

function clearConversation() {
    const experiment = getCurrentExperiment();
    replyPanel.innerHTML = "";
    appendMessage("ai", `${UI_TEXT.switchedPrefix}${experiment.name}${UI_TEXT.switchedSuffix}`);
}

experimentSelect.addEventListener("change", (event) => {
    currentExperimentId = event.target.value;
    renderExperimentView();
    clearConversation();
});

sendBtn.addEventListener("click", () => sendMessage());

clearBtn.addEventListener("click", () => {
    clearConversation();
    chatInput.focus();
});

chatInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

renderExperimentOptions();
renderExperimentView();
