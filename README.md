# Demo based on code from article

https://amanxai.com/2025/12/23/langgraph-explained-from-scratch/

## Prerequisites

```
# optional (use mise settings)
mise trust
mise install

# install uv deps
uv sync -U

# pull ollama image
ollama pull llama3
```

## Run Example

```
[0] % ./main.py

--- TEST 1: Math ---
Finished running: categorizer
--- 🧮 Entering Math Node ---
Finished running: math_node
id: lc_run--019b70b3-1c3b-78f2-b9a3-e993af380945-0
content: A simple one!

The answer is... (drumroll please)... 550!
--------------------------------------------------

--- TEST 2: General ---
Finished running: categorizer
--- 💬 Entering General Chat Node ---
Finished running: general_node
id: lc_run--019b70b3-207b-7210-8f1e-b7d46df5f529-0
content: I'd be delighted to share a fun fact with you!

Here's one: Did you know that the shortest war in recorded history was between Britain and Zanzibar on August 27, 1896? It lasted only 38 minutes! Zanzibar surrendered after just 12 minutes of fighting, but the war didn't officially end until 38 minutes had passed, as the Zanzibari forces hadn't received word of the surrender in time.

This tiny war was sparked by a dispute over who should be the ruler of Zanzibar. The British wanted to install a new sultan, while Zanzibar preferred its own choice. In the end, the British got their way, and Zanzibar became a British protectorate.

Isn't that just wild?
--------------------------------------------------
```
