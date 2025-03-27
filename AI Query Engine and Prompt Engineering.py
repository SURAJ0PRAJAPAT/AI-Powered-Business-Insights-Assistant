import os
from typing import Dict, List, Any
import google.generativeai as genai

class BusinessInsightsAssistant:
    def __init__(self, api_key: str):
        """
        Initialize the Business Insights Assistant with Google Gemini API
        
        Args:
            api_key (str): Google Gemini API key
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def preprocess_query(self, query: str) -> Dict[str, Any]:
        """
        Preprocess and extract context from business queries
        
        Args:
            query (str): Raw business query
        
        Returns:
            Dict containing processed query metadata
        """
        # Advanced query preprocessing
        context_mapping = {
            'keywords': self._extract_keywords(query),
            'business_function': self._detect_business_function(query),
            'query_complexity': self._assess_query_complexity(query)
        }
        return context_mapping
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract key business terms from query"""
        # Implement keyword extraction logic
        business_keywords = [
            'competitive', 'market', 'strategy', 'trend', 
            'performance', 'revenue', 'growth'
        ]
        return [
            keyword for keyword in business_keywords 
            if keyword.lower() in query.lower()
        ]
    
    def _detect_business_function(self, query: str) -> str:
        """Detect the primary business function of the query"""
        function_mappings = {
            'finance': ['budget', 'revenue', 'cost', 'financial'],
            'marketing': ['market', 'campaign', 'branding', 'customer'],
            'operations': ['efficiency', 'process', 'workflow', 'productivity'],
            'sales': ['sales', 'revenue', 'growth', 'pipeline']
        }
        
        for function, keywords in function_mappings.items():
            if any(keyword.lower() in query.lower() for keyword in keywords):
                return function
        
        return 'general'
    
    def _assess_query_complexity(self, query: str) -> str:
        """Assess the complexity of the business query"""
        word_count = len(query.split())
        
        if word_count <= 10:
            return 'low'
        elif 10 < word_count <= 25:
            return 'medium'
        else:
            return 'high'
    
    def generate_prompt(self, query: str) -> str:
        """
        Generate a sophisticated, context-aware prompt
        
        Args:
            query (str): Original business query
        
        Returns:
            str: Engineered prompt for Gemini API
        """
        context = self.preprocess_query(query)
        
        prompt_template = f"""
        Business Intelligence Analysis Framework:
        
        CONTEXT:
        - Business Function: {context['business_function']}
        - Query Complexity: {context['query_complexity']}
        - Detected Keywords: {', '.join(context['keywords'])}

        PRIMARY TASK:
        Analyze the following business query with a systematic, strategic approach:
        "{query}"

        ANALYSIS REQUIREMENTS:
        1. Break down the query into distinct analytical components
        2. Provide data-driven insights
        3. Suggest actionable strategic recommendations
        4. Assess potential risks and opportunities
        5. Contextualize insights within broader industry trends

        RESPONSE FORMAT:
        - Structured executive summary
        - Detailed strategic analysis
        - Actionable recommendations
        - Supporting data points
        """
        
        return prompt_template
    
    def generate_insights(self, query: str) -> Dict[str, Any]:
        """
        Generate comprehensive business insights
        
        Args:
            query (str): Business query
        
        Returns:
            Dict with generated insights
        """
        engineered_prompt = self.generate_prompt(query)
        
        try:
            response = self.model.generate_content(engineered_prompt)
            
            return {
                'raw_response': response.text,
                'business_function': self._detect_business_function(query),
                'complexity': self._assess_query_complexity(query)
            }
        
        except Exception as e:
            return {
                'error': str(e),
                'message': 'Failed to generate insights'
            }

# Example Usage
def main():
    api_key = os.getenv('GEMINI_API_KEY')
    assistant = BusinessInsightsAssistant(api_key)
    
    # Example Business Queries
    queries = [
        "Analyze our marketing strategy's effectiveness in the past quarter",
        "Forecast sales growth for our new product line",
        "Identify competitive advantages in our current market position"
    ]
    
    for query in queries:
        insights = assistant.generate_insights(query)
        print(f"Query: {query}")
        print(f"Insights: {insights}\n")

if __name__ == "__main__":
    main()
