"""Deterministic pedagogical GA. It mirrors thesis mechanics, never thesis output."""
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class MiniGAConfig:
    population_size: int = 48
    generations: int = 30
    mutation_rate: float = .18
    mutation_floor: float = .05
    elitism: int = 2
    tournament_size: int = 2
    immigrant_rate: float = .10
    seed: int = 20260808


def validate_simplex(weights, tol=1e-8):
    w = np.asarray(weights, dtype=float)
    return bool(np.all(w >= -tol) and np.allclose(w.sum(axis=-1), 1.0, atol=tol))


def random_simplex_population(size, dimension, seed):
    return np.random.default_rng(seed).dirichlet(np.ones(dimension), size=size)


def run_pedagogical_ga(objective, config=MiniGAConfig()):
    """Optimise a teaching objective while recording ancestry for every child.

    The operations match the thesis GA's visible mechanics: Dirichlet initial
    vectors, tournament selection, blend crossover, decaying Dirichlet mutation,
    elitism, and occasional immigrants.  Only ``objective`` is synthetic.
    """
    rng = np.random.default_rng(config.seed)
    pop = rng.dirichlet(np.ones(3), size=config.population_size)
    populations = []; scores_by_generation = []; best_path = []; generation_best_path = []
    best_scores = []; generation_best_scores = []; diversity = []
    events = [None]; explained_event_indices = [None]; mutation_rates = [config.mutation_rate]
    historical_best_score = np.inf; historical_best_weights = None
    for generation in range(config.generations + 1):
        scores = np.asarray(objective(pop), dtype=float)
        best_index = int(np.argmin(scores)); generation_best_score = float(scores[best_index])
        if generation_best_score < historical_best_score:
            historical_best_score = generation_best_score; historical_best_weights = pop[best_index].copy()
        populations.append(pop.copy()); scores_by_generation.append(scores.copy())
        generation_best_path.append(pop[best_index].copy()); generation_best_scores.append(generation_best_score)
        best_path.append(historical_best_weights.copy()); best_scores.append(historical_best_score)
        diversity.append(float(np.mean(np.std(pop, axis=0))))
        if generation == config.generations: break

        mutation_rate = config.mutation_floor + (config.mutation_rate - config.mutation_floor) * (np.log(config.generations + 1) - np.log(generation + 2)) / np.log(config.generations + 1)
        elite_indices = np.argsort(scores)[:min(config.elitism, config.population_size)]
        mating_pool = []
        for _ in range(max(1, config.population_size // 2)):
            contestants = rng.choice(config.population_size, size=min(config.tournament_size, config.population_size), replace=False)
            mating_pool.append(int(contestants[np.argmin(scores[contestants])]))
        children = [pop[index].copy() for index in elite_indices]
        child_events = [{"child_index": i, "event_type": "elite", "source_index": int(index), "child": pop[index].copy(), "fitness": float(scores[index])} for i, index in enumerate(elite_indices)]
        for child_index in range(len(children), config.population_size):
            parent_indices = rng.choice(mating_pool, size=2, replace=True)
            parent_a, parent_b = pop[parent_indices[0]], pop[parent_indices[1]]
            inheritance_a = float(rng.random())
            before_mutation = inheritance_a * parent_a + (1 - inheritance_a) * parent_b
            mutated = bool(rng.random() < mutation_rate)
            child = before_mutation.copy(); mutation_vector = np.zeros(3)
            if mutated:
                child = .50 * child + .50 * rng.dirichlet(np.ones(3))
                mutation_vector = child - before_mutation
            child = child / child.sum(); children.append(child)
            child_events.append({"child_index": child_index, "event_type": "offspring", "parent_a_index": int(parent_indices[0]), "parent_b_index": int(parent_indices[1]), "parent_a": parent_a.copy(), "parent_b": parent_b.copy(), "inheritance_a": inheritance_a, "before_mutation": before_mutation.copy(), "mutated": mutated, "mutation_vector": mutation_vector.copy(), "child": child.copy()})
        pop = np.asarray(children); next_scores = np.asarray(objective(pop), dtype=float)
        if (generation + 1) % 15 == 0 and config.immigrant_rate > 0:
            count = min(config.population_size, max(1, int(np.floor(config.population_size * config.immigrant_rate))))
            worst = np.argsort(next_scores)[-count:]
            pop[worst] = rng.dirichlet(np.ones(3), size=count); next_scores = np.asarray(objective(pop), dtype=float)
            for index in worst:
                child_events[int(index)] = {"child_index": int(index), "event_type": "immigrant", "child": pop[index].copy()}
        for event, score in zip(child_events, next_scores): event["fitness"] = float(score)
        events.append(child_events)
        offspring_indices = [i for i, event in enumerate(child_events) if event["event_type"] == "offspring"]
        explained_event_indices.append(min(offspring_indices, key=lambda i: next_scores[i]))
        mutation_rates.append(float(mutation_rate))
    return {"generations": np.arange(config.generations + 1), "populations": populations, "scores": scores_by_generation, "best_path": np.asarray(best_path), "generation_best_path": np.asarray(generation_best_path), "best_scores": np.asarray(best_scores), "generation_best_scores": np.asarray(generation_best_scores), "diversity": np.asarray(diversity), "events": events, "explained_event_indices": explained_event_indices, "mutation_rates": np.asarray(mutation_rates)}


def demo_ga(config=MiniGAConfig()):
    from src.simplex import demo_objective
    return run_pedagogical_ga(lambda weights: demo_objective(weights[:, 0], weights[:, 1], weights[:, 2]), config)
