import asyncio

from app.services.digest import generate_digest


async def preview():
    html_content = await generate_digest(city="London")
    with open("preview.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Digest rendered successfully! Open 'preview.html' in your browser.")

if __name__ == "__main__":
    asyncio.run(preview())