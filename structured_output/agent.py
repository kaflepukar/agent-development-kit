from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field


class EmailContent(BaseModel):
    subject: str = Field(
        description="The subject line of the email. Should be concise and descriptive."
    )
    body: str = Field(
        description="The main content of the email. Should be well-formatted with proper greeting, paragraphs, and signature."
    )


root_agent = LlmAgent(
    name="email_agent",
    model="gemini-2.0-flash",
    instruction="""
        You are an Email Generation Assistant.
        Your task is to generate a professional email if the user make a request.
        Note: Only generate email if user asks for it else have a normal conversation

        GUIDELINES WHEN CREATING EMAIL 
        - Create an appropriate subject line (concise and relevant)
        - Write a well-structured email body with:
            * Professional greeting
            * Clear and concise main content
            * Appropriate closing
            * Your name as signature
        - Suggest relevant attachments if applicable (empty list if none needed)
        - Email tone should match the purpose (formal for business, friendly for colleagues)
        - Keep emails concise but complete

        IMPORTANT: Your response MUST be valid JSON matching this structure:
        {
            "subject": "Subject line here",
            "body": "Email body here with proper paragraphs and formatting",
        }

        
    """,
    description="Generates professional emails with structured subject and body",
    output_schema=EmailContent,
    output_key="email",
)