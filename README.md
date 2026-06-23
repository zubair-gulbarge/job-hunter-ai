# 🚀 Job Hunter AI

An end-to-end, AI-powered job application tracking system (ATS) and dynamic resume generator. 

Designed with a decoupled, cloud-ready architecture, this application leverages local Large Language Models (LLMs) to automatically tailor a master resume to specific job descriptions, generate polished PDFs, and track application states via a Kanban-style dashboard.

---

## 🏗 Architecture & Tech Stack

Built for scalable deployment (AWS ECS/Fargate ready) while running entirely locally at $0 cost during development.

* **Backend:** FastAPI (Python) for high-performance, asynchronous API routing.
* **Database:** MongoDB (Containerized via Docker) for unstructured document storage and state management.
* **AI Engine:** LangChain orchestration communicating with Ollama (Llama 3), optimized natively for Apple Silicon.
* **Document Rendering:** Jinja2 templating and WeasyPrint for dynamic PDF generation.
* **Frontend:** React.js powered by Vite *(In Development)*.

---

## ✨ Core Features

* **🧠 AI Resume Tailoring:** Ingests a structured JSON master profile and a target Job Description (JD). Prompts a local LLM to rewrite and reframe experience bullets targeting specific JD keywords without fabricating history.
* **📄 Automated PDF Rendering:** Converts the AI-generated response into a cleanly formatted, professional HTML template, then renders it into a downloadable PDF.
* **📊 Kanban Application Tracking:** Logs application metadata (Company, Role, Tailored Resume ID) and tracks the CI/CD pipeline of your job hunt (Preparing ➡️ Applied ➡️ Interviewing ➡️ Offered ➡️ Rejected).

---

## 💻 Local Development Setup

### Prerequisites
1. **Docker Desktop:** Required to run the isolated MongoDB instance.
2. **Ollama:** Download from [ollama.com](https://ollama.com/) and pull the local model by running:
   ```bash
   ollama run llama3

```

3. **Python 3.13+**
4. **macOS System Dependencies:** Required for WeasyPrint to render graphics.
```bash
brew install pango cairo glib
export DYLD_FALLBACK_LIBRARY_PATH="$(brew --prefix)/lib:$DYLD_FALLBACK_LIBRARY_PATH"

```



### Installation

**1. Clone the repository & spin up the database:**

```bash
git clone [https://github.com/zubair-gulbarge/job-hunter-ai.git](https://github.com/zubair-gulbarge/job-hunter-ai.git)
cd job-hunter-ai
docker-compose up -d

```

**2. Initialize the Backend Environment:**

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

**3. Run the API Server:**

```bash
uvicorn app.main:app --reload

```

*The backend will now be available at `http://127.0.0.1:8000`.*

---

## 🛣 API Reference

Interactive Swagger API documentation is automatically generated and available at `/docs` when the server is running.

### Core Endpoints

| Method | Endpoint             | Description                                                 |
| ------ | -------------------- | ----------------------------------------------------------- |
| `POST` | `/api/tailor-resume` | Streams JD to the local LLM and returns a rendered PDF file |
| `POST` | `/api/profile`       | Upserts the user's master JSON profile                      |
| `GET`  | `/api/profile`       | Retrieves the master profile                                |
| `POST` | `/api/applications`  | Creates a new job application tracker entry                 |
| `GET`  | `/api/applications`  | Returns an array of all tracked applications                |
| `PUT`  | `/api/applications/{id}/status` | Updates the application pipeline status          |

---

## 👨‍💻 Author
**Zubair** *Cloud & DevOps Engineer* * Portfolio: [zubairlearntech.com](https://zubairlearntech.com)
* Contact: zubairgulbarge@gmail.com