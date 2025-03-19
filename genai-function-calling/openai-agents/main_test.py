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

    assert reply == "The latest version of Elasticsearch 8 is 8.17.3."
