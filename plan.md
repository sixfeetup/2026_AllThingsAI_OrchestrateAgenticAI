# Agents of Legend: the Orchestrator Dilemna

_Context, Checklists, and No-Miss Reviews_

- speaker: Calvin Hendryx-Parker
- length: 30min

#### links
- [_useful quotes_](quotes.md)
- [README](README.md)
- [talk promises](expectations.md)

# Outline

## The backstory magic

Business as usual can feel more like an epic quest into Mordor than a stock
photo of smiling generic people gather around the warm light of a laptop on a
board room table.

<buildout>
![basic old business stock image](generate)
<transition basic />
![party in peril in the dungeon](generate)
</buildout>

It is not uncommon to find ourselve operating in the worlds of best practice and
then suddenly plunged into a novel world of... chaos. One second we are planning
a cheery offsite, the next it is very dark and we might be eaten by a grue.

Whether it be good news or bad, adapting quickly to our situation requires tools
and experience.

## Agents: Everybody says they are great, but do I need one?

<quick riff: essentially our talk introduction  on how why & why, what, how, when to start using agents>

## Trouble comes knocking

But let's start with a plausible if confabulated situation for our
quest to illustrate some of the practical elements of orchestrating
agents.

Let's set the scene <improvise>

> You are the COO of a crack consulting company.
>
> You just won a contract for discovery
> with L&LL LLC (Lord and Lady LARPsalot), a rapidly growing events
> company that specialize in live action role playing events and
> accessories.
>
> They have an online marketplace for other artisans selling LARPing
> accessories (larpsy.gold) and a bitrotting site for coordinating
> events at larpsalot.party: registration, payments, game runner tools,
> community management and lots of classic rpg content modified for live
> action, licensed under the OGL.
>
> They need to migrate off a cloud PaaS provider called Hurokee which is
> sunsetting and do some improvements to their web property.  Once
> relaunch their sites, they would like to launch a mobile app on IOS to
> support their events and games.
>
> You are just about to head home when your phone starts to blow up from
> L&LL's CEO Tasha Tiamata.  Hasbro has just announced that they are
> changing the OGL and Tash needs to know ASAP how much of the content
> her event runners depend on may have to be taken down.
>
> Can your team help her?  Time to get the party together.

## the mighty fine (team)

Meet the other nondeterministic agents to orchestrate

This quest was already agentic, staffed with important team members
who will need to coordinate with your digital agents for
success. Let's quickly our team, as our agent will both be augmenting
what they do and occasionally representing them or facilitating
communication

<!-- deck-watch: processed — created 05-the-mighty-fine-team.md with team role cards -->

- Business Operations and Product Management{ The Cleric and the Bard: keep the business healthy and singing the song of the business.
- Product Engineering: The Magic users of CAPEX, wizards, sorcerors, artificers, and druids
- Technical Operations (SRE, Devops, DX, Platform Engineering,
  Sysadmin & Ops): the OPEX bruisers who keep the roads and fortress
  safe and jump into action when called or paged. Rangers, barbarians
  and ... fighters
- Security
  - Red team: Rogues of all shades
  - Blue team: Paladin, Warlock

## our newest party member

[@@img:totally metal warforge bard/warlock w/ flying V and about 25% of his body cover with modular synths and power tools]

Call them clod, gem, dex, cecily, the cursor, and many more or any combo thereof.

They enter the open office / tavern w/ great swagger,
the hyped and famed Agentic AI who is rumored to have such
promise, both a ninja and rockstar can do the
laundry, walking the dog and filing the taxes.

Except sometimes the taxes end up in the washing machine w/ their lute
and dog ends up in the dryer. And the front door was left wide open
all night long.

But maybe we can make this work

## What do we know about our quest?

Tasha has given us the following artifacts in a tarball
- the hurokee buildpack. basically a dockerfile
- the code for the 2 sites
- a database dump
- a file dump of the OGL content.

## How do you want to do this? pt 1

_critical role tag phrase, vox machina or mighty nein image_

Winter is coming? things are changing? What are these agentic wonders? These
agents, be they zombies, skeletons, familiars, djinnies or demons?  Can we work
with them? can they work together? Are they soulless NPC or funhouse mirror
reflections of ourselvf.  Consider.

The team accepts the agent as part of the party.

## Hark! there is work to be done! To our spelljammer!

![spelljammer with our team on board](images/spelljammer_web.jpg)

> Roll for initiative!
> Casting Clarity of Thought Lvl {good enough}
> Casting lv2 Locate Object

<demo starts here>

The bizops and product team members understand L&LL is face a dual existential threat... they could large parts of the content they depend on, or worse, they could end up liable for misuse of conduct and face legal action.  The licensing changes mainly apply to use of names.


The command line does not scare our cleric Sera and bard Finn, and luckily a trusted ranger named Kael is there to help get a database set up to do this work.  They import L&LL's content db. They also load and transform the content from the pdfs.

They fire the agent and COO Mira Stonebridge drives. She knows she has to do the following:
- search the pdf for all names of places, magic items, characters, and monsters. Load those and the raw text into the DB.
- search all the content in the db dump for instance of names
- report the damage
- generate and substitute replacement names if damage is high

Notes on demo:
  - Demonstrate how skills codify problem solving by creating a skill on the fly to use "say" to let you know when things are done.
  - We will have separate db for each step.
  - we could try doltgres and prompt injection on the load back

## Loot the Room

L&L is super psyched. The team has landed more work in the form of a database migration.

But now our team faces more complex tasks, with greater peril.

we might step back to consider what is possible, plausible and sensible.  We might also
consider what cognitive frameworks we already apply to non-deterministic
business process we already manage everyday.

{Intro Cynefin and OODA as ways to think about assessing agentic tools and their
use, output, etc.}

We need to orchestrate the actions of the agent(s) but we also need to
orchestrate the actions of the human players.

## Great, but I hired you for this other thing

The job is not done, we need to migrate and update their websites.


## It's a TRAP!

![Admiral Ackbar, Tal'Dorei style in a dungeon with traps](images/its-a-trap_web.jpg)

<demo>

steps:
- start claude et al in a "fresh" repo (sort of a lie/)
- ingest the contract pdf
  - use skills to generate visual explains, a central checklist, etc
- Security is a requirement: use security skills to give you a report w/ a checklist
- create a claude swarm w/ /bg & /c^2 skill to use codex and gemini to do an adversarial review of contract and security findings.
- visual explainer of
  - an overlay for the project (contract, existing art, work to do)
  - risks for this repo
  - adversarial review finding
- fire up speckit to specify and use the dialectic to create a spec from our findings, clarify, create a plan.  Look at the constitution, other artifacts.
  - show using  a claude swarm w/ /bg & /c^2 skill w/ worktrees, prs as part of the spec. begin converstation about feature oriented

## Jetpacks all around, the future is legion

Working together

<demo>

- interact w/ through agent
  - talk about how similar to apps before them, agents are now a medium w/ their own message.
  - talk about symbiogenisis, how in natural organism take evolutionary leaps when the start to act as environments for other organisms.

- specify a feature, use multiclaude to implement. Talk about multiclaude's built in TDD. CI/CD workflow
- implement something with ralph-orchestrator and Pdd. Talk about
  modeling process with the hats prompt and loop driven development.
- if want, gas town, talk about kim & yegge's book, and the future

## Closing thoughts

- Start with frameworks you already know (OODA, Cynefin) to assess what's po
ssible, plausible, sensible
- Skills codify problem solving — build them as you go, they compound
- Security and trust are enablers, not blockers — bake them in
- Orchestrate the humans AND the agents — the party works together
- The agent is part of the party, not a replacement for it
- Underpromise, deliver — then iterate. The brownian ratchet is your friend.
