import streamlit as st
import sqlite3

def sanitize_input(input_data):
    # Add your sanitization logic here
    sanitized_data = input_data.strip()  # Example: Trimming leading/trailing whitespace
    return sanitized_data

# Employee class to represent an employee record
class Employee:
    def __init__(self, name, contact, job_title, department):
        self.name = name
        self.contact = contact
        self.job_title = job_title
        self.department = department

    def __str__(self):
        return f"Name: {self.name}, Contact: {self.contact}, Job Title: {self.job_title}, Department: {self.department}"


# Employee information management class
class EmployeeManagement:
    def __init__(self):
        self.connection = sqlite3.connect("employee.db")
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT,
            job_title TEXT,
            department TEXT
        )
        """
        self.cursor.execute(query)
        self.connection.commit()

    def create_employee(self, name, contact, job_title, department):
        query = "INSERT INTO employees (name, contact,stre job_title, department) VALUES (?, ?, ?, ?)"
        self.cursor.execute(query, (name, contact, job_title, department))
        self.connection.commit()

    def read_employee(self, name):
        query = "SELECT * FROM employees WHERE name = ?"
        self.cursor.execute(query, (name,))
        result = self.cursor.fetchone()
        if result:
            employee = Employee(result[1], result[2], result[3], result[4])
            return employee
        return None

    def update_employee(self, name, new_contact, new_job_title, new_department):
        query = "UPDATE employees SET contact = ?, job_title = ?, department = ? WHERE name = ?"
        self.cursor.execute(query, (new_contact, new_job_title, new_department, name))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def delete_employee(self, name):
        query = "DELETE FROM employees WHERE name = ?"
        self.cursor.execute(query, (name,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def get_employees(self):
        query = "SELECT * FROM employees"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        employees = []
        for result in results:
            employee = Employee(result[1], result[2], result[3], result[4])
            employees.append(employee)
        return employees


emp_management = EmployeeManagement()

def home():
    st.title("Employee Information Management")

    form_col1, form_col2, form_col3, form_col4 = st.columns(4)

    with form_col1:
        name = st.text_input("Name")

    with form_col2:
        contact = st.text_input("Contact")

    with form_col3:
        job_title = st.text_input("Job Title")

    with form_col4:
        department = st.text_input("Department")

    if st.button("Add Employee"):
        # Validate and sanitize user input
        name = sanitize_input(name)
        contact = sanitize_input(contact)
        job_title = sanitize_input(job_title)
        department = sanitize_input(department)

        emp_management.create_employee(name, contact, job_title, department)
        st.success("Employee added successfully!")

    st.header("Employee List")
    employees = emp_management.get_employees()
    if len(employees) > 0:
        for i, employee in enumerate(employees):
            st.write(f"Employee {i+1}")
            st.write(f"Name: {employee.name}")
            st.write(f"Contact: {employee.contact}")
            st.write(f"Job Title: {employee.job_title}")
            st.write(f"Department: {employee.department}")
            st.write("---")

        # Employee Actions
        selected_employee = st.selectbox("Select an employee", [employee.name for employee in employees])
        selected_action = st.selectbox("Select an action", ["Read", "Update", "Delete"])

        if selected_action == "Read":
            employee = emp_management.read_employee(selected_employee)
            if employee:
                st.write(f"Name: {employee.name}")
                st.write(f"Contact: {employee.contact}")
                st.write(f"Job Title: {employee.job_title}")
                st.write(f"Department: {employee.department}")
            else:
                st.warning("Employee not found.")

        elif selected_action == "Update":
            employee = emp_management.read_employee(selected_employee)
            if employee:
                new_contact = st.text_input("New Contact", value=employee.contact)
                new_job_title = st.text_input("New Job Title", value=employee.job_title)
                new_department = st.text_input("New Department", value=employee.department)

                if st.button("Update"):
                    new_contact = sanitize_input(new_contact)
                    new_job_title = sanitize_input(new_job_title)
                    new_department = sanitize_input(new_department)

                    if emp_management.update_employee(selected_employee, new_contact, new_job_title, new_department):
                        st.success("Employee updated successfully!")
                    else:
                        st.warning("Failed to update employee.")

        elif selected_action == "Delete":
            if st.button("Delete"):
                if emp_management.delete_employee(selected_employee):
                    st.success("Employee deleted successfully!")
                else:
                    st.warning("Failed to delete employee.")

    else:
        st.write("No employees found.")


if __name__ == "__main__":
    home()
