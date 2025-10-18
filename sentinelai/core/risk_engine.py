def calculate_overall_risk(gnn_score, agent_confidences):
    """Combine model and agent scores into a single risk metric."""
    agent_avg = sum(agent_confidences) / len(agent_confidences) if agent_confidences else 0
    final_score = round((0.6 * gnn_score + 0.4 * agent_avg), 2)
    return final_score
