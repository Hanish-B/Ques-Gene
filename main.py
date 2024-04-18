import requests  # Import the requests library to make API requests
import textwrap

from app.mcq_generation import MCQGenerator

def show_result(generated: str, answer: str, context:str, original_question: str = ''):
    
    print('Context:')

    for wrap in textwrap.wrap(context, width=120):
        print(wrap)
    print()

    print('Question:')
    print(generated)

    print('Answer:')
    print(answer)
    print('-----------------------------')

# Initialize the MCQGenerator
MCQ_Generator = MCQGenerator(True)

# API endpoint URL for receiving context from Submitty
SUBMITTY_API_URL = "http://localhost:1511/courses/s24/development/generateSet"

# Dummy context for testing purposes
dummy_context = '''The koala or, inaccurately, koala bear[a] (Phascolarctos cinereus), is an arboreal herbivorous marsupial native to Australia. It is the only extant representative of the family Phascolarctidae and its closest living relatives are the wombats, which are members of the family Vombatidae. The koala is found in coastal areas of the mainland's eastern and southern regions, inhabiting Queensland, New South Wales, Victoria, and South Australia. It is easily recognisable by its stout, tailless body and large head with round, fluffy ears and large, spoon-shaped nose. The koala has a body length of 60–85 cm (24–33 in) and weighs 4–15 kg (9–33 lb). Fur colour ranges from silver grey to chocolate brown. Koalas from the northern populations are typically smaller and lighter in colour than their counterparts further south. These populations possibly are separate subspecies, but this is disputed.'''

# Make API request to Submitty to get context
response = requests.post(SUBMITTY_API_URL)
if response.status_code == 200:
    context = response.json().get("context")
    questions = MCQ_Generator.generate_mcq_questions(context, 10)

# Send questions back to Submitty
    submitty_response = requests.post(SUBMITTY_API_URL, json=questions)  # Send JSON response
    if submitty_response.status_code != 200:
        print("Error sending questions back to Submitty")

else:
    # If API request fails, fallback to dummy context
    context = dummy_context

# Generate MCQ questions using the obtained context
MCQ_Generator.generate_mcq_questions(context, 10)
