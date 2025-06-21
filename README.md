# See Also

A simple Flask web application that generates related concepts for any input text using an LLM.
The interface is styled with **Tailwind CSS** for a clean and modern look.

## Setup

1. Install dependencies with `pip install -r requirements.txt` or using Poetry:

```bash
poetry install
```

2. Provide environment variables for your OpenAI or Azure OpenAI credentials. The app reads the same variables as `gpt.py`.

3. Run the application:

```bash
flask --app app run
```

Navigate to `http://localhost:5000` and enter text to see related concepts.
