d20

rpg are collaborative stochastic storytelling.
- the gamerunner spins a storyline and rules for testing where and how the story can change
- the players develop characters who amass experience, tools and skills that help them have better outcomes
- the dice rolls, modified by circumstance, skill and tool, determine where the story goes

In business,
- the story's setting is your clients, customers, marketplace, problem
  space, operational challenges, skill pool, available resources,
  funding
- the players are you and your team, amassing experience and utilizing tools like agents and process frameworks
- it is not a simulation, probability is continuous.


Determinism

LLMs are some of the worlds largest dice.


Like a di can only land on a side that is defined,
an LLM can only provide accurate inferences on data in it's
training. Figuring out ways to constrain outcome more predictably
becomes an important tool.  If we can constrain the output to a query
to a reasonably useful and predictable space, and follow up with
repair and correction, the overall accuracy of the model is less
important.


Consider concepts like Chain of Thought help provide better focus to
outcomes by constraining the outputs by a sequence of queries, rather
than returning the first result.  The aggregate may take more
roundtrips and tokens, but if the cost is acceptable for the quality
returned, we have succeeded.

Much of what agents do is pure computer function: write files, make
api calls, push to origin, etc.  Like the game runner, there are
junctions in these mundane activities where based on some input, the
agent is take data it has, possibly templated prompts, and querying
the LLM for input that will trigger one or more decisions.

Like our player characters, part of knowledge and experience is
hardcoded into the agent, the LLM is the dice roll that give it
agency.  Unlike a while loop driving a simple daemon, undeterministic
behavior powers the AI agent, creating both risk and opportunity.
