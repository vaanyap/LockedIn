import streamlit as st

# Function to display the goal page
def goal_page():

    st.write("Enter your goal and track your progress below.")
    
    # Input for the user to set their goal
    goal = st.text_input("What is your goal?")

    # Check if the user has entered a goal
    if goal:
        st.session_state.goal = goal  # Store the goal in the session state
        
        # If the goal is entered, prompt to add tasks to the checklist
        if 'tasks' not in st.session_state:
            st.session_state.tasks = []  # Initialize an empty task list if it's not created yet
        
        st.subheader(f"Tasks for your goal: {goal}")
        
        # Get tasks from the user
        task = st.text_input("Add a task to your checklist")
        
        # Button to add a task to the checklist
        if st.button("Add Task") and task:
            st.session_state.tasks.append({"task": task, "completed": False})
            st.success(f"Task '{task}' added!")

        # Display tasks with checkboxes
        if st.session_state.tasks:
            st.write("Your tasks:")
            incomplete_tasks = []  # New list for tasks that aren't completed
            for i, task_info in enumerate(st.session_state.tasks):
                task_label = task_info["task"]
                is_checked = task_info["completed"]
                
                # Create a checkbox for each task and track if it's completed
                task_completed = st.checkbox(task_label, value=is_checked, key=f"task_{i}")
                
                # If the task is checked, mark it as completed and do not add it back to incomplete tasks
                if task_completed != is_checked:
                    st.session_state.tasks[i]["completed"] = task_completed
                
                # Only add incomplete tasks back to the list
                if not task_completed:
                    incomplete_tasks.append(task_info)

            # Only update the session state after rendering, keeping incomplete tasks
            st.session_state.tasks = incomplete_tasks

            st.success("Progress saved!")

        # Save goal to session state to ensure persistence across pages
        if 'goals' not in st.session_state:
            st.session_state.goals = []  # Initialize if not already present
        
        # Add the current goal to the goal list
        if goal not in st.session_state.goals:
            st.session_state.goals.append(goal)
            st.success(f"Goal '{goal}' added to your list!")

    else:
        st.write("Please enter a goal to start adding tasks.")
