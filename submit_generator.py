import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
import re
import base64
import pypandoc
from sqlalchemy import exists


class SubmitGenerator:
    def __init__(self):
        self.submit_json = []

    # Function: image generation
    def _image_generation(self, df, dest_path, sample):
        JPM_BLUE = '#1E3A8A'

        # get cols numa
        col_list = df.columns.tolist()

        fig, ax1 = plt.subplots(figsize=(12, 6))
        gradient = np.linspace(0.8, 0.3, len(df))
        ax1.bar(
            df['date'],
            df["revenue"],
            color=[plt.cm.Blues(g) for g in gradient],
            edgecolor=JPM_BLUE,
            linewidth=0.5,
            label="revenue"
        )

        ax2 = ax1.twinx()
        ax2.plot(
            df['date'],
            df["eps"],
            color=JPM_BLUE,
            marker='D',
            markersize=8,
            linestyle='--',
            linewidth=2,
            label="eps"
        )

        # setup professional format
        ax1.set_ylabel("revenue", fontsize=10, color=JPM_BLUE)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x / 1e6:,.0f}M"))
        ax1.tick_params(axis='y', colors=JPM_BLUE)

        ax2.set_ylabel("eps", fontsize=10, color=JPM_BLUE)
        ax2.spines['right'].set_color(JPM_BLUE)

        # Diagram Titles
        plt.title(
            f"Equity Research: Financial Highlights for revenue & eps",
            fontsize=12,
            pad=20,
            loc='left',
            color=JPM_BLUE,
            weight='bold'
        )

        plt.savefig(f'{dest_path}/{sample}_diagram.png', dpi=300, bbox_inches='tight')
        plt.close()

        # read the image and convert to base 64
        with open(f'{dest_path}/{sample}_diagram.png', "rb") as img_file:
            img_str = base64.b64encode(img_file.read()).decode("utf-8")
            return f'<img class="base64-image full-width" src="data:image/png;base64,{img_str}" alt="Embedded Image">'

    # Function: Export submission file
    def submit_json_export(self):
        if os.path.exists("Finturbo - Earnings2Insights Submission.json"):
            os.remove("Finturbo - Earnings2Insights Submission.json")

        with open("Finturbo - Earnings2Insights Submission.json", "w") as f:
            json.dump(self.submit_json, f, indent=2)
            f.close()
        print(f"Final Output Len: {len(self.submit_json)}")

    # Function: report finalization
    def Report_Process(self, sample):
        # *** Copy folder ***
        source_path = f"output/{sample}"
        dest_path = f"pro_output/{sample}"
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)
            shutil.copytree(source_path, dest_path)
        else:
            shutil.copytree(source_path, dest_path)

        # *** Read JSON file ***
        with open(dest_path + f"/{sample}_quant.json", "r") as f:
            json_string = json.load(f)  # 第一次解析，得到字符串
            data = json.loads(json_string)  # 第二次解析，得到字典
            f.close()

        financial_keys = ["financials", "financialData", "quarterlyFinancials","financial_data"]
        EPS_list = ["earningsPerShare","earnings_per_share"]
        revenue_list = ["revenue_millions"]

        # dataframe process
        if type(data) is list: # if save as list
            df = pd.DataFrame(data)
            for fi_key in df.columns:
                if fi_key in financial_keys:
                    financials_expanded = pd.json_normalize(df[fi_key])
                    df = pd.concat([df.drop(fi_key, axis=1), financials_expanded], axis=1)
        else: # if save as dict
            for fi_key in data.keys():
                if fi_key in financial_keys:
                    df = pd.DataFrame(data[fi_key])

        # revenue process - name alignment
        for item in df.columns.tolist():
            if item in revenue_list:
                df["revenue"] = df[item] * 1000000
                df.drop(item, axis=1, inplace=True)


        # period process - extract sub values
        if "period" in df.columns:
            financials_expanded = pd.json_normalize(df["period"])
            df = pd.concat([df.drop("period", axis=1), financials_expanded], axis=1)
        if "data" in df.columns:
            financials_expanded = pd.json_normalize(df["data"])
            df = pd.concat([df.drop("data", axis=1), financials_expanded], axis=1)

        # EPS processing - name alignment
        for item in df.columns.tolist():
            if item.strip() in EPS_list:
                df["eps"] = df[item]
                df.drop(item, axis=1, inplace=True)

        # data processing
        df["quarter"] = df["quarter"].apply(lambda x: "Q" + str(x))
        df["year"] = df["year"].apply(lambda x: str(x) + " ")
        df["date"] = df["year"] + df["quarter"]
        df["date"] = df["date"].apply(lambda x: x.replace("QQ", "Q"))
        df.drop(columns=["quarter", "year"], inplace=True)
        cols = df.columns.tolist()
        cols = [cols[-1]] + cols[:-1]
        df = df[cols]

        # save to json
        df.to_json(dest_path + f"/{sample}_quant.json", orient='records', indent=2)
        # convert to html
        df_html= df.to_html(index=False, justify='center',float_format='{:,.2f}'.format)
        base_64_img = self._image_generation(df, dest_path, sample)

        # *** Read Report ***
        with open(dest_path + f"/{sample}.md", "r", encoding="utf-8") as f:
            report = f.read()
        f.close()

        report = re.sub(r'^---\s*$', '', report, flags=re.MULTILINE)
        # 转义冒号
        report = report.replace(':', r'\:')


        # read the tpl file and save to local disk
        with open("src/finturbo.tpl", "r", encoding="utf-8") as f:
            template_content = f.read()
        f.close()
        processed_template = template_content.replace("<!-- TABLE_PLACEHOLDER -->", "\n"+df_html+"\n")
        processed_template = processed_template.replace("<!-- IMAGE_PLACEHOLDER -->", base_64_img+"\n")
        temp_template_path = f"{dest_path}/{sample}.tpl"
        with open(temp_template_path, "w", encoding="utf-8") as f:
            f.write(processed_template)
            f.close()

        # Export to HTML
        output = pypandoc.convert_text(
            report,
            to='html5',
            format='markdown',
            outputfile=f"{dest_path}/{sample}_pro.html",
            extra_args=[
                '--standalone',
                '--embed-resources',
                '--toc',
                f'--template={dest_path}/{sample}.tpl',
                '--citeproc',
                '--no-highlight'
            ]
        )

        # read the output html
        with open(f"{dest_path}/{sample}_pro.html", 'r', encoding='utf-8') as file:
            html_content = file.read()
        file.close()

        # inject to submit_dict
        data_inject = {"ECC": sample,"Report": html_content}
        self.submit_json.append(data_inject)
        print(f"### --> Completed for {sample}")


def main():
    # clear unexpected
    if os.path.exists("output/.DS_Store"):
        os.remove("output/.DS_Store")
    # initialize
    generator = SubmitGenerator()
    # file list
    file_list = os.listdir("output")
    # loop function
    for file in file_list:
        generator.Report_Process(file)

    # output the json file
    generator.submit_json_export()



if __name__ == "__main__":
    main()