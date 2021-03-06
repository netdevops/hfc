import pytest

from hier_config.host import Host


class TestHost:
    @pytest.fixture(autouse=True)
    def setup(self, options_ios):
        self.host = Host("example.rtr", "ios", options_ios)

    def test_load_config_from(self, running_config, generated_config):
        self.host.load_running_config(running_config)
        self.host.load_generated_config(generated_config)

        assert len(self.host.generated_config) > 0
        assert len(self.host.running_config) > 0

    def test_load_remediation(self, running_config, generated_config):
        self.host.load_running_config(running_config)
        self.host.load_generated_config(generated_config)
        self.host.remediation_config()

        assert len(self.host.remediation_config().children) > 0

    def test_load_tags(self, tags_ios):
        self.host.load_tags(tags_ios)
        assert len(self.host.hconfig_tags) > 0

    def test_filter_remediation(self, running_config, generated_config, tags_ios):
        self.host.load_running_config(running_config)
        self.host.load_generated_config(generated_config)
        self.host.load_tags(tags_ios)

        rem1 = self.host.remediation_config_filtered_text(set(), set())
        rem2 = self.host.remediation_config_filtered_text({"safe"}, set())

        assert rem1 != rem2
