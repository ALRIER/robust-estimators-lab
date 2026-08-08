"""Deterministic pedagogical GA utilities; never thesis-result computation."""
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class MiniGAConfig:
    population_size: int = 72
    generations: int = 40
    mutation_rate: float = .18
    seed: int = 20260808


def validate_simplex(weights, tol=1e-8):
    w = np.asarray(weights, dtype=float)
    return bool(np.all(w >= -tol) and np.allclose(w.sum(axis=-1), 1.0, atol=tol))


def random_simplex_population(size, dimension, seed):
    return np.random.default_rng(seed).dirichlet(np.ones(dimension), size=size)


def run_pedagogical_ga(objective, config=MiniGAConfig()):
    """Optimise a supplied 3-weight teaching objective and retain real demo history."""
    rng = np.random.default_rng(config.seed)
    pop = rng.dirichlet(np.ones(3), size=config.population_size)
    populations=[]; paths=[]; scores_history=[]; diversity=[]
    for generation in range(config.generations + 1):
        scores=np.asarray(objective(pop),dtype=float)
        best=int(np.argmin(scores))
        populations.append(pop.copy()); paths.append(pop[best].copy()); scores_history.append(float(scores[best]))
        diversity.append(float(np.mean(np.std(pop,axis=0))))
        if generation == config.generations: break
        elite=pop[np.argsort(scores)[:max(4,config.population_size//5)]]
        pair=elite[rng.integers(0,len(elite),size=(config.population_size,2))]
        mix=rng.random((config.population_size,1))
        children=mix*pair[:,0]+(1-mix)*pair[:,1]
        changed=rng.random(config.population_size)<config.mutation_rate
        if changed.any():
            children[changed]=.82*children[changed]+.18*rng.dirichlet(np.ones(3),changed.sum())
        pop=children/children.sum(axis=1,keepdims=True)
    return {"generations":np.arange(config.generations+1),"populations":populations,"best_path":np.asarray(paths),"best_scores":np.asarray(scores_history),"diversity":np.asarray(diversity),"mutation_rate":config.mutation_rate}


def demo_ga(config=MiniGAConfig()):
    from src.simplex import demo_objective
    return run_pedagogical_ga(lambda w: demo_objective(w[:,0],w[:,1],w[:,2]),config)
