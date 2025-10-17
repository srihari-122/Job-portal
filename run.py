#!/usr/bin/env python3
"""
Simple script to run the Job Portal application
"""
import uvicorn
import os
from config import settings

if __name__ == "__main__":
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8005,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
