import streamlit as st
import requests

# ---------- 你的提示词（已去敏感词）----------
SYSTEM_PROMPT = """你是“校园法治青年助手”，一位专注于普法与风险防范知识科普的智能体。你的任务是帮助团员和同学增强法治观念、提升日常生活中的风险识别与自我保护能力。

# 核心能力
1. 法律法规查询：回答《反间谍法》《数据安全法》《保守国家秘密法》等法律相关的常见问题。
2. 校园场景提示：结合学术交流、网络社交、求职兼职、出国（境）交流等场景，提供法律与安全提示。
3. 活动素材生成：协助生成主题班会、团日活动的策划大纲、宣传文案、知识竞赛题目框架。
4. 情景推演参考：提供“高薪兼职索要内部资料”等互动情景。

# 回复规范
- 语气亲切，像学长/学姐。
- 优先调用知识库内容（若有）。
- 遇到疑似泄密、非法收集信息等行为，提醒用户注意法律风险，并可建议通过12339反映。

# 行为红线
- 不提供具体法律行动建议。
- 不替代官方机构判断。
- 对复杂问题回复：“建议您向学校保卫处或拨打12339咨询。”
"""

# ---------- 调用 API（使用硅基流动的免费模型）----------
def chat_with_ai(user_message):
    url = "https://api.siliconflow.cn/v1/chat/completions"
    api_key = "sk-mstmqpwsczmdiaoctvmfoldoatgopxuddofrewclqyqlclwp"  # 去 https://siliconflow.cn 注册免费拿
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "stream": False
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()["choices"][0]["message"]["content"]

# ---------- 页面界面 ----------
st.set_page_config(page_title="校园法治青年助手", page_icon="⚖️")
st.title("⚖️ 校园法治青年助手")
st.caption("我可以帮你了解法律常识、防范校园风险、生成团日活动素材")

# 初始化聊天记录
if "messages" not in st.session_state:
    st.session_state.messages = []

# 显示历史消息
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 输入框
if prompt := st.chat_input("输入你的问题..."):
    # 显示用户消息
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 获取回复
    with st.chat_message("assistant"):
        with st.spinner("思考中..."):
            reply = chat_with_ai(prompt)
            st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})