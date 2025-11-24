from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY
from vector.vector_store import get_vector_store
import json

llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4o-mini",
    temperature=0
)

def ask_llm(query):
    db = get_vector_store()
    
    # 1️⃣ TOP MATCHED DOCUMENTS
    docs = db.similarity_search(query, k=2)

    combined_context = "\n".join([d.page_content for d in docs])

    # 2️⃣ PICK VIDEO FROM TOP MATCHED DOCUMENT
    top_doc = docs[0] if docs else None
    selected_video = None
    if top_doc:
        selected_video = top_doc.metadata.get("video_id")

    # 3️⃣ Build prompt
    prompt = prompt = f"""
You are TechiGenie.

User question: "{query}"

Relevant knowledge chunks:
{combined_context}

RULES:
1. You MUST choose a video_id from the retrieved chunks.
2. If any chunk contains onboarding, customer help, support, automation → use its video_id (likely VID001).
3. If chunk contains AI team, Technovate team → use its video_id (likely VID002 or VID003).
4. Only return null if ALL retrieved chunks have video_id = null.
5. Answer must be based ONLY on context.
6. OUTPUT STRICT JSON ONLY:

{{
 "answer": "...",
 "video_id": "..."        # VID001, VID002, VID003 or null
}}
"""


    ai_msg = llm.invoke(prompt)
    parsed = json.loads(ai_msg.content)

    # 4️⃣ RETURN FIXED STRUCTURE
    return {
        "answer": parsed["answer"],
        "video_id": selected_video  # comes from vector DB, NOT the LLM
    }
