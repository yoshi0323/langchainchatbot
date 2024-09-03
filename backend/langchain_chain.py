from langchain_community.chains import RetrievalQA
from langchain_community.llms import AzureOpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings

# Azure OpenAIのAPIキーとエンドポイントを設定
AZURE_OPENAI_API_KEY = "b806681071fa4db1afb3bf21178391d8"
AZURE_OPENAI_ENDPOINT = "https://realice-backend-openai.openai.azure.com/"

# ナレッジベースとなるURL
KNOWLEDGE_BASE_URL = "https://iyashitour.com/meigen/theme/life"

def get_answer(question: str) -> str:
    try:
        print(f"Processing question: {question}")  # 質問内容をログ出力

        # WebBaseLoaderを使って指定されたサイトから情報を取得
        loader = WebBaseLoader(KNOWLEDGE_BASE_URL)
        documents = loader.load()
        print("Documents loaded successfully.")  # ロード成功メッセージ

        # OpenAIEmbeddingsを使用してドキュメントをベクトル化
        embeddings = OpenAIEmbeddings(openai_api_key=AZURE_OPENAI_API_KEY)
        vector_store = FAISS.from_documents(documents, embeddings)
        print("Documents vectorized successfully.")  # ベクトル化成功メッセージ

        # Azure OpenAI LLMを設定
        llm = AzureOpenAI(openai_api_key=AZURE_OPENAI_API_KEY, api_base=AZURE_OPENAI_ENDPOINT)

        # RetrievalQAを使用して質問に対する回答を生成
        retriever = vector_store.as_retriever()
        qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
        answer = qa_chain.run(question=question)

        print(f"Answer generated: {answer}")  # 生成された回答をログ出力
        return answer
    except Exception as e:
        print(f"Error occurred: {e}")
        return "申し訳ありませんが、質問に対する回答を生成できませんでした。"
