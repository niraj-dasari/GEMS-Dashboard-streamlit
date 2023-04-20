import streamlit as st
import pymongo
import pandas as pd

# Connect to the MongoDB database
client = pymongo.MongoClient("mongodb://localhost:27017/mydatabase")
db = client["employees"]
collection = db["employee_data"]

# Define CRUD functions
def create_employee(emp_code, emp_name, emp_email, batch, project_name, lead_name, pm_name):
    employee = {
        "EmpCode": emp_code,
        "EmployeeName": emp_name,
        "EmployeeEmail": emp_email,
        "Batch": batch,
        "ProjectName": project_name,
        "LeadName": lead_name,
        "PMName": pm_name
    }
    result = collection.insert_one(employee)
    return result.inserted_id

def read_employee(emp_code):
    employee = collection.find_one({"EmpCode": emp_code})
    return employee

def update_employee(emp_code, emp_name=None, emp_email=None, batch=None, project_name=None, lead_name=None, pm_name=None):
    update_query = {}
    if emp_name:
        update_query["EmployeeName"] = emp_name
    if emp_email:
        update_query["EmployeeEmail"] = emp_email
    if batch:
        update_query["Batch"] = batch
    if project_name:
        update_query["ProjectName"] = project_name
    if lead_name:
        update_query["LeadName"] = lead_name
    if pm_name:
        update_query["PMName"] = pm_name
    result = collection.update_one({"EmpCode": emp_code}, {"$set": update_query})
    return result.modified_count

def delete_employee(emp_code):
    result = collection.delete_one({"EmpCode": emp_code})
    return result.deleted_count

# Streamlit UI
st.title("Employee Management System")

# Define select CRUD operation options
options = ["Create", "Read", "Update", "Delete"]
selected_option = st.sidebar.selectbox("Select an operation:", options)

# Create employee
if selected_option == "Create":
    st.subheader("Create Employee")
    emp_code = st.text_input("EmpCode")
    emp_name = st.text_input("EmployeeName")
    emp_email = st.text_input("EmployeeEmail")
    batch = st.text_input("Batch")
    project_name = st.text_input("ProjectName")
    lead_name = st.text_input("LeadName")
    pm_name = st.text_input("PMName")
    if st.button("Create"):
        create_employee(emp_code, emp_name, emp_email, batch, project_name, lead_name, pm_name)
        st.success("Employee created!")

# Read employee
elif selected_option == "Read":
    st.subheader("All Employees")
    employees = collection.find()
    st.dataframe(employees)

# Update employee
elif selected_option == "Update":
    st.subheader("Update Employee")
    update_emp_code = st.text_input("EmpCode to update")
    emp_name_update = st.text_input("EmployeeName", key="ename")
    emp_email_update = st.text_input("EmployeeEmail", key="eemail")
    batch_update = st.text_input("Batch", key="ebatch")
    project_name_update = st.text_input("ProjectName", key="eproject")
    lead_name_update = st.text_input("LeadName", key="elead")
    pm_name_update = st.text_input("PMName", key="epm")
    if st.button("Update"):
        updated_count = update_employee(
            update_emp_code, emp_name_update, emp_email_update, batch_update, project_name_update, lead_name_update, pm_name_update)
        if updated_count > 0:
            st.success("Employee updated!")
        else:
            st.warning("Employee not found")
            
else:
    st.subheader("Delete Employee")
    delete_emp_code = st.text_input("EmpCode to delete")
    if st.button("Delete"):
        deleted_count = delete_employee(delete_emp_code)
        if deleted_count > 0:
            st.success("Employee deleted!")
        else:
            st.warning("Employee not found")
