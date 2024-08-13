---
layout: post
title: Implement Causal Inference with pgmpy
date: 2024-08-13
description: How to employ correctly causal inference in Python, what is causal inference and why you need it
tags: [concepts]
category: work
related_posts: false
related_publications: true
scholar:
  bibliography: _bibliography/blog_references.bib
---

```python

import pandas as pd
import numpy as np
from pgmpy.inference.CausalInference import CausalInference
from pgmpy.models.BayesianNetwork import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
import networkx as nx
import itertools
from typing import Dict, Optional, Any

class SingleCausalInference:
    def __init__(self, data: pd.DataFrame, causal_graph: nx.DiGraph):
        """
        Initializes the SingleCausalInference class.

        Parameters:
        data (pd.DataFrame): The dataset to be used for causal inference.
        causal_graph (nx.DiGraph): A directed acyclic graph representing causal relationships.
        """
        self.data = data
        self.causal_graph = causal_graph

        # Create and fit the Bayesian Network model
        self.bayesian_network = BayesianNetwork()
        self.bayesian_network.add_edges_from(ebunch=self.causal_graph.edges())
        self.bayesian_network.fit(self.data, estimator=MaximumLikelihoodEstimator)

        # Ensure the model is valid
        assert self.bayesian_network.check_model()

        # Initialize the Causal Inference object
        self.causal_inference = CausalInference(self.bayesian_network)

    def get_bayesian_network(self) -> BayesianNetwork:
        """
        Returns the fitted Bayesian Network.

        Returns:
        BayesianNetwork: The fitted Bayesian Network.
        """
        return self.bayesian_network

    def infer(self, interventions: Dict[str, Any], target_variable: str,
              evidence: Optional[Dict[str, Any]] = None, adjustment_set: Optional[set] = None) -> Dict[str, float]:
        """
        Perform causal inference to determine the effect of interventions on the target variable.

        Parameters:
        interventions (Dict[str, Any]): A dictionary of interventions (do-operations) on variables.
        target_variable (str): The variable of interest to query.
        evidence (Optional[Dict[str, Any]]): Observed evidence (optional).
        adjustment_set (Optional[set]): A set of variables for adjustment (optional).

        Returns:
        Dict[str, float]: The probability distribution of the target variable after intervention.
        """
        # Filter out the target variable from interventions to prevent conflicts
        clean_interventions = {var: val for var, val in interventions.items() if var != target_variable}

        if adjustment_set is None:
            # If no adjustment set is provided, compute one automatically
            intervention_vars = list(clean_interventions.keys())
            adjustment_set = set(itertools.chain(*[self.causal_graph.predecessors(var) for var in intervention_vars]))
        else:
            # Ensure the target variable is not part of the adjustment set
            adjustment_set.discard(target_variable)

        # Perform the query with the provided or computed parameters
        query_result = self.causal_inference.query(
            variables=[target_variable],
            do=clean_interventions,
            evidence=clean_interventions if evidence is None else evidence,
            adjustment_set=adjustment_set,
            show_progress=False
        )

        # Convert the result (DiscreteFactor) to a dictionary format
        result_dict = {
            str(state): float(query_result.values[idx])
            for idx, state in enumerate(query_result.state_names[target_variable])
        }

        return result_dict

    @staticmethod
    def check_for_nan_or_infinite(data: Any) -> bool:
        """
        Checks if the provided data contains NaN or infinite values.

        Parameters:
        data (Any): The data to check, can be a dict or set.

        Returns:
        bool: True if NaN or infinite values are found, False otherwise.
        """
        def is_numeric(value):
            try:
                value = np.array(value, dtype=float)
                return np.isnan(value).any() or np.isinf(value).any()
            except (ValueError, TypeError):
                return False

        if isinstance(data, dict):
            for key, value in data.items():
                if is_numeric(value):
                    print(f"Warning: {key} contains NaN or infinite values.")
                    return True
        elif isinstance(data, set):
            for value in data:
                if is_numeric(value):
                    print(f"Warning: Set contains NaN or infinite values: {value}")
                    return True
        else:
            print(f"Unsupported data type: {type(data)}")
            return True

        return False

    @staticmethod
    def validate_input_data(interventions: Dict[str, Any], evidence: Optional[Dict[str, Any]],
                            adjustment_set: Optional[set]):
        """
        Validates input data to ensure it does not contain NaN or infinite values.

        Parameters:
        interventions (Dict[str, Any]): Interventions to be validated.
        evidence (Optional[Dict[str, Any]]): Evidence data to be validated.
        adjustment_set (Optional[set]): Adjustment set to be validated.

        Raises:
        ValueError: If NaN or infinite values are found in the data.
        """
        if SingleCausalInference.check_for_nan_or_infinite(interventions):
            raise ValueError("Intervention data contains NaN or infinite values.")
        if evidence is not None and SingleCausalInference.check_for_nan_or_infinite(evidence):
            raise ValueError("Evidence data contains NaN or infinite values.")
        if adjustment_set is not None and SingleCausalInference.check_for_nan_or_infinite(adjustment_set):
            raise ValueError("Adjustment set data contains NaN or infinite values.")

```

{% cite pearl2010causal %}
