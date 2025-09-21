import streamlit as st
import requests

# Sample AYUSH code descriptions
ayush_code_info = {
    "AYU001": {
        "condition": "Amavata (Rheumatoid Arthritis-like condition)",
        "description": "A chronic inflammatory disorder affecting joints, treated using herbal decoctions, Panchakarma, and dietary regulation."
    },
    "AYU002": {
        "condition": "Prameha (Diabetes Mellitus)",
        "description": "A metabolic disorder managed through herbal formulations like Nishamalaki, lifestyle changes, and detox therapies."
    },
    "AYU003": {
        "condition": "Shwasa (Respiratory Disorders)",
        "description": "Includes conditions like asthma and bronchitis, treated with herbs like Vasaka and therapies like steam inhalation."
    },
    "AYU004": {
        "condition": "Arsha (Hemorrhoids)",
        "description": "Painful swollen veins in the rectal area, treated with herbal ointments, ksharasutra therapy, and dietary regulation."
    },
    "AYU005": {
        "condition": "Kushta (Psoriasis-like skin disorders)",
        "description": "Chronic skin conditions managed with herbal oils, internal detox therapies, and lifestyle modifications."
    }
}


# Title of the app
st.title("🩺 AYUSH–ICD Code Mapper")

# Input field for AYUSH code
code = st.text_input("Enter AYUSH Code (e.g., AYU001)")

# If user enters a code, make a request to the FastAPI backend
if code:
    try:
        response = requests.get(f"http://127.0.0.1:8000/map/{code}")
        
        if response.status_code == 200:
            data = response.json()

            # Display the mapping result in a readable format
            st.markdown(f"""
            ### 🔍 Mapping Result
            - **ICD-11 Code**: `{data['icd11_code']}`
            - **Confidence Score**: `{data['confidence_score'] * 100:.1f}%`
            - **Notes**: {data['notes']}
            """)

	                # Show AYUSH code details if available
            if code in ayush_code_info:
                st.markdown(f"""
                ### 🧾 AYUSH Code Details
                - **Condition**: {ayush_code_info[code]['condition']}
                - **Description**: {ayush_code_info[code]['description']}
                """)
            else:
                st.info("ℹ️ No detailed information available for this AYUSH code yet.")


            # Show a progress bar for confidence score
            st.progress(data['confidence_score'])

            # Expandable explanation section
            with st.expander("What does this mean?"):
                st.write("This mapping shows the closest ICD-11 equivalent for the entered AYUSH code, based on clinical overlap and expert validation.")

        else:
            st.error("❌ Code not found or server error. Please check the AYUSH code and try again.")

    except requests.exceptions.ConnectionError:
        st.error("🚫 Unable to connect to the backend. Make sure your FastAPI server is running at http://127.0.0.1:8000")
