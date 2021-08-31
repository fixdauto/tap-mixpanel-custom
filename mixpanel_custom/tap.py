"""mixpanel_custom tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from mixpanel_custom.streams import (
    RESTStream,
    CohortMembersStream,
    CohortsStream
)

STREAM_TYPES = [
    CohortMembersStream,
    CohortsStream
]


class Tapmixpanel_custom(Tap):
    """mixpanel_custom tap class."""
    name = "mixpanel_custom"

    config_jsonschema = th.PropertiesList(
        th.Property("auth_token", th.StringType, required=True),
        th.Property("project_ids", th.ArrayType(th.StringType), required=False),
        th.Property("start_date", th.DateTimeType),
        th.Property("api_url", th.StringType, default="https://mixpanel.com/api/2.0/"),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
