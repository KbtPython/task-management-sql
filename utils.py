def convert_upper_underscore_to_capitalize(text):
    words = text.split('_')
    capitalized_words = [word.capitalize() for word in words]
    return ' '.join(capitalized_words)

def convert_string_to_upper_underscore(text):
    return text.upper().replace(' ', '_')


def convertEnumtoTuple(enum):
  variants = list(enum)
  tuple_of_variants = tuple(variants)
  return tuple_of_variants