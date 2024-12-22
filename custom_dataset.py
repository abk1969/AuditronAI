from promptwizard.glue.promptopt.techniques.common_logic import DatasetSpecificProcessing
import re
import json

class CustomMathDataset(DatasetSpecificProcessing):
    def extract_answer_from_output(self, answer: str) -> str:
        """Extrait la réponse concise du dataset."""
        return answer.strip()

    def extract_final_answer(self, llm_output: str) -> str:
        """Extrait la réponse finale de la sortie du LLM."""
        pattern = r'<ANS_START>(.*?)<ANS_END>'
        matches = re.findall(pattern, llm_output)
        if matches:
            return matches[0].strip()
        return ""

    def access_answer(self, llm_output: str, ground_truth: str) -> tuple:
        """Évalue la réponse du LLM par rapport à la vérité terrain."""
        extracted_answer = self.extract_final_answer(llm_output)
        is_correct = extracted_answer == self.extract_answer_from_output(ground_truth)
        return extracted_answer, is_correct
        
    def dataset_to_jsonl(self, dataset_path: str, output_path: str) -> None:
        """Convertit le dataset en format jsonl."""
        with open(dataset_path, 'r') as f:
            data = json.load(f)
            
        with open(output_path, 'w') as f:
            for item in data:
                json.dump(item, f)
                f.write('\n')
