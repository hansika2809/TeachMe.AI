# modal_summarizer.py



# Import the modal library

import modal

# Import os to get environment variables (like API keys)

import os

# Import the 'pipeline' from huggingface transformers

from transformers import pipeline



# --- Set up our Modal App ---

# We give it a name

app = modal.App(name="TeachMe-summarizer")



# --- HuggingFace API Key ---

# This tells Modal to get our secret API key

# We named this secret "huggingface-secret" in the Modal dashboard

hf_token_secret = modal.Secret.from_name("huggingface-secret")



# --- Define the server environment ---

# This tells Modal what software to install on the server

summarizer_image = (

    modal.Image.debian_slim(python_version="3.10") # Use a basic Python 3.10 image

    .pip_install( # Install these python libraries

        "torch",

        "transformers", # For the AI model

        "sentencepiece",

        "accelerate", # Helps the model run faster

        "fastapi" # To create the web URL

    )

)



# --- Define the Model Class ---

# This class will hold our model and run the summarization

@app.cls(

    image=summarizer_image, # Use the environment we just defined

    gpu="T4", # We need a T4 GPU to run this model

    secrets=[hf_token_secret], # Give it access to our API key

    scaledown_window=300, # Shut down the server after 5 mins (300 sec) of no use

)

class Summarizer:

    # This will hold the loaded AI model

    pipeline: any = None



    # This function runs once when the server starts

    @modal.enter()

    def load_model(self):

        # This is the name of the model from HuggingFace

        model_name = "ChaltaHai/my-text-summarizer-model"

        # Get the API key we passed in

        hf_token = os.environ["HF_TOKEN"]



        print(f"Loading model: {model_name}...")

        # Load the model and save it in self.pipeline

        self.pipeline = pipeline(

            "summarization",

            model=model_name,

            token=hf_token, # Pass in the API key

            device=0, # This tells it to use the GPU

        )

        print("Model loaded successfully.")



    # --- This is a helper function ---

    # It's not a web endpoint, just a normal python function

    # We put the main logic here so we don't have to write it twice

    def _run_summarization(self, text: str) -> str:

        """

        This is a helper function that does the real summarization work.

        """

        # Check if the model failed to load

        if not self.pipeline:

            return "Error: Model not loaded."



        # Try to run the summarization

        try:

            print(f"Summarizing text (length: {len(text)} chars)...")

            # Run the model!

            result = self.pipeline(

                text, min_length=30, truncation=True # 'truncation=True' shortens text if it's too long

            )

            print("Summarization complete.")

            # Get just the summary text from the result

            return result[0]["summary_text"]

        except Exception as e:

            # Handle any errors during summarization

            print(f"Error during summarization: {e}")

            return f"Error: {e}"

    # --- End of helper function ---



    # This function is a Modal "method"

    # We can use this to test from the command line

    @modal.method()

    def summarize(self, text: str) -> str:

        """

        This is a way to test the model from the command line.

        It just calls our helper function.

        """

        return self._run_summarization(text)



    # This function creates the public web URL

    # It's a "POST" endpoint, so our app can send data to it

    @modal.fastapi_endpoint(method="POST")

    def web(self, item: dict):

        """

        This is the main web endpoint that our chainlit app will call.

        """

        # Check if the user sent us a dictionary with a "text" key

        if "text" not in item:

            return {"error": "No 'text' field provided."}, 400 # 400 is a "Bad Request" error



        # Call our helper function with the text

        summary = self._run_summarization(item["text"])



        # Check if the helper function gave us an error

        if "Error:" in summary:

            return {"error": summary}, 500 # 500 is a "Server Error"



        # If everything worked, send back the summary!

        return {"summary": summary}