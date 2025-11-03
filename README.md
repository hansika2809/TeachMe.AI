# **TeachMe.AI \- An Intelligent Study Companion**

## **Author**

* **Name:** Hansika Gupta  
* **University:** Indian Institute of Technology, Kanpur  
* **Department:** BS PHY

## **1\. About the Assignment**

This project, **TeachMe.AI**, is an intelligent agent prototype designed to function as a modular, reliable, and specialized study companion for students.

Its mission is to automate common academic tasks such as **text summarization**, **code explanation**, and **quiz generation** with a higher degree of accuracy and reliability than a single, general-purpose Large Language Model (LLM) can provide.

### **Key Architectural Features**

The core of this project is its **"Gated Router" (or Orchestrator) architecture**. Unlike a monolithic agent with one large prompt, this system is composed of two main parts:

1. **A Central Router Agent:** This agent's only job is to analyze the user's intent (e.g., "are they asking for a summary?" or "are they asking for a math solution?") and route the query to the correct specialized agent.  
2. **Specialized "Worker" Agents:** A set of modular, independent agents, each with a highly-focused prompt and purpose. This includes:  
   * Text\_Summarizer  
   * Concept\_Explainer  
   * Quiz\_Generator  
   * FlashCard\_Generator\_Agent  
   * Code\_Explainer\_Agent  
   * Math\_Problem\_Solver

This modular design allows for **task specialization** and makes the system more reliable. It also allows for specific components to be independently upgraded or, in this case, replaced with entirely different models.

## **2\. Important Technologies Used**

A key design choice is the use of different models for different jobs to optimize for performance, cost, and specialization.

* **Generalist Model (Gemini 2.5 Flash):**  
  * This model is used for all "fast" and general-purpose tasks.  
  * It powers the main **Router Agent** (for intent classification) and 5 out of the 6 **Worker Agents** (like Concept\_Explainer, Math\_Problem\_Solver, etc.).  
  * It was chosen for its excellent balance of speed, capability, and cost-efficiency.  
* **Specialized Model (Fine-Tuned T5):**  
  * **This is the core of the assignment.**  
  * A **Text-to-Text Transfer Transformer (T5)** model was fine-tuned on the "CNN Daily Mail" dataset to become an expert in summarization.  
  * This specialized model is used *exclusively* by the Text\_Summarizer\_Agent.  
* **Model Hosting (Modal AI):**  
  * To make this architecture work, the fine-tuned T5 model is hosted as a separate API endpoint using **Modal AI**.  
  * When the Router Agent hands off a task to the Text\_Summarizer\_Agent, that agent is configured to call the Modal AI endpoint to get the summary, rather than calling the Gemini API.  
* **Frontend & File Handling (Chainlit):**  
  * The chat interface is built using **Chainlit**.  
  * Chainlit is also used to handle user sessions and file uploads, with a pre-processing step that extracts text from .pdf, .docx, and .txt files before they are sent to any agent.

## **3\. Steps to Setup and Run**

### **Step 1: Clone the Repository**
```bash
git clone \[YOUR\_REPOSITORY\_URL\]  
cd \[PROJECT\_DIRECTORY\]
```

### **Step 2: Create and Activate a Virtual Environment**

It is highly recommended to use a virtual environment to manage dependencies.
```bash
\# For macOS/Linux  
python3 \-m venv venv  
source venv/bin/activate

\# For Windows  
python \-m venv venv  
.\\venv\\Scripts\\activate
```
### **Step 3: Install Dependencies**

Install all the required libraries from the requirements.txt file.
```bash
pip install \-r requirements.txt
```
### **Step 4: Run the Application**

*Note: You must have your API keys (e.g., GEMINI\_API\_KEY) set as environment variables for the application to function.*

The application is run using the Chainlit CLI.
```bash
# The \-w flag enables auto-reloading during development  
chainlit run app.py \-w
```
Open your browser and navigate to http://localhost:8000 to start using TeachMe.AI.
