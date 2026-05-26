import datetime
import json
import os
import requests
import streamlit as st
from dotenv import load_dotenv
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

# create an agent, with llm and tools

load_dotenv()
st.title("🤖 Agentic Tools Demo")
st.caption("This agent can fetch the current time, stock prices, and gold prices using tools!")
st.balloons()

# create llm
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

@tool
def get_system_time(query: str) -> str:
    """Returns the current system time. Use this for questions about 'now' or 'time'."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"The current system time is {now}."



@tool
def get_edgar_api(company_name: str) -> str:
    """
    Fetches company information from the SEC EDGAR API.
    Use this for company filings, CIK numbers, and financial data.
    """
    try:
        # Search for company by name
        search_url = "https://www.sec.gov/cgi-bin/browse-edgar"
        params = {
            "company": company_name,
            "owner": "exclude",
            "action": "getcompany"
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

        response = requests.get(search_url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse response to extract company info
        if "CIK" in response.text:
            lines = response.text.split('\n')
            for line in lines:
                if "CIK" in line and company_name.upper() in line.upper():
                    return f"Found company filing data for {company_name}. Check SEC EDGAR for detailed filings."

        return f"Company information for {company_name} retrieved from SEC EDGAR API."
    except Exception as e:
        return f"Error fetching EDGAR data: {str(e)}"

@tool
def get_stock_price(ticker: str) -> str:
    """
    Fetches live stock prices using Yahoo Finance.
    Use this for current stock prices, historical data, and market information.
    Pass the stock ticker symbol (e.g., 'AAPL', 'MSFT', 'GOOGL').
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")

        if data.empty:
            return f"No data found for ticker {ticker}"

        current_price = data['Close'].iloc[-1]
        open_price = data['Open'].iloc[0]
        high_price = data['High'].max()
        low_price = data['Low'].min()

        result = {
            "ticker": ticker,
            "current_price": round(current_price, 2),
            "open_price": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2)
        }

        return json.dumps(result)
    except Exception as e:
        return f"Error fetching stock price for {ticker}: {str(e)}"

@tool
def get_gold_price(query: str) -> str:
    """
    Fetches the current gold price using a public API.
    Use this for questions about the current price of gold.
    """
    try:
        url = "https://api.gold-api.com/price/XAU"

        response = requests.get(url)
        data = response.json()

        # Gold ounce price in USD
        gold_price_usd = data.get("price")

        if not gold_price_usd:
            return "Unable to fetch gold price."

        # Approx conversion
        usd_to_aed = 3.67

        # 1 troy ounce = 31.1035 grams
        price_per_gram_aed = (gold_price_usd / 31.1035) * usd_to_aed

        return (
            f"Current estimated UAE 24K gold rate is "
            f"{price_per_gram_aed:.2f} AED per gram."
        )

    except Exception as e:
        return f"Error fetching gold price: {str(e)}"



tools = [get_system_time, get_stock_price, get_edgar_api, get_gold_price]


# create an agent, with llm and tools
from langchain.agents import create_agent

agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt="You are a helpful assistant that uses tools to provide accurate info."
)


if __name__ == "__main__":


    # implement session state for streamlit
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])



    userprompt = st.chat_input("Ask anything about stock prices or the current time or general questions...")
    st.markdown(f"**User Prompt:** {userprompt}")
    st.session_state.messages.append({"role": "user", "content": userprompt})
    with st.chat_message("user"):
        st.markdown(userprompt)

    with st.chat_message("assistant"):  
        with st.status("Agent is thinking...", expanded=True) as status:
            if userprompt:
                inputs = {"messages": [("user", userprompt)]}
                try:
                    response = agent.invoke(inputs)
                    final_text = response["messages"][-1].content
                    st.session_state.messages.append({"role": "assistant", "content": final_text})

                except Exception as e:
                    status.update(label="Error occurred", state="error")
                    final_text = f"I encountered an error: {str(e)}"

                st.markdown(final_text)
                st.session_state.messages.append({"role": "assistant", "content": final_text})



 