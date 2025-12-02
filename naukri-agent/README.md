# Naukri AI Agent

This agent automates the process of searching for jobs on Naukri.com and tailoring your resume for each job application.

## Features
-   **Automated Login**: Logs into Naukri.com (supports manual CAPTCHA solving).
-   **Job Search**: Searches for jobs based on keywords in `config.py`.
-   **Resume Tailoring**: Uses Google Gemini AI to rewrite your LaTeX resume (`main.tex`) to match the Job Description.
-   **Output**: Generates a tailored `.tex` file for each relevant job found.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Credentials**:
    -   Rename `.env.example` to `.env`.
    -   Open `.env` and fill in your details:
        ```env
        NAUKRI_USERNAME=your_email@naukri.com
        NAUKRI_PASSWORD=your_password
        GEMINI_API_KEY=your_gemini_api_key
        ```
    -   *Note: You can get a free Gemini API key from [Google AI Studio](https://aistudio.google.com/).*

3.  **Customize Search**:
    -   Edit `config.py` to change `KEYWORDS`, `LOCATION`, or `EXPERIENCE`.

## Usage

Run the agent:
```bash
python main.py
```

The agent will:
1.  Open a Chrome browser.
2.  Log in to Naukri (you may need to solve a CAPTCHA manually).
3.  Search for jobs.
4.  For each job, it will extract the description and generate a new `tailored_resume_X.tex` in the `output/` folder.

## Limitations
-   **PDF Compilation**: The agent currently generates `.tex` files. You need to compile them to PDF manually (e.g., using Overleaf or a local LaTeX installation) before applying.
-   **Anti-Bot**: Naukri may block automated access. Use with caution.
