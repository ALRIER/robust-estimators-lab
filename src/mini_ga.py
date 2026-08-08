"""Lightweight pedagogical GA utilities.

Milestone 2 should extend this module. Nothing here is a thesis result.
"""
from dataclasses import dataclass
import numpy as np

@dataclass
class MiniGAConfig:
    population_size: int = 40
    generations: int = 30
    mutation_rate: float = 0.15
    seed: int = 20260808


def demo_ga(config: MiniGAConfig = MiniGAConfig()):
    """Small deterministic 3-weight GA used exclusively for the DEMO MODE."""
    from src.simplex import demo_objective
    rng = np.random.default_rng(config.seed)
    pop = rng.dirichlet(np.ones(3), size=config.population_size)
    generations, best_path, best_scores, diversity, populations = [], [], [], [], []
    for generation in range(config.generations + 1):
        scores = demo_objective(pop[:, 0], pop[:, 1], pop[:, 2])
        best = int(np.argmin(scores))
        generations.append(generation); best_path.append(pop[best].copy())
        best_scores.append(float(scores[best])); diversity.append(float(np.mean(np.std(pop, axis=0))))
        populations.append(pop.copy())
        if generation == config.generations: break
        elite = pop[np.argsort(scores)[:max(2, config.population_size // 5)]]
        parents = elite[rng.integers(0, len(elite), size=(config.population_size, 2))]
        mix = rng.random((config.population_size, 1))
        children = mix * parents[:, 0] + (1 - mix) * parents[:, 1]
        changed = rng.random(config.population_size) < config.mutation_rate
        if np.any(changed): children[changed] = .86 * children[changed] + .14 * rng.dirichlet(np.ones(3), changed.sum())
        pop = children / children.sum(axis=1, keepdims=True)
    return {"generations": np.asarray(generations), "populations": populations, "best_path": np.asarray(best_path), "best_scores": np.asarray(best_scores), "diversity": np.asarray(diversity), "mutation_rate": config.mutation_rate}


def random_simplex_population(size: int, dimension: int, seed: int):
    rng = np.random.default_rng(seed)
    return rng.dirichlet(np.ones(dimension), size=size)


def validate_simplex(weights, tol=1e-8):
    w = np.asarray(weights, dtype=float)
    return bool(np.all(w >= -tol) and np.allclose(w.sum(axis=-1), 1.0, atol=tol))
