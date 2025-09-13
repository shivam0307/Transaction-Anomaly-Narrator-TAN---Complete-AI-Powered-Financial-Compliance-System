import google.generativeai as genai
from src.config import GEMINI_API_KEY

class NarrativeGenerator:
    """
    Generates plain-English narratives for detected anomalies using an LLM.
    """

    def __init__(self):
        """Initializes the narrative generator and configures the LLM."""
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set. Please check your .env file.")
        
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        print("✨ Narrative Generator initialized with Gemini Pro.")

    def _create_prompt(self, transaction_details: dict) -> str:
        """Creates a structured, grounded prompt for the LLM."""
        
        prompt = f"""
        You are a financial fraud analyst assistant. Your task is to write a concise, 2-sentence summary explaining why a transaction is flagged as anomalous.
        
        **Instructions:**
        1.  Base your summary **exclusively** on the data provided below. Do not add any information not present.
        2.  Be factual and direct.
        3.  Mention the key details like amount, location, time, and the specific anomaly reason.
        
        **Transaction Data:**
        - Transaction ID: {transaction_details.get('TransactionID')}
        - Account ID: {transaction_details.get('AccountID')}
        - Amount: ${transaction_details.get('Amount'):,.2f}
        - Location: {transaction_details.get('Location')}
        - Time: {transaction_details.get('Timestamp').strftime('%H:%M:%S')} on {transaction_details.get('Timestamp').strftime('%Y-%m-%d')}
        - Account's Average Daily Spend: ${transaction_details.get('AvgDailySpend'):,.2f}
        - Detected Anomaly Reasons: {transaction_details.get('AnomalyType')}
        
        Please generate the summary now.
        """
        return prompt

    def generate_narrative(self, transaction_details: dict) -> str:
        """
        Generates a narrative for a single anomalous transaction.
        
        Args:
            transaction_details (dict): A dictionary representing one transaction.
            
        Returns:
            str: The generated plain-English narrative.
        """
        try:
            prompt = self._create_prompt(transaction_details)
            response = self.model.generate_content(prompt)
            # Simple cleanup of the response text
            narrative = response.text.strip().replace("\n", " ")
            return narrative
        except Exception as e:
            print(f"❌ Could not generate narrative for Txn {transaction_details.get('TransactionID')}: {e}")
            return "Narrative generation failed."