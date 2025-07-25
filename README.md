
# 🪖 AI tank_chatbot system 
  
## 📌 Overview
This chatbot system is designed by combining **RAG (Retrieval-Augmented Generation)** and a **Large Language Model (LLM)** API to provide accurate and reliable answers to user queries based on a vast collection of **military-related documents**.

---

## 🧠 System Architecture  

### 1. 🔍 Document Retriever  
- **Role**: Quickly identifies the most relevant documents in response to user queries.
- **Method**:
  - Military documents are **vectorized** and stored in a vector database using Chroma Retriever.
  - Queries are converted into vectors and matched based on cosine similarity.

### 2. 📄 Document Storage (Database)
- **Format**: PDF, Word, and text files are parsed and stored as JSON or in a vector database.
- **Contents**: Military operation manuals, tactical guides, equipment specifications, and more.

### 3. 🧠 LLM (OpenAI GPT)
- **Role**: Generates natural language responses based on retrieved documents.
- **Input**: User question + relevant document context.
- **Output**: Reliable responses grounded in the referenced documents.

---

## 🔁 Workflow (Pipeline)

1. **User submits a question**  
   Example: "Please explain the specifications of tactic 000."

2. **Retriever searches relevant documents**  
   Retrieves the top N documents from the vector database that are most similar to the query.

3. **LLM prompt composition with documents**
   ```plaintext
   [Excerpt or summary of retrieved documents]
   User question: "..."
   Please answer the question based on the above document.

  <img width="1281" height="1241" alt="image" src="https://github.com/user-attachments/assets/abc2f13e-08c9-449f-bbbb-3f243086f0be" />



===============================================================
  
## 📌 개요
이 챗봇 시스템은 방대한 **군사 관련 문서**를 기반으로 사용자의 질문에 정확하고 신뢰성 있는 정보를 제공하기 위해 **RAG (Retrieval-Augmented Generation)** 기법과 **LLM (대형 언어 모델)** API를 결합하여 설계되었습니다.

---

## 🧠 시스템 구성  

### 1. 🔍 문서 검색기 (Retriever)  
- **역할**: 사용자의 질문에 가장 관련성 높은 문서를 빠르게 찾아냅니다.
- **방법**:
  - 군사 문서를 **벡터화**하여 벡터 DB에 저장 by Chroma retriever 
  - 질문을 벡터로 변환 후 유사도 기반 검색 (Cosine Similarity)

### 2. 📄 문서 저장소 (DataBase)  
- **형태**: PDF, Word, 텍스트 파일 등을 파싱한 후 JSON 또는 벡터 DB에 저장
- **내용**: 군사 작전 매뉴얼, 전술 지침서, 장비 설명서 등

### 3. 🧠 LLM (OpenAI GPT)  
- **역할**: 검색된 문서를 바탕으로 자연어로 응답 생성
- **입력**: 사용자 질문 + 관련 문서(문맥)
- **출력**: 문서 기반의 신뢰도 높은 응답

<img width="1281" height="1241" alt="image" src="https://github.com/user-attachments/assets/b517eebe-aa0a-4f93-a292-7df32f74018e" />


---

## 🔁 작동 흐름 (Pipeline)

1. **사용자 질문 입력**  
   예: "특정 전술 000에 대한 스펙 설명"

2. **Retriever가 관련 문서 검색**  
   벡터 DB에서 해당 질문과 유사한 문서를 N개 선택

3. **LLM에 문서와 함께 프롬프트 구성**
   ```plaintext
   [문서 요약 또는 원문 일부]
   사용자 질문: "..."
   이 질문에 위 문서를 기반으로 답변하세요.

===============================================================
