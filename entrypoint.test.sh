#!/bin/bash
set -e

echo "Running ruff lint check..."
ruff check .
