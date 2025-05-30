# Personalized greeting
name = input("What is your name?\n ")
print(f"Hello, {name}!\n")

# Initialize lists to hold diary data
date_str = [""] * 5
mood_num = [0] * 5
entries = [""] * 5
word_counts = [0] * 5  # For bonus word count requirement

i = 0
while i < 5:
    print("="*50+f"\nWelcome to your Diary,{name}!!\n"+"="*50)
    
    # Get and validate date
    while True:
        date_input = input("Date (dd/mm/yyyy): ")
        try:
            # Validate date format
            if len(date_input) == 10 and date_input[2] == '/' and date_input[5] == '/':
                day = int(date_input[:2])
                month = int(date_input[3:5])
                year = int(date_input[6:])
                if 1 <= day <= 31 and 1 <= month <= 12:
                    date_str[i] = date_input
                    break
        except ValueError:
            pass
        print("Invalid date format. Please use dd/mm/yyyy")
    
    # Get and validate mood
    while True:
        mood_input = input("Rate your mood (1-10): ")
        try:
            mood = int(mood_input)
            if 1 <= mood <= 10:
                mood_num[i] = mood
                break
            print("Please enter a number between 1 and 10")
        except ValueError:
            print("Please enter a valid number")
    
    # Get diary entry
    entries[i] = input("Diary Entry: ")
    word_counts[i] = len(entries[i].split())  # Calculate word count
    
    # Display confirmation
    #print(f"\nDiary Entry for {date_str[i]}:")
    #print(f"Mood: {mood_num[i]}/10")
    #print(f"Entry: {entries[i][:50]}...")  # Show preview
    #print(f"Word Count: {word_counts[i]}\n")
    
    i += 1

# Display all entries
print("="*20+"ALL ENTRIES"+ "="*20)
for j in range(5):
    print(f"\nEntry {j+1} - {date_str[j]}:")
    print(f"Mood: {mood_num[j]}/10")
    print(f"{entries[j]}")
    print(f"Word Count: {word_counts[j]}")

# Calculate average mood
average_mood = sum(mood_num) / 5
print(f"\nAverage Mood: {average_mood:.2f}/10")

# Find longest entry (by word count)
longest_index = word_counts.index(max(word_counts))
print("="*20+"LONGEST ENTRY "+ "="*20)
print(f"Date: {date_str[longest_index]}")
print(f"Word Count: {word_counts[longest_index]}")
print(f"{entries[longest_index]}")


