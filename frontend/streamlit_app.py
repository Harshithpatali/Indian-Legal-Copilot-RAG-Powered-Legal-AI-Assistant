import requests
import streamlit as st

# -----------------------
# CONFIG
# -----------------------

API_URL = "http://localhost:8000/ask"

st.set_page_config(
    page_title="Indian Legal Research Copilot",
    page_icon="⚖️",
    layout="wide"
)

# -----------------------
# SIDEBAR
# -----------------------

with st.sidebar:

    st.title("⚖️ Legal Copilot")

    st.markdown("---")

    st.markdown(
        """
        ### Features

        ✅ Legal Q&A

        ✅ Source Attribution

        ✅ Confidence Score

        🚧 Case Summarizer

        🚧 Contract Risk Analyzer

        🚧 Similar Cases
        """
    )

    st.markdown("---")

    st.info(
        "Powered by FAISS + Groq Llama 3.3 70B"
    )

# -----------------------
# TITLE
# -----------------------

st.title(
    "⚖️ Indian Legal Research Copilot"
)

st.caption(
    "Retrieval-Augmented Legal Assistant using IndianLawUnified"
)

# -----------------------
# CHAT HISTORY
# -----------------------

if "messages" not in st.session_state:

    st.session_state.messages = []

# Display previous messages

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):
        st.markdown(
            message["content"]
        )

# -----------------------
# USER INPUT
# -----------------------

question = st.chat_input(
    "Ask a legal question..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner(
            "Researching legal documents..."
        ):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "question": question
                    },
                    timeout=120
                )

                if response.status_code != 200:

                    st.error(
                        f"API Error: {response.status_code}"
                    )

                    st.stop()

                data = response.json()

            except Exception as e:

                st.error(str(e))

                st.stop()

        answer = data.get(
            "answer",
            "No answer returned."
        )

        confidence = data.get(
            "confidence_score",
            0
        )

        sources = data.get(
            "sources",
            []
        )

        st.markdown(answer)

        st.progress(
            min(confidence, 1.0)
        )

        st.caption(
            f"Confidence Score: {confidence:.2f}"
        )

        if len(sources) > 0:

            st.markdown(
                "### Retrieved Sources"
            )

            for idx, source in enumerate(
                sources,
                start=1
            ):

                title = (
                    source.get(
                        "question",
                        f"Source {idx}"
                    )
                )

                with st.expander(
                    f"📄 {title}"
                ):

                    st.write(
                        source.get(
                            "content",
                            ""
                        )
                    )

                    if (
                        "confidence"
                        in source
                    ):

                        st.caption(
                            f"Source Confidence: "
                            f"{source['confidence']}"
                        )

                    if (
                        "score"
                        in source
                    ):

                        st.caption(
                            f"Similarity Score: "
                            f"{source['score']}"
                        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )