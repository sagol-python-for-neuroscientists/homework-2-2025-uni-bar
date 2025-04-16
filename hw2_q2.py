from collections import namedtuple
from enum import Enum

Condition = Enum("Condition", ("CURE", "HEALTHY", "SICK", "DYING", "DEAD"))
Agent = namedtuple("Agent", ("name", "category"))

def improve(category: Condition) -> Condition:
    """Improves the condition by one step."""
    if category == Condition.SICK:
        return Condition.HEALTHY
    elif category == Condition.DYING:
        return Condition.SICK
    return category

def worsen(category: Condition) -> Condition:
    """Worsens the condition by one step."""
    if category == Condition.SICK:
        return Condition.DYING
    elif category == Condition.DYING:
        return Condition.DEAD
    return category

def is_worsen(category: Condition) -> bool:
    """Check if the condition worsens."""
    return category in (Condition.SICK, Condition.DYING)

def is_unable_to_meet(category: Condition) -> bool:
    """Check if the agent is able to meet."""
    return category in (Condition.HEALTHY, Condition.DEAD)

def meet(agent1: Agent, agent2: Agent) -> (Agent, Agent):

    # If either agent is Healthy or Dead, they are not part of any meeting.
    if agent1.category in (Condition.HEALTHY, Condition.DEAD) or \
            agent2.category in (Condition.HEALTHY, Condition.DEAD):
        return agent1, agent2

    # if any of the agents is cure, improve their condition
    if agent1.category == Condition.CURE or agent2.category == Condition.CURE:
        return Agent(agent1.name, improve(agent1.category)), \
               Agent(agent2.name, improve(agent2.category))

    # if any of the agents' condition is_worsen, worsen their condition
    if any(is_worsen(agent.category) for agent in (agent1, agent2)):
        return Agent(agent1.name, worsen(agent1.category)), \
               Agent(agent2.name, worsen(agent2.category))

    # Fallback: If for some unforeseen reason no rule applies, return them unchanged.
    return agent1, agent2


def meeting_index_generator(agents: list):
    """yielding pairs of indices (i, j) from agents
    that are able to meet (i.e., not healthy or dead).
    """
    # indices of agents that can meet.
    available = [i for i, agent in enumerate(agents) if not is_unable_to_meet(agent.category)]
    # if DEBUG_MODE is defined and True, print the available agents, without error if DEBUG_MODE is not defined.
    if DEBUG_MODE:
        print(f"available: {available}")
    # Yield them in pairs (if odd, the last available agent remains unpaired)
    for k in range(0, len(available) - 1, 2):
        yield available[k], available[k+1]

def meetup(agent_listing: tuple) -> list:
    """Model the outcome of the meetings of pairs of agents.

    The pairs of agents are ((a[0], a[1]), (a[2], a[3]), ...). If there's an uneven
    number of agents, the last agent will remain the same.

    Notes
    -----
    The rules governing the meetings were described in the question. The outgoing
    listing may change its internal ordering relative to the incoming one.

    Parameters
    ----------
    agent_listing : tuple of Agent
        A listing (tuple in this case) in which each element is of the Agent
        type, containing a 'name' field and a 'category' field, with 'category' being
        of the type Condition.

    Returns
    -------
    updated_listing : list
        A list of Agents with their 'category' field changed according to the result
        of the meeting.
    """
    updated = list(agent_listing)  # work with a mutable copy in the same order
    for i, j in meeting_index_generator(updated):
        # i and j are indices of two agents available for a meeting.
        new_a, new_b = meet(updated[i], updated[j])
        updated[i] = new_a
        updated[j] = new_b
    return updated

DEBUG_MODE = False
if __name__ == "__main__":
    # Define a sample tuple of agents.
    agents = (
        Agent("Aragorn", Condition.CURE),
        Agent("Frodo", Condition.DYING),
        Agent("Brand", Condition.DYING),
        Agent("Deirdre", Condition.SICK),
        Agent("Sauron", Condition.SICK),
        Agent("Saruman", Condition.DYING),
        Agent("Gandalf", Condition.CURE),
        Agent("Corwin", Condition.CURE),
        Agent("Legolas", Condition.SICK),
        Agent("Thorin", Condition.SICK),
        Agent("Drogon", Condition.DYING),
        Agent("khalisee", Condition.DYING),
        Agent("Galadriel", Condition.HEALTHY),
        Agent("Elrohir", Condition.DEAD),
        Agent("Merlin", Condition.CURE),
    )
    # Calculate the updated statuses.
    updated_agents = meetup(agents)
    # Print the results.
    for agent in updated_agents:
        print(f"{agent.name}: {agent.category.name}")

