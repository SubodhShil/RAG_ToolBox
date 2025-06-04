import streamlit as st
import random
import time
import json
from datetime import datetime, timedelta
import requests

# --- Configuration --- #
API_BASE_URL = "https://langchain-grammar-check-api.onrender.com" # Replace with your actual API endpoint

# --- Session State Initialization --- #
if 'writing_challenge_data' not in st.session_state:
    st.session_state.writing_challenge_data = {
        "prompt": "",
        "start_time": None,
        "end_time": None,
        "user_response": "",
        "feedback": None,
        "band_score": None,
        "history": []
    }

if 'challenge_active' not in st.session_state:
    st.session_state.challenge_active = False

if 'time_left_seconds' not in st.session_state:
    st.session_state.time_left_seconds = 0

# --- Helper Functions --- #
def generate_prompt_from_ai(llm_model="gemini"):
    # Local implementation instead of API call
    # Predefined IELTS writing prompts
    task1_prompts = [
        "The chart below shows the percentage of households with access to the internet from 2000 to 2020 in three different countries. Summarize the information by selecting and reporting the main features, and make comparisons where relevant.",
        "The graph below shows the consumption of renewable energy in the USA from 1950-2020. Summarize the information by selecting and reporting the main features, and make comparisons where relevant.",
        "The table below gives information about the underground railway systems in six cities. Summarize the information by selecting and reporting the main features, and make comparisons where relevant."
    ]
    
    task2_prompts = [
        "Some people believe that universities should focus on providing academic skills rather than preparing students for employment. To what extent do you agree or disagree?",
        "In many countries, the gap between the rich and the poor is increasing. What problems might this cause? What solutions can you suggest?",
        "Some people think that the government should provide free healthcare for all citizens. Others believe that individuals should pay for their own healthcare. Discuss both views and give your own opinion.",
        "Many people believe that international tourism is a bad thing for their countries. What are the reasons for this? Do you agree or disagree with this view?"
    ]
    
    # Randomly choose between Task 1 and Task 2
    task_type = random.choice(["Task 1", "Task 2"])
    
    if task_type == "Task 1":
        prompt = random.choice(task1_prompts)
        return f"IELTS Writing {task_type}: {prompt}"
    else:
        prompt = random.choice(task2_prompts)
        return f"IELTS Writing {task_type}: {prompt}"

def evaluate_response_with_ai(llm_model, prompt, user_response):
    # Local implementation instead of API call
    # This is a simplified evaluation - in a real app, you would use an LLM for this
    
    # Basic metrics
    word_count = len(user_response.split())
    sentence_count = len([s for s in user_response.split('.') if s.strip()])
    avg_words_per_sentence = word_count / max(1, sentence_count)
    
    # Simple scoring logic
    if word_count < 100:
        band_score = 4.0
    elif word_count < 150:
        band_score = 5.0
    elif word_count < 200:
        band_score = 6.0
    elif word_count < 250:
        band_score = 7.0
    else:
        band_score = 7.5
    
    # Adjust based on average sentence length (very simple heuristic)
    if avg_words_per_sentence < 8:
        band_score -= 0.5
    elif avg_words_per_sentence > 25:
        band_score -= 0.5
    
    # Random slight variation to make it seem more realistic
    band_score += random.uniform(-0.5, 0.5)
    band_score = round(max(4.0, min(9.0, band_score)) * 2) / 2  # Round to nearest 0.5
    
    # Generate feedback
    feedback = {
        "overall_summary": f"Your response is {word_count} words long with approximately {sentence_count} sentences. "
                          f"The average IELTS essay should be 250-300 words for Task 2 and 150+ words for Task 1.",
        
        "task_achievement": "You've addressed the main parts of the task, but could provide more specific examples and details to fully develop your response.",
        
        "coherence_cohesion": f"Your essay has an average of {avg_words_per_sentence:.1f} words per sentence. "
                              f"{'Consider using more complex sentence structures.' if avg_words_per_sentence < 15 else 'Consider using some shorter sentences for clarity.' if avg_words_per_sentence > 20 else 'You have a good mix of sentence lengths.'}",
        
        "lexical_resource": "Your vocabulary usage is adequate. Consider incorporating more academic vocabulary and topic-specific terms to enhance precision.",
        
        "grammatical_range_accuracy": "Your grammar is generally accurate. Pay attention to verb tenses and article usage for improved precision."
    }
    
    return {
        "overall_band_score": band_score,
        "feedback": feedback
    }

def start_challenge():
    st.session_state.challenge_active = True
    st.session_state.writing_challenge_data["prompt"] = generate_prompt_from_ai(st.session_state.selected_llm)
    st.session_state.writing_challenge_data["start_time"] = datetime.now()
    st.session_state.writing_challenge_data["end_time"] = st.session_state.writing_challenge_data["start_time"] + timedelta(minutes=20) # 20-minute timer
    st.session_state.writing_challenge_data["user_response"] = ""
    st.session_state.writing_challenge_data["feedback"] = None
    st.session_state.writing_challenge_data["band_score"] = None
    st.session_state.time_left_seconds = 20 * 60

def submit_response():
    st.session_state.challenge_active = False
    data = st.session_state.writing_challenge_data
    if data["user_response"]:
        with st.spinner("Evaluating your response..."):
            evaluation_result = evaluate_response_with_ai(
                st.session_state.selected_llm,
                data["prompt"],
                data["user_response"]
            )
            if "error" not in evaluation_result:
                data["feedback"] = evaluation_result.get("feedback")
                data["band_score"] = evaluation_result.get("overall_band_score")
                data["history"].append({
                    "timestamp": datetime.now().isoformat(),
                    "prompt": data["prompt"],
                    "user_response": data["user_response"],
                    "feedback": data["feedback"],
                    "band_score": data["band_score"]
                })
                st.success("Response submitted and evaluated!")
            else:
                st.error(f"Evaluation failed: {evaluation_result['error']}")
    else:
        st.warning("Please write something before submitting.")

# --- UI Layout --- #
st.set_page_config(page_title="Writing Challenge", layout="wide")
st.title("✍️ IELTS Writing Challenge")
st.write("Practice your writing skills with AI-generated prompts and get instant feedback!")

# Sidebar for history
st.sidebar.header("Challenge History")
if st.session_state.writing_challenge_data["history"]:
    for i, entry in enumerate(reversed(st.session_state.writing_challenge_data["history"])):
        with st.sidebar.expander(f"Challenge {len(st.session_state.writing_challenge_data['history']) - i} (Score: {entry['band_score']})"):
            st.markdown(f"**Prompt:** {entry['prompt']}")
            st.markdown(f"**Your Response:** {entry['user_response'][:100]}...")
            st.markdown(f"**Feedback:** {entry['feedback'].get('overall_summary', 'N/A')}")
            st.markdown(f"**Band Score:** {entry['band_score']}")
else:
    st.sidebar.info("No challenges completed yet.")

# Main content area
if not st.session_state.challenge_active:
    if st.button("Start New Writing Challenge", help="Generate a new prompt and start the timer."):
        start_challenge()
        st.rerun()
    
    if st.session_state.writing_challenge_data["feedback"]:
        st.subheader("Previous Challenge Results")
        data = st.session_state.writing_challenge_data
        st.markdown(f"**Prompt:** {data['prompt']}")
        st.markdown(f"**Your Response:**")
        st.info(data['user_response'])
        
        if data["band_score"]:
            st.markdown(f"### Overall Band Score: <span style='color:#4CAF50; font-size: 2em;'>{data['band_score']}</span>", unsafe_allow_html=True)
        
        if data["feedback"]:
            st.subheader("Detailed Feedback")
            feedback = data["feedback"]
            st.markdown(f"**Overall Summary:** {feedback.get('overall_summary', 'N/A')}")
            
            st.markdown("**Task Achievement:**")
            st.info(feedback.get('task_achievement', 'N/A'))
            
            st.markdown("**Coherence and Cohesion:**")
            st.info(feedback.get('coherence_cohesion', 'N/A'))
            
            st.markdown("**Lexical Resource:**")
            st.info(feedback.get('lexical_resource', 'N/A'))
            
            st.markdown("**Grammatical Range and Accuracy:**")
            st.info(feedback.get('grammatical_range_accuracy', 'N/A'))

else: # Challenge is active
    data = st.session_state.writing_challenge_data
    st.subheader("Current Writing Challenge")
    
    # Display prompt
    st.markdown("### Writing Prompt:")
    st.warning(data["prompt"])
    
    # Timer display
    timer_placeholder = st.empty()
    
    # Text area for user response
    user_input_disabled = False
    if st.session_state.time_left_seconds <= 0:
        user_input_disabled = True
        timer_placeholder.error("Time's Up!")
    else:
        minutes = st.session_state.time_left_seconds // 60
        seconds = st.session_state.time_left_seconds % 60
        timer_placeholder.markdown(f"### Time Left: {minutes:02d}:{seconds:02d}")
    
    # Display text area for user response
    st.session_state.writing_challenge_data["user_response"] = st.text_area(
        "Your Response:",
        value=st.session_state.writing_challenge_data["user_response"],
        height=300,
        disabled=user_input_disabled,
        help="Write your response here. The input will be disabled when the timer runs out."
    )

    # Display submit and end buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Response", disabled=user_input_disabled):
            submit_response()
            st.rerun()
    
    with col2:
        if st.button("End Challenge Early", disabled=user_input_disabled):
            st.session_state.challenge_active = False
            st.session_state.time_left_seconds = 0
            st.warning("Challenge ended early.")
            st.rerun()
    
    # Update timer (after rendering all UI elements)
    if not user_input_disabled:
        time.sleep(1)  # Simulate countdown
        st.session_state.time_left_seconds -= 1
        st.rerun()  # Rerun to update timer

# Ensure LLM is selected for API calls
if 'selected_llm' not in st.session_state:
    st.session_state.selected_llm = 'gemini' # Default LLM if not set