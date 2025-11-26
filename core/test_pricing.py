
from core.pricing import OptionPricer

# Exemple d'utilisation
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
assert abs(result['price'] - expected_price) < 0.01, f"Erreur : le prix calculé ({result['price']:.2f}) ne correspond pas au prix attendu ({expected_price:.2f})"

print("\nTest réussi ! Le prix calculé est correct.")
