import numpy as np
from core.pricing import price_european_option_mc


def test_mc_price_and_shape():
    price, stderr, paths, discounted = price_european_option_mc(
        S0=100,
        K=100,
        T=1.0,
        r=0.05,
        sigma=0.2,
        n_steps=50,
        n_sims=1_000,
        option_type="call",
        seed=42,
    )

    # prix et erreur standard raisonnables
    assert price > 0
    assert stderr > 0

    # forme des trajectoires : (n_steps + 1, n_sims)
    assert paths.shape == (51, 1000)

    # il doit y avoir autant de payoffs actualisés que de simulations
    assert discounted.shape == (1000,)


def test_mc_reproducibility_with_seed():
    """Même seed -> même prix (test de reproductibilité)."""
    p1, _, _, _ = price_european_option_mc(
        S0=100, K=100, T=1.0, r=0.05, sigma=0.2,
        n_steps=50, n_sims=5_000, option_type="call", seed=123,
    )
    p2, _, _, _ = price_european_option_mc(
        S0=100, K=100, T=1.0, r=0.05, sigma=0.2,
        n_steps=50, n_sims=5_000, option_type="call", seed=123,
    )

    assert np.isclose(p1, p2)
