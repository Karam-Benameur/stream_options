
from core.pricing import OptionPricer, price_european_option_mc

# -------------------------------------------------
# 1) Test Black-Scholes (classe OptionPricer)
# -------------------------------------------------
pricer = OptionPricer(S0=100, K=100, r=0.05, sigma=0.2, T=1, kind='call')
result = pricer.black_scholes()

print("Prix de l'option :", round(result['price'], 2))
print("Delta :", round(result['delta'], 4))
print("Gamma :", round(result['gamma'], 4))
print("Vega :", round(result['vega'], 4))
print("Theta :", round(result['theta'], 4))
print("Rho :", round(result['rho'], 4))

# Vérification du prix (valeur théorique attendue : ~10.45)
expected_price = 10.45
assert abs(result['price'] - expected_price) < 0.05, (
    f"Erreur : le prix calculé ({result['price']}) "
    f"diffère trop de la valeur attendue ({expected_price})"
)

# -------------------------------------------------
# 2) Test rapide de la fonction Monte Carlo
# -------------------------------------------------
mc_price, mc_stderr, mc_paths, mc_disc = price_european_option_mc(
    S0=100, K=100, T=1.0, r=0.05, sigma=0.2,
    n_steps=50, n_sims=1_000, option_type="call",
)

assert mc_price > 0, "Le prix Monte Carlo doit être strictement positif."
assert mc_paths.shape == (51, 1000), "Dimensions des trajectoires incorrectes."

print("\nTest Monte Carlo OK (prix positif et dimensions correctes).")
print("\nTous les tests de core/test_pricing.py sont passés avec succès ✅")
