import streamlit as st
import random
import json
import time
import datetime
from datetime import datetime, timedelta

# Initialize session state variables
if 'vocabulary_words' not in st.session_state:
    st.session_state.vocabulary_words = []

if 'learning_progress' not in st.session_state:
    st.session_state.learning_progress = {}
    
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = "input"  # Modes: input, learn, quiz, revise, story
    
if 'quiz_results' not in st.session_state:
    st.session_state.quiz_results = []
    
if 'current_word_index' not in st.session_state:
    st.session_state.current_word_index = 0
    
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = {}

if 'daily_challenge' not in st.session_state:
    st.session_state.daily_challenge = {}

if 'last_challenge_date' not in st.session_state:
    st.session_state.last_challenge_date = None

# Page title and description
st.title("AI Vocabulary Learning Tool")
st.write("Enhance your vocabulary with interactive AI-powered learning content")

# Sidebar navigation
st.sidebar.title("Navigation")
mode = st.sidebar.radio(
    "Select Mode",
    ["Input Words", "Learn Words", "Quiz Mode", "Revision", "Story Mode", "Daily Challenge"],
    index=0 if st.session_state.current_mode == "input" else 
           1 if st.session_state.current_mode == "learn" else
           2 if st.session_state.current_mode == "quiz" else
           3 if st.session_state.current_mode == "revise" else
           4 if st.session_state.current_mode == "story" else 5
)

# Update current mode based on sidebar selection
if mode == "Input Words":
    st.session_state.current_mode = "input"
elif mode == "Learn Words":
    st.session_state.current_mode = "learn"
elif mode == "Quiz Mode":
    st.session_state.current_mode = "quiz"
elif mode == "Revision":
    st.session_state.current_mode = "revise"
elif mode == "Story Mode":
    st.session_state.current_mode = "story"
elif mode == "Daily Challenge":
    st.session_state.current_mode = "challenge"

# Function to generate word content using AI
def generate_word_content(word):
    # This would normally call an AI API, but for now we'll simulate it
    # In a real implementation, this would use Gemini or HuggingFace LLMs
    
    # Simulate API call delay
    with st.spinner(f"Generating content for '{word}'..."):
        time.sleep(1)  # Simulating API call
        
        # Simulated content generation
        meaning = f"The meaning of {word}"
        sentences = [
            f"Here is a sentence using {word}.",
            f"Another example with {word} in context.",
            f"A third sentence demonstrating {word} usage."
        ]
        synonyms = [f"synonym1 of {word}", f"synonym2 of {word}", f"synonym3 of {word}"]
        antonyms = [f"antonym1 of {word}", f"antonym2 of {word}"]
        
        # Quiz questions
        multiple_choice = {
            "question": f"Which of the following best describes '{word}'?",
            "options": [meaning, "Incorrect meaning 1", "Incorrect meaning 2", "Incorrect meaning 3"],
            "answer": 0  # Index of correct answer
        }
        
        fill_blank = {
            "question": f"Complete the sentence: The _____ was evident in his speech.",
            "answer": word
        }
        
        word_meaning_match = {
            "word": word,
            "meaning": meaning,
            "decoys": [f"Fake meaning 1 for {word}", f"Fake meaning 2 for {word}"]
        }
        
        # Visual hint (emoji)
        emoji_hint = "📚"  # Default emoji
        
        return {
            "meaning": meaning,
            "sentences": sentences,
            "synonyms": synonyms,
            "antonyms": antonyms,
            "multiple_choice": multiple_choice,
            "fill_blank": fill_blank,
            "word_meaning_match": word_meaning_match,
            "emoji_hint": emoji_hint,
            "difficulty": random.randint(1, 5)  # Random difficulty from 1-5
        }

# Function to generate a story using the vocabulary words
def generate_story(words, theme="general"):
    # This would normally call an AI API, but for now we'll simulate it
    with st.spinner("Generating a story with your vocabulary words..."):
        time.sleep(2)  # Simulating API call
        
        # Simple story template with word placeholders
        story = f"Once upon a time, there was a person who was very {words[0] if len(words) > 0 else 'happy'}. "
        story += f"They lived in a {words[1] if len(words) > 1 else 'beautiful'} house. "
        story += f"Every day, they would {words[2] if len(words) > 2 else 'work'} diligently. "
        
        # Add more sentences using remaining words
        for i, word in enumerate(words[3:], start=3):
            story += f"One day, something {word} happened. "
            if i >= 10:  # Limit story length
                break
                
        story += "The end."
        
        # Highlight the vocabulary words in the story
        for word in words:
            story = story.replace(word, f"**{word}**")
            
        return story

# Function to create a daily challenge
def create_daily_challenge():
    # Check if we need to create a new challenge
    today = datetime.now().date()
    if st.session_state.last_challenge_date != today:
        # Create a new challenge using words from the user's vocabulary
        if len(st.session_state.vocabulary_words) >= 3:
            # Select 3 random words from the vocabulary
            challenge_words = random.sample(st.session_state.vocabulary_words, min(3, len(st.session_state.vocabulary_words)))
            
            # Create different types of challenges
            challenge_type = random.choice(["multiple_choice", "fill_blank", "matching"])
            
            if challenge_type == "multiple_choice":
                word = challenge_words[0]
                content = st.session_state.generated_content.get(word, generate_word_content(word))
                question = content["multiple_choice"]
                
                st.session_state.daily_challenge = {
                    "type": "multiple_choice",
                    "question": question["question"],
                    "options": question["options"],
                    "answer": question["answer"],
                    "word": word
                }
                
            elif challenge_type == "fill_blank":
                word = challenge_words[0]
                content = st.session_state.generated_content.get(word, generate_word_content(word))
                
                st.session_state.daily_challenge = {
                    "type": "fill_blank",
                    "question": f"Fill in the blank with the correct word: {content['fill_blank']['question']}",
                    "answer": word,
                    "word": word
                }
                
            elif challenge_type == "matching":
                matches = []
                for word in challenge_words:
                    content = st.session_state.generated_content.get(word, generate_word_content(word))
                    matches.append({"word": word, "meaning": content["meaning"]})
                    
                st.session_state.daily_challenge = {
                    "type": "matching",
                    "matches": matches,
                    "words": challenge_words
                }
            
            st.session_state.last_challenge_date = today
        else:
            st.session_state.daily_challenge = {
                "type": "message",
                "message": "Add at least 3 words to your vocabulary to unlock daily challenges!"
            }

# Function to update learning progress
def update_progress(word, activity, success=True):
    if word not in st.session_state.learning_progress:
        st.session_state.learning_progress[word] = {
            "exposure_count": 0,
            "success_count": 0,
            "last_reviewed": datetime.now().isoformat(),
            "next_review": (datetime.now() + timedelta(days=1)).isoformat(),
            "difficulty": 3  # Medium difficulty by default (1-5 scale)
        }
    
    progress = st.session_state.learning_progress[word]
    progress["exposure_count"] += 1
    
    if success:
        progress["success_count"] += 1
        # Decrease difficulty if consistently successful
        if progress["success_count"] > 3 and progress["difficulty"] > 1:
            progress["difficulty"] -= 1
    else:
        # Increase difficulty if unsuccessful
        if progress["difficulty"] < 5:
            progress["difficulty"] += 1
    
    # Update review schedule based on spaced repetition
    # Simple implementation: harder words reviewed sooner
    days_until_next_review = 7 // progress["difficulty"]
    progress["last_reviewed"] = datetime.now().isoformat()
    progress["next_review"] = (datetime.now() + timedelta(days=days_until_next_review)).isoformat()
    
    st.session_state.learning_progress[word] = progress

# Function to get words due for revision
def get_revision_words():
    revision_words = []
    now = datetime.now()
    
    for word, progress in st.session_state.learning_progress.items():
        next_review = datetime.fromisoformat(progress["next_review"])
        if next_review <= now:
            revision_words.append(word)
    
    return revision_words

# Input Words Mode
if st.session_state.current_mode == "input":
    st.header("Add New Words to Learn")
    
    # Input method selection
    input_method = st.radio("Select input method:", ["Enter words manually", "Upload word list"])
    
    if input_method == "Enter words manually":
        # Text area for entering words
        new_words_text = st.text_area("Enter words (one per line):", height=150)
        
        if st.button("Add Words"):
            if new_words_text.strip():
                # Process the input text
                new_words = [word.strip() for word in new_words_text.split('\n') if word.strip()]
                
                # Add new words to the vocabulary list
                for word in new_words:
                    if word and word not in st.session_state.vocabulary_words:
                        st.session_state.vocabulary_words.append(word)
                        # Generate content for the word
                        st.session_state.generated_content[word] = generate_word_content(word)
                
                st.success(f"Added {len(new_words)} new words to your vocabulary list!")
                st.session_state.current_mode = "learn"  # Switch to learn mode
            else:
                st.warning("Please enter at least one word.")
    
    else:  # Upload word list
        uploaded_file = st.file_uploader("Upload a text file with one word per line", type=["txt"])
        
        if uploaded_file is not None:
            # Read the file
            content = uploaded_file.read().decode("utf-8")
            words = [word.strip() for word in content.split('\n') if word.strip()]
            
            if st.button("Add Words from File"):
                # Add new words to the vocabulary list
                added_count = 0
                for word in words:
                    if word and word not in st.session_state.vocabulary_words:
                        st.session_state.vocabulary_words.append(word)
                        # Generate content for the word
                        st.session_state.generated_content[word] = generate_word_content(word)
                        added_count += 1
                
                st.success(f"Added {added_count} new words to your vocabulary list!")
                st.session_state.current_mode = "learn"  # Switch to learn mode
    
    # Display current vocabulary list
    if st.session_state.vocabulary_words:
        with st.expander("Your current vocabulary list"):
            for i, word in enumerate(st.session_state.vocabulary_words):
                st.write(f"{i+1}. {word}")

# Learn Words Mode
elif st.session_state.current_mode == "learn":
    st.header("Learn Your Vocabulary Words")
    
    if not st.session_state.vocabulary_words:
        st.warning("You haven't added any words yet. Please add words first.")
        st.session_state.current_mode = "input"  # Switch to input mode
    else:
        # Word selection
        word_index = st.selectbox(
            "Select a word to learn:",
            range(len(st.session_state.vocabulary_words)),
            format_func=lambda i: st.session_state.vocabulary_words[i],
            index=min(st.session_state.current_word_index, len(st.session_state.vocabulary_words)-1)
        )
        
        st.session_state.current_word_index = word_index
        current_word = st.session_state.vocabulary_words[word_index]
        
        # Get or generate content for the current word
        if current_word not in st.session_state.generated_content:
            st.session_state.generated_content[current_word] = generate_word_content(current_word)
        
        word_content = st.session_state.generated_content[current_word]
        
        # Display word content
        st.subheader(f"📝 {current_word.title()} {word_content['emoji_hint']}")
        
        # Meaning and examples
        st.markdown(f"**Meaning:** {word_content['meaning']}")
        
        st.markdown("**Example Sentences:**")
        for sentence in word_content['sentences']:
            st.markdown(f"- {sentence}")
        
        # Synonyms and antonyms
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Synonyms:**")
            for synonym in word_content['synonyms']:
                st.markdown(f"- {synonym}")
        
        with col2:
            st.markdown("**Antonyms:**")
            for antonym in word_content['antonyms']:
                st.markdown(f"- {antonym}")
        
        # Update progress for this word (exposure)
        update_progress(current_word, "learn")
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if word_index > 0:
                if st.button("⬅️ Previous Word"):
                    st.session_state.current_word_index = word_index - 1
                    st.experimental_rerun()
        
        with col2:
            if st.button("🎮 Quiz Me"):
                st.session_state.current_mode = "quiz"
                st.experimental_rerun()
        
        with col3:
            if word_index < len(st.session_state.vocabulary_words) - 1:
                if st.button("➡️ Next Word"):
                    st.session_state.current_word_index = word_index + 1
                    st.experimental_rerun()

# Quiz Mode
elif st.session_state.current_mode == "quiz":
    st.header("Test Your Knowledge")
    
    if not st.session_state.vocabulary_words:
        st.warning("You haven't added any words yet. Please add words first.")
        st.session_state.current_mode = "input"  # Switch to input mode
    else:
        # Get current word
        current_word = st.session_state.vocabulary_words[st.session_state.current_word_index]
        word_content = st.session_state.generated_content.get(current_word, generate_word_content(current_word))
        
        # Quiz type selection
        quiz_type = st.radio(
            "Select quiz type:",
            ["Multiple Choice", "Fill in the Blank", "Word-Meaning Matching"],
            index=0
        )
        
        # Multiple Choice Quiz
        if quiz_type == "Multiple Choice":
            st.subheader("Multiple Choice Question")
            
            question = word_content["multiple_choice"]
            st.markdown(question["question"])
            
            # Shuffle options
            options = question["options"].copy()
            correct_answer = options[question["answer"]]
            random.shuffle(options)
            
            # Display options as radio buttons
            user_answer = st.radio("Select the correct answer:", options, index=None)
            
            if st.button("Submit Answer"):
                if user_answer:
                    if user_answer == correct_answer:
                        st.success("Correct! 🎉")
                        update_progress(current_word, "quiz", success=True)
                    else:
                        st.error(f"Incorrect. The correct answer is: {correct_answer}")
                        update_progress(current_word, "quiz", success=False)
                else:
                    st.warning("Please select an answer.")
        
        # Fill in the Blank Quiz
        elif quiz_type == "Fill in the Blank":
            st.subheader("Fill in the Blank")
            
            question = word_content["fill_blank"]
            st.markdown(question["question"])
            
            user_answer = st.text_input("Your answer:")
            
            if st.button("Submit Answer"):
                if user_answer:
                    if user_answer.lower() == question["answer"].lower():
                        st.success("Correct! 🎉")
                        update_progress(current_word, "quiz", success=True)
                    else:
                        st.error(f"Incorrect. The correct answer is: {question['answer']}")
                        update_progress(current_word, "quiz", success=False)
                else:
                    st.warning("Please enter an answer.")
        
        # Word-Meaning Matching
        elif quiz_type == "Word-Meaning Matching":
            st.subheader("Match the Word to its Meaning")
            
            # Create a list of words and meanings
            match_data = word_content["word_meaning_match"]
            
            # Get some random words from vocabulary for decoys
            all_meanings = [match_data["meaning"]] + match_data["decoys"]
            random.shuffle(all_meanings)
            
            st.markdown(f"**Word:** {match_data['word']}")
            user_answer = st.radio("Select the correct meaning:", all_meanings, index=None)
            
            if st.button("Submit Answer"):
                if user_answer:
                    if user_answer == match_data["meaning"]:
                        st.success("Correct! 🎉")
                        update_progress(current_word, "quiz", success=True)
                    else:
                        st.error(f"Incorrect. The correct meaning is: {match_data['meaning']}")
                        update_progress(current_word, "quiz", success=False)
                else:
                    st.warning("Please select an answer.")
        
        # Navigation buttons
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("⬅️ Back to Learning"):
                st.session_state.current_mode = "learn"
                st.experimental_rerun()
        
        with col2:
            if st.button("Next Word ➡️"):
                # Move to the next word or wrap around
                next_index = (st.session_state.current_word_index + 1) % len(st.session_state.vocabulary_words)
                st.session_state.current_word_index = next_index
                st.experimental_rerun()

# Revision Mode
elif st.session_state.current_mode == "revise":
    st.header("Revision Mode")
    
    # Get words due for revision
    revision_words = get_revision_words()
    
    if not revision_words:
        st.info("No words are due for revision at this time.")
        
        # Show all words with their next review date
        if st.session_state.learning_progress:
            st.subheader("Your vocabulary review schedule:")
            
            # Create a dataframe for better display
            review_data = []
            for word, progress in st.session_state.learning_progress.items():
                next_review = datetime.fromisoformat(progress["next_review"])
                days_until = (next_review - datetime.now()).days
                review_data.append({
                    "Word": word,
                    "Next Review": next_review.strftime("%Y-%m-%d"),
                    "Days Until Review": max(0, days_until),
                    "Difficulty Level": progress["difficulty"],
                    "Times Reviewed": progress["exposure_count"]
                })
            
            # Sort by next review date
            review_data.sort(key=lambda x: x["Days Until Review"])
            
            # Display as a table
            for item in review_data:
                st.markdown(f"**{item['Word']}** - Next review: {item['Next Review']} ({item['Days Until Review']} days) - Difficulty: {item['Difficulty Level']}/5")
        
        else:
            st.warning("You haven't learned any words yet. Please add and learn words first.")
    
    else:
        st.success(f"You have {len(revision_words)} words due for revision!")
        
        # Select a word to revise
        if "revision_index" not in st.session_state:
            st.session_state.revision_index = 0
        
        current_index = min(st.session_state.revision_index, len(revision_words) - 1)
        current_word = revision_words[current_index]
        
        # Display word for revision
        word_content = st.session_state.generated_content.get(current_word, generate_word_content(current_word))
        
        st.subheader(f"Revising: {current_word}")
        
        # Simple revision quiz
        options = [word_content["meaning"]] + [f"Incorrect meaning for {current_word}"] * 3
        random.shuffle(options)
        correct_index = options.index(word_content["meaning"])
        
        user_answer = st.radio(f"What is the meaning of '{current_word}'?", options, index=None)
        
        if st.button("Check Answer"):
            if user_answer:
                if user_answer == word_content["meaning"]:
                    st.success("Correct! You remembered this word well.")
                    update_progress(current_word, "revision", success=True)
                else:
                    st.error(f"Incorrect. The correct meaning is: {word_content['meaning']}")
                    update_progress(current_word, "revision", success=False)
                    
                # Show the full word details for reinforcement
                with st.expander("Word details", expanded=True):
                    st.markdown(f"**Meaning:** {word_content['meaning']}")
                    
                    st.markdown("**Example Sentences:**")
                    for sentence in word_content['sentences']:
                        st.markdown(f"- {sentence}")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Synonyms:**")
                        for synonym in word_content['synonyms']:
                            st.markdown(f"- {synonym}")
                    
                    with col2:
                        st.markdown("**Antonyms:**")
                        for antonym in word_content['antonyms']:
                            st.markdown(f"- {antonym}")
            else:
                st.warning("Please select an answer.")
        
        # Navigation buttons
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            if current_index > 0:
                if st.button("⬅️ Previous Word"):
                    st.session_state.revision_index = current_index - 1
                    st.experimental_rerun()
        
        with col2:
            if current_index < len(revision_words) - 1:
                if st.button("Next Word ➡️"):
                    st.session_state.revision_index = current_index + 1
                    st.experimental_rerun()

# Story Mode
elif st.session_state.current_mode == "story":
    st.header("Story Mode")
    
    if len(st.session_state.vocabulary_words) < 3:
        st.warning("You need at least 3 words in your vocabulary to generate a story. Please add more words.")
    else:
        # Story theme selection
        theme = st.selectbox(
            "Select a theme for your story:",
            ["Adventure", "Mystery", "Romance", "Science Fiction", "Fantasy", "Historical"],
            index=0
        )
        
        # Word selection
        st.subheader("Select words to include in your story:")
        selected_words = []
        
        # Create columns for word selection checkboxes
        cols = st.columns(3)
        for i, word in enumerate(st.session_state.vocabulary_words):
            with cols[i % 3]:
                if st.checkbox(word, key=f"story_word_{i}"):
                    selected_words.append(word)
        
        if st.button("Generate Story") and selected_words:
            # Generate a story with the selected words
            story = generate_story(selected_words, theme.lower())
            
            # Display the story
            st.subheader(f"Your {theme} Story")
            st.markdown(story)
            
            # Download button for the story
            st.download_button(
                label="Download Story",
                data=story,
                file_name=f"{theme.lower()}_story.txt",
                mime="text/plain"
            )
            
            # Update progress for all words used in the story
            for word in selected_words:
                update_progress(word, "story")
        
        elif st.button("Generate Story") and not selected_words:
            st.warning("Please select at least one word for your story.")

# Daily Challenge Mode
elif st.session_state.current_mode == "challenge":
    st.header("Daily Challenge")
    
    # Create a daily challenge if needed
    create_daily_challenge()
    
    challenge = st.session_state.daily_challenge
    
    if challenge.get("type") == "message":
        st.info(challenge["message"])
    
    elif challenge.get("type") == "multiple_choice":
        st.subheader("Today's Challenge: Multiple Choice")
        st.markdown(challenge["question"])
        
        options = challenge["options"]
        user_answer = st.radio("Select your answer:", options, index=None)
        
        if st.button("Submit Answer"):
            if user_answer:
                correct_answer = options[challenge["answer"]]
                if user_answer == correct_answer:
                    st.success("Correct! You've completed today's challenge! 🎉")
                    update_progress(challenge["word"], "challenge", success=True)
                else:
                    st.error(f"Incorrect. The correct answer is: {correct_answer}")
                    update_progress(challenge["word"], "challenge", success=False)
            else:
                st.warning("Please select an answer.")
    
    elif challenge.get("type") == "fill_blank":
        st.subheader("Today's Challenge: Fill in the Blank")
        st.markdown(challenge["question"])
        
        user_answer = st.text_input("Your answer:")
        
        if st.button("Submit Answer"):
            if user_answer:
                if user_answer.lower() == challenge["answer"].lower():
                    st.success("Correct! You've completed today's challenge! 🎉")
                    update_progress(challenge["word"], "challenge", success=True)
                else:
                    st.error(f"Incorrect. The correct answer is: {challenge['answer']}")
                    update_progress(challenge["word"], "challenge", success=False)
            else:
                st.warning("Please enter an answer.")
    
    elif challenge.get("type") == "matching":
        st.subheader("Today's Challenge: Word-Meaning Matching")
        
        matches = challenge["matches"]
        words = [match["word"] for match in matches]
        meanings = [match["meaning"] for match in matches]
        
        # Shuffle meanings
        shuffled_meanings = meanings.copy()
        random.shuffle(shuffled_meanings)
        
        # Create a dictionary to store user's matches
        if "user_matches" not in st.session_state:
            st.session_state.user_matches = {word: "" for word in words}
        
        # Display matching interface
        st.markdown("Match each word with its correct meaning:")
        
        for i, word in enumerate(words):
            st.session_state.user_matches[word] = st.selectbox(
                f"Meaning of '{word}':",
                ["Select a meaning..."] + shuffled_meanings,
                index=0,
                key=f"match_{i}"
            )
        
        if st.button("Submit Matches"):
            # Check if all words have been matched
            if all(match != "Select a meaning..." for match in st.session_state.user_matches.values()):
                # Check correctness
                correct_count = 0
                for match in matches:
                    if st.session_state.user_matches[match["word"]] == match["meaning"]:
                        correct_count += 1
                
                if correct_count == len(matches):
                    st.success("Perfect! You've completed today's challenge! 🎉")
                    for word in words:
                        update_progress(word, "challenge", success=True)
                else:
                    st.warning(f"You got {correct_count} out of {len(matches)} correct.")
                    
                    # Show correct answers
                    st.subheader("Correct Matches:")
                    for match in matches:
                        st.markdown(f"**{match['word']}**: {match['meaning']}")
                    
                    # Update progress for each word
                    for word in words:
                        correct = False
                        for match in matches:
                            if match["word"] == word and st.session_state.user_matches[word] == match["meaning"]:
                                correct = True
                                break
                        update_progress(word, "challenge", success=correct)
            else:
                st.warning("Please match all words with their meanings.")

# Display statistics in the sidebar
if st.session_state.vocabulary_words:
    st.sidebar.markdown("---")
    st.sidebar.subheader("Your Progress")
    st.sidebar.markdown(f"**Total Words:** {len(st.session_state.vocabulary_words)}")
    
    if st.session_state.learning_progress:
        # Calculate mastery levels
        mastery_levels = {"Beginner": 0, "Intermediate": 0, "Advanced": 0, "Mastered": 0}
        
        for word, progress in st.session_state.learning_progress.items():
            ratio = progress["success_count"] / max(1, progress["exposure_count"])
            
            if ratio < 0.25:
                mastery_levels["Beginner"] += 1
            elif ratio < 0.5:
                mastery_levels["Intermediate"] += 1
            elif ratio < 0.75:
                mastery_levels["Advanced"] += 1
            else:
                mastery_levels["Mastered"] += 1
        
        # Display mastery levels
        for level, count in mastery_levels.items():
            if count > 0:
                st.sidebar.markdown(f"**{level}:** {count} words")
    
    # Option to clear all data
    st.sidebar.markdown("---")
    if st.sidebar.button("Reset All Data"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

# Add a footer
st.markdown("---")
st.markdown("*Powered by AI - Enhance your vocabulary learning experience*")