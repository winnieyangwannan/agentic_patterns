import json
import requests
from agentic_patterns.tool_pattern.tool import tool
from agentic_patterns.tool_pattern.tool_agent import ToolAgent
from pprint import pprint



def fetch_top_hacker_news_stories(top_n: int):
    """
    Fetch the top stories from Hacker News.

    This function retrieves the top `top_n` stories from Hacker News using the Hacker News API. 
    Each story contains the title, URL, score, author, and time of submission. The data is fetched 
    from the official Firebase Hacker News API, which returns story details in JSON format.

    Args:
        top_n (int): The number of top stories to retrieve.
    """
    top_stories_url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
    
    try:
        response = requests.get(top_stories_url)
        response.raise_for_status()  # Check for HTTP errors
        
        # Get the top story IDs
        top_story_ids = response.json()[:top_n]
        
        top_stories = []
        
        # For each story ID, fetch the story details
        for story_id in top_story_ids:
            story_url = f'https://hacker-news.firebaseio.com/v0/item/{story_id}.json'
            story_response = requests.get(story_url)
            story_response.raise_for_status()  # Check for HTTP errors
            story_data = story_response.json()
            
            # Append the story title and URL (or other relevant info) to the list
            top_stories.append({
                'title': story_data.get('title', 'No title'),
                'url': story_data.get('url', 'No URL available'),
            })
        
        return json.dumps(top_stories)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return []
    



if __name__ == "__main__":


    # 1.  transform the function into a Tool using tool decorator.
    hn_tool = tool(fetch_top_hacker_news_stories)

    print(f"function name: {hn_tool.name}")
    pprint(f"function signature: {hn_tool.fn_signature}")

    # 2. Create a ToolAgent
    tool_agent = ToolAgent(tools=[hn_tool])

    # 3. Run the ToolAgent
    output = tool_agent.run("What are the top 5 stories on Hacker News?")
    print(output)

    # 4. A quick check to see that everything works fine.
    # If we ask the agent something unrelated to Hacker News, it shouldn't use the tool. 
    output = tool_agent.run(user_msg="Tell me your name")
    print(output)
