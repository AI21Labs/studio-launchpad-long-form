import streamlit as st

from utils.completion import complete
from utils.studio_style import apply_studio_style
from constants import CLASSIFICATION_FEWSHOT, CLASSIFICATION_PROMPT, CLASSIFICATION_TITLE, CLASSIFICATION_SUMMARY


def query(prompt):
    config = {
        "numResults": 1,
        "maxTokens": 5,
        "temperature": 0,
        "stopSequences": ["==="]
    }
    res = complete(model_type=st.session_state['model'],
                   prompt=prompt,
                   config=config,
                   api_key=st.secrets['api-keys']['ai21-algo-team-prod'])
    return res["completions"][0]["data"]["text"]


if __name__ == '__main__':

    apply_studio_style()
    st.title("Topic Classification")

    st.subheader("Model")
    st.session_state['model'] = st.selectbox(label="Select your preferred AI21 model",
                                             options=['j1-jumbo', 'experimental/j1-grande-instruct', 'j1-grande', 'j1-large'])

    st.write("--------------------------------")
    st.text(CLASSIFICATION_PROMPT)
    classification_title = st.text_input(label="Title:", value=CLASSIFICATION_TITLE)
    classification_summary = st.text_area(label="Summary:", value=CLASSIFICATION_SUMMARY, height=100)

    if st.button(label="Classify"):
        with st.spinner("Loading..."):
            classification_prompt = f"{CLASSIFICATION_PROMPT}\nTitle:\n{classification_title}" \
                                    f"Summary:\n{classification_summary}The topic of this article is:\n"
            st.session_state["classification_result"] = query(CLASSIFICATION_FEWSHOT + classification_prompt)

    if "classification_result" in st.session_state:
        st.subheader(f"Topic: {st.session_state['classification_result']}")