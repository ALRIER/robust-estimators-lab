from src.mini_ga import random_simplex_population, validate_simplex
from src.simplex import barycentric_grid


def test_random_population_is_valid_simplex():
    pop = random_simplex_population(50, 3, 123)
    assert validate_simplex(pop)


def test_barycentric_grid_sums_to_one():
    g = barycentric_grid(0.1)
    assert validate_simplex(g, tol=1e-7)
