 Medicine_Substitutes_Finder
🏥 AI-Powered Healthcare: Access and Alternatives for Indian Medications

📖 Introduction

Medicine shortages in India often leave patients waiting while pharmacists manually search for substitutes. This project automates the process using OCR, semantic search, and containerized web services, making substitution faster and more reliable.

⸻

❗ Problem Statement

The system solves three challenges:
	1.	Extract prescribed medicines from scanned prescriptions.
	2.	Recommend therapeutic substitutes automatically.
	3.	Enable Access via a deployed web API with potential UI integration.

⸻

🚀 Features & Benefits
	•	Automated substitute search → reduces manual lookup time.
	•	REST API with docs → /predict, /healthz, /batch.
	•	Portable deployment → containerized with Docker, runs on any cloud.
	•	Scalable design → can integrate pharmacies, online retailers, or dashboards.
	•	User-friendly layer → extendable with HTML/JS frontend for non-technical use.

⸻

✅ Project Outcomes
	•	Automated extraction of prescriptions and substitutes.
	•	Successfully deployed as a containerized microservice.
	•	Demonstrated integration of ML/NLP models with production-ready backend practices.

⸻

🔮 Future Roadmap
	•	HTML/JS Web Dashboard for pharmacists/patients.
	•	Real-time inventory check via pharmacy APIs.
	•	CI/CD pipeline with GitHub Actions + Cloud Run/Fly.io.
	•	Feedback loop to refine substitute recommendations.

⸻

📖 Tech Stack & Technologies
	•	Backend Framework: FastAPI / Flask
	•	Machine Learning & NLP: PyTorch, Sentence Transformers
	•	OCR: Gemini Vision Pro API
	•	Similarity Search: Cosine similarity on embeddings
	•	Infrastructure: Docker, Cloud Run / Render / Railway for deployment
	•	Data Tools: Pandas, Pillow
	•	Frontend (optional extension): HTML, CSS, JavaScript
