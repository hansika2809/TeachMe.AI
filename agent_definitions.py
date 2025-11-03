from agents import (
    Agent, 
    OpenAIChatCompletionsModel
)
# Removed Developer tool imports
# from tools import developer_info, Developer 

# Import the new configuration file
from agent_config import (
    AgentConfig, 
    SPECIALIST_AGENTS_CONFIG, 
    MASTER_AGENT_CONFIG
)

def create_master_agent(model: OpenAIChatCompletionsModel) -> Agent: # Return type changed
    """
    Initializes and returns the master agent
    by dynamically building agents from the agent_config.py file.
    """

    # --- 1. Build Specialist Agents Dynamically ---
    
    specialist_agents = []
    for config in SPECIALIST_AGENTS_CONFIG:
        agent = Agent(
            name=config.name,
            instructions=config.instructions,
            model=model,
            handoff_description=config.handoff_description,
            tools=config.tools 
        )
        specialist_agents.append(agent)

    # --- 2. Build Master Agent ---
    
    master_agent = Agent(
        name=MASTER_AGENT_CONFIG["name"],
        instructions=MASTER_AGENT_CONFIG["instructions"],
        model=model,
        handoffs=specialist_agents,
        tools=[] # Removed developer_info tool
    )

    # --- 3. Developer Context (Removed) ---
    
    return master_agent # Return only the agent