from autogen_core.models import ModelInfo
from src.ragindexer import autogen_rag_indexer
import os
from pathlib import Path
from autogen_ext.memory.chromadb import ChromaDBVectorMemory, PersistentChromaDBVectorMemoryConfig
from autogen_ext.models.ollama import OllamaChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import DiGraphBuilder, GraphFlow
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient


# Class Multi-Agents Workflow (Auto-Gen)
class multi_agents_flow:
    def __init__(self,company, year, quarter, highlights_model, writer_moddel):
            self.company = company
            self.year = year
            self.quarter = quarter
            self.client = OpenAIChatCompletionClient(
                model = writer_moddel["model"],
                api_key = writer_moddel["apikey"],
                model_info = ModelInfo(vision=True,function_calling=True,json_output=True,
                                     family="gemini",structured_output=True,multiple_system_messages=True))

            self. summary_client = OpenAIChatCompletionClient(
                model = highlights_model["model"],
                api_key = highlights_model["apikey"],
                model_info = ModelInfo(vision=True,function_calling=True,json_output=True,
                                     family="gemini",structured_output=True,multiple_system_messages=True))


            # self.client = OllamaChatCompletionClient(model="gemma3:4b")  #    deepseek-r1:1.5b; gemma3:4b

    # Function: Create RAG info
    async def rag_create(self):
        # === prepare RAG - main transcript
        self.rag_transcript = ChromaDBVectorMemory(
            config=PersistentChromaDBVectorMemoryConfig(
                collection_name="earnings_transcript",
                persistence_path=os.path.join(str(Path.home()), ".chromadb_autogen_1"),
                k=4,  # Return top 3 results
                score_threshold=0.5,  # Minimum similarity score
            )
        )
        await self.rag_transcript.clear()  # Clear existing memory
        # load document to RAG
        async def index_autogen_docs() -> None:
            indexer = autogen_rag_indexer(memory=self.rag_transcript)
            sources = [f"raw_data/aggregate/{self.company}_{self.quarter}_{self.year}/source/source.md",]
            chunks: int = await indexer.index_documents(sources)
            print(f"Indexed {chunks} chunks from {len(sources)} AutoGen documents")
        await index_autogen_docs()



        # === prepare RAG - past quarters
        self.rag_suppliment = ChromaDBVectorMemory(
            config=PersistentChromaDBVectorMemoryConfig(
                collection_name="suppliments",
                persistence_path=os.path.join(str(Path.home()), ".chromadb_autogen_2"),
                k=3,  # Return top 3 results
                score_threshold=0.5,  # Minimum similarity score
            )
        )
        await self.rag_suppliment.clear()  # Clear existing memory
        # load document to RAG
        async def index_autogen_docs() -> None:
            indexer = autogen_rag_indexer(memory=self.rag_suppliment)

            if self.quarter == "q1":
                sources = [f"raw_data/aggregate/{self.company}_q4_{str(int(self.year-1))}/source/source.md",
                           f"raw_data/aggregate/{self.company}_q3_{str(int(self.year - 1))}/source/source.md",
                           f"raw_data/aggregate/{self.company}_q2_{str(int(self.year - 1))}/source/source.md",]
            elif self.quarter == "q2":
                sources = [f"raw_data/aggregate/{self.company}_q2_{self.year}/source/source.md",
                           f"raw_data/aggregate/{self.company}_q4_{str(int(self.year - 1))}/source/source.md",
                           f"raw_data/aggregate/{self.company}_q3_{str(int(self.year - 1))}/source/source.md",]
            elif self.quarter == "q3":
                sources = [f"raw_data/aggregate/{self.company}_q2_{self.year}/source/source.md",
                           f"raw_data/aggregate/{self.company}_q1_{self.year}/source/source.md",
                           f"raw_data/aggregate/{self.company}_q4_{str(int(self.year - 1))}/source/source.md",]
            else:
                sources = [f"raw_data/aggregate/{self.company}_q3_{self.year}/source/source.md",
                           f"raw_data/aggregate/{self.company}_q2_{self.year}/source/source.md",
                           f"raw_data/aggregate/{self.company}_q1_{self.year}/source/source.md",]
            chunks: int = await indexer.index_documents(sources)
            print(f"Indexed {chunks} chunks from {len(sources)} AutoGen documents")
        await index_autogen_docs()


        # === prepare RAG - ref
        self.rag_ref = ChromaDBVectorMemory(
            config=PersistentChromaDBVectorMemoryConfig(
                collection_name="ref",
                persistence_path=os.path.join(str(Path.home()), ".chromadb_autogen_3"),
                k=3,  # Return top 3 results
                score_threshold=0.5,  # Minimum similarity score
            )
        )
        await self.rag_ref.clear()  # Clear existing memory
        # load document to RAG
        async def index_autogen_docs() -> None:
            indexer = autogen_rag_indexer(memory=self.rag_ref)

            if self.quarter == "q1":
                sources = [f"raw_data/aggregate/{self.company}_q4_{str(int(self.year - 1))}/ref/ref.md",
                           f"raw_data/aggregate/{self.company}_q3_{str(int(self.year - 1))}/ref/ref.md",
                           f"raw_data/aggregate/{self.company}_q2_{str(int(self.year - 1))}/ref/ref.md",
                           f"raw_data/aggregate/{self.company}_{self.quarter}_{self.year}/ref/ref.md"]
            elif self.quarter == "q2":
                sources = [f"raw_data/aggregate/{self.company}_q2_{self.year}/ref/ref.md",
                           f"raw_data/aggregate/{self.company}_q4_{str(int(self.year - 1))}/ref/ref.md",
                           f"raw_data/aggregate/{self.company}_q3_{str(int(self.year - 1))}/ref/ref.md",
                           f"raw_data/aggregate/{self.company}_{self.quarter}_{self.year}/ref/ref.md"]
            elif self.quarter == "q3":
                sources = [f"raw_data/aggregate/{self.company}_q2_{self.year}/ref/ref.md",
                           f"raw_data/aggregate/{self.company}_q1_{self.year}/ref/ref.md",
                           f"raw_data/aggregate/{self.company}_q4_{str(int(self.year - 1))}/ref/ref.md",
                           f"raw_data/aggregate/{self.company}_{self.quarter}_{self.year}/ref/ref.md"]
            else:
                sources = [f"raw_data/aggregate/{self.company}_q3_{self.year}/ref/ref.md",
                           f"raw_data/aggregate/{self.company}_q2_{self.year}/ref/ref.md",
                           f"raw_data/aggregate/{self.company}_q1_{self.year}/ref/ref.md",
                           f"raw_data/aggregate/{self.company}_{self.quarter}_{self.year}/ref/ref.md"]
            chunks: int = await indexer.index_documents(sources)
            print(f"Indexed {chunks} chunks from {len(sources)} AutoGen documents")
        await index_autogen_docs()

    # Function: Report Generation Workflow
    async def report_generator(self, chart_data):

        # ***** report_writier qgent *****
        report_writier = AssistantAgent(
            "report_writier",
            model_client=self.client,
            memory=[self.rag_transcript, self.rag_ref, self.rag_suppliment],
            system_message="You are a senior equity research analyst. Draft an official, in-depth "
                           "and detailed Investment research report based on the past 4 quarters' earnings calls "
                           "transcripts. The report should have below sections written in professional "
                           "institutional tone with references in markdown. Also gives you the financial "
                           f"data summary for your writing. {str(chart_data)}. [ATTENTION] Please STRICTLY "
                           f"follow below report structure to generate. highlights_agent info is just for reference.: "
                           f"for the complete report.: "
                           "Title: Investment Research Report - [Company] [Quarter] [Year] "
                           "1. **Executive Summary**: Stock rating (Buy/Hold/Sell), target price, and 3–5 key "
                           "investment highlights. "
                           "2. **Investment Thesis**: Deep and detailed analysis of company positioning, strategy, "
                           "competitive edge, and attractiveness to institutional investors and statement the logics "
                           "for whether it is recommended to invest. Please be onjective"
                           "3. **Financials**: EPS, revenue, margins. Show YoY / QoQ trends, highlight surprises vs"
                           " consensus. And give financial highlights."
                           "4. **Valuation**: Provide valuation using PE, DCF or EV/EBITDA. Explain assumptions, "
                           "derive price target. Based on valuation result, give in-depth analysis for investment "
                           "recommendation (whether or not)."
                           "5. **Catalyst Outlook**: Discuss near-/mid-term drivers: product launches, macro factors, "
                           "regulatory shifts. And provide logic analysis for future investment on this company."
                           "6. **Risks**: Highlight key risks—macro, regulatory, execution—and their "
                           "impact on valuation/growth. ")


        # **** summary agent *****
        highlights_agent = AssistantAgent(
            "highlights_agent",
            model_client=self.summary_client,
            memory=[self.rag_transcript, self.rag_suppliment],
            system_message= "you are a research analyst that needs to extract key insights from earnings calls from "
                            f"current year quarter {self.year} {self.quarter} as well as past 3 quarters for "
                            f"{self.company}. Please focus on below key deliveries:"
                            f"1. Financial Trends (highlight changes vs. prior quarters). "
                            f"2. Strategic Shifts – New initiatives, investments, or changes in business priorities."
                            f"3. Operational Updates – Key operational strengths/weaknesses (e.g., supply chain, "
                            f"costs, demand trends)."
                            f"4. Management Tone – Confidence, caution, or notable changes in language."
                            f"5. Forward Guidance – Revisions to outlook, key risks, or opportunities mentioned. "
                            f"The output should be 3 bullet points per above focus area and needs to be neutral "
                            f"and objective."


        )

        # ***** content_editor agent *****
        content_editor = AssistantAgent(
            "content_editor",
            model_client=self.client,
            memory=[self.rag_transcript, self.rag_ref, self.rag_suppliment],
            system_message = "You are a senior equity research editor and reviewer. Your task is to edit the "
                             "report for grammar and content accuracy including claims, numbers and arguments needed to  "
                             " be supported by the source transcripts and are logically written. please strictly follow"
                             "the structure to have the sections: Executive Summary, Investment Thesis, Financials,"
                             " Valuation, Catalyst Outlook, Risks."
                             " return the edited FULL report based on the original report.")


        # ***** content_editor agent *****
        styling_editor = AssistantAgent(
            "styling_editor",
            model_client=self.client,
            memory=[self.rag_transcript, self.rag_ref, self.rag_suppliment],
            system_message = "You are a senior equity research editor and reviewer. Your task is to edit the "
                             "report for Financial institutional style for research report and please strictly follow"
                             "the structure to have the sections: Executive Summary, Investment Thesis, Financials,"
                             " Valuation, Catalyst Outlook, Risks."
                             "Only Return the edited FULL report based on the original report. ")


        # Build the workflow graph
        builder = DiGraphBuilder()
        builder.add_node(highlights_agent).add_node(report_writier).add_node(content_editor).add_node(styling_editor)

        # Fan-out from writer to editor1 and editor2
        builder.add_edge(highlights_agent, report_writier)
        builder.add_edge(highlights_agent, content_editor)
        builder.add_edge(report_writier, content_editor)
        builder.add_edge(report_writier, styling_editor)
        builder.add_edge(content_editor, styling_editor)

        # Build and validate the graph
        graph = builder.build()

        # Create the flow
        flow = GraphFlow(
            participants=builder.get_participants(),
            graph=graph,
        )

        # Run the workflow
        report = await Console(flow.run_stream(task="Write a investment guide research report for "
                                            f"{self.company}, focusing on {self.quarter} {self.year} earnings. please "
                                                    f"strictly follow the structure to have the sections: Executive "
                                                    f"Summary, Investment Thesis, Financials, Valuation, Catalyst "
                                                    f"Outlook, Risks."))


        self.report = report.messages[-2].content

        return report

    # Function: Chart Data Generation Agent
    async def chart_data_generator(self):
        data_agent = AssistantAgent(
            "data_agent",
            model_client=self.client,
            memory=[self.rag_ref],
            system_message=f"Please generate {self.quarter} {self.year} together with its past 3 quarters financial "
                           f"numerical data in JSON format with (quarter, year) and corresponding numbers. Just return "
                           f"the JSON")


        # run agent
        data_js = await data_agent.run(task=f"generate the JSON for me.")

        return data_js