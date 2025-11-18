"""
Unit tests for URL filtering.
"""

from websearch.filters import URLFilter


class TestURLFilter:
    """Tests for URLFilter class."""

    def test_create_url_filter(self):
        """Test creating URL filter."""
        url_filter = URLFilter(["youtube.com", "facebook.com"])
        assert len(url_filter.disallowed_domains) == 2

    def test_allowed_url(self):
        """Test that allowed URLs pass through."""
        url_filter = URLFilter(["youtube.com"])

        assert url_filter.is_allowed("https://example.com/page")
        assert url_filter.is_allowed("https://google.com/search")
        assert url_filter.is_allowed("https://wikipedia.org/article")

    def test_disallowed_url(self):
        """Test that disallowed URLs are blocked."""
        url_filter = URLFilter(["youtube.com", "youtu.be"])

        assert not url_filter.is_allowed("https://youtube.com/watch?v=123")
        assert not url_filter.is_allowed("https://www.youtube.com/embed/abc")
        assert not url_filter.is_allowed("https://youtu.be/xyz")

    def test_subdomain_matching(self):
        """Test that subdomains are matched."""
        url_filter = URLFilter(["example.com"])

        assert not url_filter.is_allowed("https://www.example.com/page")
        assert not url_filter.is_allowed("https://subdomain.example.com/page")

    def test_case_insensitive_matching(self):
        """Test that domain matching is case-insensitive."""
        url_filter = URLFilter(["YouTube.com"])

        assert not url_filter.is_allowed("https://youtube.com/video")
        assert not url_filter.is_allowed("https://YOUTUBE.COM/video")

    def test_empty_disallowed_list(self):
        """Test filter with empty disallowed list."""
        url_filter = URLFilter([])

        assert url_filter.is_allowed("https://youtube.com")
        assert url_filter.is_allowed("https://any-site.com")

    def test_invalid_url(self):
        """Test handling of invalid URLs."""
        url_filter = URLFilter(["youtube.com"])

        # Invalid URLs should return False
        assert not url_filter.is_allowed("not-a-url")
        assert not url_filter.is_allowed("")
