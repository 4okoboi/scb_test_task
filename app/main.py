from fastapi import FastAPI, APIRouter
from app.warehouse.router import warehouse_router


from fastapi.middleware.cors import CORSMiddleware

import uvicorn

app = FastAPI(
    title="SCB_TEST_TASK"
)

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

main_router = APIRouter()


main_router.include_router(warehouse_router, prefix="/warehouse", tags=["user"])

app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)