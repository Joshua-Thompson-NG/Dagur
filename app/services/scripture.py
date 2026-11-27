import httpx
from fastapi import HTTPException, status


async def get_random_scripture(translation: str = "web", book: str | None = None):
    # Example https://bible-api.com/data/web/random/JHN
    url = f"https://bible-api.com/data/{translation}/random"
    if book:
        url = f"{url}/{book.upper()}"

    try:

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url)
            response.raise_for_status()

            data = response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=502,  # noqa: B904
                            detail=f"Failed to fetch scripture from external provider, "
                                   f"Error: {e}")  # noqa: B904
    verse = data.get("random_verse", {})

    return {
        "reference": f"{verse.get('book')} {verse.get('chapter')}:{verse.get('verse')}",
        "text": verse.get("text", "").strip(),
        "translation": data.get("translation", {}).get("name"),
    }
