"""GeoSentinel Local Runner Entrypoint.

Starts the FastAPI server with live reload and serves both the API
and the tactical frontend dashboard at http://localhost:8000.
"""

import sys
import uvicorn
from backend.app.core.config import settings

if __name__ == "__main__":
    print(f"================================================================")
    print(f"🛰️  Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📍 Environment : {settings.ENVIRONMENT}")
    print(f"🌐 Server URL  : http://localhost:{settings.APP_PORT}")
    print(f"📚 API Docs    : http://localhost:{settings.APP_PORT}/docs")
    print(f"================================================================")
    uvicorn.run(
        "backend.app.main:app",
        host=settings.HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG
    )
