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
    # Define the system prompt
    messages = [
        {
            "role": "system",
            "content": (
                "You are an interactive storytelling chatbot designed to improve literacy levels post-COVID. "
                "You create personalized Western-themed stories based on a user's reading comprehension level and their interests. "
                "Follow these steps STRICTLY:\n\n"
                "1️⃣ Based on the user's diagnostic, classify them as Beginner, Intermediate, or Advanced.\n"
                "2️⃣ Ask the user engaging questions to personalize the story:\n"
                "- 'What’s your favorite color?'\n"
                "- 'Who is your favorite celebrity or historical figure?'\n"
                "- 'What’s your favorite movie or book?'\n"
                "- 'If you could visit any place in the world, where would it be?'\n"
                "- 'What kind of adventures do you enjoy? (e.g., mystery, sci-fi, fantasy, Western, superhero, etc.)'\n\n"
                "3️⃣ Use their responses to generate a **Western-themed story** at their reading level:\n"
                "   - **Beginner**: Simple sentences, basic vocabulary, and a **rancher** as the main character.\n"
                "   - **Intermediate**: Moderate complexity, richer vocabulary, and a **cowboy** as the main character.\n"
                "   - **Advanced**: Sophisticated language, deeper themes, and a **sheriff** as the main character.\n\n"
                "4️⃣ Ensure the story is engaging and interactive, asking the user occasional questions to keep them engaged.\n"
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
            model="llama3-8b-8192",  # Adjust model if necessary
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

if __name__ == "__main__":
    # Simulating user responses
    reading_level = input("Enter reading level (Beginner, Intermediate, Advanced): ").strip()
    
    user_answers = {
        "favorite_color": input("What’s your favorite color? ").strip(),
        "favorite_celebrity": input("Who is your favorite celebrity or historical figure? ").strip(),
        "favorite_movie": input("What’s your favorite movie or book? ").strip(),
        "dream_destination": input("If you could visit any place in the world, where would it be? ").strip(),
        "favorite_adventure": input("What kind of adventures do you enjoy? (e.g., mystery, sci-fi, fantasy, Western, superhero, etc.) ").strip()
    }

    # Generate and display the story
    western_story = generate_western_story(reading_level, user_answers)
