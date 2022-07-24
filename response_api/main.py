
import uvicorn

from response_api import create_app

# Start App.
app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", log_level="debug", port=9000)
