from pymilvus import MilvusClient as PyMilvusClient, FieldSchema, CollectionSchema, DataType, Collection, utility # type: ignore
import numpy as np # type: ignore
import sys


class MilvusClient:
    """
    Milvus vector database client
    """

    def __init__(self):
        self.collection_name = "face_embeddings"
        # try to connect to Milvus; if unavailable, fall back to in-memory store
        self.collection = None
        self.client = None
        self._memory_store = []  # list of tuples (id, embedding)

        try:
            self.client = PyMilvusClient(uri="http://localhost:19530", timeout=5)
            self.collection = self._create_collection()
        except Exception as exc:
            print(f"[MilvusClient] Milvus unavailable, using fallback: {exc}", file=sys.stderr)
            self.collection = None

    def _create_collection(self):
        """
        Create collection if not exists
        """

        fields = [
            FieldSchema(name="user_id", dtype=DataType.INT64, is_primary=True, auto_id=False),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=512)
        ]

        schema = CollectionSchema(fields, description="Face embeddings")

        if not utility.has_collection(self.collection_name):
            return Collection(name=self.collection_name, schema=schema, using="default")

        return Collection(self.collection_name, using="default")

    def insert(self, data):
        """
        Insert embeddings into Milvus
        data = [{"id": user_id, "vector": embedding}]
        """

        # accept single dict or list of dicts
        if isinstance(data, dict):
            data = [data]

        if not hasattr(data, '__iter__'):
            raise TypeError("MilvusClient.insert expects a list of dicts or a dict")

        ids = [item["id"] for item in data]
        vectors = [item["vector"] for item in data]

        if self.collection is None:
            # store in memory
            for i, v in zip(ids, vectors):
                self._memory_store.append((i, v))
            return True

        try:
            self.collection.insert([ids, vectors])
            self.collection.flush()
            return True
        except Exception as exc:
            print(f"[MilvusClient] insert failed, falling back to memory: {exc}", file=sys.stderr)
            self.collection = None
            for i, v in zip(ids, vectors):
                self._memory_store.append((i, v))
            return True

    def search(self, embedding, top_k=1):
        """
        Search similar face
        """

        if self.collection is None:
            # simple in-memory linear search (L2)
            if not self._memory_store:
                print("[MilvusClient] no memory_store entries", file=sys.stderr)
                sys.stderr.flush()
                return None

            dists = []
            for uid, vec in self._memory_store:
                a = np.array(vec, dtype=float)
                b = np.array(embedding, dtype=float)
                dist = float(np.linalg.norm(a - b))
                dists.append((uid, dist))

            dists.sort(key=lambda x: x[1])
            best_id, best_dist = dists[0]
            print(f"[MilvusClient] memory_store_len={len(self._memory_store)} best_dist={best_dist}", file=sys.stderr)
            sys.stderr.flush()
            return {"id": best_id, "score": best_dist}

        try:
            self.collection.load()

            search_params = {
                "metric_type": "L2",
                "params": {"nprobe": 10}
            }

            results = self.collection.search(
                data=[embedding],
                anns_field="embedding",
                param=search_params,
                limit=top_k,
                output_fields=["user_id"]
            )

            if not results:
                return None

            hit = results[0][0]
        except Exception as exc:
            print(f"[MilvusClient] search failed, falling back to memory: {exc}", file=sys.stderr)
            self.collection = None
            if not self._memory_store:
                return None

            dists = []
            for uid, vec in self._memory_store:
                a = np.array(vec, dtype=float)
                b = np.array(embedding, dtype=float)
                dist = float(np.linalg.norm(a - b))
                dists.append((uid, dist))

            dists.sort(key=lambda x: x[1])
            best_id, best_dist = dists[0]
            return {"id": best_id, "score": best_dist}

        return {
            "id": hit.entity.get("user_id"),
            "score": hit.distance
        }