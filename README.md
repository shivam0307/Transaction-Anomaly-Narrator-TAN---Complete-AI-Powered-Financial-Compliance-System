[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tan14092025aiagent.streamlit.app/)

# 🤖 Transaction Anomaly Narrator (TAN)

TAN is an AI-powered tool to detect and explain anomalies in financial transactions. It uses a set of rules to flag suspicious activity and leverages a Large Language Model (LLM) to generate clear, human-readable narratives for each anomaly.

![Screenshot of the TAN Streamlit app interface](https://i.postimg.cc/3xGjbR4j/TAN-preview.png)

---

## ✨ Features

- **Rule-Based Detection:** Identifies anomalies based on high value, odd hours, foreign location, and high velocity.
- **AI-Powered Narratives:** Uses Google's Gemini model to generate concise explanations for why a transaction was flagged.
- **Interactive UI:** A simple web interface built with Streamlit to upload data and view results.
- **PDF Reporting:** Automatically generates a detailed PDF incident report for each detected anomaly.

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.8+
- An API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd tan_project
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Set up your API key:**
    - Create a file named `.env` in the root of the project folder.
    - Add your Google Gemini API key to it like this:
      ```
      GEMINI_API_KEY="YOUR_API_KEY_HERE"
      ```

---

## 💻 How to Run

You can run the project in two ways:

1.  **Command-Line (for batch processing):**
    This will process the input file and generate reports in the `data/reports` folder.
    ```bash
    python main.py
    ```

2.  **Interactive Web App:**
    This will launch the Streamlit application in your web browser.
    ```bash
    streamlit run app.py
    ```
