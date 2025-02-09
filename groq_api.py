import os
import random
from groq import Groq

# Initialize the Groq client
GROQ_API_KEY = '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'
groq = Groq(api_key=GROQ_API_KEY)

# Define a function to check answers
def check_comprehension_answers(user_answers, correct_answers):
    correct_count = 0
    for q, a in user_answers.items():
        if a.lower() == correct_answers.get(q, "").lower():
            correct_count += 1
    return correct_count

def generate_western_story(reading_level, user_answers, final=False):
    """
    Uses Groq's chat completions API to generate a Western-themed story
    based on the user's reading level and answers to personalized questions.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are an interactive storytelling chatbot designed to improve literacy levels post-COVID. "
                "You create personalized Western-themed stories based on a user's reading comprehension level and their interests. "
                "The story changes based on the user's reading level and answers."
                "Follow these steps STRICTLY:\n\n"
                "1️⃣ Ask the user engaging questions to personalize the story:\n"
                "- 'What’s your favorite color?'\n"
                "- 'Who is your favorite celebrity?'\n"
                "- 'What’s your favorite movie or book?'\n"
                "2️⃣ Based on the user's diagnostic, classify them as Beginner, Intermediate, or Advanced.\n"
                "3️⃣ Use their responses to generate a **Western-themed story** at their reading level:\n"
                "   - **Beginner**: Simple sentences, basic vocabulary, and a **rancher** as the main character.\n"
                "   - **Intermediate**: Moderate complexity, richer vocabulary, and a **cowboy** as the main character.\n"
                "   - **Advanced**: Sophisticated language, deeper themes, and a **sheriff** as the main character.\n\n"
                "4️⃣ Ensure the story is engaging and interactive. Ask the user occasional reading comprehension questions based on the written story to keep them engaged.\n"
                "5️⃣ Encourage reading growth by subtly integrating comprehension prompts and vocabulary explanations at the end."
            )
        },
        {
            "role": "user",
            "content": f"Reading Level: {reading_level}\nUser Answers: {user_answers}"
        }
    ]

    if final:
        messages.append({"role": "system", "content": "The story must now reach a satisfying conclusion."})

    try:
        completion = groq.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",
            temperature=0.7
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        print("Error calling Groq API:", e)
        return None

def ask_to_continue():
    """Asks the user if they want to continue or exit."""
    while True:
        choice = input("Do you want to continue the adventure? (yes/no): ").strip().lower()
        if choice in ['yes', 'y']:
            return True
        elif choice in ['no', 'n']:
            print("Thanks for playing! See you next time. 🤠")
            return False
        else:
            print("⚠️ Invalid input. Please answer with 'yes' or 'no'.")

def interactive_story():
    """Runs an interactive quiz and story based on the user's answers."""
    print("🤠 Welcome to the Wild West Adventure Quiz!")
    print("Answer 5 comprehension questions after the story, and if you get 4/5 correct, you'll level up!")

    # Ask the user to input their current level
    while True:
        user_level = input("\nPlease enter your current level (beginner, intermediate, advanced): ").strip().lower()
        if user_level in ['beginner', 'intermediate', 'advanced']:
            break
        else:
            print("⚠️ Invalid input. Please enter one of the following: 'beginner', 'intermediate', or 'advanced'.")

    # First, ask 3 personalized questions to shape the story
    user_answers = {}

    print("\nAnswer a few questions to personalize your adventure!\n")

    questions = [
        "What’s your favorite color?",
        "Who is your favorite celebrity?",
        "What’s your favorite movie or book?"
    ]

    for question in questions:
        answer = input(f"{question} ").strip()
        user_answers[question] = answer

    # Ask if the user wants to continue before generating the story
    if not ask_to_continue():
        return

    # Generate the story based on the user's level
    print(f"\nYour current level is: {user_level.capitalize()}\n")

    print("✨ Creating your personalized Western story...\n")
    story = generate_western_story(user_level, user_answers, final=False)

    if story:
        print(story)
    else:
        print("\n⚠️ Something went wrong. Please try again later.")
        return

    # Ask if the user wants to continue before proceeding to comprehension questions
    if not ask_to_continue():
        return

    # Define the comprehension questions with multiple choice options
    comprehension_questions = {
        "What was the name of the Sheriff in the story?": {
            "choices": ["Ethan Blackwood", "John Smith", "William Turner", "James Hawk"],
            "correct_answer": "Ethan Blackwood"
        },
        "What animal did the Sheriff ride?": {
            "choices": ["Midnight", "Thunder", "Black Stallion", "Shadow"],
            "correct_answer": "Midnight"
        },
        "What was the name of the young wizard in the story?": {
            "choices": ["Finnley", "Harry Potter", "Gandalf", "Luke Skywalker"],
            "correct_answer": "Finnley"
        },
        "Who is the antagonist in the story?": {
            "choices": ["Blackjack McCoy", "Billy the Kid", "Butch Cassidy", "Doc Holliday"],
            "correct_answer": "Blackjack McCoy"
        },
        "Where is the treasure hidden?": {
            "choices": ["In the canyon", "In the cave", "In the town", "Under the saloon"],
            "correct_answer": "in the canyon"
        }
    }

    print("\n📚 Now, let's test your comprehension of the story!\n")

    # Randomize the order of the choices
    user_comprehension_answers = {}
    for question, data in comprehension_questions.items():
        print(f"\n{question}")

        # Shuffle the choices
        random.shuffle(data['choices'])
        
        # Display the randomized choices
        for idx, choice in enumerate(data['choices'], 1):
            print(f"{idx}. {choice}")
        
        answer = input("Choose the correct answer (1-4): ").strip()

        # Check if the answer is valid
        if answer.isdigit() and 1 <= int(answer) <= 4:
            selected_answer = data['choices'][int(answer) - 1]
            user_comprehension_answers[question] = selected_answer.lower()
        else:
            print("⚠️ Invalid input. Please enter a number between 1 and 4.")
            continue

    # Ask if the user wants to continue before moving on
    if not ask_to_continue():
        return

    # Check if the user passed the comprehension quiz (got 4 out of 5 correct)
    correct_count = check_comprehension_answers(user_comprehension_answers, 
                                                {q: data['correct_answer'] for q, data in comprehension_questions.items()})

    # Determine reading level based on quiz results
    if correct_count >= 4:
        print("\n🎉 Congrats! You've passed the quiz and leveled up!")
        if user_level == "beginner":
            user_level = "intermediate"  # Move to Intermediate
        elif user_level == "intermediate":
            user_level = "advanced"  # Move to Advanced
    else:
        print("\n🚫 You didn't pass the quiz. Let's stick to your current level!")

    print(f"Your new level is: {user_level.capitalize()}\n")

    # Generate and display the new story based on the level
    print("\n✨ Creating your new personalized Western story...\n")
    western_story = generate_western_story(user_level, user_answers)

    if western_story:
        print("\n📖 Your adventure begins:\n")
        print(western_story)
    else:
        print("\n⚠️ Something went wrong. Please try again later.")

    # Ask if the user wants to continue before finalizing the story
    if not ask_to_continue():
        return

    # Ending the story with a conclusion
    print("\n🏁 Wrapping up your adventure...\n")
    final_story = generate_western_story(user_level, user_answers, final=True)

    if final_story:
        print("\n🎬 The grand finale:\n")
        print(final_story)
    else:
        print("\n⚠️ Something went wrong. Please try again later.")

    print("\n✨ Thanks for playing! The adventure ends here. 🤠")

if __name__ == "__main__":
    interactive_story()
