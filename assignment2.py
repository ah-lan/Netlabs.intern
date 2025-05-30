# Step 1: Get student data
def get_student_data():
    return {
        "Alice": 87,
        "Bob": 73,
        "Charlie": 92,
        "Diana": 65,
        "Ethan": 55
    }

# Step 2: Grade calculation using if-elif-else
def calculate_grade(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    else:
        return 'F'

# Step 3: Class statistics using *args and returning multiple values
def class_statistics(*scores):
    avg = sum(scores) / len(scores)
    return min(scores), max(scores), avg

# Step 5: Recursive function to sum from 1 to n
def sum_scores(n):
    if n <= 1:
        return n
    return n + sum_scores(n - 1)

# Menu helper functions
def display_all_students(data):
    print("\n--- All Student Grades ---")
    for name, score in data.items():
        print(f"{name}: Score = {score}, Grade = {calculate_grade(score)}")

def display_statistics(data):
    scores = list(data.values())
    min_score, max_score, avg_score = class_statistics(*scores)
    print("\n--- Class Statistics ---")
    print(f"Lowest Score: {min_score}")
    print(f"Highest Score: {max_score}")
    print(f"Average Score: {avg_score:.2f}")

    # Step 5: Filter top performers (above average) using lambda + filter
    top_students = dict(filter(lambda x: x[1] > avg_score, data.items()))
    print("\nTop Performers (Above Average):")
    for name, score in top_students.items():
        print(f"{name}: {score}")

def add_new_student(data):
    name = input("Enter student name: ")
    try:
        score = int(input("Enter student score: "))
        data[name] = score
        print(f"{name} added successfully!")
    except ValueError:
        print("Invalid score! Please enter a number.")

def lookup_student(data):
    name = input("Enter student name to look up: ")
    if name in data:
        score = data[name]
        grade = calculate_grade(score)
        print(f"{name}'s score: {score}, Grade: {grade}")
    else:
        print("Student not found.")

# Main Program with Menu
def main():
    students = get_student_data()

    while True:
        print("\n==== Student Grade System ====")
        print("1. View all student grades")
        print("2. View class statistics")
        print("3. Add new student")
        print("4. Look up student")
        print("5. Sum 1 to N (recursion)")
        print("6. Exit")

        choice = input("Choose an option (1-6): ")

        if choice == '1':
            display_all_students(students)
        elif choice == '2':
            display_statistics(students)
        elif choice == '3':
            add_new_student(students)
        elif choice == '4':
            lookup_student(students)
        elif choice == '5':
            try:
                n = int(input("Enter a number N to sum from 1 to N: "))
                print(f"Sum from 1 to {n} = {sum_scores(n)}")
            except ValueError:
                print("Please enter a valid integer.")
        elif choice == '6':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the main program
if __name__ == "__main__":
    main()
