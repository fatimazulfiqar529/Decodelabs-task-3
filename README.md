##DecodeLabs Internship Artificial Intelligence (Project 3)
A content-based AI recommendation system that maps a user's skills to the most suitable tech career paths using TF-IDF weighting and Cosine Similarity.
## Goal
Build a recommendation engine that takes a user's tech skills as input and returns the top 3 most relevant career paths by calculating mathematical similarity between the user profile and job role datasets.
## How It Works
The system follows a strict 4-step pipeline:
### Step 1: Ingestion
The user selects or types a minimum of 3 skills. These are captured as the user profile.
### Step 2: Scoring
Each skill is converted into a TF-IDF weighted vector. The system then calculates the Cosine Similarity score between the user vector and every job role vector in the dataset.
### Step 3: Sorting
All job roles are sorted in descending order based on their similarity scores.
### Step 4: Filtering
Only the Top 3 highest-scoring roles are displayed to prevent information overload.
## Dataset
The system includes 15 job roles, each with 10 associated skills:

| Role                   | Key Skills                               |
| Data Scientist         | Python, ML, SQL, Statistics, TensorFlow  |
| ML Engineer            | PyTorch, Deep Learning, Model Deployment |
| Backend Developer      | Java, APIs, Docker, Microservices        |
| Frontend Developer     | JavaScript, React, CSS, TypeScript       |
| Full Stack Developer   | Python, JavaScript, React, SQL           |
| DevOps Engineer        | Docker, Kubernetes, AWS, CI/CD           |
| Cloud Architect        | AWS, Azure, Terraform, Networking        |
| Cybersecurity Analyst  | Security, Ethical Hacking, Encryption    |
| AI Engineer            | NLP, Deep Learning, Cloud, Algorithms    |
| Data Analyst           | SQL, Tableau, Power BI, Excel            |
| Mobile Developer       | Flutter, Kotlin, Swift, Android          |
| Database Administrator | MySQL, PostgreSQL, Oracle                |
| System Administrator   | Linux, Bash, Virtualization              |
| Blockchain Developer   | Solidity, Ethereum, Web3                 |
| Game Developer         | Unity, C++, Unreal Engine                |

## Requirements
* Python 3.8+
* PyQt5
## Installation & Run
### Step 1 — Install Dependency
pip install PyQt5
### Step 2 — Run the Application
python Recommendation-engine.py
