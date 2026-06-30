"""
NoteStack Subcategory Configuration
====================================
Defines 24 product-specific subcategories across 4 parent categories.
Each subcategory maps 6 user-facing sensory attributes to the 5 base model targets
via a weight matrix, enabling product-specific evaluation while reusing trained models.

Model targets per parent:
  dairy:     sweetness, sourness, body, creaminess, flavor_balance
  chocolate: bitterness, sweetness, melt, snap, flavor_balance
  spices:    pungency, aroma, colour, saltiness, flavor_balance
  snacks:    crunchiness, oiliness, saltiness, flavour, flavor_balance
"""

SUBCATEGORIES = {
    # ─── DAIRY ────────────────────────────────────────────────────
    "milk": {
        "name": "Milk",
        "icon": "🥛",
        "description": "Fresh, pasteurized, and flavored milk products",
        "parent_category": "dairy",
        "attributes": [
            {
                "key": "creaminess", "name": "Creaminess",
                "description": "How rich, smooth, and creamy the milk feels in the mouth.",
                "mapping": {"creaminess": 1.0},
            },
            {
                "key": "freshness", "name": "Freshness",
                "description": "How clean and fresh the milk tastes, free from off-flavors.",
                "mapping": {"flavor_balance": 1.0},
            },
            {
                "key": "sweetness", "name": "Sweetness",
                "description": "The level of natural or added sweetness perceived.",
                "mapping": {"sweetness": 1.0},
            },
            {
                "key": "mouthfeel", "name": "Mouthfeel",
                "description": "The body and weight of the milk on the palate.",
                "mapping": {"body": 1.0},
            },
            {
                "key": "aroma", "name": "Aroma",
                "description": "The overall fragrance and scent character of the milk.",
                "mapping": {"sourness": 0.4, "flavor_balance": 0.6},
            },
            {
                "key": "thickness", "name": "Thickness",
                "description": "How thick or thin the milk feels — its viscosity.",
                "mapping": {"body": 0.6, "creaminess": 0.4},
            },
        ],
    },
    "yogurt": {
        "name": "Yogurt",
        "icon": "🍶",
        "description": "Yoghurt, dahi, and fermented milk products",
        "parent_category": "dairy",
        "attributes": [
            {
                "key": "creaminess", "name": "Creaminess",
                "description": "How rich, smooth, and creamy the yogurt feels while eating.",
                "mapping": {"creaminess": 1.0},
            },
            {
                "key": "sourness", "name": "Sourness",
                "description": "The tangy, acidic taste from lactic acid fermentation.",
                "mapping": {"sourness": 1.0},
            },
            {
                "key": "thickness", "name": "Thickness",
                "description": "How thick and spoonable the yogurt is.",
                "mapping": {"body": 1.0},
            },
            {
                "key": "smoothness", "name": "Smoothness",
                "description": "How uniform and lump-free the texture is.",
                "mapping": {"creaminess": 0.5, "body": 0.5},
            },
            {
                "key": "sweetness", "name": "Sweetness",
                "description": "The level of sweetness, whether natural or added.",
                "mapping": {"sweetness": 1.0},
            },
            {
                "key": "aroma", "name": "Aroma",
                "description": "The fermented, milky fragrance of the yogurt.",
                "mapping": {"flavor_balance": 1.0},
            },
        ],
    },
    "cheese": {
        "name": "Cheese",
        "icon": "🧀",
        "description": "Paneer, processed cheese, and cheese spreads",
        "parent_category": "dairy",
        "attributes": [
            {
                "key": "creaminess", "name": "Creaminess",
                "description": "How creamy and spreadable the cheese feels.",
                "mapping": {"creaminess": 1.0},
            },
            {
                "key": "sharpness", "name": "Sharpness",
                "description": "The intensity of aged or tangy flavor notes.",
                "mapping": {"sourness": 1.0},
            },
            {
                "key": "firmness", "name": "Firmness",
                "description": "How firm or soft the cheese texture is.",
                "mapping": {"body": 1.0},
            },
            {
                "key": "saltiness", "name": "Saltiness",
                "description": "The perceived salt level in the cheese.",
                "mapping": {"sweetness": 0.3, "flavor_balance": 0.7},
            },
            {
                "key": "flavor_depth", "name": "Flavor Depth",
                "description": "The complexity and richness of cheese flavor.",
                "mapping": {"flavor_balance": 1.0},
            },
            {
                "key": "meltability", "name": "Meltability",
                "description": "How well the cheese melts when heated.",
                "mapping": {"creaminess": 0.6, "body": 0.4},
            },
        ],
    },
    "butter": {
        "name": "Butter",
        "icon": "🧈",
        "description": "Table butter, cooking butter, and cultured butter",
        "parent_category": "dairy",
        "attributes": [
            {
                "key": "creaminess", "name": "Creaminess",
                "description": "How rich and buttery the product feels on the palate.",
                "mapping": {"creaminess": 1.0},
            },
            {
                "key": "saltiness", "name": "Saltiness",
                "description": "The level of salt in the butter.",
                "mapping": {"sourness": 0.3, "sweetness": 0.7},
            },
            {
                "key": "spreadability", "name": "Spreadability",
                "description": "How easily the butter spreads at room temperature.",
                "mapping": {"body": 1.0},
            },
            {
                "key": "freshness", "name": "Freshness",
                "description": "How clean and fresh the butter tastes.",
                "mapping": {"flavor_balance": 1.0},
            },
            {
                "key": "aroma", "name": "Aroma",
                "description": "The buttery, milky fragrance intensity.",
                "mapping": {"sweetness": 0.4, "flavor_balance": 0.6},
            },
            {
                "key": "richness", "name": "Richness",
                "description": "The overall fat richness and indulgent character.",
                "mapping": {"creaminess": 0.7, "body": 0.3},
            },
        ],
    },
    "ice_cream": {
        "name": "Ice Cream",
        "icon": "🍦",
        "description": "Ice cream, kulfi, and frozen dairy desserts",
        "parent_category": "dairy",
        "attributes": [
            {
                "key": "creaminess", "name": "Creaminess",
                "description": "How rich, smooth, and creamy the ice cream feels.",
                "mapping": {"creaminess": 1.0},
            },
            {
                "key": "sweetness", "name": "Sweetness",
                "description": "The overall sweetness level of the dessert.",
                "mapping": {"sweetness": 1.0},
            },
            {
                "key": "smoothness", "name": "Smoothness",
                "description": "How free from ice crystals — silky texture.",
                "mapping": {"body": 1.0},
            },
            {
                "key": "flavor_intensity", "name": "Flavor Intensity",
                "description": "How strong and true the primary flavor is.",
                "mapping": {"flavor_balance": 1.0},
            },
            {
                "key": "melt_rate", "name": "Melt Rate",
                "description": "How quickly the ice cream melts — relates to body.",
                "mapping": {"body": 0.5, "creaminess": 0.5},
            },
            {
                "key": "aftertaste", "name": "Aftertaste",
                "description": "The lingering taste after swallowing.",
                "mapping": {"sourness": 0.4, "flavor_balance": 0.6},
            },
        ],
    },
    "dairy_beverage": {
        "name": "Dairy Beverage",
        "icon": "🥤",
        "description": "Lassi, buttermilk, milkshakes, and flavored drinks",
        "parent_category": "dairy",
        "attributes": [
            {
                "key": "creaminess", "name": "Creaminess",
                "description": "How rich and creamy the beverage feels.",
                "mapping": {"creaminess": 1.0},
            },
            {
                "key": "sweetness", "name": "Sweetness",
                "description": "The perceived sweetness level.",
                "mapping": {"sweetness": 1.0},
            },
            {
                "key": "tanginess", "name": "Tanginess",
                "description": "The pleasant sour or tangy flavor note.",
                "mapping": {"sourness": 1.0},
            },
            {
                "key": "body", "name": "Body",
                "description": "The thickness and weight of the drink.",
                "mapping": {"body": 1.0},
            },
            {
                "key": "refreshment", "name": "Refreshment",
                "description": "How refreshing and thirst-quenching the drink feels.",
                "mapping": {"flavor_balance": 1.0},
            },
            {
                "key": "aroma", "name": "Aroma",
                "description": "The overall fragrance of the beverage.",
                "mapping": {"flavor_balance": 0.5, "sweetness": 0.5},
            },
        ],
    },

    # ─── CHOCOLATE & CONFECTIONERY ────────────────────────────────
    "milk_chocolate": {
        "name": "Milk Chocolate",
        "icon": "🍫",
        "description": "Creamy milk chocolate bars and couverture",
        "parent_category": "chocolate",
        "attributes": [
            {
                "key": "cocoa_intensity", "name": "Cocoa Intensity",
                "description": "The strength of chocolate/cocoa flavor.",
                "mapping": {"bitterness": 1.0},
            },
            {
                "key": "sweetness", "name": "Sweetness",
                "description": "The overall sweetness of the chocolate.",
                "mapping": {"sweetness": 1.0},
            },
            {
                "key": "meltability", "name": "Meltability",
                "description": "How smoothly the chocolate melts on the tongue.",
                "mapping": {"melt": 1.0},
            },
            {
                "key": "creaminess", "name": "Creaminess",
                "description": "The milky, creamy richness of the chocolate.",
                "mapping": {"snap": 0.3, "melt": 0.4, "flavor_balance": 0.3},
            },
            {
                "key": "snap_quality", "name": "Snap Quality",
                "description": "The clean break when you snap or bite the chocolate.",
                "mapping": {"snap": 1.0},
            },
            {
                "key": "flavor_balance", "name": "Flavor Balance",
                "description": "How well cocoa, milk, and sugar harmonize together.",
                "mapping": {"flavor_balance": 1.0},
            },
        ],
    },
    "dark_chocolate": {
        "name": "Dark Chocolate",
        "icon": "🍫",
        "description": "Intense dark chocolate with high cocoa content",
        "parent_category": "chocolate",
        "attributes": [
            {
                "key": "bitterness", "name": "Bitterness",
                "description": "The intensity of bitter taste from cocoa.",
                "mapping": {"bitterness": 1.0},
            },
            {
                "key": "sweetness", "name": "Sweetness",
                "description": "The counterbalancing sweetness level.",
                "mapping": {"sweetness": 1.0},
            },
            {
                "key": "meltability", "name": "Meltability",
                "description": "How smoothly the chocolate melts in your mouth.",
                "mapping": {"melt": 1.0},
            },
            {
                "key": "snap_quality", "name": "Snap Quality",
                "description": "The crisp, clean break when biting.",
                "mapping": {"snap": 1.0},
            },
            {
                "key": "aroma", "name": "Aroma",
                "description": "The depth and complexity of chocolate aroma.",
                "mapping": {"flavor_balance": 1.0},
            },
            {
                "key": "astringency", "name": "Astringency",
                "description": "The dry, puckering sensation from tannins in cocoa.",
                "mapping": {"bitterness": 0.6, "flavor_balance": 0.4},
            },
        ],
    },
    "white_chocolate": {
        "name": "White Chocolate",
        "icon": "🍬",
        "description": "Sweet white chocolate made with cocoa butter",
        "parent_category": "chocolate",
        "attributes": [
            {
                "key": "sweetness", "name": "Sweetness",
                "description": "The dominant sweet flavor of white chocolate.",
                "mapping": {"sweetness": 1.0},
            },
            {
                "key": "creaminess", "name": "Creaminess",
                "description": "The buttery, milky cream character.",
                "mapping": {"flavor_balance": 1.0},
            },
            {
                "key": "meltability", "name": "Meltability",
                "description": "How well it melts — driven by cocoa butter content.",
                "mapping": {"melt": 1.0},
            },
            {
                "key": "vanilla_note", "name": "Vanilla Note",
                "description": "The vanilla flavoring intensity.",
                "mapping": {"bitterness": 0.3, "flavor_balance": 0.7},
            },
            {
                "key": "snap_quality", "name": "Snap Quality",
                "description": "The firmness and clean break.",
                "mapping": {"snap": 1.0},
            },
            {
                "key": "richness", "name": "Richness",
                "description": "The overall fatty, indulgent mouthfeel.",
                "mapping": {"melt": 0.5, "bitterness": 0.5},
            },
        ],
    },
    "gummy_candy": {
        "name": "Gummy Candy",
        "icon": "🍬",
        "description": "Gummies, jellies, and fruit-flavored soft candy",
        "parent_category": "chocolate",
        "attributes": [
            {
                "key": "sweetness", "name": "Sweetness",
                "description": "The dominant sweetness of the candy.",
                "mapping": {"sweetness": 1.0},
            },
            {
                "key": "chewiness", "name": "Chewiness",
                "description": "How chewy and elastic the candy texture is.",
                "mapping": {"snap": 1.0},
            },
            {
                "key": "fruitiness", "name": "Fruitiness",
                "description": "The intensity of fruit flavor.",
                "mapping": {"flavor_balance": 1.0},
            },
            {
                "key": "sourness", "name": "Sourness",
                "description": "The sour or tangy coating/flavor.",
                "mapping": {"bitterness": 1.0},
            },
            {
                "key": "softness", "name": "Softness",
                "description": "How soft and yielding the candy is.",
                "mapping": {"melt": 1.0},
            },
            {
                "key": "aroma", "name": "Aroma",
                "description": "The fruity, candy-like fragrance.",
                "mapping": {"flavor_balance": 0.5, "sweetness": 0.5},
            },
        ],
    },
    "caramel": {
        "name": "Caramel",
        "icon": "🍮",
        "description": "Caramel candies, sauces, and toffees",
        "parent_category": "chocolate",
        "attributes": [
            {
                "key": "sweetness", "name": "Sweetness",
                "description": "The caramelized sugar sweetness level.",
                "mapping": {"sweetness": 1.0},
            },
            {
                "key": "butteriness", "name": "Butteriness",
                "description": "The rich buttery flavor character.",
                "mapping": {"melt": 1.0},
            },
            {
                "key": "chewiness", "name": "Chewiness",
                "description": "How chewy or soft the caramel texture is.",
                "mapping": {"snap": 1.0},
            },
            {
                "key": "toastiness", "name": "Toastiness",
                "description": "The depth of caramelization — nutty, toasty notes.",
                "mapping": {"bitterness": 1.0},
            },
            {
                "key": "smoothness", "name": "Smoothness",
                "description": "How smooth and non-grainy the texture is.",
                "mapping": {"melt": 0.5, "flavor_balance": 0.5},
            },
            {
                "key": "flavor_balance", "name": "Flavor Balance",
                "description": "How well sweet, butter, and toasty notes harmonize.",
                "mapping": {"flavor_balance": 1.0},
            },
        ],
    },
    "cocoa_powder": {
        "name": "Cocoa Powder",
        "icon": "☕",
        "description": "Natural and Dutch-process cocoa powders",
        "parent_category": "chocolate",
        "attributes": [
            {
                "key": "bitterness", "name": "Bitterness",
                "description": "The natural bitter intensity of cocoa.",
                "mapping": {"bitterness": 1.0},
            },
            {
                "key": "cocoa_aroma", "name": "Cocoa Aroma",
                "description": "The strength of chocolate fragrance.",
                "mapping": {"flavor_balance": 1.0},
            },
            {
                "key": "sweetness", "name": "Sweetness",
                "description": "Any residual or added sweetness.",
                "mapping": {"sweetness": 1.0},
            },
            {
                "key": "colour_depth", "name": "Colour Depth",
                "description": "How deep and rich the brown color is.",
                "mapping": {"snap": 0.5, "bitterness": 0.5},
            },
            {
                "key": "solubility", "name": "Solubility",
                "description": "How well the powder dissolves in liquid.",
                "mapping": {"melt": 1.0},
            },
            {
                "key": "astringency", "name": "Astringency",
                "description": "The dry, puckering sensation from polyphenols.",
                "mapping": {"snap": 0.4, "flavor_balance": 0.6},
            },
        ],
    },

    # ─── SPICES & SEASONINGS ──────────────────────────────────────
    "spice_blend": {
        "name": "Spice Blend",
        "icon": "🫙",
        "description": "Custom multi-spice blends and mixes",
        "parent_category": "spices",
        "attributes": [
            {
                "key": "pungency", "name": "Pungency",
                "description": "The heat and spicy kick from chili and pepper.",
                "mapping": {"pungency": 1.0},
            },
            {
                "key": "aroma", "name": "Aroma",
                "description": "The overall fragrance complexity of the blend.",
                "mapping": {"aroma": 1.0},
            },
            {
                "key": "colour", "name": "Colour",
                "description": "The visual color intensity of the blend.",
                "mapping": {"colour": 1.0},
            },
            {
                "key": "saltiness", "name": "Saltiness",
                "description": "The salt level in the blend.",
                "mapping": {"saltiness": 1.0},
            },
            {
                "key": "flavor_balance", "name": "Flavor Balance",
                "description": "How well all spice components work together.",
                "mapping": {"flavor_balance": 1.0},
            },
            {
                "key": "warmth", "name": "Warmth",
                "description": "The warm, lingering sensation from cumin and coriander.",
                "mapping": {"pungency": 0.4, "aroma": 0.6},
            },
        ],
    },
    "curry_powder": {
        "name": "Curry Powder",
        "icon": "🍛",
        "description": "Traditional and regional curry powder blends",
        "parent_category": "spices",
        "attributes": [
            {
                "key": "pungency", "name": "Pungency",
                "description": "The chili heat level in the curry powder.",
                "mapping": {"pungency": 1.0},
            },
            {
                "key": "aroma", "name": "Aroma",
                "description": "The characteristic curry fragrance.",
                "mapping": {"aroma": 1.0},
            },
            {
                "key": "colour", "name": "Colour",
                "description": "The golden-yellow colour from turmeric.",
                "mapping": {"colour": 1.0},
            },
            {
                "key": "earthiness", "name": "Earthiness",
                "description": "The earthy, grounding flavor notes.",
                "mapping": {"flavor_balance": 1.0},
            },
            {
                "key": "saltiness", "name": "Saltiness",
                "description": "The salt content of the powder.",
                "mapping": {"saltiness": 1.0},
            },
            {
                "key": "complexity", "name": "Complexity",
                "description": "The layered depth of multiple spice notes.",
                "mapping": {"aroma": 0.5, "flavor_balance": 0.5},
            },
        ],
    },
    "masala_mix": {
        "name": "Masala Mix",
        "icon": "🌶️",
        "description": "Garam masala, chaat masala, and specialty mixes",
        "parent_category": "spices",
        "attributes": [
            {
                "key": "pungency", "name": "Pungency",
                "description": "The spicy heat intensity.",
                "mapping": {"pungency": 1.0},
            },
            {
                "key": "aroma", "name": "Aroma",
                "description": "The aromatic intensity of the masala.",
                "mapping": {"aroma": 1.0},
            },
            {
                "key": "tanginess", "name": "Tanginess",
                "description": "The sour or tangy notes (from amchur, citric acid).",
                "mapping": {"saltiness": 0.5, "flavor_balance": 0.5},
            },
            {
                "key": "colour", "name": "Colour",
                "description": "The visual appeal and colour richness.",
                "mapping": {"colour": 1.0},
            },
            {
                "key": "flavor_balance", "name": "Flavor Balance",
                "description": "How well sweet, sour, spicy, and salty notes harmonize.",
                "mapping": {"flavor_balance": 1.0},
            },
            {
                "key": "warmth", "name": "Warmth",
                "description": "The warm spice sensation from cinnamon, cloves, cardamom.",
                "mapping": {"pungency": 0.3, "aroma": 0.7},
            },
        ],
    },
    "seasoning_powder": {
        "name": "Seasoning Powder",
        "icon": "🧂",
        "description": "Flavored seasoning powders for snacks and meals",
        "parent_category": "spices",
        "attributes": [
            {
                "key": "saltiness", "name": "Saltiness",
                "description": "The dominant salt flavor level.",
                "mapping": {"saltiness": 1.0},
            },
            {
                "key": "pungency", "name": "Pungency",
                "description": "Any chili or pepper heat.",
                "mapping": {"pungency": 1.0},
            },
            {
                "key": "umami", "name": "Umami",
                "description": "The savory, mouth-filling taste.",
                "mapping": {"flavor_balance": 1.0},
            },
            {
                "key": "aroma", "name": "Aroma",
                "description": "The fragrance when sprinkled on food.",
                "mapping": {"aroma": 1.0},
            },
            {
                "key": "colour", "name": "Colour",
                "description": "The visual colour of the seasoning.",
                "mapping": {"colour": 1.0},
            },
            {
                "key": "aftertaste", "name": "Aftertaste",
                "description": "The lingering taste after consumption.",
                "mapping": {"aroma": 0.4, "flavor_balance": 0.6},
            },
        ],
    },
    "marinade_mix": {
        "name": "Marinade Mix",
        "icon": "🥘",
        "description": "Wet and dry marinades for meat and vegetables",
        "parent_category": "spices",
        "attributes": [
            {
                "key": "pungency", "name": "Pungency",
                "description": "The heat level of the marinade.",
                "mapping": {"pungency": 1.0},
            },
            {
                "key": "aroma", "name": "Aroma",
                "description": "The aromatic profile that develops during marination.",
                "mapping": {"aroma": 1.0},
            },
            {
                "key": "saltiness", "name": "Saltiness",
                "description": "The salt level for flavor penetration.",
                "mapping": {"saltiness": 1.0},
            },
            {
                "key": "colour", "name": "Colour",
                "description": "The colour imparted to the marinated food.",
                "mapping": {"colour": 1.0},
            },
            {
                "key": "flavor_balance", "name": "Flavor Balance",
                "description": "The harmony between spice, acid, and salt.",
                "mapping": {"flavor_balance": 1.0},
            },
            {
                "key": "penetration", "name": "Penetration",
                "description": "How deeply flavor absorbs into food.",
                "mapping": {"saltiness": 0.5, "pungency": 0.5},
            },
        ],
    },
    "sauce_paste": {
        "name": "Sauce & Paste",
        "icon": "🫕",
        "description": "Cooking pastes, chutneys, and sauce bases",
        "parent_category": "spices",
        "attributes": [
            {
                "key": "pungency", "name": "Pungency",
                "description": "The spicy heat in the sauce or paste.",
                "mapping": {"pungency": 1.0},
            },
            {
                "key": "aroma", "name": "Aroma",
                "description": "The cooked or raw aromatic intensity.",
                "mapping": {"aroma": 1.0},
            },
            {
                "key": "thickness", "name": "Thickness",
                "description": "The viscosity and body of the paste/sauce.",
                "mapping": {"colour": 0.4, "saltiness": 0.6},
            },
            {
                "key": "colour", "name": "Colour",
                "description": "The visual richness and appeal.",
                "mapping": {"colour": 1.0},
            },
            {
                "key": "flavor_balance", "name": "Flavor Balance",
                "description": "How well all flavor components come together.",
                "mapping": {"flavor_balance": 1.0},
            },
            {
                "key": "tanginess", "name": "Tanginess",
                "description": "The sour or acidic character of the sauce.",
                "mapping": {"saltiness": 0.4, "flavor_balance": 0.6},
            },
        ],
    },

    # ─── SNACKS & SAVORY FOODS ────────────────────────────────────
    "potato_chips": {
        "name": "Potato Chips",
        "icon": "🥔",
        "description": "Classic fried and baked potato chips",
        "parent_category": "snacks",
        "attributes": [
            {
                "key": "crunchiness", "name": "Crunchiness",
                "description": "How crisp and crunchy the chips feel during chewing.",
                "mapping": {"crunchiness": 1.0},
            },
            {
                "key": "saltiness", "name": "Saltiness",
                "description": "The perceived salt level on the chip surface.",
                "mapping": {"saltiness": 1.0},
            },
            {
                "key": "crispness", "name": "Crispness",
                "description": "The light, delicate cracking texture.",
                "mapping": {"crunchiness": 0.5, "flavour": 0.5},
            },
            {
                "key": "oiliness", "name": "Oiliness",
                "description": "How greasy or oily the chip feels.",
                "mapping": {"oiliness": 1.0},
            },
            {
                "key": "flavor_strength", "name": "Flavor Strength",
                "description": "The intensity of the seasoning flavor.",
                "mapping": {"flavour": 1.0},
            },
            {
                "key": "aftertaste", "name": "Aftertaste",
                "description": "The lingering taste after eating.",
                "mapping": {"flavor_balance": 1.0},
            },
        ],
    },
    "extruded_snacks": {
        "name": "Extruded Snacks",
        "icon": "🧀",
        "description": "Puffed, extruded corn and rice snacks",
        "parent_category": "snacks",
        "attributes": [
            {
                "key": "crunchiness", "name": "Crunchiness",
                "description": "The crunchy, airy bite of the puff.",
                "mapping": {"crunchiness": 1.0},
            },
            {
                "key": "puffiness", "name": "Puffiness",
                "description": "How light and airy the texture is.",
                "mapping": {"oiliness": 0.4, "crunchiness": 0.6},
            },
            {
                "key": "saltiness", "name": "Saltiness",
                "description": "The salt level in the snack.",
                "mapping": {"saltiness": 1.0},
            },
            {
                "key": "flavor_strength", "name": "Flavor Strength",
                "description": "How strong the seasoning flavor is.",
                "mapping": {"flavour": 1.0},
            },
            {
                "key": "oiliness", "name": "Oiliness",
                "description": "The oil/fat perception.",
                "mapping": {"oiliness": 1.0},
            },
            {
                "key": "flavor_balance", "name": "Flavor Balance",
                "description": "How well all taste components work together.",
                "mapping": {"flavor_balance": 1.0},
            },
        ],
    },
    "popcorn": {
        "name": "Popcorn",
        "icon": "🍿",
        "description": "Butter, caramel, and seasoned popcorn",
        "parent_category": "snacks",
        "attributes": [
            {
                "key": "crunchiness", "name": "Crunchiness",
                "description": "The crunch and pop of each kernel.",
                "mapping": {"crunchiness": 1.0},
            },
            {
                "key": "butteriness", "name": "Butteriness",
                "description": "The buttery flavor and aroma.",
                "mapping": {"oiliness": 1.0},
            },
            {
                "key": "saltiness", "name": "Saltiness",
                "description": "The salt level on the popcorn.",
                "mapping": {"saltiness": 1.0},
            },
            {
                "key": "flavor_strength", "name": "Flavor Strength",
                "description": "The intensity of added flavoring.",
                "mapping": {"flavour": 1.0},
            },
            {
                "key": "lightness", "name": "Lightness",
                "description": "How light and airy the popcorn feels.",
                "mapping": {"crunchiness": 0.6, "flavor_balance": 0.4},
            },
            {
                "key": "flavor_balance", "name": "Flavor Balance",
                "description": "How well butter, salt, and seasoning harmonize.",
                "mapping": {"flavor_balance": 1.0},
            },
        ],
    },
    "crackers": {
        "name": "Crackers",
        "icon": "🍪",
        "description": "Savory crackers, rusks, and crispy flatbreads",
        "parent_category": "snacks",
        "attributes": [
            {
                "key": "crunchiness", "name": "Crunchiness",
                "description": "The crisp, shattering bite.",
                "mapping": {"crunchiness": 1.0},
            },
            {
                "key": "saltiness", "name": "Saltiness",
                "description": "The surface salt level.",
                "mapping": {"saltiness": 1.0},
            },
            {
                "key": "toastiness", "name": "Toastiness",
                "description": "The baked, toasty grain flavor.",
                "mapping": {"flavour": 1.0},
            },
            {
                "key": "oiliness", "name": "Oiliness",
                "description": "The fat/oil content perception.",
                "mapping": {"oiliness": 1.0},
            },
            {
                "key": "dryness", "name": "Dryness",
                "description": "How dry and crisp vs. soft the cracker is.",
                "mapping": {"crunchiness": 0.5, "oiliness": 0.5},
            },
            {
                "key": "flavor_balance", "name": "Flavor Balance",
                "description": "The overall harmony of grain, salt, and seasoning.",
                "mapping": {"flavor_balance": 1.0},
            },
        ],
    },
    "namkeen": {
        "name": "Namkeen",
        "icon": "🥜",
        "description": "Traditional Indian savory snacks — sev, mixture, bhujia",
        "parent_category": "snacks",
        "attributes": [
            {
                "key": "crunchiness", "name": "Crunchiness",
                "description": "The crispy, crunchy texture.",
                "mapping": {"crunchiness": 1.0},
            },
            {
                "key": "spiciness", "name": "Spiciness",
                "description": "The chili heat and spice intensity.",
                "mapping": {"flavour": 1.0},
            },
            {
                "key": "saltiness", "name": "Saltiness",
                "description": "The salt level in the namkeen.",
                "mapping": {"saltiness": 1.0},
            },
            {
                "key": "oiliness", "name": "Oiliness",
                "description": "The frying oil perception.",
                "mapping": {"oiliness": 1.0},
            },
            {
                "key": "aroma", "name": "Aroma",
                "description": "The spiced, fried fragrance.",
                "mapping": {"flavour": 0.4, "flavor_balance": 0.6},
            },
            {
                "key": "flavor_balance", "name": "Flavor Balance",
                "description": "How well salt, spice, and crunch come together.",
                "mapping": {"flavor_balance": 1.0},
            },
        ],
    },
    "instant_noodles_seasoning": {
        "name": "Instant Noodles Seasoning",
        "icon": "🍜",
        "description": "Seasoning packets for instant noodles and ramen",
        "parent_category": "snacks",
        "attributes": [
            {
                "key": "umami", "name": "Umami",
                "description": "The savory, mouth-filling depth of flavor.",
                "mapping": {"flavour": 1.0},
            },
            {
                "key": "saltiness", "name": "Saltiness",
                "description": "The salt intensity in the seasoning.",
                "mapping": {"saltiness": 1.0},
            },
            {
                "key": "spiciness", "name": "Spiciness",
                "description": "The chili heat level.",
                "mapping": {"crunchiness": 0.3, "oiliness": 0.7},
            },
            {
                "key": "aroma", "name": "Aroma",
                "description": "The appetizing fragrance when dissolved.",
                "mapping": {"flavor_balance": 1.0},
            },
            {
                "key": "richness", "name": "Richness",
                "description": "The fatty, brothy richness of the seasoning.",
                "mapping": {"oiliness": 1.0},
            },
            {
                "key": "flavor_balance", "name": "Flavor Balance",
                "description": "How well salt, spice, umami, and oil harmonize.",
                "mapping": {"flavor_balance": 0.5, "flavour": 0.5},
            },
        ],
    },
}


def get_subcategories_for_category(category: str) -> dict:
    """Return all subcategories belonging to a parent category."""
    return {
        key: val for key, val in SUBCATEGORIES.items()
        if val["parent_category"] == category
    }


def get_subcategory(key: str) -> dict:
    """Return a single subcategory config by key."""
    return SUBCATEGORIES.get(key)
