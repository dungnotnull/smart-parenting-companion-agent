import logging

from backend.services.knowledge_seeder import seed_knowledge_base

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, force=True)
    result = seed_knowledge_base(force=True)
    print(f"Seeding complete: {result}")
