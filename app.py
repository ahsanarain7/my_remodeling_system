import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="My Remodeling System", layout="wide")

if 'leads' not in st.session_state:
    st.session_state.leads = pd.DataFrame(columns=["Name", "Contact", "Address", "Project Type", "Notes"])

if 'projects' not in st.session_state:
    st.session_state.projects = pd.DataFrame(columns=["Project Name", "Client", "Start Date", "End Date", "Status", "Estimated Cost"])

st.title(" My Remodeling System - Dashboard")
col1, col2, col3 = st.columns(3)
col1.metric(" Total Leads", len(st.session_state.leads))
col2.metric(" Active Projects", len(st.session_state.projects[st.session_state.projects["Status"] == "In Progress"]))
col3.metric(" Completed Projects", len(st.session_state.projects[st.session_state.projects["Status"] == "Completed"]))

tab1, tab2, tab3 = st.tabs([" Add Lead", " Projects", " Export / Search"])

with tab1:
    st.subheader(" Add New Lead")

    with st.form("lead_form"):
        name = st.text_input("Client Name")
        contact = st.text_input("Contact Info")
        address = st.text_area("Address")
        project_type = st.selectbox("Project Type", ["Kitchen", "Bathroom", "Both"])
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Add Lead")

        if submitted:
            if name and contact:
                new_lead = {
                    "Name": name,
                    "Contact": contact,
                    "Address": address,
                    "Project Type": project_type,
                    "Notes": notes
                }
                st.session_state.leads = pd.concat([st.session_state.leads, pd.DataFrame([new_lead])], ignore_index=True)
                st.success("Lead added successfully!")
            else:
                st.error("Name and Contact are required.")

    st.write(" All Leads")
    st.dataframe(st.session_state.leads, use_container_width=True)

with tab2:
    st.subheader(" Manage Projects")

    with st.form("project_form"):
        project_name = st.text_input("Project Name")
        client_name = st.selectbox("Select Client", st.session_state.leads["Name"].tolist() if not st.session_state.leads.empty else ["No Leads Available"])
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        status = st.selectbox("Status", ["Not Started", "In Progress", "Completed"])
        cost_option = st.radio("Cost Option", ["Auto Generate", "Manual Input"])
        if cost_option == "Manual Input":
            estimated_cost = st.text_input("Enter Estimated Cost ($)")
        else:
            estimated_cost = f"${random.randint(2000, 15000)}"

        project_submit = st.form_submit_button("Add Project")

        if project_submit and client_name != "No Leads Available":
            new_project = {
                "Project Name": project_name,
                "Client": client_name,
                "Start Date": start_date,
                "End Date": end_date,
                "Status": status,
                "Estimated Cost": estimated_cost
            }
            st.session_state.projects = pd.concat([st.session_state.projects, pd.DataFrame([new_project])], ignore_index=True)
            st.success(f"Project '{project_name}' added with cost {estimated_cost}")

    st.write(" All Projects")
    st.dataframe(st.session_state.projects, use_container_width=True)

with tab3:
    st.subheader(" Export Data")

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="⬇ Download Leads as CSV",
            data=st.session_state.leads.to_csv(index=False).encode("utf-8"),
            file_name="leads.csv",
            mime="text/csv"
        )
    with col2:
        st.download_button(
            label="⬇ Download Projects as CSV",
            data=st.session_state.projects.to_csv(index=False).encode("utf-8"),
            file_name="projects.csv",
            mime="text/csv"
        )

    st.divider()
    st.subheader(" Search Projects")

    search_term = st.text_input("Enter client or project name to search:")
    if search_term:
        results = st.session_state.projects[
            st.session_state.projects["Project Name"].str.contains(search_term, case=False) |
            st.session_state.projects["Client"].str.contains(search_term, case=False)
        ]
        st.write(f" Found {len(results)} result(s):")
        st.dataframe(results, use_container_width=True)
