import re
import pytest

# Your regex from the bot script
GITHUB_URL_REGEX = re.compile(
    r'(https://github\.com/([^/]+)/([^/]+)/blob/([0-9a-f]+)/(.+?)#L(\d+)(?:-L(\d+))?)'
)

@pytest.mark.parametrize("url,expected", [
    # Test cases with expected outcomes
    (
        "https://github.com/hyperion-mc/hyperion/blob/ef00b81042a6699573013941374099134817502d/crates/hyperion/src/simulation/handlers.rs#L257-L276",
        {
            "full_url": "https://github.com/hyperion-mc/hyperion/blob/ef00b81042a6699573013941374099134817502d/crates/hyperion/src/simulation/handlers.rs#L257-L276",
            "owner": "hyperion-mc",
            "repo": "hyperion",
            "commit": "ef00b81042a6699573013941374099134817502d",
            "filepath": "crates/hyperion/src/simulation/handlers.rs",
            "start_line": "257",
            "end_line": "276",
        },
    ),
    (
        "https://github.com/user/repo/blob/commit/file.py#L5",
        {
            "full_url": "https://github.com/user/repo/blob/commit/file.py#L5",
            "owner": "user",
            "repo": "repo",
            "commit": "commit",
            "filepath": "file.py",
            "start_line": "5",
            "end_line": None,  # No end line here
        },
    ),
    # Negative case
    ("invalid_url_example", None),
])
def test_github_url_regex(url, expected):
    match = GITHUB_URL_REGEX.search(url)
    if expected is None:
        assert match is None
    else:
        assert match is not None
        groups = match.groups()
        result = {
            "full_url": groups[0],
            "owner": groups[1],
            "repo": groups[2],
            "commit": groups[3],
            "filepath": groups[4],
            "start_line": groups[5],
            "end_line": groups[6] if len(groups) > 6 else None,
        }
        assert result == expected