#!/usr/bin/env python3
"""Test Gemini CLI directly without SDK"""

import subprocess
import os

print("Testing Gemini CLI directly...")
print(f"GEMINI_API_KEY set: {bool(os.getenv('GEMINI_API_KEY'))}")
print()

# Test 1: Simple command
print("Test 1: Running gemini -p 'What is 2+2?'")
result = subprocess.run(
    ["gemini", "-p", "What is 2+2?"],
    capture_output=True,
    text=True
)
print(f"Return code: {result.returncode}")
print(f"Stdout: {result.stdout}")
print(f"Stderr: {result.stderr}")
print("-" * 50)

# Test 2: With full path
print("\nTest 2: With full path")
gemini_path = subprocess.run(["which", "gemini"], capture_output=True, text=True).stdout.strip()
print(f"Gemini path: {gemini_path}")

if gemini_path:
    result = subprocess.run(
        [gemini_path, "-p", "Say hello"],
        capture_output=True,
        text=True
    )
    print(f"Return code: {result.returncode}")
    print(f"Stdout: {result.stdout}")
    print(f"Stderr: {result.stderr}")