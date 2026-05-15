import streamlit as st
import pandas as pd
import pdfplumber
import docx
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit.components.v1 as components

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="ResuMind",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ======================================================
# CUSTOM CSS
# ======================================================

st.markdown("""
<style>

html, body, [class*="css"]{
    font-family: 'Inter', sans-serif;
}

.stApp{
    background:
    radial-gradient(circle at top left,#111827 0%,#050816 45%,#020617 100%);
    color:white;
}

#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}

.block-container{
    padding-top:1rem;
    padding-left:2rem;
    padding-right:2rem;
    padding-bottom:1rem;
    max-width:1300px !important;
    margin:auto;
}

section[data-testid="stSidebar"]{
    background:
    linear-gradient(
        180deg,
        #081120,
        #0b1730
    );

    border-right:
    1px solid rgba(255,255,255,0.05);

    width:420px !important;
}

.stButton > button{
    width:100%;
    height:60px;
    border:none;
    border-radius:18px;

    background:
    linear-gradient(
        90deg,
        #d946ef,
        #3b82f6
    );

    color:white;
    font-size:18px;
    font-weight:700;
}

[data-testid="stFileUploader"]{
    background:#0f172a;
    border:
    1.5px dashed rgba(255,255,255,0.10);

    border-radius:20px;
    padding:20px;
}

textarea{
    background:#0f172a !important;
    color:white !important;
    border-radius:20px !important;

    border:
    1px solid rgba(255,255,255,0.08) !important;
}

.metric-card{
    background:
    linear-gradient(
        145deg,
        #0f172a,
        #131f3d
    );

    border:
    1px solid rgba(255,255,255,0.05);

    border-radius:24px;

    padding:24px;

    min-height:150px;

    box-shadow:
    0px 10px 40px rgba(0,0,0,0.35);
}

.skill{
    background:#163326;
    color:#4ade80;

    padding:7px 12px;

    border-radius:10px;

    display:inline-block;

    margin:4px;

    font-size:13px;
}

.missing{
    background:#1e293b;
    color:#cbd5e1;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# SKILLS DATABASE
# ======================================================

SKILLS = [

    "python","java","sql","machine learning","tensorflow",
    "pandas","numpy","nlp","aws","docker","kubernetes",
    "html","css","javascript","react","flask","django",
    "data science","deep learning","opencv","power bi",
    "excel","communication","leadership","api","git",
    "sap","sap hana","abap","fiori","erp","cloud integration",
    "debugging","data migration","spring boot","linux",
    "devops","blockchain","solidity","ethereum"

]

# ======================================================
# FUNCTIONS
# ======================================================

def extract_text_from_pdf(file):

    text = ""

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted

    return text


def extract_text_from_docx(file):

    doc = docx.Document(file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + " "

    return text


def extract_resume_text(file):

    if file.name.endswith(".pdf"):
        return extract_text_from_pdf(file)

    elif file.name.endswith(".docx"):
        return extract_text_from_docx(file)

    elif file.name.endswith(".txt"):
        return str(file.read(), "utf-8")

    return ""


def calculate_similarity(resume_text, jd_text):

    documents = [resume_text, jd_text]

    cv = CountVectorizer()

    matrix = cv.fit_transform(documents)

    similarity = cosine_similarity(matrix)[0][1]

    return round(similarity * 100)


def extract_skills(text):

    found = []

    text = text.lower()

    for skill in SKILLS:

        if skill.lower() in text:

            found.append(skill.lower())

    return list(set(found))

# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    st.markdown("# 🚀 ResuMind")

    st.caption("AI Resume Screening Agent")

    st.markdown("---")

    st.subheader("Upload Resumes")

    uploaded_files = st.file_uploader(
        "Upload Resume Files",
        accept_multiple_files=True,
        type=["pdf","docx","txt"]
    )

    st.subheader("Job Description")

    jd_text = st.text_area(
        "Paste JD Here",
        height=260
    )

    st.markdown("<br>", unsafe_allow_html=True)

    run = st.button("🚀 Run Screening")

# ======================================================
# MAIN
# ======================================================

if run:

    if not uploaded_files:

        st.warning("Please upload resumes")

    elif not jd_text.strip():

        st.warning("Please enter Job Description")

    else:

        results = []

        jd_skills = extract_skills(jd_text)

        for file in uploaded_files:

            resume_text = extract_resume_text(file)

            score = calculate_similarity(
                resume_text,
                jd_text
            )

            resume_skills = extract_skills(resume_text)

            matched = list(
                set(resume_skills).intersection(set(jd_skills))
            )

            missing = list(
                set(jd_skills).difference(set(resume_skills))
            )

            role = "Software Engineer"

            if "machine learning" in matched:
                role = "ML Engineer"

            elif "tensorflow" in matched:
                role = "AI Engineer"

            elif "react" in matched:
                role = "Frontend Developer"

            elif "sap" in matched:
                role = "SAP Developer"

            elif "blockchain" in matched:
                role = "Blockchain Developer"

            elif "devops" in matched:
                role = "DevOps Engineer"

            results.append({

                "name": file.name,
                "score": score,
                "role": role,

                "matched": [
                    s.title() for s in matched[:6]
                ],

                "missing": [
                    s.title() for s in missing[:6]
                ]

            })

        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        # ==================================================
        # HEADER
        # ==================================================

        st.markdown("""

        <p style="
        color:#94a3b8;
        font-size:16px;
        margin-bottom:0px;">

        Welcome back, Recruiter 👋

        </p>

        <h1 style="
        font-size:42px;
        margin-top:5px;
        color:white;">

        Resume Screening Dashboard

        </h1>

        <p style="
        color:#94a3b8;
        font-size:16px;
        margin-bottom:30px;">

        Smart ATS Matching • AI-Powered Analysis • Better Hiring Decisions

        </p>

        """, unsafe_allow_html=True)

        # ==================================================
        # METRICS
        # ==================================================

        highest = max([r["score"] for r in results])

        average = round(
            sum([r["score"] for r in results]) / len(results)
        )

        shortlisted = len([
            r for r in results if r["score"] >= 70
        ])

        c1,c2,c3,c4 = st.columns(4)

        metrics = [

            ("📄","Total Resumes",str(len(results))),
            ("📈","Highest Match",f"{highest}%"),
            ("📊","Average Match",f"{average}%"),
            ("🏆","Shortlisted",str(shortlisted))

        ]

        for col, metric in zip([c1,c2,c3,c4], metrics):

            icon,title,value = metric

            with col:

                st.markdown(f"""
                <div class="metric-card">

                <div style="font-size:32px;">
                {icon}
                </div>

                <p style="
                color:#94a3b8;
                margin-top:12px;
                font-size:15px;">

                {title}

                </p>

                <h1 style="
                font-size:34px;
                margin-top:0px;
                color:white;">

                {value}

                </h1>

                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ==================================================
        # TOP MATCHES
        # ==================================================

        st.markdown("""
        <h2 style="color:white;">
        🏆 Top Matches
        </h2>
        """, unsafe_allow_html=True)

        cols = st.columns(3)

        for col, candidate in zip(cols, results[:3]):

            matched_html = ""

            for skill in candidate["matched"]:

                matched_html += f"""
                <span class="skill">
                {skill}
                </span>
                """

            missing_html = ""

            for skill in candidate["missing"]:

                missing_html += f"""
                <span class="skill missing">
                {skill}
                </span>
                """

            card_html = f"""

            <html>

            <body style="
            margin:0;
            background:transparent;
            font-family:Inter,sans-serif;">

            <div style="

            background:
            linear-gradient(
                145deg,
                #0f172a,
                #131f3d
            );

            border:
            1px solid rgba(255,255,255,0.05);

            border-radius:24px;

            padding:22px;

            height:340px;

            color:white;

            box-shadow:
            0px 10px 40px rgba(0,0,0,0.35);

            ">

                <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;">

                    <div>

                        <h2 style="
                        margin-bottom:0px;
                        color:white;
                        font-size:22px;">

                        {candidate["name"]}

                        </h2>

                        <p style="
                        color:#94a3b8;
                        font-size:14px;">

                        {candidate["role"]}

                        </p>

                    </div>

                    <div style="

                    width:75px;
                    height:75px;

                    border-radius:50%;

                    border:5px solid #22c55e;

                    display:flex;
                    align-items:center;
                    justify-content:center;

                    font-size:24px;
                    font-weight:800;

                    color:white;

                    ">

                    {candidate["score"]}%

                    </div>

                </div>

                <br>

                <div style="
                height:8px;
                background:#1e293b;
                border-radius:999px;
                overflow:hidden;">

                    <div style="
                    width:{candidate["score"]}%;
                    height:100%;
                    background:
                    linear-gradient(
                        90deg,
                        #22c55e,
                        #3b82f6
                    );">
                    </div>

                </div>

                <br>

                <h4 style="
                color:white;
                margin-bottom:8px;">

                Matched Skills
                </h4>

                {matched_html}

                <br><br>

                <h4 style="
                color:white;
                margin-bottom:8px;">

                Missing Skills
                </h4>

                {missing_html}

            </div>

            </body>

            </html>

            """

            with col:

                components.html(
                    card_html,
                    height=350,
                    scrolling=False
                )

        # ==================================================
        # RESULTS TABLE
        # ==================================================

        st.markdown("""
        <h2 style="color:white;">
        📋 All Results
        </h2>
        """, unsafe_allow_html=True)

        table_data = []

        for r in results:

            table_data.append({

                "Candidate": r["name"],
                "ATS Score": f'{r["score"]}%',
                "Suggested Role": r["role"],
                "Matched Skills": ", ".join(r["matched"]),
                "Missing Skills": ", ".join(r["missing"])

            })

        df = pd.DataFrame(table_data)

        st.dataframe(
            df,
            use_container_width=True
        )