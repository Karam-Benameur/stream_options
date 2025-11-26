
from core.pricing import OptionPricer

# Exemple d'utilisation
pricer = OptionPricer(S0=100, K=100, r=0.05, sigma=0.2, T=1, kind='call')
result = pricer.black_scholes()

print("Prix de l'option :", result['price'])
print("Delta :", result['delta'])
print("Gamma :", result['gamma'])
print("Vega :", result['vega'])
print("Theta :", result['theta'])
print("Rho :", result['rho'])
