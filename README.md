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
## Usage of the app
* Go to https://youtubeanalyzer-data.streamlit.app/
Type a name of the youtube Channel
![image](https://github.com/user-attachments/assets/b0ebcf67-8a35-4632-9946-8a09af45ff40)

* Next click the fetch data button
![image](https://github.com/user-attachments/assets/7095c15a-eec6-4400-8409-2a51dfe548ca)
 * Now you would see a text box where you can prompt the question on the channel
![image](https://github.com/user-attachments/assets/2c63c403-20e5-458e-8246-71213d30e936)
* The above question will give you a nice insight on the query asked based on the vectorDB chunk or context it had received
  ![image](https://github.com/user-attachments/assets/29f2fbb7-1f4d-4f34-a8a4-43b3203cc1f6)
*It  will not just stop there . It would also give you ince visuals if you click visualization
![image](https://github.com/user-attachments/assets/8d9c0421-dce8-4081-86ac-106c15b1cf84)





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
