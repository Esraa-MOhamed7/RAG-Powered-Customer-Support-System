import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from rag import mmr_retriever, rag_chain, llm  

test_data = {
    "question": [
        "How to issue a refund on Shopify?",
        "What is Amazon's return window for most items?"
    ],
    "ground_truth": [
        "From your Shopify admin, go to Orders, click the order you want to issue a refund.",
        "Most items can be returned within 30 days of delivery."
    ]
}

eval_template = """You are an expert AI system evaluator. Your job is to judge the quality of a RAG system response based on 3 specific metrics.

Evaluate the following data carefully:
- User Question: {question}
- Retrieved Context from DB: {context}
- Generated Answer by RAG: {answer}
- Ground Truth (The Perfect Answer): {ground_truth}

Provide your evaluation exactly in this format (Score from 1 to 5, where 5 is perfect):
1. Faithfulness Score (1-5): [Is the answer derived ONLY from the context without hallucination?]
   - Reason: [Brief explanation]
2. Answer Relevance Score (1-5): [Does the answer directly address the user's question?]
   - Reason: [Brief explanation]
3. Context Precision Score (1-5): [Did the retriever fetch relevant context that matches the ground truth?]
   - Reason: [Brief explanation]
"""

eval_prompt = ChatPromptTemplate.from_template(eval_template)
eval_chain = eval_prompt | llm | StrOutputParser()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

if __name__ == "__main__":
    print(" Starting Custom RAG Evaluation (LLM-as-a-Judge)...")
    
    for i in range(len(test_data["question"])):
        q = test_data["question"][i]
        gt = test_data["ground_truth"][i]
        
        docs = mmr_retriever.invoke(q)
        context = format_docs(docs)
        
        answer = rag_chain({"question": q, "chat_history": []})
        
        print(f"\n--------------------------------------------------")
        print(f" Evaluating Question {i+1}: '{q}'")
        print(f"--------------------------------------------------")
        
        eval_result = eval_chain.invoke({
            "question": q,
            "context": context,
            "answer": answer,
            "ground_truth": gt
        })
        
        print(eval_result)