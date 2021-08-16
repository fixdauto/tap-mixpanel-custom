"""Stream type classes for mixpanel_custom."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from mixpanel_custom.client import mixpanel_customStream

import singer

LOGGER = singer.get_logger()

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class CohortMembersStream(mixpanel_customStream):
    """Define custom stream."""
    name = "members"
    path = "engage"
    primary_keys = ["distinct_id"]
    replication_key = None
    # Optionally, you may also use `schema_filepath` in place of `schema`:
    # schema_filepath = SCHEMAS_DIR / "users.json"
    schema = th.PropertiesList(
        th.Property("distinct_id", th.StringType),
        th.Property("email", th.StringType),
        th.Property("properties", th.StringType)
        # th.Property("results", th.StringType),
        # th.Property("page", th.StringType),
        # th.Property("session_id", th.StringType),
        # th.Property("page_size", th.StringType),
        # th.Property("total", th.StringType),
        # th.Property("status", th.StringType),
        # th.Property("computed_at", th.StringType)
    ).to_dict()


class CohortsStream(mixpanel_customStream):
    """Define custom stream."""
    name = "cohorts"
    path = "cohorts/list"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("project_id", th.IntegerType),
        th.Property("id", th.IntegerType),
        th.Property("description", th.StringType),
        th.Property("count", th.IntegerType),
        th.Property("is_visible", th.IntegerType),
        th.Property("created", th.StringType),
        th.Property("name", th.StringType)
    ).to_dict()
    LOGGER.info(f'schema is: {schema}')
