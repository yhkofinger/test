import requests
import json
from typing import Dict, Optional

class JokeGenerator:
    """A random joke generator using the JokeAPI"""
    
    BASE_URL = "https://v2.jokeapi.dev/joke"
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_random_joke(self, 
                       joke_type: str = "Any",
                       safe_mode: bool = False) -> Optional[Dict]:
        """
        Fetch a random joke from the JokeAPI.
        
        Args:
            joke_type: Type of joke - "Any", "General", "Knock-Knock", "Programming", "Dark", "Spooky", "Christmas"
            safe_mode: If True, filters out offensive content
        
        Returns:
            Dictionary containing the joke data, or None if request fails
        """
        try:
            params = {
                "format": "json",
                "safe-mode": safe_mode
            }
            
            url = f"{self.BASE_URL}/{joke_type}"
            response = self.session.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("error"):
                print(f"Error from API: {data.get('message')}")
                return None
            
            return data
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching joke: {e}")
            return None
    
    def display_joke(self, joke_data: Dict) -> None:
        """Display the joke in a formatted way"""
        if not joke_data:
            return
        
        if joke_data.get("type") == "single":
            print(f"\n😂 {joke_data.get('joke')}\n")
        elif joke_data.get("type") == "twopart":
            print(f"\n😂 {joke_data.get('setup')}")
            print(f"   {joke_data.get('delivery')}\n")
    
    def get_multiple_jokes(self, count: int = 3, joke_type: str = "Any") -> list:
        """Fetch multiple jokes"""
        jokes = []
        for _ in range(count):
            joke = self.get_random_joke(joke_type)
            if joke:
                jokes.append(joke)
        return jokes


def main():
    """Main function to demonstrate the joke generator"""
    generator = JokeGenerator()
    
    print("=" * 50)
    print("🎉 RANDOM JOKE GENERATOR 🎉")
    print("=" * 50)
    
    # Get a single random joke
    print("\n1️⃣  Getting a random joke...")
    joke = generator.get_random_joke()
    generator.display_joke(joke)
    
    # Get a programming joke
    print("\n2️⃣  Getting a programming joke...")
    programming_joke = generator.get_random_joke(joke_type="Programming")
    generator.display_joke(programming_joke)
    
    # Get multiple jokes
    print("\n3️⃣  Getting 3 random jokes...")
    multiple_jokes = generator.get_multiple_jokes(count=3)
    for i, joke_data in enumerate(multiple_jokes, 1):
        print(f"Joke {i}:")
        generator.display_joke(joke_data)
    
    print("=" * 50)


if __name__ == "__main__":
    main()
