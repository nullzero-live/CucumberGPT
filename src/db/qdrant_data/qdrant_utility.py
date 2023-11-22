import os
import sys
from utils.CONSTANTS import ENVIRONMENT

'''
Create a utility for interacting with the QDrant Vector Database

'''

from qdrant_client import QdrantClient

if ENVIRONMENT != 'dev':
    docker run -p 6333:6333 qdrant/qdrant
qdrant = QdrantClient(":memory:") # Create in-memory Qdrant instance, for testing, CI/CD
# OR
client = QdrantClient(path="path/to/db")  # Persists changes to disk, fast prototyping