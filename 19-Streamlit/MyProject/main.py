import streamlit as st
from langchain_core.messages import ChatMessage

st.title("나만의 챗GPT")

# 처음 1번만 실행하기 위한 코드
if "messages" not in st.session_state:
    # 대화 기록을 저장하기 위한 용도를 생성한다.
    st.session_state["messages"] = []

# 이전 대화를 출력

# 방법 1
# for role, message in st.session_state["messages"]:
#     st.chat_message(role).write(message)

# 방법 2
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)

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
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(user_input)

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
    add_message("assistant", user_input)