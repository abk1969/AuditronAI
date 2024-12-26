"""
Critique and Refine technique for prompt optimization with token limit handling
"""
from typing import Any, Tuple, List, Dict
from dataclasses import dataclass
import tiktoken

@dataclass
class TokenStats:
    """Track token usage statistics"""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0

class CritiqueNRefine:
    def __init__(self, config: dict):
        """
        Initialize the CritiqueNRefine technique with token-aware configuration
        
        Args:
            config: Configuration dictionary for the technique
        """
        self.config = config
        self.max_tokens = config.get('max_tokens', 100000)  # Claude's limit
        self.chunk_size = config.get('chunk_size', 8000)    # Safe chunk size
        self.encoder = tiktoken.get_encoding("cl100k_base")  # Claude's encoding
        self.token_stats = TokenStats()
        
    def count_tokens(self, text: str) -> int:
        """Count tokens in a text string"""
        return len(self.encoder.encode(text))
        
    def chunk_text(self, text: str) -> List[str]:
        """Split text into chunks that respect token limits"""
        chunks = []
        tokens = self.encoder.encode(text)
        
        for i in range(0, len(tokens), self.chunk_size):
            chunk_tokens = tokens[i:i + self.chunk_size]
            chunk_text = self.encoder.decode(chunk_tokens)
            chunks.append(chunk_text)
            
        return chunks

    def merge_critiques(self, critiques: List[Dict]) -> Dict:
        """Merge multiple critique results intelligently"""
        merged = {
            'improvements': [],
            'suggestions': [],
            'warnings': []
        }
        
        for critique in critiques:
            for key in merged:
                if key in critique:
                    merged[key].extend(critique[key])
                    
        # Remove duplicates while preserving order
        for key in merged:
            merged[key] = list(dict.fromkeys(merged[key]))
            
        return merged

    def optimize(self, dataset: Any) -> Tuple[str, dict]:
        """
        Run the optimization process with token limit handling
        
        Args:
            dataset: Dataset to optimize against
            
        Returns:
            Tuple containing:
            - best_prompt: The optimized prompt
            - expert_profile: Information about the expert profile used
        """
        current_prompt = dataset.get_initial_prompt()
        iterations = self.config.get('max_iterations', 3)
        
        for iteration in range(iterations):
            # Split prompt if needed
            prompt_chunks = self.chunk_text(current_prompt)
            chunk_critiques = []
            
            # Process each chunk while tracking tokens
            for chunk in prompt_chunks:
                # Count tokens for this chunk
                chunk_tokens = self.count_tokens(chunk)
                
                if self.token_stats.total_tokens + chunk_tokens > self.max_tokens:
                    # Implement fallback strategy
                    break
                    
                # Update token stats
                self.token_stats.prompt_tokens += chunk_tokens
                
                # Get critique for this chunk
                critique = self._get_critique(chunk, dataset)
                chunk_critiques.append(critique)
                
                # Update completion tokens
                self.token_stats.completion_tokens += self.count_tokens(str(critique))
                self.token_stats.total_tokens = (
                    self.token_stats.prompt_tokens + 
                    self.token_stats.completion_tokens
                )
            
            # Merge critiques from all chunks
            merged_critique = self.merge_critiques(chunk_critiques)
            
            # Apply improvements while respecting token limits
            current_prompt = self._apply_improvements(
                current_prompt, 
                merged_critique,
                self.chunk_size
            )
            
            # Check if we've reached token limit
            if self.token_stats.total_tokens >= self.max_tokens:
                break
                
        return current_prompt, {
            "role": "expert",
            "token_stats": self.token_stats
        }
        
    def _get_critique(self, prompt_chunk: str, dataset: Any) -> Dict:
        """
        Get critique for a prompt chunk
        
        Args:
            prompt_chunk: Chunk of prompt to critique
            dataset: Dataset to evaluate against
            
        Returns:
            Dictionary containing critique information
        """
        # TODO: Implement actual critique logic
        # This would integrate with your LLM client
        return {
            "improvements": [
                "Suggestion 1 for chunk",
                "Suggestion 2 for chunk"
            ],
            "warnings": []
        }
        
    def _apply_improvements(
        self, 
        prompt: str, 
        critique: Dict,
        max_chunk_size: int
    ) -> str:
        """
        Apply improvements from critique while respecting token limits
        
        Args:
            prompt: Current prompt
            critique: Critique dictionary
            max_chunk_size: Maximum chunk size in tokens
            
        Returns:
            Improved prompt
        """
        improved = prompt
        
        # Apply improvements incrementally while checking token count
        for improvement in critique.get('improvements', []):
            potential_prompt = self._apply_single_improvement(improved, improvement)
            
            # Check if applying this improvement would exceed chunk size
            if self.count_tokens(potential_prompt) <= max_chunk_size:
                improved = potential_prompt
            else:
                break
                
        return improved
        
    def _apply_single_improvement(self, prompt: str, improvement: str) -> str:
        """
        Apply a single improvement to the prompt
        
        Args:
            prompt: Current prompt
            improvement: Improvement suggestion
            
        Returns:
            Modified prompt
        """
        # TODO: Implement actual improvement application logic
        # This would contain the logic for applying specific types of improvements
        return prompt  # Placeholder
