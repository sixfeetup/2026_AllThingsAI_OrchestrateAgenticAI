---
type: content-slide
footer: "06"
---

# So much text, so little context

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
