INITIAL_SYSTEM_PROMPT = (
    "You are a helpful assistant that helps me negotiate car price with auto dealers."
)


def new_mail_prompt(subject: str, content: str) -> str:
    return f"""
I will send you a subject and a content of an email that is sent by an auto dealer.
Please generate a response for me.

Subject: {subject}
Content: {content}

Only include the response email content and nothing else. The email resopnse should end with:
'Best,
Yifan'
"""


def regenerate_response_prompt(prompt: str) -> str:
    return f"""
Please modify your last response according to the following requirements.

{prompt}

Only include the response email content and nothing else. The email resopnse should end with:
'Best,
Yifan'
"""
