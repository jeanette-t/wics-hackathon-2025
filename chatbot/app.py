import os
import random
from flask import Flask, request, render_template, redirect, url_for
from groq import Groq

app = Flask(__name__)

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

@app.route('/')
def home():
    return render_template('personalized.html')

@app.route('/start', methods=['POST'])
def start():
    # Handle user input for level and questions
    user_level = request.form['level']
    user_answers = {
        "favorite_color": request.form['favorite_color'],
        "favorite_celebrity": request.form['favorite_celebrity'],
        "favorite_movie_or_book": request.form['favorite_movie_or_book']
    }

    # Generate the story based on user inputs
    story = generate_western_story(user_level, user_answers, final=False)

    if story:
        return render_template('story.html', story=story, level=user_level, user_answers=user_answers)
    else:
        return "Something went wrong. Please try again later."

@app.route('/comprehension', methods=['POST'])
def comprehension():
    # Handle comprehension quiz responses
    user_comprehension_answers = request.form.to_dict()

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

    # Check the answers
    correct_count = check_comprehension_answers(user_comprehension_answers, 
                                                {q: data['correct_answer'] for q, data in comprehension_questions.items()})

    # Determine next level
    if correct_count >= 4:
        return redirect(url_for('level_up'))
    else:
        return redirect(url_for('story_failed'))

@app.route('/level_up')
def level_up():
    return render_template('level_up.html', message="Congratulations! You've leveled up!")

@app.route('/story_failed')
def story_failed():
    return render_template('story_failed.html', message="You didn't pass the quiz. Let's stick to your current level.")

@app.route('/final_story', methods=['POST'])
def final_story():
    user_level = request.form['level']
    user_answers = request.form.to_dict()

    # Final story generation
    final_story = generate_western_story(user_level, user_answers, final=True)
    
    if final_story:
        return render_template('final_story.html', story=final_story)
    else:
        return "Something went wrong. Please try again later."

if __name__ == "__main__":
    app.run(debug=True)
