# ベースイメージの指定
FROM python:3.8

# 作業ディレクトリの設定
WORKDIR /app

# 必要なパッケージのインストール
RUN pip install streamlit openai

# Streamlitのポートを指定
EXPOSE 8501

# ソースコードのコピー
COPY . /app

# コンテナ内でのコマンド実行
CMD ["streamlit", "run", "main.py"]
