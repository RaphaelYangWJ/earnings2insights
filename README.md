# Earnings Insight

Earnings Insight is a project focused on generating structured investment reports from earnings call transcripts. The goal of the project is to leverage advanced natural language processing (NLP) models to analyze earnings calls and produce actionable insights for investors.

## Features

- **Automated report generation**: Use large language models (LLMs) to generate investment research reports based on earnings call data.
- **Multi-agent system**: The architecture consists of multiple agents (e.g., highlight summarizer, content writer, report reviewer, etc.) working together to produce high-quality reports.
- **Customizable financial analysis**: Incorporate key financial metrics such as EPS, revenue, expenses, and operational trends to provide detailed investment insights.
- **Data enrichment**: Enhance the analysis with external data sources using Retrieval-Augmented Generation (RAG) to improve the accuracy and richness of the reports.

## Installation

To run this project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/EarningsInsight.git
   cd EarningsInsight
````

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the environment:

   * Ensure that you have the necessary API keys and credentials to access financial data.
   * Configure any external data sources or models (e.g., Google Gemini-Pro, Qwen2.5).

## Usage

### 1. Data Input:

* You can input earnings call transcripts in various formats (e.g., text, CSV, JSON) into the system for analysis.

### 2. Report Generation:

* Use the script `generate_report.py` to process the earnings call transcripts and generate a structured investment report:

  ```bash
  python generate_report.py --input_path path/to/transcripts --output_path path/to/save/report
  ```

### 3. Evaluation:

* After generating the reports, you can evaluate them using built-in evaluation scripts to measure clarity, logic, persuasiveness, readability, and usefulness.

## Example Output

A sample generated report from the system includes key sections such as:

* **Executive Summary**: High-level analysis and stock rating.
* **Investment Thesis**: In-depth evaluation of the company’s positioning and strategy.
* **Financial Analysis**: Detailed examination of the company's financial metrics, including EPS, revenue, and operational updates.
* **Valuation**: Valuation using financial metrics like PE ratio or EV/EBITDA.
* **Risks and Opportunities**: Key risks and potential investment opportunities.

### Sample JSON Data

The system processes the following structure for input data:

```json
{
  "company": "XYZ Corp.",
  "quarter": "Q1 2025",
  "financials": {
    "EPS": 1.25,
    "Revenue": 50000000,
    "Expenses": 20000000
  },
  "highlights": [
    {"financial_trend": "EPS increased by 10% compared to Q4 2024"},
    {"strategic_shift": "New investment in AI technology"},
    {"management_tone": "Optimistic outlook for the next quarter"}
  ]
}
```

## Contributors

* **Weijie Yang** – University of California, Berkeley ([raphaelyang1998@berkeley.edu](mailto:raphaelyang1998@berkeley.edu))
* **Junbo Peng, Ph.D** – Georgia Institute of Technology ([pjbustc@gmail.com](mailto:pjbustc@gmail.com))
* **Xinyun Rong** – University of California, Berkeley ([roxyrong@berkeley.edu](mailto:roxyrong@berkeley.edu))

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

We would like to thank the organizers of the FinEval Shared Task for providing the dataset and evaluation framework, as well as the developers of the AutoGen framework for enabling the multi-agent architecture.
