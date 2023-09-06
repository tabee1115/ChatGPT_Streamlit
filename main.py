import openai
import streamlit as st
import os

st.title("ChatGPTと対話") # タイトルの設定

openai.api_key = os.getenv('OPENAI_API_KEY') # OpenAIのAPIキーを設定

# セッション内で使用するモデルが指定されていない場合のデフォルト値
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# セッション内のメッセージが指定されていない場合のデフォルト値
if "messages" not in st.session_state:
    st.session_state.messages = []

# セッション内でチャット履歴をクリアするかどうかの状態変数
if "Clear" not in st.session_state:
    st.session_state.Clear = False

# 以前のメッセージを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ユーザーからの新しい入力を取得
if prompt := st.chat_input("今何してる？"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty() # 一時的なプレースホルダーを作成
        full_response = ""
        # ChatGPTからのストリーミング応答を処理
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌") # レスポンスの途中結果を表示
        message_placeholder.markdown(full_response) # 最終レスポンスを表示
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    st.session_state.Clear = True # チャット履歴のクリアボタンを有効にする

# チャット履歴をクリアするボタンが押されたら、メッセージをリセット
if st.session_state.Clear:
    if st.button('対話履歴の消去'):
        st.session_state.messages = [] # メッセージのリセット
        full_response = ""
        st.session_state.Clear = False # クリア状態をリセット
        st.experimental_rerun() # 画面を更新