import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# LangChainのインポート
from langchain_openai import OpenAIEmbeddings  # 修正済み
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.llms import AzureOpenAI
from langchain.chains import RetrievalQA

# .envファイルから環境変数を読み込む
load_dotenv()

# 環境変数を取得
AZURE_OPENAI_API_KEY = os.getenv("b806681071fa4db1afb3bf21178391d8")
AZURE_OPENAI_ENDPOINT = os.getenv("https://realice-backend-openai.openai.azure.com/")

# FastAPIアプリケーションの初期化
app = FastAPI()

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# リクエストボディのスキーマ定義
class QuestionRequest(BaseModel):
    question: str

# 質問応答を行う関数
def get_answer(question: str) -> str:
    try:
        # ナレッジベースのURLを指定
        KNOWLEDGE_BASE_URL = "https://iyashitour.com/meigen/theme/life"
        
        # WebBaseLoaderを使用してドキュメントをロード
        loader = WebBaseLoader(KNOWLEDGE_BASE_URL)
        documents = loader.load()
        print("Documents loaded successfully.")
        
        # OpenAIEmbeddingsを使用してドキュメントをベクトル化
        embeddings = OpenAIEmbeddings(openai_api_key=AZURE_OPENAI_API_KEY)
        vector_store = FAISS.from_documents(documents, embeddings)
        
        # Azure OpenAIを使用したLLMの設定
        llm = AzureOpenAI(api_key=AZURE_OPENAI_API_KEY, api_base=AZURE_OPENAI_ENDPOINT)
        
        # RetrievalQAを使用して質問応答チェーンを構築
        retriever = vector_store.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
        
        # 質問に対する回答を生成
        answer = qa_chain.run(question=question)
        return answer
    except Exception as e:
        print(f"Error during QA processing: {e}")
        return "申し訳ありませんが、質問に対する回答を生成できませんでした。"

# ルートエンドポイント
@app.get("/")
async def read_root():
    return {"message": "Welcome to the LangChain Chatbot API"}

# 質問応答のエンドポイント
@app.post("/ask")
async def ask_question(request: QuestionRequest):
    question = request.question
    answer = get_answer(question)
    if answer:
        return {"answer": answer}
    else:
        raise HTTPException(status_code=500, detail="回答を生成できませんでした")

# テスト用のサンプルコード
if __name__ == "__main__":
    import requests

    url = "http://127.0.0.1:8000/ask"
    data = {"question": "あなたの質問"}
    response = requests.post(url, json=data)

    print(response.json())