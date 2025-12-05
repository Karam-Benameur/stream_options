import streamlit as st
import numpy as np
import math
from scipy.stats import norm
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf

# -----------------------------------------------------------------------------
# 1. MODEL ENGINE: Core Financial Calculations
# -----------------------------------------------------------------------------
class OptionModel:
    """
    Handles all mathematical calculations for Black-Scholes and Binomial Models.
    Methods are static and cached for performance.
    """

    @staticmethod
    @st.cache_data
    def black_scholes_price(S, K, T, r, sigma, option_type="call"):
        """Calculates the theoretical price using the Black-Scholes analytical formula."""
        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        
        if option_type == "call":
            price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
        else:
            price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        return price

    @staticmethod
    @st.cache_data
    def calculate_bopm(S0, K, T, r, sigma, N, option_type="call", style="European"):
        """
        Calculates the option price using the Cox-Ross-Rubinstein Binomial Model.
        Returns the stock tree, option tree, early exercise map, price, and delta.
        """
        dt = T / N if N > 0 else 0
        if N == 0:
            return [[S0]], [[max(0.0, S0-K) if option_type=="call" else max(0.0, K-S0)]], [[False]], 0.0, 0.0

        # 1. Tree Parameters
        u = math.exp(sigma * math.sqrt(dt))
        d = 1/u
        disc = math.exp(-r*dt)
        q = (math.exp(r*dt) - d) / (u - d)
        q = min(max(q, 0.0), 1.0)

        # 2. Forward Pass: Stock Price Tree
        stock = []
        for t in range(N+1):
            row = [S0 * (u**i) * (d**(t-i)) for i in range(t+1)]
            stock.append(row)

        # 3. Initialize Option Tree
        option = [[0.0]*(t+1) for t in range(N+1)]
        early = [[False]*(t+1) for t in range(N+1)]

        # 4. Terminal Payoff
        for i, S in enumerate(stock[-1]):
            option[-1][i] = max(0.0, S-K) if option_type=="call" else max(0.0, K-S)

        # 5. Backward Pass: Induction
        for t in range(N-1, -1, -1):
            for i in range(t+1):
                cont = disc * (q * option[t+1][i+1] + (1-q) * option[t+1][i])
                intrinsic = max(0.0, stock[t][i]-K) if option_type=="call" else max(0.0, K-stock[t][i])
                
                if style == "American" and intrinsic > cont + 1e-9:
                    option[t][i] = intrinsic
                    early[t][i] = True
                else:
                    option[t][i] = cont
        
        # 6. Calculate Delta
        delta = 0.0
        if N >= 1:
            d_option = option[1][1] - option[1][0]
            d_stock = stock[1][1] - stock[1][0]
            delta = d_option / d_stock if d_stock != 0 else 0

        return stock, option, early, option[0][0], delta

# -----------------------------------------------------------------------------
# 2. DATA MANAGER: External Data Fetching
# -----------------------------------------------------------------------------
class MarketData:
    """Handles fetching and processing market data from Yahoo Finance."""
    
    @staticmethod
    def fetch_history(ticker, period="2y"):
        """Fetches historical data and returns the dataframe and latest price."""
        try:
            ticker_obj = yf.Ticker(ticker)
            hist = ticker_obj.history(period=period)
            if not hist.empty:
                current_price = float(hist["Close"].iloc[-1])
                return hist, current_price
            return None, None
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            return None, None

# -----------------------------------------------------------------------------
# 3. VISUALIZATION ENGINE: Charts and Graphs
# -----------------------------------------------------------------------------
class Visualizer:
    """Generates all Plotly and Graphviz visualizations."""

    @staticmethod
    def tree_to_graphviz(tree, early_ex=None):
        """Generates DOT code for tree visualization."""
        lines = ["digraph G {", "rankdir=TB;", "node [shape=circle, style=filled, fillcolor=white, fontsize=10];"]
        for t, row in enumerate(tree):
            for i, val in enumerate(row):
                color = 'fillcolor="#ffcccb"' if early_ex and early_ex[t][i] else 'fillcolor="white"'
                label = f"{val:.2f}"
                lines.append(f'n{t}_{i} [label="{label}", {color}];')
            rank_nodes = " ".join([f"n{t}_{i}" for i in range(len(row))])
            lines.append(f'{{ rank = same; {rank_nodes}; }}')
        for t, row in enumerate(tree[:-1]):
            for i in range(len(row)):
                lines.append(f'n{t}_{i} -> n{t+1}_{i+1};')
                lines.append(f'n{t}_{i} -> n{t+1}_{i};')
        lines.append("}")
        return "\n".join(lines)

    @staticmethod
    def plot_heatmap(tree_data, title):
        """Generates a heatmap for large trees."""
        heatmap_data = []
        max_len = len(tree_data)
        for t, row in enumerate(tree_data):
            padded = row + [None]*(max_len-t)
            heatmap_data.append(padded)
        heatmap_data = list(map(list, zip(*heatmap_data))) 
        fig = px.imshow(heatmap_data, labels=dict(x="Time Step", y="Up Moves", color="Value"),
                        title=title, origin='lower')
        return fig

    @staticmethod
    def plot_trend(hist_df, ticker_name):
        """Plots historical stock price trend."""
        max_price = hist_df["Close"].max()
        min_price = hist_df["Close"].min()
        max_date = hist_df["Close"].idxmax()
        min_date = hist_df["Close"].idxmin()

        fig = px.line(hist_df, y="Close", title=None)
        fig.add_trace(go.Scatter(
            x=[max_date], y=[max_price], mode="markers+text", name="Peak",
            text=[f"High: {max_price:.2f}"], textposition="top center",
            marker=dict(color="green", size=10, symbol="triangle-up")
        ))
        fig.add_trace(go.Scatter(
            x=[min_date], y=[min_price], mode="markers+text", name="Low",
            text=[f"Low: {min_price:.2f}"], textposition="bottom center",
            marker=dict(color="red", size=10, symbol="triangle-down")
        ))
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=10, b=20), showlegend=False)
        return fig

    @staticmethod
    def plot_pnl(S0, K, price, option_type):
        """Plots Profit & Loss at expiration."""
        spot_range = np.linspace(S0 * 0.5, S0 * 1.5, 100)
        if option_type == "call":
            payoff = np.maximum(spot_range - K, 0) - price
        else:
            payoff = np.maximum(K - spot_range, 0) - price
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=spot_range, y=payoff, mode='lines', name='P&L', fill='tozeroy'))
        fig.add_vline(x=S0, line_dash="dash", annotation_text="Current Price")
        fig.add_hline(y=0, line_color="black", line_width=1)
        fig.update_layout(xaxis_title="Stock Price at Exp", yaxis_title="Profit / Loss ($)", height=300)
        return fig

    @staticmethod
    def plot_volatility_sensitivity(S0, K, T, r, current_sigma, bs_val, option_type):
        """Plots Option Price vs Volatility."""
        vol_range = np.linspace(0.05, 1.0, 50) 
        prices_vol = [OptionModel.black_scholes_price(S0, K, T, r, v, option_type) for v in vol_range]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=vol_range, y=prices_vol, mode='lines', name='Price Sensitivity'))
        fig.add_trace(go.Scatter(x=[current_sigma], y=[bs_val], mode='markers', 
                                 marker=dict(color='red', size=10), name='Current σ'))
        fig.update_layout(xaxis_title="Volatility (σ)", yaxis_title="Option Price ($)", height=300)
        return fig

    @staticmethod
    def plot_convergence(S0, K, T, r, sigma, option_type, style, bs_val):
        """Plots Binomial convergence to Black-Scholes as steps increase."""
        steps_range = range(2, 51, 2)
        prices = [OptionModel.calculate_bopm(S0, K, T, r, sigma, n, option_type, style)[3] for n in steps_range]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(steps_range), y=prices, mode='lines+markers', name='Binomial'))
        fig.add_hline(y=bs_val, line_dash="dash", line_color="red", annotation_text="Black-Scholes")
        fig.update_layout(title="Price Precision vs. Steps", xaxis_title="N Steps", yaxis_title="Price", height=300)
        return fig

# -----------------------------------------------------------------------------
# 4. APP CONTROLLER: Main UI Logic
# -----------------------------------------------------------------------------
class BinomialApp:
    """Main application class controlling the Streamlit interface."""

    def __init__(self):
        st.set_page_config(page_title="Binomial Model", layout="wide")
        self._inject_custom_css()
        self._initialize_session_state()

    def _inject_custom_css(self):
        st.markdown("""
        <style>
        div.stButton > button {
            width: 50px; height: 50px; border-radius: 50%; padding: 0;
            font-size: 24px; display: flex; align-items: center; justify-content: center;
            margin-top: 28px;
        }
        </style>
        """, unsafe_allow_html=True)

    def _initialize_session_state(self):
        if "ticker" not in st.session_state: st.session_state.ticker = "SPY"
        if "s0_input" not in st.session_state: st.session_state["s0_input"] = 100.0
        if "k_input" not in st.session_state: st.session_state["k_input"] = 100.0

    def run(self):
        st.title("📊 Binomial Option Model")
        st.subheader("Model Inputs & Contract Specifications")

        # --- Section 1: Ticker Input ---
        tick_col1, tick_col2 = st.columns([6, 1]) 
        with tick_col1:
            ticker = st.text_input("Ticker Symbol", value=st.session_state.ticker)
        with tick_col2:
            if st.button("➜"):
                hist, current_price = MarketData.fetch_history(ticker)
                if hist is not None:
                    st.session_state["s0_input"] = current_price
                    st.session_state["k_input"] = current_price - 10 
                    st.session_state.ticker = ticker 
                    st.session_state["history_df"] = hist

        # --- Section 2: Historical Trend ---
        if "history_df" in st.session_state and not st.session_state["history_df"].empty:
            with st.expander(f"📉 {st.session_state.ticker} - 2 Year Trend", expanded=True):
                st.plotly_chart(
                    Visualizer.plot_trend(st.session_state["history_df"], st.session_state.ticker),
                    use_container_width=True
                )

        st.markdown("---")

        # --- Section 3: Financial Inputs ---
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            S0 = st.number_input("Price (S₀)", key="s0_input")
            K = st.number_input("Strike (K)", key="k_input")
        with col2:
            T = st.number_input("Time (Yrs)", value=1.0)
            r = st.number_input("Risk-free (r)", value=0.05)
        with col3:
            sigma = st.number_input("Volatility (σ)", value=0.2)
            N = st.number_input("Steps (N)", min_value=1, max_value=100, value=5)
        with col4:
            option_type = st.selectbox("Type", ["call", "put"])
            style = st.selectbox("Style", ["European", "American"])

        st.markdown("---")

        # --- Section 4: Execution & Metrics ---
        # Run calculations
        stock_tree, opt_tree, early_ex, price, delta = OptionModel.calculate_bopm(
            S0, K, T, r, sigma, N, option_type, style
        )
        bs_val = OptionModel.black_scholes_price(S0, K, T, r, sigma, option_type)

        # Display Metrics
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Binomial Price", f"{price:.4f}")
        m2.metric("Black-Scholes", f"{bs_val:.4f}", delta=f"{price-bs_val:.4f}") 
        m3.metric("Delta (Δ)", f"{delta:.4f}")
        m4.metric("Steps Used", N)

        st.markdown("---")

        # --- Section 5: Analysis Charts ---
        st.subheader("Sensitivity & P&L Analysis")
        pnl_col, vol_col = st.columns(2)

        with pnl_col:
            st.caption("Profit/Loss at Expiration")
            st.plotly_chart(Visualizer.plot_pnl(S0, K, price, option_type), use_container_width=True)

        with vol_col:
            st.caption("Option Price vs. Volatility (σ)")
            st.plotly_chart(
                Visualizer.plot_volatility_sensitivity(S0, K, T, r, sigma, bs_val, option_type),
                use_container_width=True
            )

        st.markdown("---")

        # --- Section 6: Tree Visualizations ---
        col_viz, col_conv = st.columns([2, 1])
        with col_viz:
            st.subheader("1. Stock Price Tree")
            if N > 15:
                st.plotly_chart(Visualizer.plot_heatmap(stock_tree, "Stock Price Evolution"), use_container_width=True)
            else:
                st.graphviz_chart(Visualizer.tree_to_graphviz(stock_tree))
            
            st.markdown("⬇️ *Asset prices drive the option payoffs below*")
            
            st.subheader(f"2. Option Value Tree ({style} {option_type.title()})")
            if N > 15:
                st.plotly_chart(Visualizer.plot_heatmap(opt_tree, "Option Value Map"), use_container_width=True)
            else:
                st.graphviz_chart(Visualizer.tree_to_graphviz(opt_tree, early_ex if style=="American" else None))

        with col_conv:
            st.subheader("Model Accuracy Check")
            st.plotly_chart(
                Visualizer.plot_convergence(S0, K, T, r, sigma, option_type, style, bs_val), 
                use_container_width=True
            )

# -----------------------------------------------------------------------------
# Main Execution
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    app = BinomialApp()
    app.run()
