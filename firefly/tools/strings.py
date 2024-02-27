"""Collection of tools for working with strings."""

import random
import string
import textwrap
import time

from firefly.validation.int import validate_positive_integer

__all__ = [
    "generate_random_string",
    "add_unique_suffix",
    "indent",
    "LoremIpsum"
]

def generate_random_string(length_str: int) -> str:
    """
    Generate a random string of a given length.

    :param length: The length of the string to generate.
    :return: A random string of the given length.
    """
    length_str = validate_positive_integer(length_str)

    return ''.join(
        random.choice(string.ascii_letters + string.digits)
        for _ in range(length_str))
    
def generate_unique_id() -> str:
    """
    Generate a unique identifier.

    Returns:
        str: A unique identifier.
    """
    return str(time.perf_counter()).replace('.', '')

def add_unique_suffix(str2modify: str) -> str:
    """
    Adds a unique suffix to a string.

    Args:
        str2modify (str): The string to modify.

    Returns:
        str: The modified string with a unique suffix.
    """
    perf_counter = str(time.perf_counter()).replace('.', '')
    return f"{str2modify}_{perf_counter}"

def indent(
    text:str,
    amount:int,
    ch: str =' '):
    """
    Indents the given text by the specified amount using the specified character.

    Args:
        text (str): The text to be indented.
        amount (int): The number of times the character should be repeated for
            each indentation level.
        ch (str, optional): The character used for indentation. Defaults to a space (' ').

    Returns:
        str: The indented text.
    """
    return textwrap.indent(text, amount * ch)


# list of possibles words
DATA = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam placerat
mauris ut est ultricies, ut iaculis ipsum cursus. Pellentesque venenatis
viverra augue id venenatis. Mauris suscipit nunc non ipsum commodo ultrices.
Curabitur cursus rhoncus sapien, at cursus odio. Nullam eleifend, neque vitae
consequat tincidunt, justo massa auctor nisl, vitae ullamcorper mi metus sed
risus. Donec maximus orci sed laoreet ultricies. Etiam malesuada lacus sit
amet felis interdum efficitur. Vestibulum sagittis leo et mauris dapibus
congue. Integer luctus justo odio, ut bibendum velit aliquet non. In feugiat
a mi eu euismod. Nam dapibus nunc eu ex congue, nec tincidunt sapien vulputate.
Donec congue odio mi, a laoreet massa tincidunt id. Nulla at tincidunt metus.
Cras sit amet velit at purus gravida elementum a nec libero. Morbi malesuada
nulla nec dui efficitur ultricies. Sed ultricies dictum arcu a efficitur.
Vestibulum ac ex eget massa convallis dignissim at at nisl. Mauris tristique
velit at ultricies dictum. Curabitur dignissim tincidunt mi, sit amet congue
mi fermentum vitae. Nullam ut aliquam dolor. Sed in orci ut sem sollicitudin
posuere eu non libero. Nam ut sem eu felis luctus finibus. In hac habitasse
platea dictumst. Aenean interdum libero ac quam iaculis, id ultrices nunc
tempor. Suspendisse varius dui a sem gravida, vel interdum ligula commodo.
Curabitur venenatis tortor non odio gravida, non rutrum metus congue. Nulla
aliquet aliquam tincidunt. Nullam congue feugiat dui at tempus.
Quisque interdum auctor risus, in venenatis neque tincidunt sed.
Nullam interdum elit in fringilla facilisis. Suspendisse fermentum auctor
libero ut vulputate. Pellentesque efficitur, lectus in semper hendrerit,
justo ligula vestibulum purus, in dapibus felis purus et metus. Morbi dapibus
convallis finibus. Nullam ut enim eget nisl efficitur luctus in at augue. Ut
auctor elementum sapien, sit amet consequat ex tempus non. Curabitur lobortis
metus id elit lobortis, sit amet facilisis dui congue. Sed eget rutrum elit.
Aliquam mollis dictum fringilla. Donec ac tellus eget magna placerat mattis.
Vivamus fringilla, felis nec rhoncus varius, neque nisi iaculis libero, non
fringilla nunc purus non tortor. Quisque varius libero vitae ante lobortis
vestibulum. Nulla facilisi.
Mauris ultricies tortor vitae orci luctus, ac dignissim justo consequat.
Sed viverra scelerisque scelerisque. Donec posuere interdum neque, in
vestibulum neque viverra et. Mauris vitae tellus lobortis, tristique arcu ege,
fermentum nisl. Nam vel
""".replace(".", "").replace(",","").split()

WORD_SEPARATORS = {
    "value":[" ", ", ", "; ", ": "],
    "probability":[0.8, 0.1, 0.05, 0.05]}
SENTENCE_SEPARATORS = {
    "value":[". ", "! ", "? "],
    "probability":[0.7, 0.15, 0.15]}
PARAGRAPH_SEPARATOR = "\n\n"


class LoremIpsum:
    """
    LoremIpsum class for generating Lorem Ipsum text.
    """

    @staticmethod
    def generate_word() -> str:
        """
        Generate a word of Lorem Ipsum.

        Returns:
            str: A randomly generated word.
        """
        return random.choice(DATA)

    @staticmethod
    def generate_sentence(max_characters: int = 100) -> str:
        """
        Generates a random sentence.

        Args:
            max_characters (int): The maximum number of characters in the sentence. Default is 100.

        Returns:
            str: The generated sentence.
        """

        # validate the max_characters
        max_characters = validate_positive_integer(max_characters)

        # calculate the biais of the sentence separators i.e the maximum number of characters
        # of the sentence separators
        max_sentence_separator = max(
            len(separator) for separator in SENTENCE_SEPARATORS["value"])

        # calculate the biais of the word separators i.e the maximum number of characters
        # of the word separators
        max_word_separator = max(
            len(separator) for separator in WORD_SEPARATORS["value"])

        sentence: str = ""

        while len(sentence) < max_characters - max_sentence_separator:
            word: str = random.choice(DATA)
            new_sentence: str = sentence + word

            if len(new_sentence) + max_word_separator > max_characters - max_sentence_separator:
                break

            # done to avoid adding a word separator at the end of the sentence
            sentence: str = new_sentence + random.choices(
                WORD_SEPARATORS["value"],
                weights=WORD_SEPARATORS["probability"], k=1)[0]

        # add a sentence separator
        sentence += random.choices(
            SENTENCE_SEPARATORS["value"],
            weights=SENTENCE_SEPARATORS["probability"],
            k=1,
        )[0]

        return sentence[0].upper() + sentence[1:]

    @staticmethod
    def generate_paragraph(max_characters: int = 2000) -> str:
        """
        Generates a paragraph of text with a maximum number of characters.

        Args:
            max_characters (int): The maximum number of characters for the paragraph.

        Returns:
            str: The generated paragraph.

        Raises:
            ValueError: If max_characters is not a positive integer.
        """
        # validate the max_characters
        max_characters = validate_positive_integer(max_characters)

        # calculate the bias of the paragraph separator i.e the maximum number of characters
        # of the paragraph separator
        max_paragraph_separator = len(PARAGRAPH_SEPARATOR)

        paragraph = ""
        while len(paragraph) < max_characters - max_paragraph_separator:
            sentence = LoremIpsum.generate_sentence(int(max_characters / 5))
            new_paragraph = paragraph + sentence
            if len(new_paragraph) > max_characters - max_paragraph_separator:
                break
            paragraph = new_paragraph

        # add a paragraph separator
        return paragraph + PARAGRAPH_SEPARATOR
