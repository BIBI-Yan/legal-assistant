import streamlit as st
import requests

# ---------- 团员教育版提示词 ----------
SYSTEM_PROMPT = """你是团支部的“国安教育辅导员”，名字叫“小安”。你的工作是：用同学们爱听的方式，讲清楚国家安全那些事，顺便帮团支书省点力气。

# 你擅长做的事
- **解答疑惑**：《国家安全法》第几条？发军舰照违法吗？境外组织的问卷能填吗？—— 随时问，随时答。
- **风险识别**：帮同学判断“这兼职是不是有问题”“这人是不是在套我话”。
- **团日助攻**：要开主题团会？给我主题，我出策划、出PPT大纲、出主持词、出10道抢答题。
- **情景模拟**：比如“假如有人加你微信，说要买你课题里的数据……” 我可以扮演对方，和你过一遍。

# 说话风格
- 就像你们班那个懂法又爱帮忙的团支书。
- 可以带点感叹号、可以叫“同学”“伙伴”。
- 如果需要严肃提醒，就认真说；平时可以轻松点。

# 重要原则
- 不编法律条文。
- 不确定的就建议去查官方渠道或打12339。
- 对明显违法的问题，不回避，正面提示风险。

# 开场白
嗨～我是咱团支部的小安。国家安全听起来很大，其实就跟我们刷手机、找实习、写论文这些事儿有关。有啥拿不准的，找我聊聊呗。对了，需要帮团日活动出材料的，直接甩主题给我。"""

# ---------- 调用硅基流动 API ----------
def chat_with_ai(user_message):
    url = "https://api.siliconflow.cn/v1/chat/completions"
    api_key = "sk-mstmqpwsczmdiaoctvmfoldoatgopxuddofrewclqyqlclwp"  # 替换成你自己的
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
    result = response.json()
    return result["choices"][0]["message"]["content"]

# ---------- Streamlit 页面 ----------
st.set_page_config(page_title="团支部·国安小助手", page_icon="🇨🇳")

# 侧边栏支部信息
st.sidebar.markdown("🇨🇳 **我们是 嘉兴大学 材料与纺织工程学院 非织造251团支部**")
st.sidebar.markdown("---")
st.sidebar.markdown("**小安的服务范围：**")
st.sidebar.markdown("- 法律法规常识")
st.sidebar.markdown("- 校园风险识别")
st.sidebar.markdown("- 团日活动素材")
st.sidebar.markdown("- 情景互动模拟")
st.sidebar.markdown("---")
st.sidebar.caption("遇到可疑情况，请拨打 12339")

st.title("🇨🇳 团支部·国安小助手")
st.caption("我是小安，你的团员教育好伙伴。有啥拿不准的，都可以问我～")

# 初始化聊天记录
if "messages" not in st.session_state:
    # 开场白
    st.session_state.messages = [
        {"role": "assistant", "content": "嗨～我是咱团支部的小安。国家安全听起来很大，其实就跟我们刷手机、找实习、写论文这些事儿有关。有啥拿不准的，找我聊聊呗。对了，需要帮团日活动出材料的，直接甩主题给我。"}
    ]

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
        with st.spinner("小安思考中..."):
            reply = chat_with_ai(prompt)
            st.markdown(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
