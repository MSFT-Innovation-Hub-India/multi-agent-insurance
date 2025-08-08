"""
Azure OpenAI client management.
"""

from openai import AzureOpenAI
from config.settings import settings

class AzureOpenAIClient:
    """Manages Azure OpenAI client initialization and configuration."""
    
    def __init__(self):
        """Initialize the Azure OpenAI client."""
        settings.validate_settings()
        self._client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the Azure OpenAI client with configured settings."""
        try:
            self._client = AzureOpenAI(
                api_key=settings.AZURE_OPENAI_API_KEY,
                azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
                api_version=settings.AZURE_OPENAI_API_VERSION
            )
        except Exception as e:
            raise Exception(f"Failed to initialize Azure OpenAI client: {e}")
    
    @property
    def client(self) -> AzureOpenAI:
        """Get the Azure OpenAI client instance."""
        if self._client is None:
            self._initialize_client()
        return self._client
    
    def create_response(self, **kwargs):
        """Create a response using the Azure OpenAI client."""
        return self.client.responses.create(**kwargs)
    
    def create_initial_response(self, message: str):
        """Create an initial response with system tools."""
        return self.create_response(
            model=settings.AZURE_OPENAI_MODEL,
            input=[{"role": "user", "content": message}],
            tools=settings.COMPUTER_USE_TOOLS,
            reasoning={"generate_summary": "concise"},
            truncation="auto"
        )
    
    def create_followup_response(self, previous_response_id: str, input_data):
        """Create a follow-up response based on previous response."""
        return self.create_response(
            model=settings.AZURE_OPENAI_MODEL,
            previous_response_id=previous_response_id,
            tools=settings.COMPUTER_USE_TOOLS,
            input=input_data,
            truncation="auto"
        )

# Global client instance
azure_client = AzureOpenAIClient()
