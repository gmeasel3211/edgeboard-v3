import asyncio

from ..db import SessionLocal
from ..services.pipeline import Pipeline


async def main() -> None:
    with SessionLocal() as db:
        result = await Pipeline().refresh(db, triggered_by="scheduled-refresh")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
