import os
from groq import Groq
# from dotenv import load_dotenv

# Load your environment variables (make sure GROQ_API_KEY is set)
# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_KEY = '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'


# Initialize the Groq client
groq = Groq(api_key=GROQ_API_KEY)

def generate_western_story(reading_level, user_answers):
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

    try:
        completion = groq.chat.completions.create(
            messages=messages,
            model="llama3-8b-8192",
            temperature=0.7  # Adjust for creativity
        )

        # Extract the story from the response
        story = completion.choices[0].message.content.strip()
        print("\nGenerated Western Story:\n")
        print(story)

        return story

    except Exception as e:
        print("Error calling Groq API:", e)
        return None


def interactive_chat():
    """Runs an interactive session where the chatbot asks the user questions step by step."""
    print("🤠 Welcome to the Wild West!")
    print("Answer a few questions to generate your own personalized Western story.")
    print("Type 'exit' at any time to quit.\n")

    # Get reading level
    while True:
        reading_level = input("Enter your reading level (Beginner, Intermediate, Advanced): ").strip().capitalize()
        if reading_level in ["Beginner", "Intermediate", "Advanced"]:
            break
        elif reading_level.lower() == "exit":
            return
        print("⚠️ Please enter a valid reading level (Beginner, Intermediate, Advanced).")

    # Collect user responses interactively
    questions = [
        "What’s your favorite color?",
        "Who is your favorite celebrity?",
        "What’s your favorite movie or book?",
    ]

    user_answers = {}

    for question in questions:
        answer = input(f"{question} ").strip()
        if answer.lower() == "exit":
            print("👋 Exiting. See you next time!")
            return
        user_answers[question] = answer

    # Generate and display the story
    print("\n✨ Creating your personalized Western story...\n")
    western_story = generate_western_story(reading_level, user_answers)

    if western_story:
        print("\n📖 Enjoy your adventure!\n")
    else:
        print("\n⚠️ Something went wrong. Please try again later.")

if __name__ == "__main__":
    interactive_chat()