from markflow.formatters.util import truncate_str


class TestTruncateStr:
    def test_shorter(self) -> None:
        assert truncate_str("123456789", 19) == "123456789"

    def test_exact_length(self) -> None:
        assert truncate_str("123456789", 9) == "123456789"

    def test_longer(self) -> None:
        assert truncate_str("123456789", 5) == "12..."

    def test_truncate_less_than_ellipsis(self) -> None:
        assert truncate_str("123456789", 2) == ".."
