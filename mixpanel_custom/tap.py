"""mixpanel_custom tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from mixpanel_custom.streams import (
    mixpanel_customStream,
    CohortMembersStream,
    CohortsStream
)
# TODO: Compile a list of custom stream types here
#       OR rewrite discover_streams() below with your custom logic.
STREAM_TYPES = [
    CohortMembersStream,
    CohortsStream
]


class Tapmixpanel_custom(Tap):
    """mixpanel_custom tap class."""
    name = "mixpanel_custom"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property("auth_token", th.StringType, default="53b27283c68fd96b757c9b557d959c23", required=True),
        th.Property("project_ids", th.ArrayType(th.StringType), required=False),
        th.Property("start_date", th.DateTimeType),
        th.Property("api_url", th.StringType, default="https://mixpanel.com/api/2.0/"),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
