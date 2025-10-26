# Phone Assistant Chatbot

This project is a production-grade chatbot designed to assist users with phone recommendations and answer their queries. It features a user-friendly interface and a robust backend powered by modern technologies.

## Motivation

The primary motivation behind this project is to create a reliable and intelligent chatbot that can provide accurate and helpful information about mobile phones. In a market flooded with numerous options, this chatbot aims to simplify the decision-making process for users by offering personalized recommendations based on their needs and preferences.

## Tech Stack and Architecture

### Frontend

- **Framework:** React with Vite
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **UI Components:** Lucide React
- **Dependencies:** Supabase Client, React Markdown

### Backend

- **Framework:** FastAPI
- **Language:** Python
- **AI/ML:** LangChain, Google Generative AI
- **Database:** Supabase
- **API:** RESTful API with Pydantic models
- **Server:** Uvicorn

### Architecture Overview

The application is designed with a decoupled frontend and backend architecture:

1.  **Frontend:** The user interacts with a React-based single-page application (SPA). All user input is captured here and sent to the backend via REST API calls.

2.  **Backend:** The FastAPI backend serves as the core of the application. It receives requests from the frontend, processes them, and returns the appropriate responses. It is responsible for:
    *   **Authentication:** Managing user authentication and authorization.
    *   **Business Logic:** Implementing the core logic of the chatbot.
    *   **AI/ML Integration:** Interacting with LangChain and Google Generative AI to generate chatbot responses.
    *   **Database Interaction:** Storing and retrieving data from the Supabase database.

3.  **Supabase:** Supabase is used as the database to store chat history and other relevant data.

4.  **Google Generative AI:** This is the AI model that powers the chatbot's responses. The backend sends prompts to this model and receives the generated text.

## Features

- **Personalized Recommendations:** Get phone recommendations based on your specific needs and preferences.
- **Natural Language Understanding:** Interact with the chatbot using natural language, just like you would with a human.
- **Real-time Responses:** Receive instant responses to your queries, ensuring a seamless user experience.
- **User-Friendly Interface:** The intuitive and responsive design makes it easy to interact with the chatbot.

## Setup and Installation

### Prerequisites

- Node.js and npm
- Python 3.9+ and pip
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/phone-assistant-chatbot.git
   cd phone-assistant-chatbot
   ```

2. **Backend Setup:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Frontend Setup:**
   ```bash
   cd frontend
   npm install
   ```

### Environment Variables

Create a `.env` file in the `backend` directory and add the following:

```
GOOGLE_API_KEY="your-google-api-key"
SUPABASE_URL="your-supabase-url"
SUPABASE_KEY="your-supabase-key"
```

Create a `.env` file in the `frontend` directory and add the following:

```
VITE_API_BASE_URL="http://localhost:8000/api/v1"
```

### Running the Application

1.  **Backend:**
    Navigate to the `backend` directory and run the following command to start the development server:
    ```bash
    uvicorn main:app --reload
    ```
    The backend will be available at `http://localhost:8000`.

2.  **Frontend:**
    Navigate to the `frontend` directory and run the following command to start the development server:
    ```bash
    npm run dev
    ```
    The frontend will be available at `http://localhost:5173`.

## Prompt Design and Safety

The chatbot's effectiveness and safety are paramount. We have implemented the following strategies to ensure a reliable and secure user experience:

- **Persona-Based Prompts:** The chatbot is designed with a specific persona to maintain a consistent tone and style in its responses.
- **Contextual Understanding:** The prompts are designed to provide the chatbot with the necessary context to understand user queries accurately.
- **Guardrails and Filters:** We have implemented safety filters and guardrails to prevent the chatbot from generating inappropriate or harmful content.

## Known Limitations

- **Limited Knowledge Base:** The chatbot's knowledge is limited to the data it was trained on. It may not be able to answer queries about very new or niche phone models.
- **Potential for Inaccuracies:** While we strive for accuracy, the chatbot may occasionally provide incorrect information. We are continuously working to improve its knowledge base and accuracy.
