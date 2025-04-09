import streamlit as st

def resume_maker_page():
    st.title("Resume Maker")
    st.write("Create professional resumes with ease!")
    
    # Basic resume form
    with st.form("resume_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        
        # Education section
        st.subheader("Education")
        school = st.text_input("School/University")
        degree = st.text_input("Degree")
        graduation_year = st.text_input("Graduation Year")
        
        # Experience section
        st.subheader("Work Experience")
        job_title = st.text_input("Job Title")
        company = st.text_input("Company")
        job_duration = st.text_input("Duration")
        responsibilities = st.text_area("Responsibilities")
        
        # Skills section
        st.subheader("Skills")
        skills = st.text_area("List your skills (comma separated)")
        
        # Generate button
        submitted = st.form_submit_button("Generate Resume")
        if submitted:
            st.success("Resume generated successfully!")
            # Here you would add the resume generation logic

if __name__ == "__main__":
    resume_maker_page()