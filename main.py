import chainlit as cl
import json
from typing import cast
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_default_openai_api,
    set_default_openai_client,
    set_tracing_disabled,
    RunConfig,
)
from openai.types.responses import ResponseTextDeltaEvent
from my_secrets import Secrets

# Import modular components
from agent_definitions import create_master_agent
from file_utils import read_file_content, UnsupportedFileError
from utils import get_thinking_message
import ui_config  # Imports chat_profile and starter

@cl.on_chat_start
async def start():
    # 1. Setup Secrets and Client
    secrets = Secrets()
    client = AsyncOpenAI(
        api_key=secrets.gemini_api_key,
        base_url=secrets.gemini_base_url,
    )
    set_default_openai_api("chat_completions")
    set_default_openai_client(client)
    set_tracing_disabled(True)
    
    # 2. Setup Model
    model = OpenAIChatCompletionsModel(
        model=secrets.gemini_api_model,
        openai_client=client,
    )

    # 3. Create Agent Network
    agent = create_master_agent(model) # Changed: no longer returns 'dev'

    # 4. Initialize User Session
    # cl.user_session.set("dev", dev) # Removed
    cl.user_session.set("agent", agent)
    cl.user_session.set("history", [])

    # ---
    # --- CRITICAL: SET YOUR MODAL URL HERE ---
    # ---
    cl.user_session.set("modal_url", "MODAL_WEB_ENDPOINT_URL")
    # ---

@cl.on_message
async def main(message: cl.Message):
    agent = cast(Agent, cl.user_session.get("agent"))
    history: list = cl.user_session.get("history") or []
    # dev = cl.user_session.get("dev") # Removed

    file_content = None
    if message.elements:
        uploaded_file = message.elements[0]
        file_path = uploaded_file.path
        file_name = uploaded_file.name

        try:
            file_content = read_file_content(file_path, file_name)
        except UnsupportedFileError as e:
            await cl.Message(content=f"❌ Unsupported file type: {e.extension}").send()
            return
        except IOError as e:
            await cl.Message(content=f"❌ Could not read file: {str(e)}").send()
            return
        except Exception as e:
            await cl.Message(content=f"❌ An error occurred while processing the file: {str(e)}").send()
            return

    thinking_msg = cl.Message(content=get_thinking_message())
    await thinking_msg.send()

    history.append({
        "role": "user",
        "content": message.content + (f"\n\n[File Content]:\n{file_content}" if file_content else "")
    })

    try:
        result = Runner.run_streamed(
            starting_agent=agent,
            input=history,
        )

        response_msg = cl.Message(content="")
        first_response = True

        async for chunk in result.stream_events():
            if chunk.type == "raw_response_event" and isinstance(chunk.data, ResponseTextDeltaEvent):
                if first_response:
                    await thinking_msg.remove()
                    await response_msg.send()
                    first_response = False
                await response_msg.stream_token(chunk.data.delta)
        
        history.append({
            "role": "assistant",
            "content": response_msg.content,
        })

        cl.user_session.set("history", history)
        await response_msg.update()

    except Exception as e:
        await thinking_msg.remove()
        await cl.Message(content=f"❌ An Error Occurred: {str(e)}").send()
        print(f"Error: {e}")

@cl.on_chat_end
async def end():
    history = cl.user_session.get("history") or []
    with open("history.json", "w") as f:
        json.dump(history, f, indent=4)