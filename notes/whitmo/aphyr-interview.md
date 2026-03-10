# Transcript: Breaking Distributed Systems with Kyle Kingsbury from Jepsen

**Video URL:** [Breaking Distributed Systems with Kyle Kingsbury from Jepsen](http://www.youtube.com/watch?v=IvE1VbOol88)
**Channel:** [The Geek Narrator](https://www.youtube.com/@thegeeknarrator)
**Date:** 2025-07-06

---

## Introduction and Process

* **[00:00](http://www.youtube.com/watch?v=IvE1VbOol88&t=0)** Host Kaivalya Apte (Kav) introduces Kyle Kingsbury, known for the Jepsen safety analyses of distributed systems.
* **[01:31](http://www.youtube.com/watch?v=IvE1VbOol88&t=91)** Kyle discusses his current focus, including moving Jepsen testing into [Antithesis](https://antithesis.com/).
* **[01:47](http://www.youtube.com/watch?v=IvE1VbOol88&t=107)** **The Testing Process:** Kyle starts by reading documentation to find precise safety claims (e.g., strong serializability, snapshot isolation) and fault models (clock skew, network partitions). [02:22](http://www.youtube.com/watch?v=IvE1VbOol88&t=142)
* **[04:21](http://www.youtube.com/watch?v=IvE1VbOol88&t=261)** **Domain Specificity:** For specialized systems like [Tiger Beetle](https://tigerbeetle.com/) (financial transactions), Kyle replicates the state machine from documentation to verify semantic compliance. [05:43](http://www.youtube.com/watch?v=IvE1VbOol88&t=343)

## Common Bugs and Patterns

* **[09:23](http://www.youtube.com/watch?v=IvE1VbOol88&t=563)** **Definite vs. Indefinite Failures:** A common mistake is mismanaging request errors where it's unclear if an operation succeeded. This often leads to unsafe idempotent retries. [09:55](http://www.youtube.com/watch?v=IvE1VbOol88&t=595)
* **[11:15](http://www.youtube.com/watch?v=IvE1VbOol88&t=675)** **Happy Path Bias:** Most initial test suites focus on successful operations, missing failure recovery cases or unusual concurrent interleavings visible only during partitions. [12:02](http://www.youtube.com/watch?v=IvE1VbOol88&t=722)
* **[13:04](http://www.youtube.com/watch?v=IvE1VbOol88&t=784)** **Functional vs. Safety Bugs:** Jepsen is "black-box" testing; therefore, almost everything found is a functional bug from the user's perspective. [13:10](http://www.youtube.com/watch?v=IvE1VbOol88&t=790) Kyle shares an example from **Fauna** where indices failed for negative numbers. [14:04](http://www.youtube.com/watch?v=IvE1VbOol88&t=844)

## The Impact of AI and Hardware

* **[17:17](http://www.youtube.com/watch?v=IvE1VbOol88&t=1037)** **Evolution of Testing:** While infrastructure has moved to the cloud, core safety properties like serializability remain the same. [17:33](http://www.youtube.com/watch?v=IvE1VbOol88&t=1053) Modern vendors now place more emphasis on safety and consensus. [18:03](http://www.youtube.com/watch?v=IvE1VbOol88&t=1083)
* **[18:28](http://www.youtube.com/watch?v=IvE1VbOol88&t=1108)** **Hardware Changes:** SSDs have shifted performance characteristics, but Kyle notes that "bad performance" is often better for safety testing as it widens concurrency windows. [19:18](http://www.youtube.com/watch?v=IvE1VbOol88&t=1158)
* **[21:22](http://www.youtube.com/watch?v=IvE1VbOol88&t=1282)** **The AI Problem:** Kyle expresses strong ethical concerns regarding LLMs, citing issues like spam bots hitting his site [22:04](http://www.youtube.com/watch?v=IvE1VbOol88&t=1324), automated disinformation, and hallucinations—such as an LLM fabricating a paper he never wrote. [23:02](http://www.youtube.com/watch?v=IvE1VbOol88&t=1382)
* **[23:47](http://www.youtube.com/watch?v=IvE1VbOol88&t=1427)** **Trust in Code:** Kyle avoids using AI for code generation in Jepsen because establishing correctness requires the deep thinking process of manual writing. [24:53](http://www.youtube.com/watch?v=IvE1VbOol88&t=1493)

## Testing Methodology and Tools

* **[26:03](http://www.youtube.com/watch?v=IvE1VbOol88&t=1563)** **False Positives/Negatives:** To ensure checkers are sound, Kyle uses generative tests on the checkers themselves and validates them against real histories. [27:08](http://www.youtube.com/watch?v=IvE1VbOol88&t=1628)
* **[30:16](http://www.youtube.com/watch?v=IvE1VbOol88&t=1816)** **Intentional Sabotage:** Kyle verifies his tests by intentionally breaking a system (e.g., turning off `fsync`) to see if the checker catches the violation. [31:00](http://www.youtube.com/watch?v=IvE1VbOol88&t=1860)
* **[35:56](http://www.youtube.com/watch?v=IvE1VbOol88&t=2156)** **Boring Technology:** Jepsen is a JVM program using proven tools like `gnuplot`, `graphviz`, and `vim`. [36:45](http://www.youtube.com/watch?v=IvE1VbOol88&t=2205) Kyle avoids modern browser-based libraries that fail at the scale of a billion points. [37:03](http://www.youtube.com/watch?v=IvE1VbOol88&t=2223)

## Formal Verification and Notorious Bugs

* **[48:43](http://www.youtube.com/watch?v=IvE1VbOol88&t=2923)** **Formal Verification Challenges:** Kyle notes that tools like TLA+ and Isabelle remain difficult to use due to "obscurantist APIs" and high overhead for simple proofs. [49:00](http://www.youtube.com/watch?v=IvE1VbOol88&t=2940)
* **[51:32](http://www.youtube.com/watch?v=IvE1VbOol88&t=3092)** **Nasty Bugs:**
* **Elasticsearch:** A simple node reboot once caused a 30% data loss. [51:58](http://www.youtube.com/watch?v=IvE1VbOol88&t=3118)
* **TiDB:** Transactions were found reading values from the future. [52:35](http://www.youtube.com/watch?v=IvE1VbOol88&t=3155)
* **Kafka/Buffstream:** A protocol issue where transactions could be "sliced in half" due to out-of-order commits. [53:38](http://www.youtube.com/watch?v=IvE1VbOol88&t=3218)


* **[55:04](http://www.youtube.com/watch?v=IvE1VbOol88&t=3304)** **Rock Solid Systems:** Kyle highlights [Datomic](https://www.datomic.com/) as one of the most solid systems he has ever tested. [55:12](http://www.youtube.com/watch?v=IvE1VbOol88&t=3312)

## Advice for Engineers

* **[57:59](http://www.youtube.com/watch?v=IvE1VbOol88&t=3479)** **Why Clojure?** Kyle chose Clojure for its JVM ecosystem, immutability, and expressive power for experimental work. [59:41](http://www.youtube.com/watch?v=IvE1VbOol88&t=3581)
* **[01:01:09](http://www.youtube.com/watch?v=IvE1VbOol88&t=3669)** **Building Intuition:** To learn distributed systems, Kyle recommends writing toy systems and tests. He suggests resources like [Martin Kleppmann’s book](https://dataintensive.net/) and his own [Distributed Systems Class](https://github.com/aphyr/distsys-class). [01:01:22](http://www.youtube.com/watch?v=IvE1VbOol88&t=3682)
* **[01:03:53](http://www.youtube.com/watch?v=IvE1VbOol88&t=3833)** **Learning Through Failure:** "There is nothing like firefighting a DNS inconsistency at 4 in the morning to teach you important lessons." [01:04:05](http://www.youtube.com/watch?v=IvE1VbOol88&t=3845)
