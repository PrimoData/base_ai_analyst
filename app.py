import streamlit as st
import os
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import pandas as pd
import requests
import json
import re
import openai
from flipside import Flipside

# Configure Streamlit Page
page_icon = "https://altcoinsbox.com/wp-content/uploads/2023/02/base-logo-in-blue.png"
st.set_page_config(page_title="Base AI Analyst", page_icon=page_icon, layout="wide")

# Read Custom CSS
with open("assets/css/style.css", "r") as f:
    css_text = f.read()
custom_css = f"<style>{css_text}</style>"
st.markdown(custom_css, unsafe_allow_html=True)

# Get API Keys
openai_api_key = os.environ["OPENAI_API_KEY"]
FLIPSIDE_API_KEY = os.environ["FLIPSIDE_API_KEY"]

# Heading
st.write(
    f"""<h1>
            <img src="https://altcoinsbox.com/wp-content/uploads/2023/02/base-logo-in-blue.png" alt="Base logo" height="36" style="margin-bottom:6px">
            Base AI Analyst
        </h1>""",
    unsafe_allow_html=True,
)
st.subheader("Analyze blockchain data and create charts using natural language")


# Generate SQL Query
def generate_sql(prompt):
    system_description = """
    "You are an SQL assistant. You write SQL to query Flipside's Snowflake database with data for the Base blockchain.

    The database has the following tables and columns:
    [{""TABLE_NAME"":""dim_contracts"",""COLUMN_NAMES"":[""created_block_number"",""decimals"",""creator_address"",""address"",""created_tx_hash"",""symbol"",""name"",""created_block_timestamp""]},{""TABLE_NAME"":""dim_labels"",""COLUMN_NAMES"":[""address_name"",""label_subtype"",""label_type"",""address"",""blockchain"",""creator"",""project_name""]},{""TABLE_NAME"":""ez_decoded_event_logs"",""COLUMN_NAMES"":[""origin_to_address"",""origin_function_signature"",""event_removed"",""tx_hash"",""block_number"",""full_decoded_log"",""tx_status"",""contract_name"",""data"",""event_index"",""event_name"",""block_timestamp"",""origin_from_address"",""contract_address"",""decoded_log"",""topics""]},{""TABLE_NAME"":""ez_nft_transfers"",""COLUMN_NAMES"":[""event_type"",""tx_hash"",""project_name"",""block_number"",""nft_from_address"",""event_index"",""nft_to_address"",""nft_address"",""erc1155_value"",""tokenid"",""block_timestamp""]},{""TABLE_NAME"":""fact_blocks"",""COLUMN_NAMES"":[""blockchain"",""size"",""parent_hash"",""gas_limit"",""sha3_uncles"",""block_header_json"",""block_number"",""network"",""uncle_blocks"",""extra_data"",""block_timestamp"",""difficulty"",""receipts_root"",""total_difficulty"",""hash"",""gas_used"",""tx_count""]},{""TABLE_NAME"":""fact_decoded_event_logs"",""COLUMN_NAMES"":[""event_index"",""block_timestamp"",""decoded_log"",""tx_hash"",""event_name"",""contract_address"",""full_decoded_log"",""block_number""]},{""TABLE_NAME"":""fact_event_logs"",""COLUMN_NAMES"":[""tx_status"",""data"",""tx_hash"",""_log_id"",""event_index"",""block_timestamp"",""topics"",""block_number"",""event_removed"",""contract_address"",""origin_from_address"",""origin_to_address"",""origin_function_signature""]},{""TABLE_NAME"":""fact_hourly_token_prices"",""COLUMN_NAMES"":[""is_imputed"",""decimals"",""symbol"",""token_address"",""hour"",""price""]},{""TABLE_NAME"":""fact_token_transfers"",""COLUMN_NAMES"":[""to_address"",""block_timestamp"",""from_address"",""raw_amount"",""raw_amount_precise"",""origin_function_signature"",""origin_to_address"",""contract_address"",""_log_id"",""tx_hash"",""origin_from_address"",""block_number""]},{""TABLE_NAME"":""fact_traces"",""COLUMN_NAMES"":[""type"",""tx_hash"",""to_address"",""trace_index"",""block_number"",""gas"",""from_address"",""eth_value"",""eth_value_precise_raw"",""block_timestamp"",""data"",""trace_status"",""error_reason"",""eth_value_precise"",""input"",""sub_traces"",""identifier"",""output"",""gas_used"",""tx_status""]},{""TABLE_NAME"":""fact_transactions"",""COLUMN_NAMES"":[""cumulative_gas_used"",""tx_fee_precise"",""tx_fee"",""l1_gas_used"",""position"",""l1_fee"",""eth_value"",""input_data"",""block_hash"",""l1_gas_price"",""l1_fee_precise"",""v"",""gas_price"",""status"",""effective_gas_price"",""block_timestamp"",""l1_submission_details"",""nonce"",""eth_value_precise_raw"",""tx_hash"",""from_address"",""max_priority_fee_per_gas"",""eth_value_precise"",""gas_limit"",""block_number"",""origin_function_signature"",""l1_fee_scalar"",""r"",""gas_used"",""s"",""max_fee_per_gas"",""to_address""]}]

    Please respond to a user's question about the Base blockchain with a SQL query."
    """

    # Fine tuned GPT-3.5 model
    completion = openai.ChatCompletion.create(
        model="ft:gpt-3.5-turbo-0613:personal::7qa9UP0a",
        messages=[
            {"role": "system", "content": system_description},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    return completion.choices[0].message["content"]


# Query Flipside using their Python SDK
def query_flipside(sql):
    flipside = Flipside(FLIPSIDE_API_KEY, "https://api-v2.flipsidecrypto.xyz")
    results = flipside.query(sql)
    results_df = pd.DataFrame(results.rows, columns=results.columns).drop(
        columns=["__row_index"]
    )
    return results_df


# Generate Python Plot Chart Query
def create_chart(prompt):
    system_description = """
    Your task is to write Python code to make charts using Plotly Express for a local Pandas dataframe `st.session_state.df` based on the user's request.
    The code should be compatible with the Streamlit library, using st.plotly_chart() to render plots and st.write() to display output.
    """

    # General GPT-3.5 model
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_description},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
    )

    return completion.choices[0].message["content"]


# Initialize Session State
if "df" not in st.session_state:
    st.session_state["df"] = ""

col1, col2 = st.columns(2)

with col1:
    query_question = st.text_input(
        "(1) What Base blockchain data would you like to analyze?"
    )

    with st.expander("Example Query:"):
        txns = st.button("What are the total number of daily transactions on Base?")

    submit_query = st.button("Query Data")

    if submit_query or txns:
        if txns:
            query_question = "What are the total number of daily transactions on Base?"

        st.session_state.query = generate_sql(query_question)
        with st.expander("SQL Query"):
            st.code(st.session_state.query)

        with st.spinner("Querying Flipside..."):
            st.session_state.df = query_flipside(st.session_state.query)

        st.write("Query Results")
        st.table(st.session_state.df)

    elif isinstance(st.session_state.df, pd.DataFrame):
        st.table(st.session_state.df)

# Ask Question
with col2:
    # Analyze Data
    chart_question = st.text_input(
        "(2) Ask to create a chart based on the query results."
    )
    with st.expander("Example Chart:"):
        txn_bar = st.button(
            "Create a bar chart of the sum of total transactions by date."
        )
    submit_question = st.button("Make Chart")

    if submit_question or txn_bar:
        with st.spinner("Thinking..."):
            if txn_bar:
                chart_question = "Create a bar chart of the total transactions by date."

            st.session_state.chart_code = create_chart(chart_question)

            # Parse out python code
            if "```python" in st.session_state.chart_code:
                start = st.session_state.chart_code.find("```python") + len(
                    "```python\n"
                )
                end = st.session_state.chart_code.find("\n```", start)
                python_code = st.session_state.chart_code[start:end]
                with st.expander("Python Code"):
                    st.code(python_code)
                exec(python_code)

            # Determine if all response is python code
            elif st.session_state.chart_code.startswith("import"):
                with st.expander("Python Code"):
                    st.code(st.session_state.chart_code)
                exec(st.session_state.chart_code)

            # Otherwise, just print the response
            else:
                st.write(st.session_state.chart_code, unsafe_allow_html=True)
