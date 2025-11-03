import chainlit as cl
import httpx
from agents import function_tool, RunContextWrapper
from dataclasses import dataclass

# Define a constant for the remote call timeout
REMOTE_CALL_TIMEOUT = 180.0

# --- Tool 1: External Summarizer Service ---
# (Developer tool has been removed)

@function_tool("invoke_summarization_service")
@cl.step(type="External Summarizer")
async def invoke_summarization_service(input_corpus: str) -> str:
    """
    Communicates with a remote, specialized AI model
    to perform high-quality text summarization.
    """
    # Retrieve the service endpoint from the user's active session
    service_endpoint = cl.user_session.get("modal_url")
    if not service_endpoint:
        return "Failure: Summarization service endpoint is unconfigured. The developer must set the 'modal_url' in main.py."

    # The external model has a known character limit.
    char_limit = 3800
    if len(input_corpus) > char_limit:
        input_corpus = input_corpus[:char_limit]

    # Use httpx for the asynchronous POST request
    try:
        async with httpx.AsyncClient(timeout=REMOTE_CALL_TIMEOUT) as client:
            
            payload = {"text": input_corpus}
            response = await client.post(service_endpoint, json=payload)
            
            # Check for any HTTP errors (e.g., 404, 500, 403)
            response.raise_for_status()  
            
            response_json = response.json()
            
            # Check the structure of the JSON response
            if "summary" in response_json:
                return response_json["summary"]  # Success
            elif "error" in response_json:
                return "Service Error: " + response_json["error"]
            else:
                return "Failure: The summarizer returned an unknown response format."
    
    except httpx.HTTPStatusError as http_err:
        return "HTTP Error: Failed to contact summarizer. Status: " + str(http_err.response.status_code)
    except httpx.RequestError as req_err:
        return "Network Error: Could not connect to summarization service. " + str(req_err)
    except Exception as e:
        return "An unexpected error occurred during summarization: " + str(e)