# mixpanel_custom

`mixpanel_custom` is a Singer tap for Mixpanel.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

It uses the Mixpanel Engage API to fetch cohort and cohort member data.

## Installation

```bash
pipx install mixpanel_custom
```

## Configuration

### Accepted Config Options

```bash
{
  "api_secret": "YOUR_API_SECRET"
  "start_date": "rfc3339_date_string"
  "project_timezone": "US/Eastern"
  "date_window_size": "30"
  "attribution_window": "5"
  "user_agent": "tap-mixpanel <api_user_email@your_company.com>"
  "cohortIDs": ["List of cohort IDs"]
}
```

A full list of supported settings and capabilities for this
tap is available by running:

```bash
mixpanel_custom --about
```

## Usage

You can easily run `mixpanel_custom` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
mixpanel_custom --version
mixpanel_custom --help
mixpanel_custom --config CONFIG --discover > ./catalog.json
```

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `mixpanel_custom/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `mixpanel_custom` CLI interface directly using `poetry run`:

```bash
poetry run mixpanel_custom --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd mixpanel_custom
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke mixpanel_custom --version
# OR run a test `elt` pipeline:
meltano elt mixpanel_custom target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to develop your own taps and targets.
