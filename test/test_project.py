import pytest

from glotter.core.project import AcronymScheme, CoreProject, NamingScheme

project_scheme_permutation_map = [
    {
        "id": "single_word_no_acronym",
        "words": ["word"],
        "acronyms": None,
        "schemes": {
            (NamingScheme.hyphen, None): "word",
            (NamingScheme.underscore, None): "word",
            (NamingScheme.camel, None): "word",
            (NamingScheme.camel, AcronymScheme.upper): "word",
            (NamingScheme.camel, AcronymScheme.lower): "word",
            (NamingScheme.camel, AcronymScheme.two_letter_limit): "word",
            (NamingScheme.pascal, None): "Word",
            (NamingScheme.pascal, AcronymScheme.upper): "Word",
            (NamingScheme.pascal, AcronymScheme.lower): "Word",
            (NamingScheme.pascal, AcronymScheme.two_letter_limit): "Word",
            (NamingScheme.lower, None): "word",
        },
    },
    {
        "id": "multiple_words_no_acronym",
        "words": ["multiple", "words"],
        "acronyms": None,
        "schemes": {
            (NamingScheme.hyphen, None): "multiple-words",
            (NamingScheme.underscore, None): "multiple_words",
            (NamingScheme.camel, None): "multipleWords",
            (NamingScheme.camel, AcronymScheme.upper): "multipleWords",
            (NamingScheme.camel, AcronymScheme.lower): "multipleWords",
            (NamingScheme.camel, AcronymScheme.two_letter_limit): "multipleWords",
            (NamingScheme.pascal, None): "MultipleWords",
            (NamingScheme.pascal, AcronymScheme.upper): "MultipleWords",
            (NamingScheme.pascal, AcronymScheme.lower): "MultipleWords",
            (NamingScheme.pascal, AcronymScheme.two_letter_limit): "MultipleWords",
            (NamingScheme.lower, None): "multiplewords",
        },
    },
    {
        "id": "single_acronym",
        "words": ["io"],
        "acronyms": ["io"],
        "schemes": {
            (NamingScheme.hyphen, None): "io",
            (NamingScheme.underscore, None): "io",
            (NamingScheme.camel, None): "io",
            (NamingScheme.camel, AcronymScheme.upper): "io",
            (NamingScheme.camel, AcronymScheme.lower): "io",
            (NamingScheme.camel, AcronymScheme.two_letter_limit): "io",
            (NamingScheme.pascal, None): "IO",
            (NamingScheme.pascal, AcronymScheme.upper): "IO",
            (NamingScheme.pascal, AcronymScheme.lower): "io",
            (NamingScheme.pascal, AcronymScheme.two_letter_limit): "IO",
            (NamingScheme.lower, None): "io",
        },
    },
    {
        "id": "multiple_words_with_acronym_at_front",
        "words": ["io", "word"],
        "acronyms": ["io"],
        "schemes": {
            (NamingScheme.hyphen, None): "io-word",
            (NamingScheme.underscore, None): "io_word",
            (NamingScheme.camel, None): "ioWord",
            (NamingScheme.camel, AcronymScheme.upper): "ioWord",
            (NamingScheme.camel, AcronymScheme.lower): "ioWord",
            (NamingScheme.camel, AcronymScheme.two_letter_limit): "ioWord",
            (NamingScheme.pascal, None): "IOWord",
            (NamingScheme.pascal, AcronymScheme.upper): "IOWord",
            (NamingScheme.pascal, AcronymScheme.lower): "ioWord",
            (NamingScheme.pascal, AcronymScheme.two_letter_limit): "IOWord",
            (NamingScheme.lower, None): "ioword",
        },
    },
    {
        "id": "multiple_words_with_acronym_in_middle",
        "words": ["words", "io", "multiple"],
        "acronyms": ["io"],
        "schemes": {
            (NamingScheme.hyphen, None): "words-io-multiple",
            (NamingScheme.underscore, None): "words_io_multiple",
            (NamingScheme.camel, None): "wordsIOMultiple",
            (NamingScheme.camel, AcronymScheme.upper): "wordsIOMultiple",
            (NamingScheme.camel, AcronymScheme.lower): "wordsioMultiple",
            (NamingScheme.camel, AcronymScheme.two_letter_limit): "wordsIOMultiple",
            (NamingScheme.pascal, None): "WordsIOMultiple",
            (NamingScheme.pascal, AcronymScheme.upper): "WordsIOMultiple",
            (NamingScheme.pascal, AcronymScheme.lower): "WordsioMultiple",
            (NamingScheme.pascal, AcronymScheme.two_letter_limit): "WordsIOMultiple",
            (NamingScheme.lower, None): "wordsiomultiple",
        },
    },
    {
        "id": "multiple_words_with_acronym_at_end",
        "words": ["multiple", "words", "io"],
        "acronyms": ["io"],
        "schemes": {
            (NamingScheme.hyphen, None): "multiple-words-io",
            (NamingScheme.underscore, None): "multiple_words_io",
            (NamingScheme.camel, None): "multipleWordsIO",
            (NamingScheme.camel, AcronymScheme.upper): "multipleWordsIO",
            (NamingScheme.camel, AcronymScheme.lower): "multipleWordsio",
            (NamingScheme.camel, AcronymScheme.two_letter_limit): "multipleWordsIO",
            (NamingScheme.pascal, None): "MultipleWordsIO",
            (NamingScheme.pascal, AcronymScheme.upper): "MultipleWordsIO",
            (NamingScheme.pascal, AcronymScheme.lower): "MultipleWordsio",
            (NamingScheme.pascal, AcronymScheme.two_letter_limit): "MultipleWordsIO",
            (NamingScheme.lower, None): "multiplewordsio",
        },
    },
    {
        "id": "same_acronym_twice",
        "words": ["io", "word", "io"],
        "acronyms": ["io"],
        "schemes": {
            (NamingScheme.hyphen, None): "io-word-io",
            (NamingScheme.underscore, None): "io_word_io",
            (NamingScheme.camel, None): "ioWordIO",
            (NamingScheme.camel, AcronymScheme.upper): "ioWordIO",
            (NamingScheme.camel, AcronymScheme.lower): "ioWordio",
            (NamingScheme.camel, AcronymScheme.two_letter_limit): "ioWordIO",
            (NamingScheme.pascal, None): "IOWordIO",
            (NamingScheme.pascal, AcronymScheme.upper): "IOWordIO",
            (NamingScheme.pascal, AcronymScheme.lower): "ioWordio",
            (NamingScheme.pascal, AcronymScheme.two_letter_limit): "IOWordIO",
            (NamingScheme.lower, None): "iowordio",
        },
    },
    {
        "id": "multiple_acronyms",
        "words": ["io", "word", "ui"],
        "acronyms": ["ui", "io"],
        "schemes": {
            (NamingScheme.hyphen, None): "io-word-ui",
            (NamingScheme.underscore, None): "io_word_ui",
            (NamingScheme.camel, None): "ioWordUI",
            (NamingScheme.camel, AcronymScheme.upper): "ioWordUI",
            (NamingScheme.camel, AcronymScheme.lower): "ioWordui",
            (NamingScheme.camel, AcronymScheme.two_letter_limit): "ioWordUI",
            (NamingScheme.pascal, None): "IOWordUI",
            (NamingScheme.pascal, AcronymScheme.upper): "IOWordUI",
            (NamingScheme.pascal, AcronymScheme.lower): "ioWordui",
            (NamingScheme.pascal, AcronymScheme.two_letter_limit): "IOWordUI",
            (NamingScheme.lower, None): "iowordui",
        },
    },
    {
        "id": "multiple_acronyms_together",
        "words": ["word", "io", "ui"],
        "acronyms": ["ui", "io"],
        "schemes": {
            (NamingScheme.hyphen, None): "word-io-ui",
            (NamingScheme.underscore, None): "word_io_ui",
            (NamingScheme.camel, None): "wordIOUI",
            (NamingScheme.camel, AcronymScheme.upper): "wordIOUI",
            (NamingScheme.camel, AcronymScheme.lower): "wordioui",
            (NamingScheme.camel, AcronymScheme.two_letter_limit): "wordIOUI",
            (NamingScheme.pascal, None): "WordIOUI",
            (NamingScheme.pascal, AcronymScheme.upper): "WordIOUI",
            (NamingScheme.pascal, AcronymScheme.lower): "Wordioui",
            (NamingScheme.pascal, AcronymScheme.two_letter_limit): "WordIOUI",
            (NamingScheme.lower, None): "wordioui",
        },
    },
]


def get_project_scheme_permutations():
    for perm in project_scheme_permutation_map:
        id_ = perm["id"]
        words = perm["words"]
        acronyms = perm["acronyms"]
        for (naming_scheme, acronym_scheme), expected in perm["schemes"].items():
            yield id_, words, acronyms, naming_scheme, acronym_scheme, expected


def get_test_id(perm):
    acronym_scheme = perm[4].value if perm[4] else "None"
    return "-".join([perm[0], perm[3].value, acronym_scheme])


@pytest.mark.parametrize(
    ("words", "acronyms", "naming_scheme", "acronym_scheme", "expected"),
    [perm[1:] for perm in get_project_scheme_permutations()],
    ids=[get_test_id(perm) for perm in get_project_scheme_permutations()],
)
def test_get_project_name_by_scheme(words, acronyms, naming_scheme, acronym_scheme, expected):
    value = {"words": words}
    if acronym_scheme is not None:
        value["acronym_scheme"] = acronym_scheme

    if acronyms is not None:
        value["acronyms"] = acronyms

    project = CoreProject(**value)
    actual = project.get_project_name_by_scheme(naming_scheme)
    assert actual == expected


def test_get_project_name_by_scheme_bad():
    project = CoreProject(words=["blah"])
    with pytest.raises(KeyError):
        project.get_project_name_by_scheme("junk")


@pytest.mark.parametrize(
    ("value", "expected_display_name"),
    [
        pytest.param({"words": ["foo", "bar"]}, "Foo Bar", id="not-in-acronyms"),
        pytest.param(
            {
                "words": ["file", "io", "stuff"],
                "acronyms": ["io", "stuff"],
                "acronym_scheme": AcronymScheme.upper,
            },
            "File IO STUFF",
            id="acronym-upper",
        ),
        pytest.param(
            {
                "words": ["file", "io", "stuff"],
                "acronyms": ["io", "stuff"],
                "acronym_scheme": AcronymScheme.lower,
            },
            "File io stuff",
            id="acronym-lower",
        ),
        pytest.param(
            {"words": ["some", "xyz"], "acronyms": ["xyz"]},
            "Some Xyz",
            id="acronym-two-letter-limit",
        ),
    ],
)
def test_get_display_name(value, expected_display_name):
    project = CoreProject(**value)
    assert project.display_name == expected_display_name
