# 🧪 ResearchLab AI

ResearchLab AI is an autonomous research assistant for the education domain. It helps users explore student performance questions by planning a study, analyzing real data, surfacing contradictions, and generating a structured research report grounded in computed statistics.

## Overview

This project turns a natural-language question into a research workflow:

1. It identifies the most relevant variables and research direction.
2. It analyzes student performance data using statistical checks and summaries.
3. It detects contradictions or shifts in the leading group across subjects.
4. It produces a narrative report with findings, limitations, and hypotheses.

The app is designed to keep outputs evidence-based by basing the narrative on Python-generated metrics rather than freeform assumptions.

## Key Features

- Research planning from user questions
- Statistical analysis of student performance data
- Contradiction detection across math, reading, and writing outcomes
- Structured report generation with findings and caveats
- Interactive Streamlit interface
- Groq-powered language workflow for planning and report writing

## Tech Stack

- Python
- Streamlit
- LangGraph
- Groq API
- Pandas
- SciPy
- Plotly

## Installation

Clone the repository and set up a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with your Groq credentials:

```env
GROQ_API_KEY=your_key_here
GROQ_MODEL=openai/gpt-oss-120b
```

You can also export the variables directly in your shell if preferred.

## Running the App

Start the Streamlit app:

```bash
streamlit run app.py
```

## Project Structure

- `app.py` — Streamlit user interface
- `graph.py` — LangGraph orchestration logic
- `planner.py` — question-to-plan logic
- `analysis_tools.py` — data analysis and contradiction detection functions
- `reporter.py` — report generation
- `data/students.csv` — student performance dataset used for analysis
- `requirements.txt` — Python dependencies

## Data Source

The project uses a student performance dataset inspired by publicly available education datasets and adapted for research-style analysis in the repository.

## Contributors

### Foundational Developer
- Hadeed Ahsan (Project Leader)
### Refinements
- Kiran Shams
- Mahnoor Fatima
### Documentation
- Aima Muzammil
### Presentation
- Alishba Ishrat

### Community Contributions

Contributions are welcome. If you would like to contribute, please open an issue or submit a pull request.

## Contributing

We welcome improvements, bug fixes, documentation updates, and feature ideas.

Suggested workflow:

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Run the relevant checks and validations.
5. Open a pull request with a clear description.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Roadmap

Potential next steps include:

- Better model configuration controls
- More advanced statistical tests
- Exporting reports to PDF or Markdown
- Additional educational datasets and domains
- Improved research workflow validation and QA

## Contact

For questions or collaboration inquiries, please reach out through the repository issues or contact the maintainer via the project profile associated with this repo.
