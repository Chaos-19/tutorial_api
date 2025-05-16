import base64
import os
from google import genai
from google.genai import types


def generate(content_html):
    client = genai.Client(
        
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=content_html),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""You are a highly skilled developer and documentation expert. Convert the following HTML content into clean, professional-grade Markdown.

Ensure all HTML tags are properly and semantically converted.

Use code blocks for any programming code or technical snippets.

Convert HTML tables into Markdown tables with proper alignment and formatting.

Translate headings (<h1>–<h6>) into corresponding Markdown syntax (#, ##, etc.).

Turn lists (<ul>, <ol>) into proper bullet or numbered lists.

Convert inline formatting like <strong>, <em>, <code>, <a> tags into their Markdown equivalents.

Remove any redundant tags, scripts, or inline styles not relevant to the Markdown output.

Preserve the content's structure, readability, and intent.


Here is the HTML content:"""),
        ],
    )
    
    response_markdown = ""

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        #print(chunk.text, end="")
        response_markdown+=chunk.text
        
        
        
    return response_markdown

if __name__ == "__main__":
    generate()
