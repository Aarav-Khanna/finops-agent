from typing import List, Dict
import json
from datetime import datetime
import numpy as np
from openai import OpenAI
from config import Config

class RAGManager:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.vector_store: List[Dict] = []
        self.embedding_model = "text-embedding-3-small"
        
    def _get_embedding(self, text: str) -> List[float]:
        """Get embedding for a text using OpenAI's embedding model"""
        response = self.client.embeddings.create(
            model=self.embedding_model,
            input=text
        )
        return response.data[0].embedding
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def add_alert(self, alert_data: Dict, analysis: str, solution: str):
        """Add a new alert and its analysis to the vector store"""
        # Create a document with alert details and analysis
        document = {
            "timestamp": datetime.now().isoformat(),
            "alert_name": alert_data["name"],
            "alert_message": alert_data["message"],
            "alert_query": alert_data["query"],
            "alert_tags": alert_data["tags"],
            "analysis": analysis,
            "solution": solution,
            "embedding": self._get_embedding(f"{alert_data['message']} {alert_data['query']}")
        }
        self.vector_store.append(document)
        
        # Keep only last 1000 alerts to manage memory
        if len(self.vector_store) > 1000:
            self.vector_store = self.vector_store[-1000:]
    
    def get_relevant_context(self, alert_data: Dict, top_k: int = 3) -> str:
        """Retrieve relevant context from past alerts"""
        if not self.vector_store:
            return ""
            
        # Get embedding for current alert
        current_embedding = self._get_embedding(f"{alert_data['message']} {alert_data['query']}")
        
        # Calculate similarities and get top k matches
        similarities = [
            (doc, self._cosine_similarity(current_embedding, doc["embedding"]))
            for doc in self.vector_store
        ]
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Format relevant context
        context = "Relevant past alerts and solutions:\n\n"
        for doc, score in similarities[:top_k]:
            if score > 0.7:  # Only include if similarity is high enough
                context += f"Alert: {doc['alert_name']}\n"
                context += f"Message: {doc['alert_message']}\n"
                context += f"Analysis: {doc['analysis']}\n"
                context += f"Solution: {doc['solution']}\n\n"
        
        return context 