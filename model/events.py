# -*- coding: utf-8 -*-

"""
Events (goals and things that are going to happen)
"""
import model.needs as needs
from configuration import Settings

goal = None


class Event(object):
    """Events are anticipated situations in the inner or perceptual world of the agent. They become
    relevant if they are associated with the expectation of a consumption, i.e. with satisfying or
    frustrating a need.
    If an event is associated with a leading motive, we call it a goal. Goals can be appetive (positive
    reward) or aversive (negative reward). In the latter case, the goal is to avoid the event."""

    def __init__(self, id, consumption, expected_reward=0, certainty=1, skill=0.8, expiration=-1):
        self.id = id  # identifier for the event
        self.consumption = consumption  # consumption that would be affected by the reward
        self.expected_reward = expected_reward  # if positive, satisfaction; if negative, frustration of the need
        self.certainty = certainty  # confidence that the event will happen
        self.skill = skill  # competence to handle the situation if is a goal (0..1)
        self.expiration = expiration  # time left until event in s (-1: event does not time out)

    def update(self):
        # generate pleasure and pain for anticipated events
        self.consumption.anticipate(reward=self.expected_reward, certainty=self.certainty, skill=self.skill,
                                    expiration=self.expiration)

        if self.expiration > 0:
            self.expiration -= Settings.update_milliseconds / 1000
            if self.expiration < 0:
                self.expiration = 0  # you have to drop expired events explicitly

    def is_goal(self):
        return self is goal


events = {}

def estimate_future_appetence():
    """Hope"""
    import model.modulators as modulators
    s = 0
    for e in events.values():
        if e.expected_reward>0 and e.expiration != 0:
            anticipated_reward = e.consumption.get_anticipated_reward(e.expected_reward, e.expiration)
            s+= anticipated_reward *(1+modulators.modulators["focus"].value) if e.is_goal() else anticipated_reward
    return s


def estimate_future_aversion():
    """Fear"""
    import model.modulators as modulators
    s = 0
    for e in events.values():
        if e.expected_reward < 0 and e.expiration != 0:
            anticipated_reward = e.consumption.get_anticipated_reward(e.expected_reward, e.expiration)
            s += anticipated_reward * (1+modulators.modulators["focus"].value) if e.is_goal() else anticipated_reward
    return s


def create_event(id, consumption_name, expected_reward=0, certainty=1, skill=0.8, expiration=-1):
    """Create a new expected event (can also be aversive).
    These are not actual events, but estimates of the agent.
    The creation of events gives us pleasure and pain signals, too.
    Note that we are only interested in events with motivation relevance, i.e. anticipated consumption"""
    if id not in events:
        consumption = needs.consumptions[consumption_name]
        event = Event(id, consumption=consumption, expected_reward=0, certainty=0, skill=skill,
                      expiration=expiration)
        events[id] = event

    change_event(id, expected_reward, certainty, skill, expiration)


def change_event(id, expected_reward=None, certainty=None, skill=None, expiration=None):
    """Change the expectations of an event. The amount of change results in pleasure and pain signals."""

    event = events[id]

    # calculate differences between old and new values, update old values with new ones
    expected_reward_delta = expected_reward - event.expected_reward if expected_reward is not None else 0
    event.expected_reward += expected_reward_delta
    certainty_delta = certainty - event.certainty if certainty is not None else 0
    event.certainty += certainty_delta
    skill_delta = skill - event.skill if skill is not None else 0
    event.skill += skill_delta
    if expiration is not None:
        event.expiration = expiration

    relevance = abs(event.consumption.get_anticipated_reward(event.expected_reward, event.expiration) *
                    event.consumption.need.weight)

    # trigger a satisfaction or frustration event based on the anticipated reward change
    event.consumption.anticipate(expected_reward_delta, event.certainty, event.skill, event.expiration)

    # react to changes in certainty
    if certainty_delta > 0:  # increase in certainty, proportional to relevance of event
        needs.consumptions["confirmation"].trigger(certainty_delta * relevance)
    if certainty_delta < 0:  # decrease in certainty
        needs.consumptions["disconfirmation"].trigger(- certainty_delta * relevance)

    if event.is_goal():
        needs.consumptions["failure"].trigger(-relevance * goal.skill * goal.certainty)

        # react to changes in expected competence
        if skill_delta > 0:  # increase in epistemic competence
            needs.consumptions["success"].anticipate(skill_delta * relevance)
        if skill_delta < 0:
            needs.consumptions["failure"].anticipate(-skill_delta * relevance)


def drop_event(id):
    """This is effectively a change of the event, in which we also delete the event. We are disappointed."""
    change_event(id, expected_reward=0, certainty=0)
    remove_event(id)


def remove_event(id):
    """Delete the event from our expectations, without any other consequences"""
    del events[id]


def execute_event(id, reward=None):
    """Make an event happen, and react to its deviation from or confirmation of expectations.
    The reward reflects the actual reward generated by the world. If the parameter is omitted,
    we assume the reward to be exactly as expected."""
    event = events[id]
    global goal
    if reward is None: reward = event.expected_reward
    event.consumption.trigger(reward)

    relevance = abs(reward * event.consumption.need.weight)

    # how well could I predict the event?
    needs.consumptions["confirmation"].trigger((1 - abs(reward - event.expected_reward)) * relevance)
    # I am only disappointed if I assumed the event to happen with high certainty
    needs.consumptions["disconfirmation"].trigger(-abs(reward - event.expected_reward) * relevance * event.certainty)

    if reward < event.expected_reward:
        needs.consumptions["failure"].trigger((reward - event.expected_reward) * relevance)
        if event.is_goal():
            needs.consumptions["failure"].trigger(event.skill * relevance)  # I failed at my skillz

    else:  # better than expected
        if event.is_goal():
            needs.consumptions["success"].trigger((1 - event.skill) * relevance)  # I succeeded at my skillz

    if event is goal: set_goal(None)
    remove_event(id)


def consume(consumption_name, reward=None):
    """Just consume an unexpected gain or loss, without going to the trouble of creating an event or goal first"""
    consumption = needs.consumptions[consumption_name]
    if reward is None: reward = consumption.default_reward

    consumption.trigger(reward)

    if reward < 0:  # something bad happened unexpectedly, increase uncertainty
        needs.consumptions["disconfirmation"].trigger(reward)
    else:  # something good happened unexpectedly, still increase uncertainty
        needs.consumptions["disconfirmation"].trigger(reward / 2)


def get_events():
    """Returns a sorted list with anticipated events"""
    event_list = [{"id": e.id,
                   "time": e.expiration,
                   "type": "aversive" if e.expected_reward < 0 else "appetitive",
                   "action": e.consumption.name,
                   "need": e.consumption.need.name,
                   "reward": e.expected_reward,
                   "discounted_reward": e.consumption.get_anticipated_reward(e.expected_reward, e.expiration),
                   "certainty": e.certainty,
                   "competence": e.skill,
                   "is_goal": goal == e
                   } for e in events.values()]
    return sorted(event_list, key=lambda k: k['time'])


def set_goal(event_id=None):
    """Set the current goal. There can be only one."""
    global goal
    if event_id is None:
        goal = None
    else:
        goal = events[event_id]


def drop_goal():
    """Give up on a goal because we cannot get it. If we found something better, use set_goal."""
    # If the goal was relevant, we will be disappointed.
    drop_event(goal)


def reset():
    events.clear()
    set_goal(None)


def update():
    for key, event in events.items():
        event.update()
        if event.expiration == 0:  # remove expired events
            del events[key]
