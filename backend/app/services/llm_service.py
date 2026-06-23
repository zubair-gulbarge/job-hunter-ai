from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 1. Initialize the local LLM
# This connects natively to the Ollama process running in your background
llm = ChatOllama(
    model="llama3",
    temperature=0.7, # Adds slight creativity for rewriting bullets
)

def tailor_resume_content(master_resume: str, job_description: str) -> str:
    # 2. Create the System and Human Prompts
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert technical recruiter and resume writer. "
                   "Your task is to tailor a master resume to match a specific job description. "
                   "Only use the facts provided in the master resume. Do not invent experience. "
                   "Output ONLY the tailored resume text."),
        ("human", "Master Resume:\n{resume}\n\nJob Description:\n{jd}")
    ])
    
    # 3. Build the LangChain Pipeline
    # The pipe symbol (|) chains the prompt -> model -> string output
    chain = prompt | llm | StrOutputParser()
    
    # 4. Execute the chain
    response = chain.invoke({
        "resume": master_resume,
        "jd": job_description
    })
    
    return response