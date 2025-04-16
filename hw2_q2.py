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
    if any(is_worsen(agent.category) for agent in (agent1, agent2)) and not all(
            agent.category == Condition.SICK for agent in (agent1, agent2)):
        return Agent(agent1.name, worsen(agent1.category)), \
               Agent(agent2.name, worsen(agent2.category))

    # Fallback: If for some unforeseen reason no rule applies, return them unchanged.
    return agent1, agent2


def meeting_pair_generator(agents: list):
    """Generator for yielding meeting pairs and skipping over those unable to meet.

    Yields tuples (agent1, agent2) when both agents are available to meet;
    if an agent is not able to meet, yields (None, agent), for logging
    """
    it = iter(agents)
    for agt in it:
        if is_unable_to_meet(agt.category):
            yield None, agt  # this agent cannot meet.
        else:
            # We have an available agent and we looking for the next available partner
            partner = None
            for candidate in it:
                if is_unable_to_meet(candidate.category):
                    yield candidate, None # this agent cannot meet too.
                else:
                    partner = candidate
                    break
            if partner is not None:
                yield agt, partner
            else:
                # No partner found; yield the lone agent.
                yield None, agt

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
    updated = []
    cache = []
    pairs = meeting_pair_generator(list(agent_listing))
    for a, b in pairs:
        if a is None:
            # b is an agent that cannot meet or did not get a partner.
            updated.append(b)
        elif b is None:
            cache.append(a)
        else:
            # a and b are both available to meet.
            new_a, new_b = meet(a, b)
            # if the cache is not empty, we should extend the update to be new_a, cache[0], new_b and clear cache
            if len(cache) > 0:
                updated.extend([new_a, cache[0], new_b])
                cache.clear()
            else:
                updated.extend([new_a, new_b])
    return updated

if __name__ == "__main__":
    # Define a sample tuple of agents.
    agents = (
        Agent("Mark", Condition.SICK),
        Agent("Mork", Condition.HEALTHY),
        Agent("Harry", Condition.DYING),
        Agent("Cure", Condition.CURE),
        Agent("Lora", Condition.SICK),
        Agent("Monica", Condition.SICK),
    )
    # Calculate the updated statuses.
    updated_agents = meetup(agents)
    # Print the results.
    for agent in updated_agents:
        print(f"{agent.name}: {agent.category.name}")

# Agent("Aragorn", Condition.CURE),
# Agent("Frodo", Condition.DYING),
# Agent("Brand", Condition.DYING),
# Agent("Deirdre", Condition.SICK),
# Agent("Sauron", Condition.SICK),
# Agent("Saruman", Condition.DYING),
# Agent("Gandalf", Condition.CURE),
# Agent("Corwin", Condition.CURE),
# Agent("Legolas", Condition.SICK),
# Agent("Thorin", Condition.SICK),
# Agent("Drogon", Condition.DYING),
# Agent("khalisee", Condition.DYING),
# Agent("Galadriel", Condition.HEALTHY),
# Agent("Elrohir", Condition.DEAD)