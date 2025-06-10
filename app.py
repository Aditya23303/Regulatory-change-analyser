import streamlit as st
from backend import compare_documents
from llm_utils import generate_prompt, call_llm, extract_json

st.set_page_config(page_title="Regulatory Change Analyzer", layout="wide")

st.title(" Regulatory Change Analyzer")

uploaded_v1 = st.file_uploader("Upload BEFORE document (Text_v1.txt)", type="txt")
uploaded_v2 = st.file_uploader("Upload AFTER document (Text_v2.txt)", type="txt")

if st.button("Analyze Changes"):
    if uploaded_v1 and uploaded_v2:
        text_v1 = uploaded_v1.read().decode('utf-8')
        text_v2 = uploaded_v2.read().decode('utf-8')

        with st.spinner(" Detecting changes..."):
            changes = compare_documents(text_v1, text_v2)

        st.success(f" Detected {len(changes)} changes.")

        for idx, change in enumerate(changes):
            with st.expander(f"Change #{idx+1} — {change['change_type']}"):
                if 'old_text' in change:
                    st.markdown(f"**Old Text:**\n\n{change['old_text']}")
                if 'new_text' in change:
                    st.markdown(f"**New Text:**\n\n{change['new_text']}")

                prompt = generate_prompt(change.get('old_text'), change.get('new_text'))
                with st.spinner(" Analyzing with LLM..."):
                    llm_output = call_llm(prompt)
                    llm_json = extract_json(llm_output)

                st.markdown(f"**Change Summary:** {llm_json['change_summary']}")
                st.markdown(f"**Change Type:** {llm_json['change_type']}")

    else:
        st.error(" Please upload BOTH documents.")
