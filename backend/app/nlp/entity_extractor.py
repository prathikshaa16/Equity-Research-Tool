import spacy
import logging
from typing import List, Dict, Tuple
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import torch
from ..core.config import settings

logger = logging.getLogger(__name__)


class EntityExtractor:
    def __init__(self):
        self.nlp_model = None
        self.transformer_pipeline = None
        self.device = 0 if torch.cuda.is_available() else -1
        self._load_models()
    
    def _load_models(self):
        """Load NLP models for entity extraction"""
        # Load spaCy model
        try:
            self.nlp_model = spacy.load("en_core_web_sm")
            logger.info("Loaded spaCy model")
        except OSError:
            logger.warning("spaCy model not found. Downloading...")
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            try:
                self.nlp_model = spacy.load("en_core_web_sm")
                logger.info("Downloaded and loaded spaCy model")
            except Exception as e:
                logger.error(f"Error loading spaCy model: {e}")
        
        # Load transformer model
        try:
            model_name = settings.NER_MODEL
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForTokenClassification.from_pretrained(model_name)
            
            self.transformer_pipeline = pipeline(
                "ner",
                model=model,
                tokenizer=tokenizer,
                aggregation_strategy="simple",
                device=self.device
            )
            logger.info(f"Loaded transformer NER model: {model_name}")
        except Exception as e:
            logger.error(f"Error loading transformer NER model: {e}")
    
    def extract_entities_spacy(self, text: str) -> List[Dict]:
        """Extract entities using spaCy"""
        if not self.nlp_model:
            return []
        
        try:
            doc = self.nlp_model(text)
            entities = []
            
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char,
                    "confidence": 1.0  # spaCy doesn't provide confidence scores
                })
            
            return entities
        except Exception as e:
            logger.error(f"Error extracting entities with spaCy: {e}")
            return []
    
    def extract_entities_transformers(self, text: str) -> List[Dict]:
        """Extract entities using transformer model"""
        if not self.transformer_pipeline:
            return []
        
        try:
            # Truncate text if too long
            max_length = 512
            if len(text) > max_length:
                text = text[:max_length]
            
            results = self.transformer_pipeline(text)
            
            entities = []
            for result in results:
                entities.append({
                    "text": result["word"],
                    "label": result["entity_group"],
                    "start": result["start"],
                    "end": result["end"],
                    "confidence": result["score"]
                })
            
            return entities
        except Exception as e:
            logger.error(f"Error extracting entities with transformers: {e}")
            return []
    
    def extract_companies(self, text: str) -> List[str]:
        """Extract company names from text"""
        entities = self.extract_entities_spacy(text)
        companies = []
        
        for entity in entities:
            if entity["label"] in ["ORG", "PRODUCT"]:
                companies.append(entity["text"])
        
        # Remove duplicates
        return list(set(companies))
    
    def extract_financial_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract financial entities like companies, people, locations"""
        entities = self.extract_entities_spacy(text)
        
        financial_entities = {
            "companies": [],
            "people": [],
            "locations": [],
            "organizations": [],
            "money": [],
            "dates": []
        }
        
        for entity in entities:
            label = entity["label"]
            text = entity["text"]
            
            if label == "ORG":
                financial_entities["organizations"].append(text)
                financial_entities["companies"].append(text)  # Assume ORG could be company
            elif label == "PERSON":
                financial_entities["people"].append(text)
            elif label in ["GPE", "LOC"]:
                financial_entities["locations"].append(text)
            elif label == "MONEY":
                financial_entities["money"].append(text)
            elif label == "DATE":
                financial_entities["dates"].append(text)
        
        # Remove duplicates
        for key in financial_entities:
            financial_entities[key] = list(set(financial_entities[key]))
        
        return financial_entities
    
    def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """Extract keywords using spaCy's POS tagging"""
        if not self.nlp_model:
            return []
        
        try:
            doc = self.nlp_model(text)
            
            # Extract nouns and proper nouns as keywords
            keywords = []
            for token in doc:
                if (token.pos_ in ["NOUN", "PROPN"] and 
                    not token.is_stop and 
                    not token.is_punct and
                    len(token.text) > 2):
                    keywords.append(token.lemma_.lower())
            
            # Remove duplicates and return top keywords
            unique_keywords = list(set(keywords))
            return unique_keywords[:max_keywords]
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []
    
    def extract_all(self, text: str) -> Dict:
        """Extract all types of entities and information"""
        return {
            "entities": self.extract_entities_spacy(text),
            "companies": self.extract_companies(text),
            "financial_entities": self.extract_financial_entities(text),
            "keywords": self.extract_keywords(text)
        }
