import pytest
import warnings
from firefly.markdown.tools import MkFormat
from firefly.markdown.tools import TextAlignment
from firefly.markdown.tools import HeaderLevel


# Test MkFormat.bold
@pytest.mark.parametrize("input_text, expected_output", [
    ("Hello World", "**Hello World**"),  # ID: TestBoldSimple
    ("", "**" "**"),  # ID: TestBoldEmpty
    ("123", "**123**"),  # ID: TestBoldNumbers
    ("!@#$%^&*()", "**!@#$%^&*()**"),  # ID: TestBoldSpecialChars
], ids=["TestBoldSimple", "TestBoldEmpty", "TestBoldNumbers", "TestBoldSpecialChars"])
def test_bold(input_text, expected_output):
    # Act
    result = MkFormat.bold(input_text)

    # Assert
    assert result == expected_output

# Test MkFormat.italics
@pytest.mark.parametrize("input_text, expected_output", [
    ("Hello World", "*Hello World*"),  # ID: TestItalicsSimple
    ("", "*" "*"),  # ID: TestItalicsEmpty
    ("123", "*123*"),  # ID: TestItalicsNumbers
    ("!@#$%^&*()", "*!@#$%^&*()*"),  # ID: TestItalicsSpecialChars
], ids=["TestItalicsSimple", "TestItalicsEmpty", "TestItalicsNumbers", "TestItalicsSpecialChars"])
def test_italics(input_text, expected_output):
    # Act
    result = MkFormat.italics(input_text)

    # Assert
    assert result == expected_output

# Test MkFormat.inline_code
@pytest.mark.parametrize("input_text, expected_output", [
    ("Hello World", "``Hello World``"),  # ID: TestInlineCodeSimple
    ("", "``" "``"),  # ID: TestInlineCodeEmpty
    ("123", "``123``"),  # ID: TestInlineCodeNumbers
    ("!@#$%^&*()", "``!@#$%^&*()``"),  # ID: TestInlineCodeSpecialChars
], ids=["TestInlineCodeSimple", "TestInlineCodeEmpty", "TestInlineCodeNumbers", "TestInlineCodeSpecialChars"])
def test_inline_code(input_text, expected_output):
    # Act
    result = MkFormat.inline_code(input_text)

    # Assert
    assert result == expected_output

# Test MkFormat.center_text
@pytest.mark.parametrize("input_text, expected_output", [
    ("Hello World", "<center>Hello World</center>"),  # ID: TestCenterTextSimple
    ("", "<center></center>"),  # ID: TestCenterTextEmpty
    ("123", "<center>123</center>"),  # ID: TestCenterTextNumbers
    ("!@#$%^&*()", "<center>!@#$%^&*()</center>"),  # ID: TestCenterTextSpecialChars
], ids=["TestCenterTextSimple", "TestCenterTextEmpty", "TestCenterTextNumbers", "TestCenterTextSpecialChars"])
def test_center_text(input_text, expected_output):
    # Act
    result = MkFormat.center_text(input_text)

    # Assert
    assert result == expected_output

# Test MkFormat.text_color
@pytest.mark.parametrize("input_text, color, expected_output", [
    ("Hello World", "red", '<font color="red">Hello World</font>'),  # ID: TestTextColorRed
    ("Hello World", "#ffce00", '<font color="#ffce00">Hello World</font>'),  # ID: TestTextColorHex
    ("", "blue", '<font color="blue"></font>'),  # ID: TestTextColorEmpty
    ("Hello World", "", '<font color="black">Hello World</font>'),  # ID: TestTextColorDefault
], ids=["TestTextColorRed", "TestTextColorHex", "TestTextColorEmpty", "TestTextColorDefault"])
def test_text_color(input_text, color, expected_output):
    # Act
    result = MkFormat.text_color(input_text, color)

    # Assert
    assert result == expected_output

# Test MkFormat.text_external_link
@pytest.mark.parametrize("input_text, link, expected_output", [
    ("Google", "https://google.com", "[Google](https://google.com)"),  # ID: TestTextExternalLinkSimple
    ("", "", "[]()"),  # ID: TestTextExternalLinkEmpty
    ("GitHub", "", "[GitHub]()"),  # ID: TestTextExternalLinkNoURL
    ("", "https://github.com", "[](https://github.com)"),  # ID: TestTextExternalLinkNoText
], ids=["TestTextExternalLinkSimple", "TestTextExternalLinkEmpty", "TestTextExternalLinkNoURL", "TestTextExternalLinkNoText"])
def test_text_external_link(input_text, link, expected_output):
    # Act
    result = MkFormat.text_external_link(input_text, link)

    # Assert
    assert result == expected_output

# Test MkFormat.insert_code
@pytest.mark.parametrize("code, language, expected_output", [
    ("print('Hello World')", "python", "```python\nprint('Hello World')\n```"),  # ID: TestInsertCodePython
    ("const a = 10;", "javascript", "```javascript\nconst a = 10;\n```"),  # ID: TestInsertCodeJavaScript
    ("SELECT * FROM users;", "sql", "```sql\nSELECT * FROM users;\n```"),  # ID: TestInsertCodeSQL
    ("print('Hello World')", "", "```\nprint('Hello World')\n```"),  # ID: TestInsertCodeNoLanguage
], ids=["TestInsertCodePython", "TestInsertCodeJavaScript", "TestInsertCodeSQL", "TestInsertCodeNoLanguage"])
def test_insert_code(code, language, expected_output):
    # Act
    result = MkFormat.insert_code(code, language)

    # Assert
    assert result == expected_output


# Parametrized test for happy path scenarios
@pytest.mark.parametrize("test_id, text, align, bold, italic, text_color, background_color, font_size, expected", [
    ("happy-1", "Hello World", "left", False, False, "", "", 0, "<p style='text-align: left'>Hello World</p>"),
    ("happy-2", "Hello World", "right", True, False, "red", "", 12, "<p style='text-align: right; font-weight: bold; color: red; font-size: 12px'>Hello World</p>"),
    ("happy-3", "Hello World", "center", False, True, "", "blue", 14, "<p style='text-align: center; font-style: italic; background-color: blue; font-size: 14px'>Hello World</p>"),
    # Add more happy path cases as needed
])
def test_text_style_happy_path(test_id, text, align, bold, italic, text_color, background_color, font_size, expected):
    # Act
    result = MkFormat.text_style(text, align=align, bold=bold, italic=italic, text_color=text_color, background_color=background_color, font_size=font_size)

    # Assert
    assert result == expected, f"Failed {test_id}"

# Parametrized test for edge cases
@pytest.mark.parametrize("test_id, text, align, bold, italic, text_color, background_color, font_size, expected", [
    ("edge-1", "", "left", False, False, "", "", 0, "<p style='text-align: left'></p>"),  # Empty text
    ("edge-2", "Hello World", "justify", False, False, "#000", "", -1, "<p style='text-align: justify; color: #000'>Hello World</p>"),  # Negative font size
    # Add more edge cases as needed
])
def test_text_style_edge_cases(test_id, text, align, bold, italic, text_color, background_color, font_size, expected):
    # Act
    result = MkFormat.text_style(text, align=align, bold=bold, italic=italic, text_color=text_color, background_color=background_color, font_size=font_size)

    # Assert
    assert result == expected, f"Failed {test_id}"


# Test cases for happy path with various realistic test values
@pytest.mark.parametrize("input_value, expected_value", [
    ("right", TextAlignment.right), # ID: test_alignment_right
    ("left", TextAlignment.left),   # ID: test_alignment_left
    ("center", TextAlignment.center), # ID: test_alignment_center
    ("justify", TextAlignment.justify) # ID: test_alignment_justify
])
def test_valid_alignments(input_value, expected_value):
    # Act
    alignment = TextAlignment(input_value)

    # Assert
    assert alignment == expected_value, f"Expected {expected_value} for input {input_value}"

# Test cases for edge cases
@pytest.mark.parametrize("input_value, expected_value", [
    ("Right", TextAlignment.left), # ID: test_alignment_case_insensitive
    ("LEFT", TextAlignment.left),  # ID: test_alignment_uppercase
    ("", TextAlignment.left),      # ID: test_alignment_empty_string
    (None, TextAlignment.left),    # ID: test_alignment_none
])
def test_edge_cases(input_value, expected_value):
    # Act
    with pytest.warns(UserWarning) as record:
        alignment = TextAlignment(input_value)

    # Assert
    assert alignment == expected_value, f"Expected {expected_value} for input {input_value}"
    assert len(record) == 1
    assert f"{input_value} is not a valid TextAlignment." in str(record[0].message)

# Test cases for error cases
@pytest.mark.parametrize("input_value, expected_warning", [
    (123, "123 is not a valid TextAlignment."), # ID: test_alignment_numeric
    (["left"], "['left'] is not a valid TextAlignment."), # ID: test_alignment_list
    ({"value": "left"}, "{'value': 'left'} is not a valid TextAlignment."), # ID: test_alignment_dict
])
def test_error_cases(input_value, expected_warning):
    # Act
    with pytest.warns(UserWarning) as record:
        alignment = TextAlignment(input_value)

    # Assert
    assert alignment == TextAlignment.left, f"Expected default value for input {input_value}"
    assert len(record) == 1
    assert expected_warning in str(record[0].message)


# Test IDs for different scenarios
HAPPY_PATH_ID = "happy"
EDGE_CASE_ID = "edge"
ERROR_CASE_ID = "error"

# Happy path test values
happy_test_values = [
    (HeaderLevel.TITLE, 1),
    (HeaderLevel.HEADING, 2),
    (HeaderLevel.SUBHEADING, 3),
    (HeaderLevel.SUBSUBHEADING, 4),
    (HeaderLevel.MINORHEADING, 5),
    (HeaderLevel.LEASTHEADING, 6),
]

# Edge case test values
# Since this is an enum, edge cases might involve the boundaries of the enum values
edge_test_values = [
    (HeaderLevel.TITLE, 1),
    (HeaderLevel.LEASTHEADING, 6),
]

# Error case test values
# Enums will raise errors when invalid values are used to access members
error_test_values = [
    ("TITLE", ValueError),
    (0, ValueError),
    (7, ValueError),
]

@pytest.mark.parametrize("enum_member, expected", happy_test_values, ids=[f"{HAPPY_PATH_ID}_{index}" for index, _ in enumerate(happy_test_values)])
def test_header_level_happy_path(enum_member, expected):
    # Act
    result = enum_member.value

    # Assert
    assert result == expected, f"Expected {enum_member} to have value {expected}, but got {result}."

@pytest.mark.parametrize("enum_member, expected", edge_test_values, ids=[f"{EDGE_CASE_ID}_{index}" for index, _ in enumerate(edge_test_values)])
def test_header_level_edge_cases(enum_member, expected):
    # Act
    result = enum_member.value

    # Assert
    assert result == expected, f"Expected {enum_member} to have value {expected}, but got {result}."

@pytest.mark.parametrize("invalid_value, expected_exception", error_test_values, ids=[f"{ERROR_CASE_ID}_{index}" for index, _ in enumerate(error_test_values)])
def test_header_level_error_cases(invalid_value, expected_exception):
    # Act & Assert
    with pytest.raises(expected_exception):
        _ = HeaderLevel(invalid_value)
