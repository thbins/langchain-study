import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import ChatMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# API KEY 정보로드
load_dotenv()

st.title("나만의 챗GPT")

# 처음 1번만 실행하기 위한 코드
if "messages" not in st.session_state:
    # 대화 기록을 저장하기 위한 용도를 생성한다.
    st.session_state["messages"] = []

# 사이드바 생성
with st.sidebar:
    # 초기화 버튼 생성
    clear_btn = st.button("대화 초기화")

# 이전 대화를 출력

# 방법 1
# for role, message in st.session_state["messages"]:
#     st.chat_message(role).write(message)

# 방법 2
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)

# 체인 생성
def create_chain():
    # prompt | llm | output_parser

    # 프롬프트
    prompt = ChatPromptTemplate(
        [
            ("system", "당신은 친절한 AI 어시스턴트입니다."),
            ("user", "Question:\n{question}"),
        ]
    )

    # LLM(GPT)
    llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

    # 출력 파서
    output_parser = StrOutputParser()

    # 체인 생성
    chain = prompt | llm | output_parser
    
    return chain

# 초기화 버튼이 눌리면
if clear_btn:
    st.session_state["messages"] = []

# 이전 대화 기록 출력
print_messages()

# 사용자의 입력
user_input = st.chat_input("궁금한 내용을 물어보세요!")

# 만약 사용자 입력이 들어오면
# if user_input:
#     st.write("사용자 입력: {user_input}")

if user_input:
    # 웹에 대화를 출력
    # with st.chat_message("user"):
    #     st.write("사용자 입력: {user_input}")
    
    # 사용자의 입력
    st.chat_message("user").write(user_input)
    
    # chain을 생성
    chain = create_chain()
    
    # ai_answer = chain.invoke({"question" : user_input})
    # AI의 답변
    # st.chat_message("assistant").write(ai_answer)
    
    # invoke 말고 스트리밍 출력
    response = chain.stream({"question": user_input})
    with st.chat_message("assistant"):
        # 빈 공간(컨테이너)를 만들어서, 여기에 토큰을 스트리밍 출력한다.
        container = st.empty()

        ai_answer = ""
        for token in response:
            ai_answer += token
            container.markdown(ai_answer)

    # 대화기록을 저장

    # 방법 1
    # st.session_state["messages"].append(("user", user_input))
    # st.session_state["messages"].append(("assistant", user_input))

    # 방법 2
    # ChatMessage(role="user", content=user_input)
    # ChatMessage(role="assistant", content=user_input)

    # 방법 2를 응용
    def add_message(role, message):
        st.session_state["messages"].append(ChatMessage(role=role, content=message))

    add_message("user", user_input)
    add_message("assistant", ai_answer)