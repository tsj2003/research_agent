import streamlit as st
import os
from datetime import datetime
import json
import re
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, save_tool

# Load environment variables
load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

def initialize_llm():
    """Initialize the Google Gemini LLM"""
    return ChatGoogleGenerativeAI(model="gemini-1.5-flash")

def create_research_agent():
    """Create the research agent with tools"""
    llm = initialize_llm()
    parser = PydanticOutputParser(pydantic_object=ResearchResponse)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use necessary tools. 
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]).partial(format_instructions=parser.get_format_instructions())

    tools = [search_tool, wiki_tool, save_tool]
    agent = create_tool_calling_agent(
        llm=llm,
        prompt=prompt,
        tools=tools
    )

    return AgentExecutor(agent=agent, tools=tools, verbose=False), parser

def parse_response(raw_response, parser):
    """Parse the agent response and extract structured data"""
    try:
        output_text = raw_response.get("output")
        if isinstance(output_text, str):
            json_match = re.search(r'\{.*\}', output_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return parser.parse(json_str)
        else:
            return parser.parse(output_text[0]["text"])
    except Exception as e:
        st.error(f"Error parsing response: {e}")
        return None

def main():
    # Page configuration
    st.set_page_config(
        page_title="AI Research Agent",
        page_icon="🔍",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .research-card {
        background: #1f2937;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        color: #ffffff;
    }
    .research-card h3 {
        color: #667eea;
        margin-bottom: 1rem;
    }
    .research-card p {
        color: #ffffff;
        line-height: 1.6;
    }
    .source-badge {
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    .tool-badge {
        background: #f3e5f5;
        color: #7b1fa2;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.2rem;
        display: inline-block;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    .stMarkdown {
        color: #333333 !important;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
        color: #333333 !important;
    }
    .stMarkdown p {
        color: #333333 !important;
    }
    .stTextInput > div > div > input {
        color: #333333 !important;
    }
    .stTextArea > div > div > textarea {
        color: #333333 !important;
    }
    .stSelectbox > div > div > select {
        color: #333333 !important;
    }
    .stMetric {
        color: #333333 !important;
    }
    .stMetric > div > div > div {
        color: #333333 !important;
    }
    .stAlert {
        color: #333333 !important;
    }
    .stSuccess {
        color: #333333 !important;
    }
    .stError {
        color: #333333 !important;
    }
    .stWarning {
        color: #333333 !important;
    }
    .stInfo {
        color: #333333 !important;
    }
    .stButton > button {
        color: white !important;
    }
    .stDownloadButton > button {
        color: white !important;
    }
    /* Force all text to be dark except main page */
    * {
        color: #333333 !important;
    }
    /* Exception for buttons and specific elements */
    .stButton > button, .stDownloadButton > button, .main-header, .main-header * {
        color: white !important;
    }
    /* Main page text should be white on dark background */
    .main .stMarkdown, .main .stMarkdown * {
        color: #ffffff !important;
    }
    .main .stText, .main .stText * {
        color: #ffffff !important;
    }
    .main .stAlert, .main .stAlert * {
        color: #ffffff !important;
    }
    .main .stSuccess, .main .stSuccess * {
        color: #10b981 !important;
    }
    .main .stWarning, .main .stWarning * {
        color: #f59e0b !important;
    }
    .main .stError, .main .stError * {
        color: #ef4444 !important;
    }
    .main .stInfo, .main .stInfo * {
        color: #3b82f6 !important;
    }
    .main h1, .main h2, .main h3, .main h4, .main h5, .main h6 {
        color: #ffffff !important;
    }
    .main p {
        color: #ffffff !important;
    }
    .main ul, .main ol, .main li {
        color: #ffffff !important;
    }
    /* Ensure sidebar text is visible */
    .css-1d391kg, .css-1v0mbdj, .css-1v0mbdj * {
        color: #ffffff !important;
    }
    /* Sidebar specific styling */
    .css-1d391kg {
        color: #ffffff !important;
    }
    .css-1d391kg * {
        color: #ffffff !important;
    }
    /* Sidebar text elements */
    .stSidebar .stMarkdown, .stSidebar .stMarkdown * {
        color: #ffffff !important;
    }
    .stSidebar .stText, .stSidebar .stText * {
        color: #ffffff !important;
    }
    .stSidebar .stAlert, .stSidebar .stAlert * {
        color: #ffffff !important;
    }
    .stSidebar .stSuccess, .stSidebar .stSuccess * {
        color: #ffffff !important;
    }
    .stSidebar .stWarning, .stSidebar .stWarning * {
        color: #ffffff !important;
    }
    .stSidebar .stInfo, .stSidebar .stInfo * {
        color: #ffffff !important;
    }
    .stSidebar .stError, .stSidebar .stError * {
        color: #ffffff !important;
    }
    /* Sidebar input fields */
    .stSidebar .stTextInput > div > div > input {
        color: #333333 !important;
        background-color: #ffffff !important;
    }
    .stSidebar .stTextArea > div > div > textarea {
        color: #333333 !important;
        background-color: #ffffff !important;
    }
    /* Sidebar headers */
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar h4, .stSidebar h5, .stSidebar h6 {
        color: #ffffff !important;
    }
    /* Sidebar paragraphs */
    .stSidebar p {
        color: #ffffff !important;
    }
    /* Sidebar lists */
    .stSidebar ul, .stSidebar ol, .stSidebar li {
        color: #ffffff !important;
    }
    /* Force Streamlit text elements */
    .stText, .stText * {
        color: #333333 !important;
    }
    .stMarkdown, .stMarkdown * {
        color: #333333 !important;
    }
    /* Override Streamlit's dark theme for sidebar */
    .stSidebar {
        background-color: #262730 !important;
    }
    .stSidebar .stMarkdown {
        color: #ffffff !important;
    }
    .stSidebar .stMarkdown h1, .stSidebar .stMarkdown h2, .stSidebar .stMarkdown h3, 
    .stSidebar .stMarkdown h4, .stSidebar .stMarkdown h5, .stSidebar .stMarkdown h6 {
        color: #ffffff !important;
    }
    .stSidebar .stMarkdown p {
        color: #ffffff !important;
    }
    .stSidebar .stMarkdown ul, .stSidebar .stMarkdown ol, .stSidebar .stMarkdown li {
        color: #ffffff !important;
    }
    /* Sidebar success/error messages */
    .stSidebar .stSuccess {
        background-color: #1f2937 !important;
        color: #10b981 !important;
    }
    .stSidebar .stWarning {
        background-color: #1f2937 !important;
        color: #f59e0b !important;
    }
    .stSidebar .stError {
        background-color: #1f2937 !important;
        color: #ef4444 !important;
    }
    .stSidebar .stInfo {
        background-color: #1f2937 !important;
        color: #3b82f6 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🔍 AI Research Agent</h1>
        <p>Powered by Google Gemini • Multi-Source Research • Automated Analysis</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # API Key input
        api_key = st.text_input(
            "Google API Key",
            value=os.getenv("GOOGLE_API_KEY", ""),
            type="password",
            help="Enter your Google Gemini API key"
        )
        
        if api_key:
            os.environ["GOOGLE_API_KEY"] = api_key
            st.success("✅ API Key configured")
        else:
            st.warning("⚠️ Please enter your API key")
        
        st.markdown("---")
        
        # Features
        st.header("🚀 Features")
        st.markdown("""
        - **Wikipedia Search** - Academic information
        - **Web Search** - Current information
        - **AI Analysis** - Intelligent summarization
        - **Auto-Save** - Results stored locally
        - **Structured Output** - Clean, organized data
        """)
        
        st.markdown("---")
        
        # Instructions
        st.header("📝 How to Use")
        st.markdown("""
        1. Enter your research topic
        2. Click 'Research Now'
        3. View structured results
        4. Download or save findings
        """)

    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🎯 Research Topic")
        
        # Research input
        research_topic = st.text_input(
            "What would you like to research?",
            placeholder="e.g., Artificial Intelligence, Climate Change, Quantum Computing...",
            help="Enter any topic you'd like to research"
        )
        
        # Research button
        if st.button("🔍 Research Now", type="primary", use_container_width=True):
            if not api_key:
                st.error("Please enter your Google API key in the sidebar")
            elif not research_topic:
                st.error("Please enter a research topic")
            else:
                with st.spinner("🔍 Conducting research... This may take a moment"):
                    try:
                        # Initialize agent
                        agent_executor, parser = create_research_agent()
                        
                        # Run research
                        raw_response = agent_executor.invoke({"query": research_topic})
                        
                        # Parse response
                        structured_response = parse_response(raw_response, parser)
                        
                        if structured_response:
                            # Store in session state
                            st.session_state.research_result = structured_response
                            st.session_state.research_topic = research_topic
                            
                            # Save to file
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
                            
                            st.success("✅ Research completed successfully!")
                            st.rerun()
                        else:
                            st.error("Failed to parse research results")
                            
                    except Exception as e:
                        st.error(f"Research failed: {str(e)}")
    
    with col2:
        st.header("📊 Quick Stats")
        
        if 'research_result' in st.session_state:
            result = st.session_state.research_result
            
            st.metric("Topic", result.topic)
            st.metric("Sources", len(result.sources))
            st.metric("Tools Used", len(result.tools_used))
            
            # Word count
            word_count = len(result.summary.split())
            st.metric("Summary Length", f"{word_count} words")
        else:
            st.info("Run a research to see stats")

    # Display results
    if 'research_result' in st.session_state:
        st.markdown("---")
        st.header("📋 Research Results")
        
        result = st.session_state.research_result
        
        # Research card
        st.markdown(f"""
        <div class="research-card">
            <h3>🎯 {result.topic}</h3>
            <p><strong style="color: #667eea;">Summary:</strong></p>
            <p style="color: #ffffff; font-size: 16px; line-height: 1.6;">{result.summary}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sources and tools
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📚 Sources")
            for source in result.sources:
                st.markdown(f'<span class="source-badge">{source}</span>', unsafe_allow_html=True)
        
        with col2:
            st.subheader("🛠️ Tools Used")
            for tool in result.tools_used:
                st.markdown(f'<span class="tool-badge">{tool}</span>', unsafe_allow_html=True)
        
        # Download section
        st.markdown("---")
        st.header("💾 Download Results")
        
        # Create downloadable content
        download_content = f"""
# Research Report: {result.topic}

**Generated on:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary
{result.summary}

## Sources
{chr(10).join([f"- {source}" for source in result.sources])}

## Tools Used
{chr(10).join([f"- {tool}" for tool in result.tools_used])}

---
*Generated by AI Research Agent*
"""
        
        st.download_button(
            label="📥 Download as Markdown",
            data=download_content,
            file_name=f"research_{result.topic.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown"
        )
        
        # JSON download
        json_data = {
            "topic": result.topic,
            "summary": result.summary,
            "sources": result.sources,
            "tools_used": result.tools_used,
            "timestamp": datetime.now().isoformat()
        }
        
        st.download_button(
            label="📥 Download as JSON",
            data=json.dumps(json_data, indent=2),
            file_name=f"research_{result.topic.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🤖 AI Research Agent • Built with Streamlit & Google Gemini</p>
        <p>💡 Perfect for academic research, content creation, and knowledge discovery</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
