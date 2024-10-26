## Benchmarking LLMs in the Comprehension of EU Payments Regulations (OpenAI-Evals, LLaMA-Index)
This project employs **OpenAI** models and the **OpenAI-Evals** platform to assess the performance of **Large Language Models (LLMs)** in accurately answering multiple-choice questions related to the European Regulation on **Strong Customer Authentication (SCA)** for electronic payments.

The **LLaMA-Index** framework facilitates the ingestion of the SCA regulation into a **FAISS Vector Database**, enabling efficient query and response processes under a **Retrieval Augmented Generation (RAG)** approach. The **OpenAI-Evals** platform is utilized to process a prepared benchmark dataset and evaluate the accuracy of various OpenAI models.

Results indicate that the most advanced models achieve high accuracy rates: "text-davinci-003" at **88%**, "gpt-3.5-turbo" at **89%** "gpt-4o-mini" at **94%**, and "gpt-4o" at **97%**.

This application is not intended for direct integration into production environments. Rather, it demonstrates, with a few lines of Python code, how these platforms can be utilized to support flexible validation of large language models (LLMs).

### Purpose 
Strong Customer Authentication (SCA) regulation is essential in electronic payments to enhance security by requiring multi-factor verification. This reduces fraud risk, safeguards customer data, and aligns with regulatory standards like the EU’s Payments Services Directive II. 

However, European regulations governing banks, payments, and financial services are both critical and highly complex. They are frequently updated, making it challenging for institutions to stay current, while the complexity and interconnectivity of these texts underscore the need for advanced tools to efficiently manage regulatory compliance.

By leveraging advanced natural language processing, LLMs can interpret regulatory texts, identify compliance obligations, and facilitate continuous monitoring. 

Benchmarking of LLMs is crucial to ensure their reliability, accuracy, and relevance in real-world applications. Before deployment in production, rigorous evaluation assesses model performance across diverse linguistic and contextual tasks, revealing potential biases, limitations, and areas for optimization. 

This project presents a straightforward benchmarking example designed to evaluate the performance of large language models (LLMs), serving as a step toward aligning AI models with industry standards.

### Process Overview 
The ingestion of the SCA regulation contents and the benchmarking of LLMs follow the below steps:

![Process Overview](https://github.com/antdragiotis/LLMs-benchmarking-for-SCA-Reg/blob/main/assets/SCA_Bench_Overview.PNG)

### Features
- **Source Data**: The project uses as source data  the MS-word file **SCA_2018_10_Scource.docx** which is an annotated version of the Strong Customer Authentication Regulation (SCA). The original SCA text is available at EUR-Lex (https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32018R0389). For this  application, only the regulation articles have been retained and marked with symbols to denote the chapters and the articles of the regulation. The introductory sections have been excluded, resulting in a focused text file to serve as the project's source data.
- **Ingestion**: The 'Ingestion' process is performed by the *EU_SCA_REG_INGEST.py* Python code file. This process reads the Source Data and splits the SCA text into separate **LLaMA-Index** type documents, assigning also to each document metadata about the relevant article number, article title and the relevant chapter. Next to this, the process splits the documents into chunks text and uses **VectorStoreIndex** function to vectorize the text.  Then, it uses**FAISS** library to store the results to the *FAISS_storage* directory. 
- To test the performance of various LLM models, the **SCA_Bench_MC.JSON** benchmark file has been prepared containing 100 multiple-choice questions . The format of the file is according to the instructions of the **OpenAI Evals** so as to be readable by the processes of this platform (see the README file in the GitHub repo: https://github.com/openai/evals/tree/main/evals/registry/data). For each atrticle of the SCA regulation 3 questions have been prepared at maximum. For short and simple articles 2 questions have been prepared. For each question 4 alternative choices are given. A sample of this file is found in the **./source** directory and contains the first 10 questions of the total set of 100 questions used for the evaluation.
  - For the evaluation process the **OpenAI-Evals** platform is utilized. In addition to a large set of pre-defined evaluation processes (including benchmark files) OpenAI-Evals provides the option to run custom evaluations and implement own **Completion Functions** which actually respond to the taks defined in the benchmark files. Instructions to implement own Completion Functions are given in https://github.com/openai/evals/blob/main/docs/completion-fns.md. In this project the custom module **SCA_completion_fn.py** is used to read from the vectorized text and respond to the questions included in the **SCA_Bench_MC.JSON** file. 
  - After the running of the evaluation process the results are stored in the **C:\tmp\evallogs** directory. The results of the 4 evaluation runs of this project may be found in the **./results** directory.
  
  - ### How to run the app:
- clone the repository: https://github.com/antdragiotis/LLMs-benchmarking-for-SCA-Reg
- change current directory to cloned repository
- pip install -r requirements.txt
- it is assumed that your system has been configured with the OPENAI_API_KEY, otherwise you need to add the following statements to the python code files:
  - import os
  - os.environ["OPENAI_API_KEY"] = "your-openai-api-key"
- run the two Python file EU_SCA_REG_INGEST.py
- utilize the **SCA_completion_fn.py** according to the instructions of the OpenAI-Evals platform to run the evaluation
- review the results of the evaluation in the **C:\tmp\evallogs** directory.
 
### Project Structure
- *.py: main application code
- source: directory with the source data file
- results: directory with a file containing the results files
- README.md: project documentation
