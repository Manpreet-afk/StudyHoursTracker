import streamlit as st
import plotly.express as px
from db import get_study_time, get_streak, add_session, get_all_sessions, get_subject_breakdown, update_session, delete_session

st.set_page_config(page_title="Study Tracker", page_icon="📚",layout="wide")
st.title("📚 Study Hours Dashboard")
st.write("Welcome to your personal AI & Data Engineering study tracker!")

total_minutes = get_study_time("all")
total_hours = round(total_minutes / 60, 2)
current_streak = get_streak()

col1, col2 = st.columns(2)

with col1:
    st.metric(label="All-Time Study Hours", value=f"{total_hours} hrs", delta=f"{total_minutes} mins")

with col2:
    trend_msg = "🔥 Keep it up!" if current_streak > 0 else "Log time to start!"
    st.metric(label="Current Streak", value=f"{current_streak} Days", delta=trend_msg)

st.divider()

left_col, right_col = st.columns([1.2, 1])

with left_col:
    st.subheader("📋 Session Log")
    sessions = get_all_sessions()
    
    if sessions:
        table_data = [{"ID": r[0], "Date": str(r[1]), "Topic": r[2], "Minutes": r[3]} for r in sessions]
        st.dataframe(table_data, use_container_width=True, hide_index=True)
    else:
        st.info("No study sessions logged yet. Use the form to add one!")

with right_col:
    st.subheader("✏️ Log New Session")

    with st.form("log_form", clear_on_submit=True):
        subject = st.text_input("Subject")
        mins = st.number_input("Minutes", min_value=1, step=1)
        
        submitted = st.form_submit_button("Save Session")
        
        if submitted:
            if subject and mins:
                add_session(subject, mins)  
                st.success(f"Saved {mins} mins for {subject}!")
                st.rerun()  
            else:
                st.error("Please fill in all fields.")
    st.divider()
    st.subheader("⚙️ Manage Records")
    
    with st.expander("Edit or Delete a Session"):
        st.write("Find the Session ID in the table.")
        target_id = st.number_input("Session ID", min_value=1, step=1)
        new_mins = st.number_input("New Minutes (for editing)", min_value=1, step=1)
        
        edit_btn, del_btn = st.columns(2)
        
        with edit_btn:
            if st.button("Update"):
                if update_session(target_id, new_mins):
                    st.success(f"Updated Session {target_id}!")
                    st.rerun()
                    
        with del_btn:
            if st.button("Delete"):
                if delete_session(target_id):
                    st.success(f"Deleted Session {target_id}!")
                    st.rerun()


st.divider()
st.subheader("📊 Subject Breakdown (Minutes)")
breakdown = get_subject_breakdown()

if breakdown:
    subjects = list(breakdown.keys())
    mins = list(breakdown.values())

    fig = px.bar(
        x=mins,              
        y=subjects,           
        orientation='h',      
        color=subjects,       
        text=mins,            
        labels={'x': 'Total Minutes', 'y': 'Subject'}
    )
    

    fig.update_layout(showlegend=False)
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Chart will appear once you log data.")

