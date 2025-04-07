def generate_prompt(
    personality: str,
    content_type: str,
    content_format: str,
) -> str:
    """
    Generates a prompt for an LLM to create a tweet.

    Args:
        personality: The desired personality/tone (e.g., "Witty", "Formal").
        content_type: The type of content (e.g., "Educational", "Promotional").
        content_format: The type of content format (e.g., "Text", "Image", "Video").

    Returns:
        A formatted prompt string.
    """

    # --- Enhanced Prompt Instructions ---
    prompt = f"""
    Generate a concise and engaging tweet (max 280 characters) with the following characteristics:

    - Personality/Tone: {personality}
    - Content Type: {content_type}

    **Important Guidelines for Twitter:**
    - Write in a natural, human-like style. Avoid robotic phrasing.
    - Ensure the content is original and provides value (inform, entertain, or engage).
    - Be concise and clear.
    - Adhere to Twitter's content policies. Avoid anything that could be flagged as spam or harmful.
    - Use hashtags sparingly and only if highly relevant (max 2-3).
    - Do NOT include generic calls to action unless it fits the specific topic naturally.

    Generate ONLY the tweet text.
    """
    # --- End Enhanced Prompt Instructions ---

    return prompt.strip()
