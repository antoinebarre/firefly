

from firefly.validation.string import validate_string


class HTMLTag(str):
    def __new__(cls, value: str):
        HTMLTag.__validate(value)
        modified_value = f"<{value}>"
        return super(HTMLTag, cls).__new__(cls, modified_value)
    @classmethod
    def __validate(cls, value):
        value = validate_string(value, empty_allowed=False)

        if "<" in value or ">" in value:
            raise ValueError("HTML Tag Value cannot contain '<' or '>' characters.")

if __name__ == "__main__":
    tag = HTMLTag("di>v")
    print(tag)  # "<div>