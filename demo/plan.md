# Original Plan

the set up:
## Trouble comes knocking

Let's start with a plausible if confabulated situation for our quest
to illustrate some of the practical elements of orchestrating agents.

Let's set the scene <improvise>

You are the COO of a crack consulting company.

You just won a contract for discovery
with L&LL LLC (Lord and Lady LARPsalot), a rapidly growing events
company that specialize in live action role playing events and
accessories.

They have an online marketplace for other artisans selling LARPing
accessories (larpsy.gold) and a bitrotting site for coordinating
events at larpsalot.party: registration, payments, game runner tools,
community management and lots of classic rpg content modified for live
action, licensed under the Open Gaming Licence.

They need to migrate off a cloud PaaS provider called Hurokee which is
sunsetting and do some improvements to their web property.  Once
relaunch their sites, they would like to launch a mobile app on IOS to
support their events and games.

You are just about to head home when your phone starts to blow up from
L&LL's CEO Tasha Tiamata.  Hasbro has just announced that they are
changing the OGL and Tash needs to know ASAP how much of the content
her event runners depend on may have to be taken down.

Can your team help her?  Time to get the party together.

Tasha has given us the following artifacts in a tarball
- the hurokee buildpack. basically a dockerfile
- the code for the 2 sites
- a database dump
- a file dump of the OGL content.

Demo (options):

1. precached as much as possible, process the pdf content, load into PG, search for copyright issues. demonstrate how to use persistents outside the context window get better results.  this will likely use a big pdf of 25year of classic gaming content
2. we use skills in claude to do a brief security audit of the buildpack. It finds some vulns in the sbom, and corrects it for us to safe launch one of the sites
3. Survivability using DoltGres. Blow away DB via prompt inject (new npc johnny drop tables), but then recover quickly.  talk about the importance of creating resilient environment in dev and prod
4. Orchestration NG 1: give the agents some rails: utilize human patterns of software dev, speckit, adversarial review
5. Orchestration NG 2: orchestrates itself: multiclaude/multiplex skill, ralph-orchestrator, gas town
