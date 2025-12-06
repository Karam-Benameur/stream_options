# verify_installation.py
import importlib
import sys

print("=" * 50)
print("VÉRIFICATION DES INSTALLATIONS")
print("=" * 50)

packages = [
    ("streamlit", "1.39.0"),
    ("pandas", "2.2.3"),
    ("numpy", "2.1.3"),
    ("scipy", "1.14.0"),
    ("yfinance", "0.2.66"),
    ("plotly", "5.22.0"),
    ("matplotlib", "3.9.2"),
    ("curl_cffi", "0.13.0"),
    ("websockets", "13.0")
]

all_ok = True
for package_name, expected_version in packages:
    try:
        module = importlib.import_module(package_name.replace('-', '_'))
        version = getattr(module, '__version__', 'N/A')
        status = "✓" if expected_version in version or expected_version == "N/A" else "⚠"
        print(f"{status} {package_name}: {version}")
    except ImportError as e:
        print(f"✗ {package_name}: NON INSTALLÉ - {e}")
        all_ok = False

print("=" * 50)
if all_ok:
    print("✅ TOUTES LES DÉPENDANCES SONT INSTALLÉES !")
    print("🎉 Vous pouvez maintenant lancer votre application:")
    print("   streamlit run Home.py")
else:
    print("❌ Certaines dépendances manquent.")
    print("   Exécutez: pip install -r requirements.txt")
print("=" * 50)
