import asyncio
import streamlit as st

async def wait_with_emoji(duration, process):
    """
    Waits for an asynchronous process to complete, printing an emoji every second.
    """
    # Start the async process
    process = asyncio.create_task(process(duration))
    
    emoji_count = 0
    # While the process is running, print emojis every second
    while not process.done():
        emoji_count += 1
        
        await asyncio.sleep(1)

    
    await process  # Wait for the process to complete
    