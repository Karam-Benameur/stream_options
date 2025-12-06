from core.pricing import OptionPricer, price_european_option_mc


def test_black_scholes_call_price():
    """
    Vérifie que le prix Black-Scholes du call (S0=K=100, r=5%, sigma=20%, T=1)
    est proche de la valeur de référence ~10.45.
    """
    pricer = OptionPricer(S0=100, K=100, r=0.05, sigma=0.2, T=1.0, kind="call")
    result = pricer.black_scholes()

    expected_price = 10.45
    assert abs(result["price"] - expected_price) < 0.05, (
        f"Prix trop éloigné de la référence : {result['price']} vs {expected_price}"
    )


def test_monte_carlo_basic():
    """
    Test basique sur la fonction Monte Carlo :
    - le prix doit être strictement positif
    - la forme du tableau de trajectoires doit être (n_steps + 1, n_sims)
    """
    n_steps = 50
    n_sims = 1_000

    price, stderr, paths, discounted = price_european_option_mc(
        S0=100,
        K=100,
        T=1.0,
        r=0.05,
        sigma=0.2,
        n_steps=n_steps,
        n_sims=n_sims,
        option_type="call",
        seed=123,  # pour avoir un test reproductible
    )

    assert price > 0.0, "Le prix Monte Carlo doit être strictement positif."
    assert paths.shape == (n_steps + 1, n_sims), "Dimensions des trajectoires incorrectes."
    assert discounted.shape == (n_sims,), "Dimensions des payoffs actualisés incorrectes."
