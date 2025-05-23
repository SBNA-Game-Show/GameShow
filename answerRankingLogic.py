import difflib  # For finding close matches between strings
from collections import defaultdict, Counter  # For grouping and counting answers
import json  # To read JSON data

# Function to normalize text by converting it to lowercase and stripping whitespace
def normalize(text):
    return text.lower().strip()

# Function to group similar answers using string similarity
def group_answers(answers, cutoff=0.75):
    grouped = []  # Final grouped list of normalized answers
    labels = []   # Unique labels of grouped answers

    for answer in answers:
        norm = normalize(answer)
        # Try to find a similar label using difflib (e.g., 'Yes' and 'yes')
        match = difflib.get_close_matches(norm, labels, n=1, cutoff=cutoff)
        if match:
            grouped.append(match[0])  # If similar label found, use it
        else:
            labels.append(norm)       # Otherwise, add it as a new label
            grouped.append(norm)      # And append it to the group
    return grouped

# Function to process the full survey data
def process_survey_data(survey_data):
    questions = defaultdict(list)  # Dictionary to store answers grouped by question

    # Separate answers by question
    for entry in survey_data:
        questions[entry["question"]].append(entry["answer"])

    final_output = {}  # Final structured results for each question

    # Process each question
    for question, answers in questions.items():
        grouped = group_answers(answers)  # Group similar answers
        count = Counter(grouped)          # Count frequency of each answer
        sorted_counts = sorted(count.items(), key=lambda x: x[1], reverse=True)  # Sort by count

        max_votes = sorted_counts[0][1]  # Max count for calculating points

        # Assign points based on popularity
        scored_answers = [
            {
                "answer": a.capitalize(),                     # Capitalize for display
                "count": c,                                   # Number of votes
                "points": int((c / max_votes) * 100)          # Score out of 100
            }
            for a, c in sorted_counts
        ]
        final_output[question] = scored_answers  # Store results for the question

    return final_output

# Read the survey data JSON file
with open("C:/Users/Khushpreet/GameShow/sanskrit_survey_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Process the survey responses
results = process_survey_data(data)

# Print results to the console
print("\nSurvey Results:")
for question, answers in results.items():
    print(f"\nQuestion: {question}")
    for i, ans in enumerate(answers, 1):
        print(f"{i}. {ans['answer']} - {ans['points']} points ({ans['count']} votes)")
