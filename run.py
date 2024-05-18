
import uvicorn


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host='localhost', reload=True, workers=2)
    