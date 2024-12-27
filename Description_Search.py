import re


def get_sentence_with_word(text, word):
    """
    Finds the first sentence in the text where the word appears.
    If the word doesn't appear, returns the first sentence of the text.

    Parameters:
        text (str): The text to search in.
        word (str): The word to search for.

    Returns:
        str: The first sentence containing the word or the first sentence if the word is not found.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    for sentence in sentences:
        if word.lower() in sentence.lower():
            return sentence.strip()
    return sentences[0].strip() if sentences else ""


# Example usage:
text = """Merry Christmas and Happy Holidays, everyone! 
We just wanted everyone to know how much we appreciate you. 
Have a wonderful holiday season!"""
word = ""

result = get_sentence_with_word(text, word)
print(result)













