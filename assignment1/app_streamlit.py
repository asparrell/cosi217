from collections import Counter
from operator import itemgetter

import streamlit as st
import pandas as pd
import altair as alt
import graphviz as gv

import spacy_process


example = (
        "When Sebastian Thrun started working on self-driving cars at "
        "Google in 2007, few people outside of the company took him "
        "seriously. “I can tell you very senior CEOs of major American "
        "car companies would shake my hand and turn away because I wasn’t "
        "worth talking to,” said Thrun, in an interview with Recode earlier "
        "this week.")


# st.set_page_config(layout='wide')
st.markdown('## spaCy visualization')

text = st.text_area('Text to process', value=example, height=100)
# understood_text = st.text("Understood text", value=text)

doc = spacy_process.SpacyDocument(text)

entities = doc.get_entities()
dependencies = doc.get_dependencies()
tokens = doc.get_tokens()
counter = Counter(tokens)
words = list(sorted(counter.most_common(30)))




# https://pandas.pydata.org
chart = pd.DataFrame({
    'frequency': [w[1] for w in words],
    'word': [w[0] for w in words]})

# https://pypi.org/project/altair/
bar_chart = alt.Chart(chart).mark_bar().encode(x='word', y='frequency')



with st.sidebar:
    st.title("Settings")
    method = st.radio(
        "Select view", ("entities", "dependencies")
    )
if method == "entities":
    st.markdown(f'Total number of tokens: {len(tokens)}<br/>'
                f'Total number of types: {len(counter)}', unsafe_allow_html=True)
    # https://docs.streamlit.io/library/api-reference/data/st.table
    st.table(entities)
    # https://docs.streamlit.io/library/api-reference/charts/st.altair_chart
    st.altair_chart(bar_chart)

else:
    table, graph = st.tabs(["table", "graph"])
    with table:
        st.table(dependencies)
    with graph:
        g = gv.Digraph()
        for dep in dependencies:
            g.edge(dep[2], dep[0], dep[1])
        st.graphviz_chart(g)


