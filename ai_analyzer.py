from openai import OpenAI
from config import Config
from rag_manager import RAGManager

class AIAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.rag_manager = RAGManager()

    async def analyze_alert(self, alert_data):
        """Analyze the alert and provide root cause analysis and solution"""
        try:
            # Get relevant context from past alerts
            context = self.rag_manager.get_relevant_context(alert_data)
            
            # Prepare the prompt for the AI
            prompt = f"""
            Analyze this Datadog alert and provide:
            1. Root cause analysis
            2. Proposed solution
            
            Alert Details:
            Name: {alert_data['name']}
            Message: {alert_data['message']}
            Query: {alert_data['query']}
            Tags: {alert_data['tags']}
            State: {alert_data['state']}
            
            {context}
            """

            # Get AI response
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a FinOps expert analyzing Datadog alerts. Provide clear, concise root cause analysis and actionable solutions. Use the provided context from past alerts to inform your analysis when relevant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )

            # Parse the response
            analysis = response.choices[0].message.content
            
            # Split the response into analysis and solution
            parts = analysis.split("Proposed Solution")
            root_cause = parts[0].replace("Root Cause Analysis", "").strip()
            solution = parts[1].strip() if len(parts) > 1 else "No solution provided"

            # Store the alert and its analysis in the RAG system
            self.rag_manager.add_alert(alert_data, root_cause, solution)

            return root_cause, solution
        except Exception as e:
            print(f"Error in AI analysis: {str(e)}")
            return "Error in analysis", "Unable to provide solution" 