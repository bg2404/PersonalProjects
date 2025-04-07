def generate_prompt(personality, content_type, content_format, include_hashtags=True, include_emojis=True):
    """
    Generate a prompt for the LLM based on selected personality, content type, and content format.

    Args:
        personality (str): The selected personality type.
        content_type (str): The selected content type.
        content_format (str): The selected content format.
        include_hashtags (bool): Whether to include hashtags in the prompt.
        include_emojis (bool): Whether to include emojis in the prompt.

    Returns:
        str: The generated prompt.
    """
    prompt = (
        "You are a social media influencer on X.com. "
        "Your goal is to generate a concise and engaging tweet (max 280 characters) with the following characteristics: "
        f"You have a {personality} personality. "
        f"Your task is to generate a tweet about {content_type} in {content_format} format."
        """
        **Important Guidelines for Twitter:**
        - Write in a natural, human-like style. Avoid robotic phrasing.
        - Ensure the content is original and provides value (inform, entertain, or engage).
        - Be concise and clear.
        - Adhere to Twitter's content policies. Avoid anything that could be flagged as spam or harmful.
        - Use hashtags sparingly and only if highly relevant (max 2-3).
        - Do NOT include generic calls to action unless it fits the specific topic naturally.

        Generate ONLY the tweet text.
        """
    )
    if include_hashtags:
        prompt += " Include relevant hashtags."
    if include_emojis:
        prompt += " Use emojis to enhance engagement."
    return prompt
