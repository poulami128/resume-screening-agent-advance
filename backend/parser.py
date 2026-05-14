import re
from typing import List, Dict

# Improved skill mapping with synonyms
SKILL_SYNONYMS = {

    # Programming
    "python": ["python", "py"],
    "java": ["java"],
    "c++": ["c++"],
    "javascript": ["javascript", "js"],

    # Frameworks
    "django": ["django"],
    "flask": ["flask"],
    "react": ["react", "reactjs"],

    # Databases
    "sql": ["sql", "mysql", "postgresql", "sqlite"],
    "mongodb": ["mongodb", "nosql"],

    # Cloud & DevOps
    "aws": ["aws", "amazon web services"],
    "docker": ["docker", "containerization"],
    "kubernetes": ["kubernetes", "k8s"],
    "ci/cd": [
        "ci/cd",
        "jenkins",
        "github actions",
        "pipeline"
    ],

    # AI/ML
    "machine learning": [
        "machine learning",
        "ml"
    ],

    "nlp": [
        "nlp",
        "natural language processing"
    ],

    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],

    "scikit-learn": [
        "scikit-learn",
        "sklearn"
    ],

    # APIs
    "rest api": [
        "rest api",
        "restful api",
        "restful services",
        "web services",
        "api integration"
    ],

    # Agile
    "agile": [
        "agile",
        "scrum",
        "kanban",
        "sprint planning"
    ],

    # QA / Testing
    "testing": [
        "testing",
        "unit testing",
        "qa",
        "quality assurance",
        "automation testing",
        "manual testing",
        "functional testing",
        "regression testing",
        "integration testing",
        "system testing",
        "test cases",
        "test scenario",
        "bug tracking",
        "defect tracking"
    ],

    "selenium": [
        "selenium",
        "selenium webdriver"
    ],

    "jira": [
        "jira",
        "atlassian jira"
    ],

    "postman": [
        "postman",
        "api testing"
    ],

    "pytest": [
        "pytest"
    ],

    # Version Control
    "git": [
        "git",
        "github",
        "version control"
    ]
}


def parse_job_description(jd_text: str) -> Dict:
    if not jd_text:
        return {"skills": [], "years": None}

    text = jd_text.lower()

    skills = extract_skills_from_text(text)

    # Extract years of experience
    m = re.search(r'(\d+)[\+]? years?', text)
    years = int(m.group(1)) if m else None

    return {
        "skills": skills,
        "years": years
    }


def extract_skills_from_text(text: str) -> List[str]:
    text = text.lower()
    found = set()

    for main_skill, variations in SKILL_SYNONYMS.items():

        for keyword in variations:

            # safer matching using regex
            pattern = r'\b' + re.escape(keyword) + r'\b'

            if re.search(pattern, text):
                found.add(main_skill)

    return list(found)