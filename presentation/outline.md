# Orchestrate Agentic AI
---
type: title-slide
---

## Context, Checklists, and No-Miss Reviews

_Calvin Hendryx-Parker — Six Feet Up_

???

- introduce your self, whatever usual patter, etc

# 01 What is this really about, who is it for

Getting Things Done (.AI)

???

- talk is for folks who have used AI in apps or the browser, but suspect that it could do more to solve their business problems
- technically enthusiastic, are familar with the terminal, or have the patience and persistence to give it a try.
- some words as a preamble and reassurance:
  - it may be more technical than some of you are ready for, but if you understand the capability, you should be able to benefit
  - we will move, but not too fast
  - there will be resource available online after the talk

# Where we are going

![Agentic horizon](img)

???

We are going to a place where we can boil down some the noise so you
can feel confident making use and building your own simple agent based
systems.

To do that, we are going to demo a fictious problem that might feel
familiar.  We will use coding agents, and show you how you can use
them in a business operations settings.  We discuss the pitfalls,
tradeoff and the opportunities that are unfolding in the space.




# 02 Orchestration

![an orchestra](img) ![a data center](img) ![dice](img)

???

Wikipedia has 3 definitions for "Orchestration": for music, for
computers and for games.  In all three cases, you could make the
argument orchestration is an act of managing complexity and the
uncertainty it can create.

We are going talk about managing agents to help manage the complexity
incipient to working in the digital age.

We will start with the operator to agent relationship and then talk
about what we can do with larger groups of agents.


# 03 Let's Get Real (sort of)



???

Let's dive in to made up problem that should illustrate some real
tecniques you can use. We will explore how not managing context can
impact outcome, techniques for detail with context limits, [fill in
the rest]


# This is a contracts, there are many like it

_but this could ruin your day_




# 04 So much text, so little context

[table of info about modules pdfs: files size, token sizes, totals]
[table of info about context windows: claude, chatgpt, gemini]

???

<demo>
Show of borking the context
</demo>
Wouldn't it be nice if you could just dump all the things into Claude or chatgpt.

One of the more frustrating things about LLMs and the agent that use
them is the constraint of the context buffer.  Since LLMs do not learn
in our interactions, we must maintain state elsewhere.  The context
buffer is the default place... as you chat it fills with everything
you ask the model, every please and thank you and every reply.  Any
digression become part of this state, as other mechanisms often hidden
behind the user interface.

Eventually nothing more can go in and in fact your prompt cannot be
added to context to send to the model unless something gets removed.
Different systems use different strategies, some give you way to
explicitly in how you manage the context sent, but the limitation
always means the model's response will become more and more impacted
by history until it is cleaned.

The difficulty of controlling context contributes to the
nondeterministic behavior of LLM driven software.  When we humans,
also nondeterministic agents, interact directly, determinism gets
harder.

afaict, in the claude code agent, the context is saved as raw tokenized text
and is not exposed by any api.

The context buffer is a bit like an agents working memory & long term
memory rolled into one.  If one talks directly to the LLM, it is
possible to aggressively manage this "hand" to create more
durable memories while scrubbing the context.

otoh, we just need to get this information back to Safe Houses lawyer.

- show [context management explainer](context-window-explainer.html):
  has context windows sizes for all of the major models.  Also talks about ways to monitor context.
- show /context



# 05 Exo-context & skills

[brain picture](img)

???

We need an exocortex for our agent. It can do the remembering about
all these text files while we explore the data. To do this we have
create another kind of memory: the agent skill.  Skills allow us to
codify (save) things we know how to do and need to do in a form that
the agent can do them for us, either explicitly or implicitly.

For memory, we will utilize the reigning champion for remember, the
database. We will use 2 different forms of member: sql and vector
storage.

The first is well known by LLMs who can write sql better than me.
- introduce sqllite skill

The second storages data in a way similar to the LLM, as embeddings
- show off chroma

<demo>
- show off definitions of each skill
- make a query for each
- load some small amount of data for each (list of adventures from hasbro)
</demo>


# 06 The orchestration loop

???

Many of you will recognize the following pattern which is one
operators tend to follow: observe, orient, decide, act. The OODA was
formally define by USAF Colonel John Boyd in the early 70s.

Unlike most formalized engineering process, it is designed for practical
in the moment work.

While claude code could do engineering for us, we are more in a making
furniture with a chainsaw sort of situation.  The lawyers need to
know, but we do know yet what the outcome will look like.

We will do what we can reasonable to encourage deterministic behavior,
but the clock is ticking.


# 06 See

![1 agents](img)

???

<demo>

Observe

Explore the data, prototype how to make a match

</demo>

# 07 Plan

![2 agents](img)

???

<demo>

Orient

use claude to explore the space and suggest options:
- dialectic with agent
- create a skill that helps toward final goal
- use a visualizer to understand problem

</demo>

# 08 Choose

![3 agents](img)

???

<demo>

Decide

- adversarial review
- create agents to do special parts of the job like reporter and ingester, supervisor
- discuss how encapsulation can help w/ context bitrot as well other things like auditing
- define an aceptance criterion

</demo>

# 09 Act

![4 agents](img)

???

<demo>

Act

- work with claude to multiplex the action using agents and skills
- discuss routing and handoffs
- have claude report progress, have a final report (explainer?)

</demo>

# 10 Live and let die another day

![]()

???

Safe house is happy, their deal can move forward, their fans will be
happy, they will hire us again.


Talk about repo and playbook


# 11 The Future is Agentic

The Future is Agentic
_But so was the past_

???

Closing remarks --
- multi-agent workflow can model how we do things in an office as well as more low level processes
- we can model and enforce engineer practice in ways we never could before and it is having interesting outcomes
- software is cheaper which make operation more expensive
- context buffers issue also occur between the ears and between people -- the struggle to keep down the noice is real.
