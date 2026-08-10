from src.mini_ga import MiniGAConfig, demo_ga, random_simplex_population, validate_simplex
from src.simplex import barycentric_grid, demo_objective, demo_surface_with_population, teaching_terrain


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


def test_terrain_figure_exposes_axes_and_search_visuals():
    population = random_simplex_population(12, 3, 22)
    terrain = teaching_terrain("normal", "upper_tail", .10, 10., 0., "q95(MSE)")
    fig = demo_surface_with_population(population, population[:4], terrain)
    names = {trace.name for trace in fig.data if trace.name}
    assert {"GA candidates", "Best-so-far trace", "Perfect convergence", "Contamination stress"} <= names
    corner_trace = next(trace for trace in fig.data if trace.name == "Simplex axes")
    assert list(corner_trace.text) == ["X\n(1, 0, 0)", "Y\n(0, 1, 0)", "Z\n(0, 0, 1)"]
