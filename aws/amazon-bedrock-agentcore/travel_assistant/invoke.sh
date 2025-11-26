#!/bin/bash
# Test script for regular search (no delay)
# This will use both Tavily and DuckDuckGo search engines

START=$(date +%s)
agentcore invoke '{"prompt":"Best places to visit in Netherlands"}'
END=$(date +%s)
echo "Time taken: $((END - START)) seconds"
