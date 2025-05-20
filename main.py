"""
EXP FARM - Main Entry Point
"""
import sys
from core.database import init_database


def main():
    """Initialize and run the EXP FARM application"""
    # Initialize database on startup
    init_database()


if __name__ == "__main__":
    main()
