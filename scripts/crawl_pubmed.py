async def main():
    """Standalone script entry point for running PubMed crawl."""
    import logging
    logging.basicConfig(level=logging.INFO)
    from backend.ingestion.pubmed import crawl_pubmed
    result = await crawl_pubmed()
    print(f"Done: {result}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
