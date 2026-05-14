import logging
from typing import List, Dict
from backend.embeddings_store import get_embeddings_for_texts
from backend.parser import extract_skills_from_text

logger = logging.getLogger(__name__)


def compute_scores(jd_text: str, resumes: List[Dict]) -> List[Dict]:

    # Validate JD text
    if jd_text is None:
        jd_text = ""

    elif not isinstance(jd_text, str):
        jd_text = str(jd_text)

    # Prepare resumes safely
    safe_resumes = []
    texts_for_emb = [jd_text]

    for idx, r in enumerate(resumes or []):

        if not isinstance(r, dict):

            safe = {
                "name": f"resume_{idx}",
                "text": ""
            }

            safe_resumes.append(safe)
            texts_for_emb.append("")
            continue

        txt = r.get("text", "")

        if txt is None:
            txt = ""

        elif not isinstance(txt, str):
            txt = str(txt)

        safe = dict(r)
        safe["text"] = txt

        safe_resumes.append(safe)
        texts_for_emb.append(txt)

    # Generate embeddings
    try:
        vectors = get_embeddings_for_texts(texts_for_emb)

    except Exception as e:

        logger.exception("Embedding generation failed: %s", e)

        for r in safe_resumes:
            r["score"] = 0.0
            r["matched_skills"] = []

        return safe_resumes

    # Validate vectors
    if not vectors or len(vectors) < 1:

        for r in safe_resumes:
            r["score"] = 0.0
            r["matched_skills"] = []

        return safe_resumes

    jd_vec = vectors[0]
    resume_vectors = vectors[1:]

    # Cosine similarity
    def cosine(a, b):

        try:
            import math

            if len(a) != len(b):
                return 0.0

            dot = sum(x * y for x, y in zip(a, b))

            norm_a = math.sqrt(sum(x * x for x in a))
            norm_b = math.sqrt(sum(y * y for y in b))

            if norm_a == 0 or norm_b == 0:
                return 0.0

            return dot / (norm_a * norm_b)

        except Exception:
            return 0.0

    # Extract JD skills
    jd_skills = set(
        extract_skills_from_text(jd_text.lower())
    )

    results = []

    # Process resumes
    for r_meta, vec in zip(safe_resumes, resume_vectors):

        try:
            semantic_score = float(cosine(jd_vec, vec))

        except Exception:
            semantic_score = 0.0

        # Resume skills
        resume_text = r_meta.get("text", "").lower()

        resume_skills = set(
            extract_skills_from_text(resume_text)
        )

        matched = list(
            jd_skills.intersection(resume_skills)
        )

        # Skill overlap score
        skill_score = 0.0

        if len(jd_skills) > 0:
            skill_score = len(matched) / len(jd_skills)

        # Final hybrid score
        final_score = (
            (0.7 * semantic_score) +
            (0.3 * skill_score)
        )

        # Missing skills
        missing_skills = list(
            jd_skills - resume_skills
        )

        # Suggested role logic
        suggested_role = "General Software Engineer"

        if "testing" in resume_skills or "selenium" in resume_skills:
            suggested_role = "QA Engineer"

        elif "machine learning" in resume_skills or "tensorflow" in resume_skills:
            suggested_role = "Machine Learning Engineer"

        elif "django" in resume_skills or "flask" in resume_skills:
            suggested_role = "Backend Developer"

        elif "react" in resume_skills:
            suggested_role = "Frontend Developer"

        # Output
        r_out = dict(r_meta)

        r_out["score"] = round(final_score, 3)

        r_out["semantic_score"] = round(semantic_score, 3)

        r_out["skill_score"] = round(skill_score, 3)

        r_out["matched_skills"] = matched

        r_out["missing_skills"] = missing_skills

        r_out["suggested_role"] = suggested_role

        results.append(r_out)

    # Sort descending
    results.sort(
        key=lambda x: x.get("score", 0.0),
        reverse=True
    )

    return results