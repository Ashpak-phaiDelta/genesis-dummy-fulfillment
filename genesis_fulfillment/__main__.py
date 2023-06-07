
import uvicorn

if __name__ == '__main__':
    # Start with reloading enabled (must be string to work)
    uvicorn.run("genesis_fulfillment:create_app", host='localhost',
                port=8001, factory=True, reload=True)
