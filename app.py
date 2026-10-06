import streamlit as st
import sqlite3
import os
from datetime import datetime
import re


# =====================================================
# DATABASE SETUP
# =====================================================

DB_PATH = os.path.join(
    "data",
    "reading_history_new.sqlite"
)


def database_setup():

    os.makedirs("data", exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reading_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            text_title TEXT,
            reading_duration INTEGER,
            word_count INTEGER,
            completed TEXT
        )
    """)

    connection.commit()
    connection.close()


# Create database
database_setup()


# =====================================================
# SAVE READING PROGRESS
# =====================================================

def save_reading_progress(
    title,
    duration,
    word_count,
    completed
):

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO reading_history
        (
            date,
            text_title,
            reading_duration,
            word_count,
            completed
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            title,
            duration,
            word_count,
            completed
        )
    )

    connection.commit()
    connection.close()


# =====================================================
# GET READING HISTORY
# =====================================================

def get_reading_history():

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            date,
            text_title,
            reading_duration,
            word_count,
            completed
        FROM reading_history
        ORDER BY id DESC
        """
    )

    records = cursor.fetchall()

    connection.close()

    return records


# =====================================================
# AI TEXT SIMPLIFICATION
# =====================================================

def ai_simplification(text):

    replacements = {
        "approximately": "about",
        "assist": "help",
        "assistance": "help",
        "commence": "start",
        "demonstrate": "show",
        "difficult": "hard",
        "essential": "important",
        "frequently": "often",
        "obtain": "get",
        "purchase": "buy",
        "require": "need",
        "required": "needed",
        "utilize": "use",
        "numerous": "many",
        "individuals": "people",
        "information": "details",
        "additional": "extra",
        "therefore": "so",
        "however": "but",
        "construct": "build",
        "modify": "change",
        "objective": "goal",
        "complicated": "hard",
        "assistance": "help",
        "sufficient": "enough",
        "components": "parts",
        "functionality": "function",
        "implementation": "use",
        "approximately": "about"
    }

    simplified_text = text

    for difficult_word, simple_word in replacements.items():

        pattern = r"\b" + re.escape(difficult_word) + r"\b"

        simplified_text = re.sub(
            pattern,
            simple_word,
            simplified_text,
            flags=re.IGNORECASE
        )

    return simplified_text


# =====================================================
# DIFFICULT WORD DETECTION
# =====================================================

def difficult_words(text):

    simple_meanings = {
        "approximately": "about",
        "assist": "help",
        "assistance": "help",
        "commence": "start",
        "demonstrate": "show",
        "difficult": "hard",
        "essential": "important",
        "frequently": "often",
        "obtain": "get",
        "purchase": "buy",
        "require": "need",
        "required": "needed",
        "utilize": "use",
        "numerous": "many",
        "individuals": "people",
        "information": "details",
        "additional": "extra",
        "therefore": "so",
        "however": "but",
        "construct": "build",
        "modify": "change",
        "objective": "goal",
        "complicated": "hard",
        "sufficient": "enough",
        "components": "parts",
        "functionality": "function",
        "implementation": "use"
    }

    words = text.split()

    difficult = []

    for word in words:

        clean_word = word.strip(
            ".,!?;:()[]{}\"'"
        ).lower()

        if len(clean_word) >= 10:

            meaning = simple_meanings.get(
                clean_word,
                "Simple meaning not available"
            )

            difficult.append(
                (clean_word, meaning)
            )

    return list(dict.fromkeys(difficult))


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Dyslexia Reading Support",
    page_icon="📖",
    layout="wide"
)


# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("📖 Dyslexia Support")

page = st.sidebar.radio(
    "Select a Feature",
    [
        "🏠 Home",
        "📖 Reading Support",
        "✨ Text Adaptation",
        "🤖 AI Simplification",
        "🔎 Difficult Words",
        "🎯 Focus Reading",
        "🔊 Text-to-Speech",
        "📊 Reading Progress",
        "⚙️ Settings"
    ]
)


# =====================================================
# HOME DASHBOARD
# =====================================================

if page == "🏠 Home":

    st.title(
        "📖 Dyslexia-Friendly Reading Support"
    )

    st.subheader(
        "Read • Understand • Learn"
    )

    st.write(
        "A simple reading support system designed "
        "to make digital text easier and more "
        "comfortable to read."
    )

    st.divider()

    st.info(
        "💡 Dyslexia is a learning difference that "
        "can make reading, spelling, and processing "
        "written words more difficult."
    )

    st.subheader("🚀 What can you do?")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 📖 Reading Support")

        st.write(
            "• Type or paste reading material"
        )

        st.write(
            "• Upload TXT files"
        )

        st.write(
            "• Count words automatically"
        )

        st.markdown("### ✨ Text Adaptation")

        st.write(
            "• Change font size settings"
        )

        st.write(
            "• Adjust line spacing"
        )

        st.write(
            "• Adjust letter and word spacing"
        )

        st.markdown("### 🎯 Focus Reading")

        st.write(
            "• Read one paragraph at a time"
        )

        st.write(
            "• Reduce distractions"
        )

    with col2:

        st.markdown("### 🤖 AI Simplification")

        st.write(
            "• Convert difficult words into simpler words"
        )

        st.write(
            "• Make text easier to understand"
        )

        st.markdown("### 🔎 Difficult Words")

        st.write(
            "• Detect long words"
        )

        st.write(
            "• Show simple meanings"
        )

        st.markdown("### 📊 Reading Progress")

        st.write(
            "• Save reading sessions"
        )

        st.write(
            "• Track duration and word count"
        )

    st.divider()

    st.subheader("🛠️ How to Start")

    st.write(
        "1️⃣ Go to Reading Support and enter your text."
    )

    st.write(
        "2️⃣ Use Text Adaptation to customize reading."
    )

    st.write(
        "3️⃣ Use AI Simplification for easier English."
    )

    st.write(
        "4️⃣ Use Focus Reading to read paragraph by paragraph."
    )

    st.write(
        "5️⃣ Use Text-to-Speech to listen to the text."
    )

    st.write(
        "6️⃣ Check Reading Progress to save your activity."
    )

    st.success(
        "🌟 Your comfortable reading experience starts here!"
    )


# =====================================================
# READING SUPPORT
# =====================================================

elif page == "📖 Reading Support":

    st.title("📖 Reading Support")

    st.write(
        "Enter or upload your reading material."
    )

    st.divider()

    st.subheader("📝 Type or Paste Text")

    typed_text = st.text_area(
        "Enter your text:",
        height=250,
        placeholder="Type or paste your reading material here..."
    )

    st.divider()

    st.subheader("📂 Upload TXT File")

    uploaded_file = st.file_uploader(
        "Choose a .txt file",
        type=["txt"]
    )

    uploaded_text = ""

    if uploaded_file is not None:

        try:

            uploaded_text = uploaded_file.read().decode(
                "utf-8"
            )

            st.success(
                "✅ File uploaded successfully!"
            )

        except Exception:

            st.error(
                "❌ Could not read this file."
            )

    if typed_text.strip():

        final_text = typed_text

    elif uploaded_text.strip():

        final_text = uploaded_text

    else:

        final_text = ""

    if final_text:

        st.session_state["reading_text"] = final_text

        st.subheader("📖 Your Reading Text")

        st.text_area(
            "Reading Material:",
            value=final_text,
            height=300
        )

        word_count = len(
            final_text.split()
        )

        st.success(
            f"🔤 Word Count: {word_count}"
        )

    else:

        st.warning(
            "Please enter text or upload a TXT file."
        )

# =====================================================
# TEXT ADAPTATION
# =====================================================

elif page == "✨ Text Adaptation":

    st.title(
        "✨ Dyslexia-Friendly Text Adaptation"
    )

    st.write(
        "Customize your reading experience "
        "using the settings you saved."
    )

    st.divider()

    reading_text = st.session_state.get(
        "reading_text",
        ""
    )

    if not reading_text:

        st.warning(
            "⚠️ No text found."
        )

        st.info(
            "Go to Reading Support first "
            "and enter your reading material."
        )

    else:

        st.subheader("📖 Reading Preview")

        # Get saved settings
        font_size = st.session_state.get(
            "font_size",
            24
        )

        line_spacing = st.session_state.get(
            "line_spacing",
            1.8
        )

        letter_spacing = st.session_state.get(
            "letter_spacing",
            2
        )

        word_spacing = st.session_state.get(
            "word_spacing",
            5
        )

        background_color = st.session_state.get(
            "background_color",
            "#FFF8E7"
        )

        text_color = st.session_state.get(
            "text_color",
            "#222222"
        )

        st.info(
            "Your saved reading settings are shown below."
        )

        st.write(
            f"🔠 Font Size: {font_size}px"
        )

        st.write(
            f"↕️ Line Spacing: {line_spacing}"
        )

        st.write(
            f"↔️ Letter Spacing: {letter_spacing}px"
        )

        st.write(
            f"🔡 Word Spacing: {word_spacing}px"
        )

        st.write(
            f"🎨 Background: {background_color}"
        )

        st.write(
            f"🖊️ Text Color: {text_color}"
        )

        st.divider()

        st.subheader("📚 Your Reading Text")

        st.text_area(
            "Adapted Reading Text:",
            value=reading_text,
            height=400
        )

        st.success(
            "✅ Your saved reading settings are ready."
        )

        st.info(
            "💡 You can change these settings "
            "anytime from the Settings page."
        )

# =====================================================
# AI SIMPLIFICATION
# =====================================================

elif page == "🤖 AI Simplification":

    st.title("🤖 AI Text Simplification")

    st.write(
        "Convert difficult words into simpler English."
    )

    st.divider()

    reading_text = st.session_state.get(
        "reading_text",
        ""
    )

    if not reading_text:

        st.warning(
            "⚠️ No text found."
        )

        st.info(
            "Go to Reading Support first and enter text."
        )

    else:

        st.subheader("📄 Original Text")

        st.text_area(
            "Original:",
            value=reading_text,
            height=220,
            disabled=True
        )

        st.divider()

        simplified_text = ai_simplification(
            reading_text
        )

        st.subheader("✨ Simplified Text")

        st.text_area(
            "Simple English:",
            value=simplified_text,
            height=220
        )

        st.success(
            "✅ Text has been simplified successfully!"
        )


# =====================================================
# DIFFICULT WORDS
# =====================================================

elif page == "🔎 Difficult Words":

    st.title("🔎 Difficult Word Detection")

    st.write(
        "This feature identifies long or difficult "
        "words and provides simpler meanings."
    )

    st.divider()

    reading_text = st.session_state.get(
        "reading_text",
        ""
    )

    if not reading_text:

        st.warning(
            "⚠️ No text found."
        )

        st.info(
            "Go to Reading Support first and enter text."
        )

    else:

        st.subheader("📄 Your Text")

        st.text_area(
            "Reading Text:",
            value=reading_text,
            height=200,
            disabled=True
        )

        difficult = difficult_words(
            reading_text
        )

        st.divider()

        st.subheader("📚 Difficult Words")

        if difficult:

            for word, meaning in difficult:

                st.write(
                    f"🔴 **{word}** → {meaning}"
                )

        else:

            st.success(
                "🎉 No difficult words detected!"
            )


# =====================================================
# FOCUS READING
# =====================================================

elif page == "🎯 Focus Reading":

    st.title("🎯 Focus Reading Mode")

    st.write(
        "Read one paragraph at a time "
        "to improve concentration."
    )

    st.divider()

    reading_text = st.session_state.get(
        "reading_text",
        ""
    )

    if not reading_text:

        st.warning(
            "⚠️ No text found."
        )

        st.info(
            "Go to Reading Support first and enter text."
        )

    else:

        paragraphs = [
            paragraph.strip()
            for paragraph in reading_text.split("\n")
            if paragraph.strip()
        ]

        if paragraphs:

            st.subheader("📖 Focus Reading")

            paragraph_number = st.number_input(
                "Select Paragraph",
                min_value=1,
                max_value=len(paragraphs),
                value=1,
                step=1
            )

            current_paragraph = paragraphs[
                paragraph_number - 1
            ]

            st.info(
                f"Paragraph {paragraph_number} "
                f"of {len(paragraphs)}"
            )

            st.subheader("📚 Read This")

            st.write(
                current_paragraph
            )

            st.divider()

            if paragraph_number == len(paragraphs):

                st.success(
                    "🎉 You reached the end of the text!"
                )

            else:

                st.info(
                    "➡️ Select the next paragraph above "
                    "when you are ready."
                )

        else:

            st.warning(
                "No paragraphs found."
            )


# =====================================================
# TEXT-TO-SPEECH
# =====================================================

elif page == "🔊 Text-to-Speech":

    st.title("🔊 Text-to-Speech")

    st.write(
        "Listen to your reading material aloud."
    )

    st.divider()

    reading_text = st.session_state.get(
        "reading_text",
        ""
    )

    if not reading_text:

        st.warning(
            "⚠️ No text found."
        )

        st.info(
            "Go to Reading Support first and enter text."
        )

    else:

        st.subheader("📖 Text to Read")

        st.text_area(
            "Reading Text:",
            value=reading_text,
            height=250,
            disabled=True
        )

        reading_speed = st.slider(
            "🔊 Reading Speed",
            50,
            200,
            st.session_state.get(
                "reading_speed",
                100
            ),
            10
        )

        st.info(
            f"Reading speed: {reading_speed}"
        )

        st.write(
            "Text-to-speech setup is available through "
            "the pyttsx3 package."
        )

        if st.button("🔊 Prepare Audio"):

            try:

                import pyttsx3

                engine = pyttsx3.init()

                engine.setProperty(
                    "rate",
                    reading_speed
                )

                audio_path = os.path.join(
                    "data",
                    "reading_audio.wav"
                )

                engine.save_to_file(
                    reading_text,
                    audio_path
                )

                engine.runAndWait()

                if os.path.exists(audio_path):

                    st.audio(
                        audio_path,
                        format="audio/wav"
                    )

                    st.success(
                        "✅ Audio generated successfully!"
                    )

                else:

                    st.error(
                        "❌ Audio file could not be created."
                    )

            except Exception as error:

                st.error(
                    "❌ Text-to-speech error."
                )

                st.write(
                    str(error)
                )


# =====================================================
# READING PROGRESS
# =====================================================

elif page == "📊 Reading Progress":

    st.title("📊 Reading Progress")

    st.write(
        "Track your reading activity and progress."
    )

    st.divider()

    reading_text = st.session_state.get(
        "reading_text",
        ""
    )

    if reading_text:

        st.subheader("📝 Save Current Reading")

        title = st.text_input(
            "Text Title",
            value="My Reading"
        )

        duration = st.number_input(
            "Reading Duration (minutes)",
            min_value=1,
            max_value=300,
            value=5
        )

        word_count = len(
            reading_text.split()
        )

        st.info(
            f"🔤 Word Count: {word_count}"
        )

        completed = st.selectbox(
            "Reading Status",
            [
                "Completed",
                "Not Completed"
            ]
        )

        if st.button(
            "💾 Save Reading Progress"
        ):

            save_reading_progress(
                title,
                duration,
                word_count,
                completed
            )

            st.success(
                "✅ Reading progress saved successfully!"
            )

    else:

        st.info(
            "Go to Reading Support and enter text first."
        )

    st.divider()

    st.subheader("📚 Reading History")

    records = get_reading_history()

    if records:

        for record in records:

            date = record[0]
            title = record[1]
            duration = record[2]
            words = record[3]
            status = record[4]

            st.write(
                f"📅 **{date}**"
            )

            st.write(
                f"📖 Title: {title}"
            )

            st.write(
                f"⏱️ Duration: {duration} minutes"
            )

            st.write(
                f"🔤 Words: {words}"
            )

            st.write(
                f"✅ Status: {status}"
            )

            st.divider()

    else:

        st.info(
            "No reading history available yet."
        )


# =====================================================
# SETTINGS
# =====================================================

elif page == "⚙️ Settings":

    st.title("⚙️ Reading Settings")

    st.write(
        "Customize your reading experience."
    )

    st.divider()

    st.subheader("🔠 Text Settings")

    font_size = st.slider(
        "Font Size",
        16,
        40,
        st.session_state.get(
            "font_size",
            24
        )
    )

    line_spacing = st.slider(
        "Line Spacing",
        1.0,
        3.0,
        st.session_state.get(
            "line_spacing",
            1.8
        ),
        0.1
    )

    letter_spacing = st.slider(
        "Letter Spacing",
        0,
        10,
        st.session_state.get(
            "letter_spacing",
            2
        )
    )

    word_spacing = st.slider(
        "Word Spacing",
        0,
        20,
        st.session_state.get(
            "word_spacing",
            5
        )
    )

    st.divider()

    st.subheader("🎨 Color Settings")

    background_color = st.color_picker(
        "Background Color",
        st.session_state.get(
            "background_color",
            "#FFF8E7"
        )
    )

    text_color = st.color_picker(
        "Text Color",
        st.session_state.get(
            "text_color",
            "#222222"
        )
    )

    st.divider()

    st.subheader("🔊 Reading Settings")

    reading_speed = st.slider(
        "Reading Speed",
        50,
        200,
        st.session_state.get(
            "reading_speed",
            100
        ),
        10
    )

    st.divider()

    if st.button("💾 Save Settings"):

        st.session_state["font_size"] = font_size
        st.session_state["line_spacing"] = line_spacing
        st.session_state["letter_spacing"] = letter_spacing
        st.session_state["word_spacing"] = word_spacing
        st.session_state["background_color"] = background_color
        st.session_state["text_color"] = text_color
        st.session_state["reading_speed"] = reading_speed

        st.success(
            "✅ Settings saved successfully!"
        )

    st.divider()

    st.subheader("👀 Current Settings")

    st.write(
        f"🔠 Font Size: {font_size}px"
    )

    st.write(
        f"↕️ Line Spacing: {line_spacing}"
    )

    st.write(
        f"↔️ Letter Spacing: {letter_spacing}px"
    )

    st.write(
        f"🔡 Word Spacing: {word_spacing}px"
    )

    st.write(
        f"🎨 Background: {background_color}"
    )

    st.write(
        f"🖊️ Text Color: {text_color}"
    )

    st.write(
        f"🔊 Reading Speed: {reading_speed}"
    )

    st.success(
        "🌟 Settings are saved for this session."
    )