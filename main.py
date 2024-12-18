import pandas as pd

# Extract data from table.csv file
df = pd.read_csv("table.csv", delimiter=';', header=None)

# Assign the first row as the id project
project_ids = df.iloc[0].tolist()
# Assign the second row as the revenues
revenues = df.iloc[1].tolist()
# Assign the third row as the days
days = df.iloc[2].tolist()
# Complete the projects list with these data
projects = []
for i in range(len(revenues)):
    projects.append({
        'project_id': project_ids[i],
        'revenue': revenues[i],
        'days': days[i]
    })

# Maximum number of researcher days available
max_days = int(input("Max days : "))

best_solution = None
best_revenue = 0


def bound(current_value, current_days, index): # Calculate upper bound for the remaining projects.
    if current_days > max_days:
        return 0  # If days exceed max, return zero as this branch is not feasible
    # Calculate maximum possible revenue by considering fractional inclusion of remaining projects
    bound_value = current_value
    remaining_days = max_days - current_days
    while index < len(projects) and projects[index]['days'] <= remaining_days:
        bound_value += projects[index]['revenue']
        remaining_days -= projects[index]['days']
        index += 1
    
    if index < len(projects):
        bound_value += (remaining_days / projects[index]['days']) * projects[index]['revenue']
    return bound_value

def branch_and_bound(current_value, current_days, index, current_solution): # Explore the solution space using the Branch and Bound algorithm.
    global best_revenue, best_solution
    if index >= len(projects):
        if current_value > best_revenue:
            best_revenue = current_value
            best_solution = current_solution.copy()
        return
    # Compute the bound for the current branch
    upper_bound = bound(current_value, current_days, index)
    
    # If the upper bound is better than the best solution, explore further
    if upper_bound > best_revenue:
        # Option 1: Include the current project
        if current_days + projects[index]['days'] <= max_days:
            current_solution[index] = 1
            branch_and_bound(current_value + projects[index]['revenue'], 
                                  current_days + projects[index]['days'], 
                                  index + 1, current_solution)
            current_solution[index] = 0  # Backtrack
        # Option 2: Exclude the current project
        current_solution[index] = 0
        branch_and_bound(current_value, current_days, index + 1, current_solution)


# Initialize the solution list (0 = exclude, 1 = include)
initial_solution = [0] * len(projects)

# Start Branch and Bound process
branch_and_bound(0, 0, 0, initial_solution)

# Output the best solution
print(f"Best Revenue: {best_revenue}")
print("Selected Projects:")
for i in range(len(projects)):
    if best_solution[i] == 1:
        print(f"Project {i+1}: Revenue = {projects[i]['revenue']}, Days = {projects[i]['days']}")
