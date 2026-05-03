"""Pytest configuration for Finlo test suite."""
import sys
import os

# Add parent directory to path so 'app' module can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
