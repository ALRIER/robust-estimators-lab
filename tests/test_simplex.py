from src.mini_ga import MiniGAConfig, demo_ga, random_simplex_population, validate_simplex
from src.simplex import barycentric_grid, demo_objective


def test_random_population_is_valid_simplex():
    pop = random_simplex_population(50, 3, 123)
    assert validate_simplex(pop)


def test_barycentric_grid_sums_to_one():
    g = barycentric_grid(0.1)
    assert validate_simplex(g, tol=1e-7)


def test_pedagogical_ga_is_deterministic_and_preserves_simplex():
    config = MiniGAConfig(population_size=12, generations=4, seed=7)
    first, second = demo_ga(config), demo_ga(config)
    assert all(validate_simplex(population) for population in first["populations"])
    assert (first["best_scores"] == second["best_scores"]).all()
    assert (first["best_scores"][1:] <= first["best_scores"][:-1]).all()


def test_explained_child_fitness_matches_displayed_terrain():
    run = demo_ga(MiniGAConfig(population_size=12, generations=2, seed=9))
    event = run["events"][1][run["explained_event_indices"][1]]
    assert event["event_type"] == "offspring"
    assert validate_simplex(event["child"])
    assert event["fitness"] == demo_objective(*event["child"])
