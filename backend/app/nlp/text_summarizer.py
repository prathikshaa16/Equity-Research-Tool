from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch
import logging
from typing import Dict, List
from ..core.config import settings

logger = logging.getLogger(__name__)


class TextSummarizer:
    def __init__(self):
        self.model_name = settings.SUMMARIZATION_MODEL
        self.device = 0 if torch.cuda.is_available() else -1
        self.pipeline = None
        self._load_model()
    
    def _load_model(self):
        """Load the summarization model"""
        try:
            self.pipeline = pipeline(
                "summarization",
                model=self.model_name,
                tokenizer=self.model_name,
                device=self.device
            )
            logger.info(f"Loaded summarization model: {self.model_name}")
        except Exception as e:
            logger.error(f"Error loading summarization model: {e}")
            # Fallback to a smaller model
            try:
                self.pipeline = pipeline(
                    "summarization",
                    model="t5-small",
                    device=self.device
                )
                logger.info("Loaded fallback summarization model")
            except Exception as e2:
                logger.error(f"Error loading fallback model: {e2}")
                self.pipeline = None
    
    def summarize_text(self, text: str, max_length: int = 150, 
                      min_length: int = 50) -> Dict:
        """Summarize the given text"""
        if not self.pipeline:
            return {
                "summary": text[:200] + "..." if len(text) > 200 else text,
                "confidence": 0.0,
                "error": "Model not available"
            }
        
        try:
            # Truncate text if too long for the model
            max_input_length = 1024
            if len(text) > max_input_length:
                text = text[:max_input_length]
            
            # Ensure text is not too short
            if len(text.strip()) < 50:
                return {
                    "summary": text,
                    "confidence": 1.0,
                    "error": None
                }
            
            result = self.pipeline(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            
            return {
                "summary": result[0]["summary_text"],
                "confidence": 0.8,  # BART doesn't provide confidence scores
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Error summarizing text: {e}")
            return {
                "summary": text[:200] + "..." if len(text) > 200 else text,
                "confidence": 0.0,
                "error": str(e)
            }
    
    def batch_summarize(self, texts: List[str], max_length: int = 150) -> List[Dict]:
        """Summarize multiple texts"""
        results = []
        for text in texts:
            result = self.summarize_text(text, max_length)
            results.append(result)
        return results
    
    def extract_key_points(self, text: str) -> List[str]:
        """Extract key points from text using sentence importance"""
        try:
            # Simple extractive summarization
            sentences = text.split('. ')
            sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
            
            # Score sentences by length and keywords
            scored_sentences = []
            for i, sentence in enumerate(sentences):
                score = len(sentence.split())  # Simple scoring based on word count
                scored_sentences.append((score, sentence, i))
            
            # Sort by score and take top sentences
            scored_sentences.sort(reverse=True)
            key_points = [s[1] for s in scored_sentences[:3]]
            
            return key_points
            
        except Exception as e:
            logger.error(f"Error extracting key points: {e}")
            return []
