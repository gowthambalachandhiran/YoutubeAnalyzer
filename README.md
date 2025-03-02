# YouTube Channel Insights App

This application leverages the power of Google's Gemini Pro model and Streamlit to provide in-depth insights into YouTube channels. It uses two agents: a data retrieval agent and a business intelligence agent.

## Features

* **YouTube Channel Data Retrieval:**
    * Takes a YouTube channel name as input.
    * Uses the YouTube Data API to fetch channel information, including videos, descriptions, and statistics.
    * Converts the retrieved data into a vector database for efficient semantic search.
* **Gemini-Powered Insights:**
    * Allows users to ask questions about the channel, such as:
        * "Summarize the channel."
        * "What is the channel about?"
        * "Can I contact the channel for ads?"
        * "How should I improve the channel?"
    * Uses Gemini Pro to generate insightful answers based on the data stored in the vector database.
* **Business Intelligence Visualization:**
    * Generates graphs and visualizations from the insights, providing a clear and concise overview of the channel's performance.
    * Uses Streamlit to display the graphs.

## How It Works

1.  **Data Retrieval Agent:**
    * The user inputs a YouTube channel name.
    * The application uses the YouTube Data API to fetch relevant channel data.
    * The data is processed and embedded into a vector database.
2.  **Gemini Insights Agent:**
    * The user asks a question about the channel.
    * The application uses the vector database to find relevant information.
    * Gemini Pro analyzes the information and generates a comprehensive answer.
3.  **Business Intelligence Agent:**
    * The business intelligence agent takes the text responses from the Gemini insights agent, and extracts numerical data, and relevant information for graphing.
    * Streamlit displays the generated graphs and visualizations.

## Prerequisites

* Python 3.x
* Google Cloud Platform (GCP) account with the following APIs enabled:
    * YouTube Data API v3
    * Generative Language API
* Streamlit
* A vector database of your choice, and the python library for it. (such as ChromaDB, or FAISS)
* Google generativeai python library.
* Google API python client.
* A google api key.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone [repository URL]
    cd [repository directory]
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your Google Cloud credentials:**

    * Download your service account JSON key file from the GCP console.
    * Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to the path of your JSON key file.
    * Or use a google api key, and set that in the code.

4.  **Configure API keys:**
    * Add your Youtube Data API key, and your google generative ai api key to your application.

5.  **Run the Streamlit app:**

    ```bash
    streamlit run app.py
    ```

## Usage

1.  Open the Streamlit app in your browser.
2.  Enter the YouTube channel name in the input field.
3.  Ask a question about the channel.
4.  The application will display the generated insights and visualizations.

## Example Questions

* "Summarize the channel."
* "What is the channel about?"
* "Can I contact the channel for ads?"
* "How should I improve the channel?"
* "What are the most popular video topics?"
* "What is the average view count?"

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

[License]
