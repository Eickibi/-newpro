"""Vercel Python Function entrypoint.

The application logic stays in the project-root index.py so it can also be
run locally with: python index.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import index as root_index
handler = root_index.handler
