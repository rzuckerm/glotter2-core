import pytest

from glotter_core.project import AcronymScheme, CoreProject, NamingScheme

project_scheme_permutation_map = [
    {
        "id": "single_word_no_acronym",
        "words": ["word"],
        "acronyms": None,
        "schemes": {
            (NamingScheme.hyphen, None): "word",
            (NamingScheme.underscore, None): "word",
            (NamingScheme.camel, None): "word",
            (NamingScheme.camel, "upper"): "word",
            (NamingScheme.camel, "lower"): "word",
            (NamingScheme.camel, "two_letter_limit"): "word",
            (NamingScheme.pascal, None): "Word",
            (NamingScheme.pascal, "upper"): "Word",
            (NamingScheme.pascal, "lower"): "Word",
            (NamingScheme.pascal, "two_letter_limit"): "Word",
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
            (NamingScheme.camel, "upper"): "multipleWords",
            (NamingScheme.camel, "lower"): "multipleWords",
            (NamingScheme.camel, "two_letter_limit"): "multipleWords",
            (NamingScheme.pascal, None): "MultipleWords",
            (NamingScheme.pascal, "upper"): "MultipleWords",
            (NamingScheme.pascal, "lower"): "MultipleWords",
            (NamingScheme.pascal, "two_letter_limit"): "MultipleWords",
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
            (NamingScheme.camel, "upper"): "io",
            (NamingScheme.camel, "lower"): "io",
            (NamingScheme.camel, "two_letter_limit"): "io",
            (NamingScheme.pascal, None): "IO",
            (NamingScheme.pascal, "upper"): "IO",
            (NamingScheme.pascal, "lower"): "io",
            (NamingScheme.pascal, "two_letter_limit"): "IO",
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
            (NamingScheme.camel, "upper"): "ioWord",
            (NamingScheme.camel, "lower"): "ioWord",
            (NamingScheme.camel, "two_letter_limit"): "ioWord",
            (NamingScheme.pascal, None): "IOWord",
            (NamingScheme.pascal, "upper"): "IOWord",
            (NamingScheme.pascal, "lower"): "ioWord",
            (NamingScheme.pascal, "two_letter_limit"): "IOWord",
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
            (NamingScheme.camel, "upper"): "wordsIOMultiple",
            (NamingScheme.camel, "lower"): "wordsioMultiple",
            (NamingScheme.camel, "two_letter_limit"): "wordsIOMultiple",
            (NamingScheme.pascal, None): "WordsIOMultiple",
            (NamingScheme.pascal, "upper"): "WordsIOMultiple",
            (NamingScheme.pascal, "lower"): "WordsioMultiple",
            (NamingScheme.pascal, "two_letter_limit"): "WordsIOMultiple",
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
            (NamingScheme.camel, "upper"): "multipleWordsIO",
            (NamingScheme.camel, "lower"): "multipleWordsio",
            (NamingScheme.camel, "two_letter_limit"): "multipleWordsIO",
            (NamingScheme.pascal, None): "MultipleWordsIO",
            (NamingScheme.pascal, "upper"): "MultipleWordsIO",
            (NamingScheme.pascal, "lower"): "MultipleWordsio",
            (NamingScheme.pascal, "two_letter_limit"): "MultipleWordsIO",
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
            (NamingScheme.camel, "upper"): "ioWordIO",
            (NamingScheme.camel, "lower"): "ioWordio",
            (NamingScheme.camel, "two_letter_limit"): "ioWordIO",
            (NamingScheme.pascal, None): "IOWordIO",
            (NamingScheme.pascal, "upper"): "IOWordIO",
            (NamingScheme.pascal, "lower"): "ioWordio",
            (NamingScheme.pascal, "two_letter_limit"): "IOWordIO",
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
            (NamingScheme.camel, "upper"): "ioWordUI",
            (NamingScheme.camel, "lower"): "ioWordui",
            (NamingScheme.camel, "two_letter_limit"): "ioWordUI",
            (NamingScheme.pascal, None): "IOWordUI",
            (NamingScheme.pascal, "upper"): "IOWordUI",
            (NamingScheme.pascal, "lower"): "ioWordui",
            (NamingScheme.pascal, "two_letter_limit"): "IOWordUI",
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
            (NamingScheme.camel, "upper"): "wordIOUI",
            (NamingScheme.camel, "lower"): "wordioui",
            (NamingScheme.camel, "two_letter_limit"): "wordIOUI",
            (NamingScheme.pascal, None): "WordIOUI",
            (NamingScheme.pascal, "upper"): "WordIOUI",
            (NamingScheme.pascal, "lower"): "Wordioui",
            (NamingScheme.pascal, "two_letter_limit"): "WordIOUI",
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
    acronym_scheme = perm[4] if perm[4] else "None"
    return "-".join([perm[0], perm[3].value, acronym_scheme])


@pytest.mark.parametrize(
    ("acronym_scheme", "expected_acronym_scheme"),
    [pytest.param(member.value, member, id=member.value) for member in AcronymScheme],
)
def test_acronym_scheme(acronym_scheme, expected_acronym_scheme):
    project = CoreProject({"words": ["whatever"], "acronym_scheme": acronym_scheme})
    assert project.acronym_scheme == expected_acronym_scheme


def test_acronym_scheme_bad():
    with pytest.raises(ValueError):
        CoreProject({"words": ["whatever"], "acronym_scheme": "bad"})


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

    project = CoreProject(value)
    actual = project.get_project_name_by_scheme(naming_scheme)
    assert actual == expected


@pytest.mark.parametrize(
    ("naming_scheme", "expected"),
    [
        pytest.param("hyphen", "hello-world", id="hyphen"),
        pytest.param("underscore", "hello_world", id="underscore"),
        pytest.param("camel", "helloWorld", id="camel"),
        pytest.param("pascal", "HelloWorld", id="pascal"),
        pytest.param("lower", "helloworld", id="lower"),
    ],
)
def test_get_project_name_by_scheme_str(naming_scheme, expected):
    project = CoreProject({"words": ["hello", "world"]})
    assert project.get_project_name_by_scheme(naming_scheme) == expected


def test_get_project_name_by_scheme_bad():
    project = CoreProject({"words": ["blah"]})
    with pytest.raises(ValueError):
        project.get_project_name_by_scheme("junk")


@pytest.mark.parametrize(
    ("value", "expected_display_name"),
    [
        pytest.param({"words": ["foo", "bar"]}, "Foo Bar", id="not-in-acronyms"),
        pytest.param(
            {
                "words": ["file", "io", "stuff"],
                "acronyms": ["io", "stuff"],
                "acronym_scheme": "upper",
            },
            "File IO STUFF",
            id="acronym-upper",
        ),
        pytest.param(
            {
                "words": ["file", "io", "stuff"],
                "acronyms": ["io", "stuff"],
                "acronym_scheme": "lower",
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
    project = CoreProject(value)
    assert project.display_name == expected_display_name
