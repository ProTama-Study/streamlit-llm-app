from dotenv import load_dotenv

load_dotenv()
import os
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

# 専門家モード
PERSONA_MAP = {
    "A：キャリアコーチ": "あなたは思いやりのあるキャリアコーチです。具体的な行動を提案してください。",
    "B：データアナリスト": "あなたは実務志向のデータアナリストです。課題を仮説→指標→分析手順で整理してください。"
}

def generate_answer(user_text: str, persona_key: str) -> str:
    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model="gpt-3.5-turbo",
        temperature=0.4
    )
    messages = [
        SystemMessage(content=PERSONA_MAP[persona_key]),
        HumanMessage(content=user_text),
    ]
    response = llm.invoke(messages)
    return response.content

st.set_page_config(page_title="専門家モードアプリ", page_icon="💬")
st.title("💬 専門家モードアプリ")

with st.expander("アプリの概要 / 使い方", expanded=True):
    st.markdown(
        """
- 入力欄に質問や相談内容を入力  
- 専門家モードを選択して送信すると、その専門家としての回答が表示されます  
- A：キャリアコーチ / B：データアナリスト
        """
    )

user_text = st.text_area("質問 / 相談を入力", height=140)
persona_key = st.radio("専門家モード", options=list(PERSONA_MAP.keys()), horizontal=True, index=0)

if st.button("送信"):
    if not user_text.strip():
        st.error("テキストを入力してください。")
    elif not OPENAI_API_KEY:
        st.error("APIキーが設定されていません。")
    else:
        with st.spinner("回答を生成中…"):
            answer = generate_answer(user_text, persona_key)
        st.subheader("回答")
        st.write(answer)

st.caption("※ 本アプリの回答は参考情報です。重要な判断はご自身で行ってください。")
