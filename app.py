import streamlit as st
import pandas as pd
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

/* HIDE STREAMLIT */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

header{
    visibility:hidden;
}

/* MAIN LAYOUT */

.block-container{

    padding-top:1rem;

    padding-left:3rem;

    padding-right:3rem;

    padding-bottom:2rem;

    max-width:100% !important;
}

/* SIDEBAR */

section[data-testid="stSidebar"]{

    background:
    linear-gradient(
        180deg,
        #081120,
        #0b1730
    );

    border-right:
    1px solid rgba(255,255,255,0.05);

    width:340px !important;
}

/* BUTTON */

.stButton > button{

    width:100%;
    height:58px;

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

/* FILE UPLOADER */

[data-testid="stFileUploader"]{

    background:#0f172a;

    border:
    1.5px dashed rgba(255,255,255,0.10);

    border-radius:20px;

    padding:20px;
}

/* TEXT AREA */

textarea{

    background:#0f172a !important;

    color:white !important;

    border-radius:20px !important;

    border:
    1px solid rgba(255,255,255,0.08) !important;
}

/* METRIC CARD */

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

    padding:28px;

    min-height:170px;

    box-shadow:
    0px 10px 40px rgba(0,0,0,0.35);
}

/* DATAFRAME */

[data-testid="stDataFrame"]{
    width:100% !important;
    border-radius:20px;
    overflow:hidden;
}

/* SKILLS */

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

/* BETTER SPACING */

.element-container{
    margin-bottom:0.8rem;
}

div[data-testid="column"]{
    padding:0.2rem;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:

    st.markdown("# 🚀 ResuMind")

    st.caption("AI Resume Screening Agent")

    st.markdown("---")

    st.subheader("Upload Resumes")

    st.file_uploader(
        "Upload Files",
        accept_multiple_files=True
    )

    st.subheader("Job Description")

    st.text_area(
        "Paste JD Here",
        height=220
    )

    st.checkbox("Use Sample Resumes")

    st.markdown("<br>", unsafe_allow_html=True)

    run = st.button("🚀 Run Screening")

# ======================================================
# DATA
# ======================================================

data = [

    {
        "name":"Aarav Sharma",
        "score":92,
        "role":"Data Scientist",
        "matched":["Python","Machine Learning","SQL","TensorFlow"],
        "missing":["Kubernetes"]
    },

    {
        "name":"Priya Patel",
        "score":78,
        "role":"ML Engineer",
        "matched":["Python","SQL","Pandas","NLP"],
        "missing":["Docker","AWS"]
    },

    {
        "name":"Rohan Verma",
        "score":65,
        "role":"Backend Developer",
        "matched":["Python","Java","SQL"],
        "missing":["TensorFlow","Kubernetes"]
    }

]

# ======================================================
# MAIN UI
# ======================================================

if run:

    st.markdown("""

    <p style="
    color:#94a3b8;
    font-size:18px;
    margin-bottom:0px;">

    Welcome back, Recruiter 👋

    </p>

    <h1 style="
    font-size:52px;
    margin-top:5px;
    color:white;">

    Resume Screening Dashboard

    </h1>

    <p style="
    color:#94a3b8;
    font-size:18px;
    margin-bottom:40px;">

    Smart ATS Matching • AI-Powered Analysis • Better Hiring Decisions

    </p>

    """, unsafe_allow_html=True)

    # ==================================================
    # METRICS
    # ==================================================

    c1,c2,c3,c4 = st.columns(
        [1,1,1,1],
        gap="large"
    )

    metrics = [

        ("📄","Total Resumes","12"),
        ("📈","Highest Match","92%"),
        ("📊","Average Match","68%"),
        ("🏆","Shortlisted","4")

    ]

    for col, metric in zip([c1,c2,c3,c4], metrics):

        icon,title,value = metric

        with col:

            st.markdown(f"""
            <div class="metric-card">

            <div style="font-size:40px;">
            {icon}
            </div>

            <p style="
            color:#94a3b8;
            margin-top:15px;
            font-size:16px;">

            {title}

            </p>

            <h1 style="
            font-size:42px;
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

    cols = st.columns(
        [1,1,1],
        gap="large"
    )

    for col, candidate in zip(cols, data):

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

        padding:24px;

        height:380px;

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
                    color:white;">

                    {candidate["name"]}

                    </h2>

                    <p style="
                    color:#94a3b8;">

                    {candidate["role"]}

                    </p>

                </div>

                <div style="

                width:90px;
                height:90px;

                border-radius:50%;

                border:6px solid #22c55e;

                display:flex;
                align-items:center;
                justify-content:center;

                font-size:28px;
                font-weight:800;

                color:white;

                ">

                {candidate["score"]}%

                </div>

            </div>

            <br>

            <div style="
            height:10px;
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

            <h4 style="color:white;">
            Matched Skills
            </h4>

            {matched_html}

            <br><br>

            <h4 style="color:white;">
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
                height=390,
                scrolling=False
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ==================================================
    # TABLE
    # ==================================================

    st.markdown("""
    <h2 style="color:white;">
    📋 All Results
    </h2>
    """, unsafe_allow_html=True)

    df = pd.DataFrame(data)

    st.dataframe(
        df,
        use_container_width=True
    )