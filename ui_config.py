import chainlit as cl

@cl.set_chat_profiles
def chat_profile():
    return [
        cl.ChatProfile(
            name="TeachMe.AI",
            markdown_description="TeachMe.AI Your AI-powered toolkit for smarter, faster studying.",
            icon="/public/reading.svg"
        )
    ]

@cl.set_starters
async def starter():
    return [
        cl.Starter(
            label="Text Summarizer",
            message="Meet your Summarizer – ready to condense content into clear summaries.",
            icon="/public/summarization.svg",
        ),
        cl.Starter(
            label="Concept Explainer",
            message="Need help understanding a topic? Your Concept Explainer is here to assist.",
            icon="/public/discussion.svg",
        ),
        cl.Starter(
            label="Quiz Generator",
            message="Ready to test your knowledge? Let the Quiz Generator create custom quizzes for you.",
            icon="/public/quiz.svg",
        ),
        
        cl.Starter(
            label="Flashcard Generator",
            message="Boost your memory with smart flashcards – generated just for you.",
            icon="/public/flash-card.svg",
        ),
        cl.Starter(
            label="Code Explainer",
            message="Confused by code? The Code Explainer is here to break it down for you.",
            icon="/public/binary-code.svg",
        ),
        cl.Starter(
            label="Math Solver",
            message="Tackle math problems with confidence – your Math Solver is ready.",
            icon="/public/calculating.svg"
        ),
        
    ]