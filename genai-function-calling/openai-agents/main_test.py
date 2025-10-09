#
# Copyright Elasticsearch B.V. and contributors
# SPDX-License-Identifier: Apache-2.0
#
import pytest

from main import main


@pytest.mark.vcr
@pytest.mark.asyncio
async def test_main(default_openai_env, capsys):
    await main()

    reply = capsys.readouterr().out.strip()

    assert (
        reply
        == "Latest Elasticsearch 9.x GA version: 9.1.5.\n\nWould you like release notes or guidance on upgrading to 9.1.5?"
    )
