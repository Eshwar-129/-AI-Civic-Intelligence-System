import asyncio
from backend.agents.detection_agent import detection_agent

async def main():
    state = {"image_path": "uploads/Potholes_and_RoadCracks_57_jpg.rf.d4783af45b0dc27aa69d4a0d48e7c537.jpg"}
    try:
        res = await detection_agent(state)
        print(res)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
