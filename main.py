import os
import shutil
import json
from src.multiagents import multi_agents_flow
import asyncio


os.environ["TOKENIZERS_PARALLELISM"] = "false" # for MAC OS


# model engage
highlights_model = {
    "model": "gemini-2.5-flash",
    "apikey": ""}
writer_moddel = {
    "model": "gemini-2.5-pro",
    "apikey": ""}


if __name__ == "__main__":

    file_list = [] # input folder name

    for sample in file_list:

        # File path
        output_path = f"output/{sample}"
        if os.path.exists(output_path):
            shutil.rmtree(output_path)
            os.mkdir(output_path)
        else:
            os.mkdir(output_path)
        # get basic info
        company, quarter, year = sample.split("_")
        agent_flow = multi_agents_flow(company=company,
                                       quarter=quarter,
                                       year=int(year),
                                       highlights_model=highlights_model,
                                       writer_moddel=writer_moddel)
        # run the rag create
        asyncio.run(agent_flow.rag_create())
        # get financial data
        agent_eps = asyncio.run(agent_flow.chart_data_generator())
        # save to locals
        json_raw = agent_eps.messages[-1].content
        json_raw = json_raw.replace("```json\n", "").replace("```", "")
        with open(f"{output_path}/{sample}_quant.json", "w", encoding="utf-8") as f:
            json.dump(json_raw, f)
        # get report
        agent_report = asyncio.run(agent_flow.report_generator(json_raw))
        # save to locals
        investment_report = agent_report.messages[-1].content
        with open(f"{output_path}/{sample}.md", 'w', encoding='utf-8') as f:
            f.write(investment_report)
        print(f"#### -- Completed for {sample}")