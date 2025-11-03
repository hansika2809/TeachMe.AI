import random

def get_thinking_message() -> str:
    """Returns a random thinking message."""
    messages = [
        "🧠 Thinking... Just a moment while I gather your answer!",
        "📚 Processing your request... Let me put my study cap on!",
        "🤓 Crunching data and decoding knowledge... hang tight!",
        "🧠 Analyzing your input and retrieving the best response...",
        "⏳ Working on it...",
        "🔍 Gathering insights... this won't take long!",
        "💡 One sec, the neurons are firing!",
        "Give me a moment — I'm looking into it... 📚",
        "Thinking this through like a top student... ✍️",
        "Let me gather the best explanation for you... 🧠✨",
        "Crunching some knowledge for you... ⏳",
        "Analyzing this like a pro — hang tight! 🔍",
        "Almost there... just connecting the academic dots! 📖",
        "Sharpening my pencils... and my thoughts! ✏️💭",
        "Solving this puzzle one piece at a time... 🧩",
        "Flipping through mental textbooks... 📘📘📘",
        "Checking my notes on that topic... 📝",
        "Calculating the smartest answer for you... 🧮",
        "Channeling my inner tutor — just a sec! 🎓",
        "Compiling your custom study guide... ⌛",
    ]
    return random.choice(messages)