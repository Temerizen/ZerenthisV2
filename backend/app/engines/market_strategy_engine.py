from backend.app.engines.market_adaptation_engine import get_bias

def generate_signals(market_data):
    signals = []

    for item in market_data:
        change = float(item.get("change", 0))
        asset = item.get("asset", "UNKNOWN")

        if change >= 5:
            action = "BUY"
            reason = "strong_upside_momentum"
        elif change >= 2:
            action = "BUY"
            reason = "moderate_upside_momentum"
        elif change <= -5:
            action = "SELL"
            reason = "strong_downside_momentum"
        elif change <= -2:
            action = "SELL"
            reason = "moderate_downside_momentum"
        else:
            action = "HOLD"
            reason = "no_clear_edge"

        # 🔥 APPLY LEARNING BIAS
        bias = get_bias(asset, action)

        confidence = abs(change) * bias

        signals.append({
            "asset": asset,
            "action": action,
            "confidence": round(confidence, 2),
            "reason": reason,
            "bias": round(bias, 2)
        })

    return signals
