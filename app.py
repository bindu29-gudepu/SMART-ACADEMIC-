import streamlit as st
import pandas as pd
import urllib.parse
from curriculum import curriculum
from quiz_engine import generate_quiz, get_auto_difficulty
import os

st.set_page_config(page_title="Smart Academic Platform", layout="wide")

st.title("🎓 Student Comfort Learning Platform")

# -------- ENTER NAME --------
name = st.text_input("Enter Your Name")

if name:

    # ========== LEFT & RIGHT COLUMNS ==========
    left, right = st.columns([1,2])

    # ================= LEFT PANEL =================
    with left:

        st.header("👤 Student Preferences")

        selected_class = st.radio(
            "Select Class",
            list(curriculum.keys())
        )

        comfortable_language = st.radio(
            "Select Comfortable Language",
            ["Telugu","Hindi","English"]
        )

        preferred_style = st.radio(
            "Preferred Learning Style",
            ["Video","Text (PDF Material)"]
        )

    # ================= RIGHT PANEL =================
    with right:

        st.header("📚 Learning Section")

        selected_subject = st.selectbox(
            "Select Subject",
            list(curriculum[selected_class].keys())
        )

        lessons = curriculum[selected_class][selected_subject]

        selected_lesson = st.selectbox("Select Lesson", lessons)

        if selected_lesson:

            st.subheader(f"📖 {selected_lesson}")

            # ===== VIDEO OPTION =====
            if preferred_style == "Video":
                query = f"{selected_class} {selected_subject} {selected_lesson} {comfortable_language}"
                encoded = urllib.parse.quote(query)
                youtube_link = f"https://www.youtube.com/results?search_query={encoded}"
                st.markdown(f"🎥 Watch Lesson Video: [Click Here]({youtube_link})")

            # ===== TEXT PDF OPTION =====
            else:
                st.info("📄 Text Material (PDF)")
                pdf_path = "pdf_materials/sample.pdf"

                if os.path.exists(pdf_path):
                    with open(pdf_path, "rb") as pdf_file:
                        st.download_button(
                            label="Download PDF Material",
                            data=pdf_file,
                            file_name="Lesson_Material.pdf",
                            mime="application/pdf"
                        )
                else:
                    st.warning("PDF not found. Add lesson PDF inside pdf_materials folder.")

            st.markdown("---")

            # ================= AI DIFFICULTY =================
            previous_score = 0

            try:
                old = pd.read_csv("scores.csv")
                student_records = old[old["Name"] == name]
                if not student_records.empty:
                    previous_score = student_records.iloc[-1]["Percentage"]
            except:
                pass

            difficulty = get_auto_difficulty(previous_score)

            st.write("🤖 AI Selected Difficulty Level:", difficulty)

            # ================= QUIZ =================
            st.subheader("📝 8 MCQ Questions")

            questions = generate_quiz(selected_lesson, difficulty)

            score = 0

            for i, q in enumerate(questions):
                user_answer = st.radio(
                    q["question"],
                    q["options"],
                    key=f"q{i}"
                )

                if user_answer == q["answer"]:
                    score += 1

            if st.button("Submit Quiz"):

                percentage = (score / 8) * 100

                st.success(f"Score: {score}/8")
                st.info(f"Percentage: {percentage}%")

                data = {
                    "Name": name,
                    "Class": selected_class,
                    "Subject": selected_subject,
                    "Lesson": selected_lesson,
                    "Difficulty": difficulty,
                    "Score": score,
                    "Percentage": percentage
                }

                df = pd.DataFrame([data])

                try:
                    old = pd.read_csv("scores.csv")
                    df = pd.concat([old, df], ignore_index=True)
                except:
                    pass

                df.to_csv("scores.csv", index=False)

    # ================= DASHBOARD =================
    st.markdown("---")
    st.header("📊 Student Performance Dashboard")

    try:
        df = pd.read_csv("scores.csv")
        student_data = df[df["Name"] == name]
        st.dataframe(student_data)
    except:
        st.info("No records yet.")

else:
    st.warning("Please enter your name to continue.")
