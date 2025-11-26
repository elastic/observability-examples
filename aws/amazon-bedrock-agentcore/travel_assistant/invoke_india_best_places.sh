#!/bin/bash
# Test script for country-specific search with 120-second delay
# This triggers the special India search tool

START=$(date +%s)
agentcore invoke '{"prompt":"Best places to visit in India"}'
END=$(date +%s)
echo "Time taken: $((END - START)) seconds"
echo "Note: Expected time is 120+ seconds due to intentional delay"
