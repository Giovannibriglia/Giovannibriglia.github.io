---
layout: post
title: Improving Reinforcement Learning Exploration with Causal Models
date: 2024-09-25
description: New paper accepted at PRIMA 2024, Kyoto, 18-24 November
tags: [concepts, update]
category: research
---

### Resume

In this work, we explore a novel way to enhance reinforcement learning (RL) in autonomous agents by integrating causal
models into the learning process. We introduce the Causality-Driven Reinforcement Learning (CDRL) framework, it can
improve exploration efficiency by leveraging causal discovery. Rather than requiring agents to explore all possible
actions and states, CDRL learns a causal model from a simplified version of the environment. This model focuses
on key transitions, such as actions that lead directly to success or failure, and then serves as a guide to navigate
more complex environments. The two-phase approach—Causal Discovery (CD) and Causal RL (CRL)—allows for a faster
and more efficient learning process.

Using various RL algorithms, we demonstrate that CDRL consistently improves both the speed and effectiveness of
learning in complex environments. Not only does it reduce the number of actions required to complete tasks, but it
also generalizes well to previously unseen environments. The experiments show that CDRL can be implemented in both
online and offline settings, with offline learning yielding particularly promising results, as the causal model
can be trained once and reused in larger environments without degradation in performance.

This approach offers a modular solution to enhance existing RL frameworks, making it adaptable and scalable for
a wide range of applications in AI and autonomous systems.

[Explore the Code and Results on GitHub](https://github.com/Giovannibriglia/AgentGroup_CausalRL)

---

### Environment Examples

Below are examples of the environments considered:

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="lazy" path="assets/img/grid.gif" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="lazy" path="assets/img/maze.gif" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

---

### Plot Extract

Here is an extract from the results:

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="lazy" path="assets/img/prima_plot1.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.liquid loading="lazy" path="assets/img/prima_plot2.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

---
