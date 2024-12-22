from AuditronAI.core.custom_dataset import CustomDataset
from dotenv import load_dotenv

def main():
    # Charger les variables d'environnement
    load_dotenv()
    
    # Créer une instance du dataset
    dataset = CustomDataset("code_review_examples")
    
    # Exemple de code à analyser
    code_examples = [
        {
            "code": """
def calculate_sum(a, b):
    return a + b
            """
        },
        {
            "code": """
def process_data(data):
    if data == None:
        return []
    return [x * 2 for x in data]
            """
        }
    ]
    
    # Générer des revues de code pour chaque exemple
    for example in code_examples:
        response = dataset.generate_completion("code_review", example)
        print("\nCode à analyser:")
        print(example["code"])
        print("\nRevue de code:")
        print(response)
        print("-" * 80)

if __name__ == "__main__":
    main()
