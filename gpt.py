import sys
import os
from openai import OpenAI, AzureOpenAI
from pydantic import BaseModel, Field
from typing import List

AIPHORIA_AZURE_OPENAI_ENDPOINT = os.getenv("AIPHORIA_AZURE_OPENAI_ENDPOINT")
AIPHORIA_AZURE_OPENAI_DEPLOYMENT = os.getenv("AIPHORIA_AZURE_OPENAI_DEPLOYMENT")
AIPHORIA_AZURE_OPENAI_KEY = os.getenv("AIPHORIA_AZURE_OPENAI_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=AIPHORIA_AZURE_OPENAI_ENDPOINT,
    api_key=AIPHORIA_AZURE_OPENAI_KEY,
)
model = AIPHORIA_AZURE_OPENAI_DEPLOYMENT


# Optionally, package up as a function
def complete(message, developer_message = "You are a helpful assistant", max_completion_tokens = 4096, response_format = { "type": "text" }):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": developer_message},
            {"role": "user", "content": message}
        ],
        max_tokens=max_completion_tokens,
        response_format=response_format
    )
    return completion.choices[0].message.content


class RelatedConcept(BaseModel):
    """A single concept related to the provided text."""
    short_name: str = Field(..., description="Concise name of the concept")
    definition: str = Field(..., description="Brief definition of the concept")
    explanation: str = Field(..., description="Why the concept is relevant or builds on the given text")
    start_here: str = Field(..., description="Any references to leading thinkers, organisations or other resources which would help the user to find out more about the given concept.")

class RelatedConceptsResponse(BaseModel):
    concepts: List[RelatedConcept] = Field(..., description="List of related concepts")


class SubmissionSummary(BaseModel):
    """Short summary of the user's submission."""
    title: str = Field(..., description="Brief title of the concept overall")
    description: str = Field(..., description="Brief description of the submission")

def complete_structured(message, developer_message = "You are a helpful assistant. You always respond using a JSON object containing a response key, where you write your freetext response, and an 'observations' key, where you may include any additional observations about the user query or the nature of the conversation. ", max_completion_tokens = 4096, output_model = RelatedConceptsResponse):
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": developer_message},
            {"role": "user", "content": message}
        ],
        max_tokens=max_completion_tokens,
        response_format=output_model
    )
    return completion.choices[0].message.parsed.model_dump_json()
