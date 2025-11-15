"""
Production server runner.
Loads .env.prod environment and runs uvicorn without reload.
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set environment to production
os.environ["APP_ENV"] = "production"

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,
        log_level="info",
        env_file=".env.prod",
    )
