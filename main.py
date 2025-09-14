from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool

load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]
    

# llm = ChatAnthropic(model="claude-3-5-sonnet-20241022")
# llm = ChatOpenAI(model="gpt-3.5-turbo")
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use neccessary tools. 
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

tools = [search_tool, wiki_tool, save_tool]
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
query = input("What can i help you research? ")
raw_response = agent_executor.invoke({"query": query})

try:
    # Extract the JSON from the response
    output_text = raw_response.get("output")
    if isinstance(output_text, str):
        # Try to find JSON in the output
        import re
        json_match = re.search(r'\{.*\}', output_text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            structured_response = parser.parse(json_str)
            print(structured_response)
            
            # Save the research results to file
            print("\n💾 Saving research results...")
            research_data = f"""
Research Topic: {structured_response.topic}

SUMMARY:
{structured_response.summary}

SOURCES:
{', '.join(structured_response.sources)}

TOOLS USED:
{', '.join(structured_response.tools_used)}
"""
            save_result = save_tool.run(research_data)
            print(f"✅ {save_result}")
            
        else:
            print("No JSON found in output:", output_text)
    else:
        structured_response = parser.parse(output_text[0]["text"])
        print(structured_response)
        
        # Save the research results to file
        print("\n💾 Saving research results...")
        research_data = f"""
Research Topic: {structured_response.topic}

SUMMARY:
{structured_response.summary}

SOURCES:
{', '.join(structured_response.sources)}

TOOLS USED:
{', '.join(structured_response.tools_used)}
"""
        save_result = save_tool.run(research_data)
        print(f"✅ {save_result}")
        
except Exception as e:
    print("Error parsing response", e, "Raw Response - ", raw_response)