"""
llm_repl.py: LangChain-powered REPL for jlistings tools

- Loads OpenAI API key from OPENAI_JLISTINGS_API_KEY
- Registers scrape_tool (and later enrich/persist) as LangChain tools
- Accepts user input, routes to LLM agent, prints results
"""
import os
import warnings
import argparse
warnings.filterwarnings("ignore", category=UserWarning, module="langsmith.client")

from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain import hub
from tools.langchain_tools import scrape_tool

api_key = os.environ.get("OPENAI_JLISTINGS_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_JLISTINGS_API_KEY not set in environment.")

llm = ChatOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo", temperature=0)

tools = [
    scrape_tool,
    # Add enrich_tool and persist_tool here when ready
]

prompt = hub.pull("hwchase17/openai-functions-agent")

agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def main():
    parser = argparse.ArgumentParser(description="jlistings LLM REPL")
    parser.add_argument('-e', '--execute', type=str, help='Run a single command as the first input')
    parser.add_argument('--one-shot', action='store_true', help='Exit after running the first command')
    args = parser.parse_args()

    print("Welcome to the jlistings LLM REPL! Type 'exit' to quit.")
    try:
        first_command = args.execute
        ran_first = False
        while True:
            if first_command and not ran_first:
                user_input = first_command
                ran_first = True
            else:
                user_input = input("\n> ")
            if user_input.strip().lower() in ("exit", "quit"): break
            try:
                result = agent_executor.invoke({"input": user_input})
                print(f"\n{result['output']}")
            except Exception as e:
                if "insufficient_quota" in str(e) or "quota" in str(e).lower():
                    print("\n[ERROR] Your OpenAI API key has exceeded its quota or does not have sufficient billing enabled.")
                    print("Please visit https://platform.openai.com/settings/organization/billing/overview to recharge your account or check your billing status.")
                    break
                else:
                    print(f"\n[ERROR] {e}")
            if args.one_shot:
                break
    except KeyboardInterrupt:
        print("\nExiting jlistings LLM REPL. Goodbye!")

if __name__ == "__main__":
    main()
