import re
from . import Commands, TextSnippets

MD_ESCAPE_PATTERN = re.compile('([*_`])')


def get_field(obj, key):
    if key in obj:
        return obj[key]
    else:
        return None


def _escape_markdown_special_chars(str):
    return re.sub(MD_ESCAPE_PATTERN, r'\\\g<1>', str)


def _stringify_field(field):
    if field in (False, None, {}, [], ''):
        return TextSnippets.FIELD_IS_EMPTY_PLACEHOLDER
    else:
        return field

def prepare_external_field(obj, key):
    val = get_field(obj, key)

    if type(val) is list:
        val = ', '.join(val)

    return _escape_markdown_special_chars(_stringify_field(val))