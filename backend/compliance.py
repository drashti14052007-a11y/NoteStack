def check_compliance(category: str, formulation: dict) -> dict:
    flags = []
    warnings = []
    passed = []

    if category == "dairy":
        fat = formulation.get("fat_pct", 0)
        if fat >= 3.25:
            passed.append(f"Fat {fat}% meets FSSAI minimum of 3.25% (FSS Regulations 2011, Schedule I, Part B)")
        else:
            flags.append(f"Fat {fat}% is below FSSAI minimum of 3.25% for dahi (FSS Regulations 2011, Schedule I, Part B)")

        starter = formulation.get("starter_pct", 0)
        if starter >= 1.0:
            passed.append(f"Starter culture {starter}% present — lactic acid fermentation confirmed")
        else:
            flags.append("Starter culture below 1% — product may not qualify as dahi under FSSAI")

    elif category == "chocolate":
        cocoa = formulation.get("cocoa_solids_pct", 0)
        cocoa_butter = formulation.get("cocoa_butter_pct", 0)
        milk = formulation.get("milk_solids_pct", 0)
        sugar = formulation.get("sugar_pct", 0)

        if cocoa >= 35:
            passed.append(f"Cocoa solids {cocoa}% meets dark chocolate minimum of 35% (FSS Regulations 2011, Schedule I)")
        else:
            flags.append(f"Cocoa solids {cocoa}% below 35% minimum for dark chocolate")

        if cocoa_butter >= 20:
            passed.append(f"Cocoa butter {cocoa_butter}% meets minimum 20% requirement")
        else:
            flags.append(f"Cocoa butter {cocoa_butter}% below 20% minimum")

        total = cocoa + sugar + milk
        if total <= 100:
            passed.append(f"Total composition {round(total, 1)}% within acceptable range")
        else:
            flags.append(f"Total composition {round(total, 1)}% exceeds 100% — formulation needs rebalancing")

    elif category == "spices":
        chili = formulation.get("chili_pct", 0)
        salt = formulation.get("salt_pct", 0)

        if chili > 25:
            warnings.append(
                f"Chili content {chili}% is high — formulations above 25% chili require "
                f"aflatoxin lab verification (FSSAI limit: ≤10 ppb total aflatoxins, "
                f"Contaminants Regulations 2011, Schedule I, Appendix B)"
            )
        else:
            passed.append(f"Chili content {chili}% — within normal range, aflatoxin risk low")

        if salt <= 8:
            passed.append(f"Salt {salt}% within acceptable range for spice blends")
        else:
            flags.append(f"Salt {salt}% is very high — review formulation for consumer safety")

    elif category == "snacks":
        fat = formulation.get("fat_pct", 0)
        moisture = formulation.get("moisture_pct", 0)

        if fat > 20:
            warnings.append(
                f"Fat content {fat}% — if hydrogenated fats are used, trans fat must be "
                f"≤2% of total fat (FSSAI Notification, January 2022). "
                f"Requires fat type verification before labelling."
            )
        else:
            passed.append(f"Fat {fat}% — moderate; trans fat risk low but verify fat source")

        if moisture <= 4:
            passed.append(f"Moisture {moisture}% is within safe range for shelf-stable snacks (≤4%)")
        else:
            warnings.append(
                f"Moisture {moisture}% exceeds 4% threshold — "
                f"product shelf life and microbial safety require validation"
            )

    status = "NON-COMPLIANT" if flags else ("ADVISORY" if warnings else "COMPLIANT")

    return {
        "status": status,
        "passed": passed,
        "warnings": warnings,
        "flags": flags,
    }