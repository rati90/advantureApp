import sys
sys.path.append("..")

from app import create_app # for the deta.space use only app without .

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)