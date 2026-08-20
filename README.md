<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./banner-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="./banner-light.svg" />
  <img alt="Mohammad Atef — applied AI engineer" src="./banner-light.svg" />
</picture>

I lead the AI pod at **Valsoft**, where I own an agentic support system handling customer
tickets across web chat, phone, and email, and the roadmap for what the product does with AI
next. Alongside that I ship full-stack features on the platform itself — React and TypeScript
on the front, Python and .NET on the back.

Before this I was founding AI engineer at an automation startup, moving an enterprise customer
base off brittle RPA and onto multi-agent orchestration across 50+ databases and 100+ users.

### What I've built

**Agentic support system** *(private)* — voice, chat, and email agents over a shared tool
layer, with assistant and tool configuration held as code and synced to production through
GitHub Actions. Real telephony, real ticketing, real escalation paths.

**[inkris](https://github.com/madatef/inkris)** — a modular AI workspace. Async ingestion to
S3, RAG over mixed file types, web search and scraping, multimodal generation, conversational
memory. FastAPI · React · LangChain · LangSmith · Docker on EC2 behind Nginx.

**[url-shortener](https://github.com/madatef/url-shortener)** — a rebuild of something I wrote
five years ago, done properly: rate limiting, connection pooling, ELK logging, dependency
injection, service/repository separation. A good look at how I structure a backend.

**[flairstechAgent](https://github.com/madatef/flairstechAgent)** — a conversational
support agent that triages issues through natural dialogue and files structured tickets.
The closest public analogue to the production system above: LangChain tool-calling over a
category taxonomy, FastAPI, Supabase, React.

**[Content-evaluator](https://github.com/madatef/Content-evaluator)** — RAG system scoring
marketing assets against brand guidelines via multimodal analysis over SharePoint documents.
Replaced a manual review process.

**[fire-detection](https://github.com/madatef/fire-detection)** — YOLOv8 over live CCTV,
triggering suppression hardware and pushing timestamped alert frames.

### Stack

```
AI systems    LangChain · LangGraph · RAG · vector search · evals · guardrails · OCR
Backend       Python · FastAPI · Celery · Redis · SQLAlchemy · Node · Express
Frontend      TypeScript · React · Tailwind · Vite
Data          PostgreSQL · SQL Server · MongoDB · Qdrant · Pinecone · DuckDB
Infra         Docker · AWS (EC2, S3) · GitHub Actions · ELK
```

### Elsewhere

[LinkedIn](https://linkedin.com/in/madatef) · [itsmadatef@gmail.com](mailto:itsmadatef@gmail.com) · Cairo, Egypt

<sub><img src="./stats.svg" alt="" align="top" /></sub>
