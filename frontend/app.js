const API_BASE = "https://notestack-api-aiyj.onrender.com";

let categoryConfig = null;
let selectedCategory = null;
let selectedSubcategory = null;
let selectedSubcatConfig = null;
let radarChart = null;
let lastFormulationResult = null;
let ratingValues = {};   // { attrKey: value }
let suppressPopState = false;

// ── Screen order for history navigation ─────────────────────
const SCREEN_ORDER = ["screen-welcome", "screen-category", "screen-subcategory", "screen-sliders", "screen-results"];

// ── Embedded subcategory data (works without backend redeployment) ──
const SUBCATEGORY_DATA = {
  dairy: [
    {
      key: "milk", name: "Milk", icon: "🥛", description: "Fresh, pasteurized, and flavored milk products", attributes: [
        { key: "creaminess", name: "Creaminess", description: "How rich, smooth, and creamy the milk feels in the mouth.", mapping: { creaminess: 1.0 } },
        { key: "freshness", name: "Freshness", description: "How clean and fresh the milk tastes, free from off-flavors.", mapping: { flavor_balance: 1.0 } },
        { key: "sweetness", name: "Sweetness", description: "The level of natural or added sweetness perceived.", mapping: { sweetness: 1.0 } },
        { key: "mouthfeel", name: "Mouthfeel", description: "The body and weight of the milk on the palate.", mapping: { body: 1.0 } },
        { key: "aroma", name: "Aroma", description: "The overall fragrance and scent character of the milk.", mapping: { sourness: 0.4, flavor_balance: 0.6 } },
        { key: "thickness", name: "Thickness", description: "How thick or thin the milk feels — its viscosity.", mapping: { body: 0.6, creaminess: 0.4 } },
      ]
    },
    {
      key: "yogurt", name: "Yogurt", icon: "🍶", description: "Yoghurt, dahi, and fermented milk products", attributes: [
        { key: "creaminess", name: "Creaminess", description: "How rich, smooth, and creamy the yogurt feels while eating.", mapping: { creaminess: 1.0 } },
        { key: "sourness", name: "Sourness", description: "The tangy, acidic taste from lactic acid fermentation.", mapping: { sourness: 1.0 } },
        { key: "thickness", name: "Thickness", description: "How thick and spoonable the yogurt is.", mapping: { body: 1.0 } },
        { key: "smoothness", name: "Smoothness", description: "How uniform and lump-free the texture is.", mapping: { creaminess: 0.5, body: 0.5 } },
        { key: "sweetness", name: "Sweetness", description: "The level of sweetness, whether natural or added.", mapping: { sweetness: 1.0 } },
        { key: "aroma", name: "Aroma", description: "The fermented, milky fragrance of the yogurt.", mapping: { flavor_balance: 1.0 } },
      ]
    },
    {
      key: "cheese", name: "Cheese", icon: "🧀", description: "Paneer, processed cheese, and cheese spreads", attributes: [
        { key: "creaminess", name: "Creaminess", description: "How creamy and spreadable the cheese feels.", mapping: { creaminess: 1.0 } },
        { key: "sharpness", name: "Sharpness", description: "The intensity of aged or tangy flavor notes.", mapping: { sourness: 1.0 } },
        { key: "firmness", name: "Firmness", description: "How firm or soft the cheese texture is.", mapping: { body: 1.0 } },
        { key: "saltiness", name: "Saltiness", description: "The perceived salt level in the cheese.", mapping: { sweetness: 0.3, flavor_balance: 0.7 } },
        { key: "flavor_depth", name: "Flavor Depth", description: "The complexity and richness of cheese flavor.", mapping: { flavor_balance: 1.0 } },
        { key: "meltability", name: "Meltability", description: "How well the cheese melts when heated.", mapping: { creaminess: 0.6, body: 0.4 } },
      ]
    },
    {
      key: "butter", name: "Butter", icon: "🧈", description: "Table butter, cooking butter, and cultured butter", attributes: [
        { key: "creaminess", name: "Creaminess", description: "How rich and buttery the product feels on the palate.", mapping: { creaminess: 1.0 } },
        { key: "saltiness", name: "Saltiness", description: "The level of salt in the butter.", mapping: { sourness: 0.3, sweetness: 0.7 } },
        { key: "spreadability", name: "Spreadability", description: "How easily the butter spreads at room temperature.", mapping: { body: 1.0 } },
        { key: "freshness", name: "Freshness", description: "How clean and fresh the butter tastes.", mapping: { flavor_balance: 1.0 } },
        { key: "aroma", name: "Aroma", description: "The buttery, milky fragrance intensity.", mapping: { sweetness: 0.4, flavor_balance: 0.6 } },
        { key: "richness", name: "Richness", description: "The overall fat richness and indulgent character.", mapping: { creaminess: 0.7, body: 0.3 } },
      ]
    },
    {
      key: "ice_cream", name: "Ice Cream", icon: "🍦", description: "Ice cream, kulfi, and frozen dairy desserts", attributes: [
        { key: "creaminess", name: "Creaminess", description: "How rich, smooth, and creamy the ice cream feels.", mapping: { creaminess: 1.0 } },
        { key: "sweetness", name: "Sweetness", description: "The overall sweetness level of the dessert.", mapping: { sweetness: 1.0 } },
        { key: "smoothness", name: "Smoothness", description: "How free from ice crystals — silky texture.", mapping: { body: 1.0 } },
        { key: "flavor_intensity", name: "Flavor Intensity", description: "How strong and true the primary flavor is.", mapping: { flavor_balance: 1.0 } },
        { key: "melt_rate", name: "Melt Rate", description: "How quickly the ice cream melts — relates to body.", mapping: { body: 0.5, creaminess: 0.5 } },
        { key: "aftertaste", name: "Aftertaste", description: "The lingering taste after swallowing.", mapping: { sourness: 0.4, flavor_balance: 0.6 } },
      ]
    },
    {
      key: "dairy_beverage", name: "Dairy Beverage", icon: "🥤", description: "Lassi, buttermilk, milkshakes, and flavored drinks", attributes: [
        { key: "creaminess", name: "Creaminess", description: "How rich and creamy the beverage feels.", mapping: { creaminess: 1.0 } },
        { key: "sweetness", name: "Sweetness", description: "The perceived sweetness level.", mapping: { sweetness: 1.0 } },
        { key: "tanginess", name: "Tanginess", description: "The pleasant sour or tangy flavor note.", mapping: { sourness: 1.0 } },
        { key: "body", name: "Body", description: "The thickness and weight of the drink.", mapping: { body: 1.0 } },
        { key: "refreshment", name: "Refreshment", description: "How refreshing and thirst-quenching the drink feels.", mapping: { flavor_balance: 1.0 } },
        { key: "aroma", name: "Aroma", description: "The overall fragrance of the beverage.", mapping: { flavor_balance: 0.5, sweetness: 0.5 } },
      ]
    },
  ],
  chocolate: [
    {
      key: "milk_chocolate", name: "Milk Chocolate", icon: "🍫", description: "Creamy milk chocolate bars and couverture", attributes: [
        { key: "cocoa_intensity", name: "Cocoa Intensity", description: "The strength of chocolate/cocoa flavor.", mapping: { bitterness: 1.0 } },
        { key: "sweetness", name: "Sweetness", description: "The overall sweetness of the chocolate.", mapping: { sweetness: 1.0 } },
        { key: "meltability", name: "Meltability", description: "How smoothly the chocolate melts on the tongue.", mapping: { melt: 1.0 } },
        { key: "creaminess", name: "Creaminess", description: "The milky, creamy richness of the chocolate.", mapping: { snap: 0.3, melt: 0.4, flavor_balance: 0.3 } },
        { key: "snap_quality", name: "Snap Quality", description: "The clean break when you snap or bite the chocolate.", mapping: { snap: 1.0 } },
        { key: "flavor_balance", name: "Flavor Balance", description: "How well cocoa, milk, and sugar harmonize together.", mapping: { flavor_balance: 1.0 } },
      ]
    },
    {
      key: "dark_chocolate", name: "Dark Chocolate", icon: "🍫", description: "Intense dark chocolate with high cocoa content", attributes: [
        { key: "bitterness", name: "Bitterness", description: "The intensity of bitter taste from cocoa.", mapping: { bitterness: 1.0 } },
        { key: "sweetness", name: "Sweetness", description: "The counterbalancing sweetness level.", mapping: { sweetness: 1.0 } },
        { key: "meltability", name: "Meltability", description: "How smoothly the chocolate melts in your mouth.", mapping: { melt: 1.0 } },
        { key: "snap_quality", name: "Snap Quality", description: "The crisp, clean break when biting.", mapping: { snap: 1.0 } },
        { key: "aroma", name: "Aroma", description: "The depth and complexity of chocolate aroma.", mapping: { flavor_balance: 1.0 } },
        { key: "astringency", name: "Astringency", description: "The dry, puckering sensation from tannins in cocoa.", mapping: { bitterness: 0.6, flavor_balance: 0.4 } },
      ]
    },
    {
      key: "white_chocolate", name: "White Chocolate", icon: "🍬", description: "Sweet white chocolate made with cocoa butter", attributes: [
        { key: "sweetness", name: "Sweetness", description: "The dominant sweet flavor of white chocolate.", mapping: { sweetness: 1.0 } },
        { key: "creaminess", name: "Creaminess", description: "The buttery, milky cream character.", mapping: { flavor_balance: 1.0 } },
        { key: "meltability", name: "Meltability", description: "How well it melts — driven by cocoa butter content.", mapping: { melt: 1.0 } },
        { key: "vanilla_note", name: "Vanilla Note", description: "The vanilla flavoring intensity.", mapping: { bitterness: 0.3, flavor_balance: 0.7 } },
        { key: "snap_quality", name: "Snap Quality", description: "The firmness and clean break.", mapping: { snap: 1.0 } },
        { key: "richness", name: "Richness", description: "The overall fatty, indulgent mouthfeel.", mapping: { melt: 0.5, bitterness: 0.5 } },
      ]
    },
    {
      key: "gummy_candy", name: "Gummy Candy", icon: "🍬", description: "Gummies, jellies, and fruit-flavored soft candy", attributes: [
        { key: "sweetness", name: "Sweetness", description: "The dominant sweetness of the candy.", mapping: { sweetness: 1.0 } },
        { key: "chewiness", name: "Chewiness", description: "How chewy and elastic the candy texture is.", mapping: { snap: 1.0 } },
        { key: "fruitiness", name: "Fruitiness", description: "The intensity of fruit flavor.", mapping: { flavor_balance: 1.0 } },
        { key: "sourness", name: "Sourness", description: "The sour or tangy coating/flavor.", mapping: { bitterness: 1.0 } },
        { key: "softness", name: "Softness", description: "How soft and yielding the candy is.", mapping: { melt: 1.0 } },
        { key: "aroma", name: "Aroma", description: "The fruity, candy-like fragrance.", mapping: { flavor_balance: 0.5, sweetness: 0.5 } },
      ]
    },
    {
      key: "caramel", name: "Caramel", icon: "🍮", description: "Caramel candies, sauces, and toffees", attributes: [
        { key: "sweetness", name: "Sweetness", description: "The caramelized sugar sweetness level.", mapping: { sweetness: 1.0 } },
        { key: "butteriness", name: "Butteriness", description: "The rich buttery flavor character.", mapping: { melt: 1.0 } },
        { key: "chewiness", name: "Chewiness", description: "How chewy or soft the caramel texture is.", mapping: { snap: 1.0 } },
        { key: "toastiness", name: "Toastiness", description: "The depth of caramelization — nutty, toasty notes.", mapping: { bitterness: 1.0 } },
        { key: "smoothness", name: "Smoothness", description: "How smooth and non-grainy the texture is.", mapping: { melt: 0.5, flavor_balance: 0.5 } },
        { key: "flavor_balance", name: "Flavor Balance", description: "How well sweet, butter, and toasty notes harmonize.", mapping: { flavor_balance: 1.0 } },
      ]
    },
    {
      key: "cocoa_powder", name: "Cocoa Powder", icon: "☕", description: "Natural and Dutch-process cocoa powders", attributes: [
        { key: "bitterness", name: "Bitterness", description: "The natural bitter intensity of cocoa.", mapping: { bitterness: 1.0 } },
        { key: "cocoa_aroma", name: "Cocoa Aroma", description: "The strength of chocolate fragrance.", mapping: { flavor_balance: 1.0 } },
        { key: "sweetness", name: "Sweetness", description: "Any residual or added sweetness.", mapping: { sweetness: 1.0 } },
        { key: "colour_depth", name: "Colour Depth", description: "How deep and rich the brown color is.", mapping: { snap: 0.5, bitterness: 0.5 } },
        { key: "solubility", name: "Solubility", description: "How well the powder dissolves in liquid.", mapping: { melt: 1.0 } },
        { key: "astringency", name: "Astringency", description: "The dry, puckering sensation from polyphenols.", mapping: { snap: 0.4, flavor_balance: 0.6 } },
      ]
    },
  ],
  spices: [
    {
      key: "spice_blend", name: "Spice Blend", icon: "🫙", description: "Custom multi-spice blends and mixes", attributes: [
        { key: "pungency", name: "Pungency", description: "The heat and spicy kick from chili and pepper.", mapping: { pungency: 1.0 } },
        { key: "aroma", name: "Aroma", description: "The overall fragrance complexity of the blend.", mapping: { aroma: 1.0 } },
        { key: "colour", name: "Colour", description: "The visual color intensity of the blend.", mapping: { colour: 1.0 } },
        { key: "saltiness", name: "Saltiness", description: "The salt level in the blend.", mapping: { saltiness: 1.0 } },
        { key: "flavor_balance", name: "Flavor Balance", description: "How well all spice components work together.", mapping: { flavor_balance: 1.0 } },
        { key: "warmth", name: "Warmth", description: "The warm, lingering sensation from cumin and coriander.", mapping: { pungency: 0.4, aroma: 0.6 } },
      ]
    },
    {
      key: "curry_powder", name: "Curry Powder", icon: "🍛", description: "Traditional and regional curry powder blends", attributes: [
        { key: "pungency", name: "Pungency", description: "The chili heat level in the curry powder.", mapping: { pungency: 1.0 } },
        { key: "aroma", name: "Aroma", description: "The characteristic curry fragrance.", mapping: { aroma: 1.0 } },
        { key: "colour", name: "Colour", description: "The golden-yellow colour from turmeric.", mapping: { colour: 1.0 } },
        { key: "earthiness", name: "Earthiness", description: "The earthy, grounding flavor notes.", mapping: { flavor_balance: 1.0 } },
        { key: "saltiness", name: "Saltiness", description: "The salt content of the powder.", mapping: { saltiness: 1.0 } },
        { key: "complexity", name: "Complexity", description: "The layered depth of multiple spice notes.", mapping: { aroma: 0.5, flavor_balance: 0.5 } },
      ]
    },
    {
      key: "masala_mix", name: "Masala Mix", icon: "🌶️", description: "Garam masala, chaat masala, and specialty mixes", attributes: [
        { key: "pungency", name: "Pungency", description: "The spicy heat intensity.", mapping: { pungency: 1.0 } },
        { key: "aroma", name: "Aroma", description: "The aromatic intensity of the masala.", mapping: { aroma: 1.0 } },
        { key: "tanginess", name: "Tanginess", description: "The sour or tangy notes (from amchur, citric acid).", mapping: { saltiness: 0.5, flavor_balance: 0.5 } },
        { key: "colour", name: "Colour", description: "The visual appeal and colour richness.", mapping: { colour: 1.0 } },
        { key: "flavor_balance", name: "Flavor Balance", description: "How well sweet, sour, spicy, and salty notes harmonize.", mapping: { flavor_balance: 1.0 } },
        { key: "warmth", name: "Warmth", description: "The warm spice sensation from cinnamon, cloves, cardamom.", mapping: { pungency: 0.3, aroma: 0.7 } },
      ]
    },
    {
      key: "seasoning_powder", name: "Seasoning Powder", icon: "🧂", description: "Flavored seasoning powders for snacks and meals", attributes: [
        { key: "saltiness", name: "Saltiness", description: "The dominant salt flavor level.", mapping: { saltiness: 1.0 } },
        { key: "pungency", name: "Pungency", description: "Any chili or pepper heat.", mapping: { pungency: 1.0 } },
        { key: "umami", name: "Umami", description: "The savory, mouth-filling taste.", mapping: { flavor_balance: 1.0 } },
        { key: "aroma", name: "Aroma", description: "The fragrance when sprinkled on food.", mapping: { aroma: 1.0 } },
        { key: "colour", name: "Colour", description: "The visual colour of the seasoning.", mapping: { colour: 1.0 } },
        { key: "aftertaste", name: "Aftertaste", description: "The lingering taste after consumption.", mapping: { aroma: 0.4, flavor_balance: 0.6 } },
      ]
    },
    {
      key: "marinade_mix", name: "Marinade Mix", icon: "🥘", description: "Wet and dry marinades for meat and vegetables", attributes: [
        { key: "pungency", name: "Pungency", description: "The heat level of the marinade.", mapping: { pungency: 1.0 } },
        { key: "aroma", name: "Aroma", description: "The aromatic profile that develops during marination.", mapping: { aroma: 1.0 } },
        { key: "saltiness", name: "Saltiness", description: "The salt level for flavor penetration.", mapping: { saltiness: 1.0 } },
        { key: "colour", name: "Colour", description: "The colour imparted to the marinated food.", mapping: { colour: 1.0 } },
        { key: "flavor_balance", name: "Flavor Balance", description: "The harmony between spice, acid, and salt.", mapping: { flavor_balance: 1.0 } },
        { key: "penetration", name: "Penetration", description: "How deeply flavor absorbs into food.", mapping: { saltiness: 0.5, pungency: 0.5 } },
      ]
    },
    {
      key: "sauce_paste", name: "Sauce & Paste", icon: "🫕", description: "Cooking pastes, chutneys, and sauce bases", attributes: [
        { key: "pungency", name: "Pungency", description: "The spicy heat in the sauce or paste.", mapping: { pungency: 1.0 } },
        { key: "aroma", name: "Aroma", description: "The cooked or raw aromatic intensity.", mapping: { aroma: 1.0 } },
        { key: "thickness", name: "Thickness", description: "The viscosity and body of the paste/sauce.", mapping: { colour: 0.4, saltiness: 0.6 } },
        { key: "colour", name: "Colour", description: "The visual richness and appeal.", mapping: { colour: 1.0 } },
        { key: "flavor_balance", name: "Flavor Balance", description: "How well all flavor components come together.", mapping: { flavor_balance: 1.0 } },
        { key: "tanginess", name: "Tanginess", description: "The sour or acidic character of the sauce.", mapping: { saltiness: 0.4, flavor_balance: 0.6 } },
      ]
    },
  ],
  snacks: [
    {
      key: "potato_chips", name: "Potato Chips", icon: "🥔", description: "Classic fried and baked potato chips", attributes: [
        { key: "crunchiness", name: "Crunchiness", description: "How crisp and crunchy the chips feel during chewing.", mapping: { crunchiness: 1.0 } },
        { key: "saltiness", name: "Saltiness", description: "The perceived salt level on the chip surface.", mapping: { saltiness: 1.0 } },
        { key: "crispness", name: "Crispness", description: "The light, delicate cracking texture.", mapping: { crunchiness: 0.5, flavour: 0.5 } },
        { key: "oiliness", name: "Oiliness", description: "How greasy or oily the chip feels.", mapping: { oiliness: 1.0 } },
        { key: "flavor_strength", name: "Flavor Strength", description: "The intensity of the seasoning flavor.", mapping: { flavour: 1.0 } },
        { key: "aftertaste", name: "Aftertaste", description: "The lingering taste after eating.", mapping: { flavor_balance: 1.0 } },
      ]
    },
    {
      key: "extruded_snacks", name: "Extruded Snacks", icon: "🧀", description: "Puffed, extruded corn and rice snacks", attributes: [
        { key: "crunchiness", name: "Crunchiness", description: "The crunchy, airy bite of the puff.", mapping: { crunchiness: 1.0 } },
        { key: "puffiness", name: "Puffiness", description: "How light and airy the texture is.", mapping: { oiliness: 0.4, crunchiness: 0.6 } },
        { key: "saltiness", name: "Saltiness", description: "The salt level in the snack.", mapping: { saltiness: 1.0 } },
        { key: "flavor_strength", name: "Flavor Strength", description: "How strong the seasoning flavor is.", mapping: { flavour: 1.0 } },
        { key: "oiliness", name: "Oiliness", description: "The oil/fat perception.", mapping: { oiliness: 1.0 } },
        { key: "flavor_balance", name: "Flavor Balance", description: "How well all taste components work together.", mapping: { flavor_balance: 1.0 } },
      ]
    },
    {
      key: "popcorn", name: "Popcorn", icon: "🍿", description: "Butter, caramel, and seasoned popcorn", attributes: [
        { key: "crunchiness", name: "Crunchiness", description: "The crunch and pop of each kernel.", mapping: { crunchiness: 1.0 } },
        { key: "butteriness", name: "Butteriness", description: "The buttery flavor and aroma.", mapping: { oiliness: 1.0 } },
        { key: "saltiness", name: "Saltiness", description: "The salt level on the popcorn.", mapping: { saltiness: 1.0 } },
        { key: "flavor_strength", name: "Flavor Strength", description: "The intensity of added flavoring.", mapping: { flavour: 1.0 } },
        { key: "lightness", name: "Lightness", description: "How light and airy the popcorn feels.", mapping: { crunchiness: 0.6, flavor_balance: 0.4 } },
        { key: "flavor_balance", name: "Flavor Balance", description: "How well butter, salt, and seasoning harmonize.", mapping: { flavor_balance: 1.0 } },
      ]
    },
    {
      key: "crackers", name: "Crackers", icon: "🍪", description: "Savory crackers, rusks, and crispy flatbreads", attributes: [
        { key: "crunchiness", name: "Crunchiness", description: "The crisp, shattering bite.", mapping: { crunchiness: 1.0 } },
        { key: "saltiness", name: "Saltiness", description: "The surface salt level.", mapping: { saltiness: 1.0 } },
        { key: "toastiness", name: "Toastiness", description: "The baked, toasty grain flavor.", mapping: { flavour: 1.0 } },
        { key: "oiliness", name: "Oiliness", description: "The fat/oil content perception.", mapping: { oiliness: 1.0 } },
        { key: "dryness", name: "Dryness", description: "How dry and crisp vs. soft the cracker is.", mapping: { crunchiness: 0.5, oiliness: 0.5 } },
        { key: "flavor_balance", name: "Flavor Balance", description: "The overall harmony of grain, salt, and seasoning.", mapping: { flavor_balance: 1.0 } },
      ]
    },
    {
      key: "namkeen", name: "Namkeen", icon: "🥜", description: "Traditional Indian savory snacks — sev, mixture, bhujia", attributes: [
        { key: "crunchiness", name: "Crunchiness", description: "The crispy, crunchy texture.", mapping: { crunchiness: 1.0 } },
        { key: "spiciness", name: "Spiciness", description: "The chili heat and spice intensity.", mapping: { flavour: 1.0 } },
        { key: "saltiness", name: "Saltiness", description: "The salt level in the namkeen.", mapping: { saltiness: 1.0 } },
        { key: "oiliness", name: "Oiliness", description: "The frying oil perception.", mapping: { oiliness: 1.0 } },
        { key: "aroma", name: "Aroma", description: "The spiced, fried fragrance.", mapping: { flavour: 0.4, flavor_balance: 0.6 } },
        { key: "flavor_balance", name: "Flavor Balance", description: "How well salt, spice, and crunch come together.", mapping: { flavor_balance: 1.0 } },
      ]
    },
    {
      key: "instant_noodles_seasoning", name: "Instant Noodles Seasoning", icon: "🍜", description: "Seasoning packets for instant noodles and ramen", attributes: [
        { key: "umami", name: "Umami", description: "The savory, mouth-filling depth of flavor.", mapping: { flavour: 1.0 } },
        { key: "saltiness", name: "Saltiness", description: "The salt intensity in the seasoning.", mapping: { saltiness: 1.0 } },
        { key: "spiciness", name: "Spiciness", description: "The chili heat level.", mapping: { crunchiness: 0.3, oiliness: 0.7 } },
        { key: "aroma", name: "Aroma", description: "The appetizing fragrance when dissolved.", mapping: { flavor_balance: 1.0 } },
        { key: "richness", name: "Richness", description: "The fatty, brothy richness of the seasoning.", mapping: { oiliness: 1.0 } },
        { key: "flavor_balance", name: "Flavor Balance", description: "How well salt, spice, umami, and oil harmonize.", mapping: { flavor_balance: 0.5, flavour: 0.5 } },
      ]
    },
  ],
};

// Helper: inject subcategory data into categoryConfig after API fetch
function ensureSubcategories(config) {
  for (const cat of Object.keys(config)) {
    if (!config[cat].subcategories || config[cat].subcategories.length === 0) {
      config[cat].subcategories = SUBCATEGORY_DATA[cat] || [];
    }
    // Also ensure targets use flavor_balance instead of overall_liking
    if (config[cat].targets) {
      config[cat].targets = config[cat].targets.map(t =>
        t === "overall_liking" ? "flavor_balance" : t
      );
    }
  }
  return config;
}

// ── Connection state ─────────────────────────────────────────
const CONNECTION_MESSAGES = [
  "Preparing Formulation Engine…",
  "Connecting to Formulation Service…",
  "Waking up the server…",
  "Almost ready…",
];

const FORMULATION_MESSAGES = [
  "Generating Your Formulation…",
  "Running optimization models…",
  "Calculating ingredient ratios…",
  "Analyzing sensory targets…",
];

const MAX_RETRIES = 5;
const BASE_DELAY_MS = 2000;

function setConnectionStatus(msg) {
  const el = document.getElementById("connection-status-text");
  if (el) el.textContent = msg;
}

function showConnectionOverlay() {
  const overlay = document.getElementById("connection-overlay");
  if (overlay) overlay.classList.remove("hidden");
  const retryWrap = document.getElementById("connection-retry-wrap");
  if (retryWrap) retryWrap.classList.add("hidden");
}

function hideConnectionOverlay() {
  const overlay = document.getElementById("connection-overlay");
  if (overlay) {
    overlay.classList.add("fade-out");
    setTimeout(() => {
      overlay.classList.add("hidden");
      overlay.classList.remove("fade-out");
    }, 400);
  }
}

function showConnectionError() {
  const retryWrap = document.getElementById("connection-retry-wrap");
  if (retryWrap) retryWrap.classList.remove("hidden");
  setConnectionStatus("Could not reach the formulation service.");
}

// ── Rotating message helper ──────────────────────────────────
let messageInterval = null;

function startRotatingMessages(messages, setter) {
  stopRotatingMessages();
  let idx = 0;
  setter(messages[0]);
  messageInterval = setInterval(() => {
    idx = (idx + 1) % messages.length;
    setter(messages[idx]);
  }, 2500);
}

function stopRotatingMessages() {
  if (messageInterval) {
    clearInterval(messageInterval);
    messageInterval = null;
  }
}

// ── Init: fetch category config with retry ───────────────────
async function init() {
  const cached = sessionStorage.getItem("notestack_categories_v2");
  if (cached) {
    try {
      const parsed = JSON.parse(cached);
      if (parsed.ts && Date.now() - parsed.ts < 3600000) {
        categoryConfig = parsed.data;
        ensureSubcategories(categoryConfig);
        const overlay = document.getElementById("connection-overlay");
        if (overlay) overlay.classList.add("hidden");
        return;
      }
    } catch (_) { /* stale cache, re-fetch */ }
  }

  showConnectionOverlay();
  startRotatingMessages(CONNECTION_MESSAGES, setConnectionStatus);

  let attempt = 0;
  while (attempt < MAX_RETRIES) {
    try {
      const healthRes = await fetch(`${API_BASE}/`, { signal: AbortSignal.timeout(8000) });
      if (!healthRes.ok) throw new Error("Health check failed");

      setConnectionStatus("Loading product categories…");
      const res = await fetch(`${API_BASE}/categories`, { signal: AbortSignal.timeout(10000) });
      if (!res.ok) throw new Error("Categories fetch failed");
      categoryConfig = await res.json();
      ensureSubcategories(categoryConfig);

      sessionStorage.setItem("notestack_categories_v2", JSON.stringify({
        data: categoryConfig,
        ts: Date.now(),
      }));

      stopRotatingMessages();
      hideConnectionOverlay();
      return;
    } catch (e) {
      attempt++;
      if (attempt < MAX_RETRIES) {
        const delay = BASE_DELAY_MS * Math.pow(2, attempt - 1);
        setConnectionStatus(`Retrying connection… (attempt ${attempt + 1}/${MAX_RETRIES})`);
        await new Promise(r => setTimeout(r, delay));
      }
    }
  }

  stopRotatingMessages();
  showConnectionError();
}

// ── Screen navigation with history ───────────────────────────
function showScreen(id, pushHistory = true) {
  document.querySelectorAll(".screen").forEach(s => s.classList.remove("active"));
  document.getElementById(id).classList.add("active");
  window.scrollTo({ top: 0, behavior: "smooth" });

  if (pushHistory) {
    history.pushState({ screen: id }, "", `#${id.replace("screen-", "")}`);
  }
}

// Handle browser back/forward navigation
window.addEventListener("popstate", (e) => {
  if (suppressPopState) { suppressPopState = false; return; }

  if (e.state && e.state.screen) {
    showScreen(e.state.screen, false);
  } else {
    // Default to welcome screen
    showScreen("screen-welcome", false);
  }
});

// Set initial history state
history.replaceState({ screen: "screen-welcome" }, "", "#welcome");

// ── Welcome → Category ───────────────────────────────────────
document.getElementById("btn-start").addEventListener("click", () => {
  if (!categoryConfig) {
    init();
    return;
  }
  showScreen("screen-category");
});

document.getElementById("btn-back-welcome").addEventListener("click", () => {
  showScreen("screen-welcome");
});

// ── Retry button ─────────────────────────────────────────────
document.getElementById("btn-connection-retry").addEventListener("click", () => {
  init();
});

// ── Category → Subcategory ───────────────────────────────────
document.querySelectorAll(".cat-card").forEach(card => {
  card.addEventListener("click", () => {
    document.querySelectorAll(".cat-card").forEach(c => c.classList.remove("active"));
    card.classList.add("active");
    selectedCategory = card.dataset.cat;
    selectedSubcategory = null;
    selectedSubcatConfig = null;

    buildSubcategoryGrid(selectedCategory);
    document.getElementById("subcat-parent-label").textContent = capitalize(selectedCategory);
    showScreen("screen-subcategory");
  });
});

// ── Build subcategory grid ───────────────────────────────────
function buildSubcategoryGrid(category) {
  const container = document.getElementById("subcat-grid");
  container.innerHTML = "";

  const config = categoryConfig[category];
  if (!config || !config.subcategories) return;

  config.subcategories.forEach(sub => {
    const card = document.createElement("button");
    card.className = "subcat-card";
    card.dataset.subcat = sub.key;
    card.innerHTML = `
      <span class="subcat-icon">${sub.icon}</span>
      <div class="subcat-info">
        <span class="subcat-name">${sub.name}</span>
        <span class="subcat-desc">${sub.description}</span>
      </div>
    `;

    card.addEventListener("click", () => {
      document.querySelectorAll(".subcat-card").forEach(c => c.classList.remove("active"));
      card.classList.add("active");
      selectedSubcategory = sub.key;
      selectedSubcatConfig = sub;

      buildRatingButtons(sub);

      const labelText = `${capitalize(category)} · ${sub.name}`;
      document.getElementById("slider-cat-label").textContent = labelText;
      showScreen("screen-sliders");
    });

    container.appendChild(card);
  });
}

// ── Back from subcategory → category ─────────────────────────
document.getElementById("btn-back-category-from-sub").addEventListener("click", () => {
  showScreen("screen-category");
});

// ── Back from sliders → subcategory ──────────────────────────
document.getElementById("btn-back-category").addEventListener("click", () => {
  showScreen("screen-subcategory");
});

// ── Build button-based 0–10 ratings ──────────────────────────
function buildRatingButtons(subcatConfig) {
  const container = document.getElementById("sliders-grid");
  container.innerHTML = "";

  const attrs = subcatConfig.attributes;

  attrs.forEach((attr) => {
    const attrKey = attr.key;

    // Preserve previous selection if navigating back
    if (ratingValues[attrKey] === undefined) {
      ratingValues[attrKey] = 5;
    }

    const row = document.createElement("div");
    row.className = "rating-row";

    const currentVal = ratingValues[attrKey];

    let buttonsHTML = "";
    for (let v = 0; v <= 10; v++) {
      const activeClass = v === currentVal ? " active" : "";
      buttonsHTML += `<button type="button" class="rating-btn${activeClass}" data-attr="${attrKey}" data-val="${v}">${v}</button>`;
    }

    row.innerHTML = `
      <div class="rating-header">
        <div class="rating-info">
          <span class="rating-label">${attr.name}</span>
          <span class="rating-desc">${attr.description}</span>
        </div>
        <span class="rating-val" id="val-${attrKey}">${currentVal}</span>
      </div>
      <div class="rating-btn-group">
        ${buttonsHTML}
      </div>
    `;

    // Attach click handlers to buttons
    row.querySelectorAll(".rating-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const val = parseInt(btn.dataset.val);
        ratingValues[attrKey] = val;

        // Update display
        document.getElementById(`val-${attrKey}`).textContent = val;

        // Update active state
        row.querySelectorAll(".rating-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
      });
    });

    container.appendChild(row);
  });
}

// ── Loading overlay helpers ──────────────────────────────────
function showLoading() {
  const overlay = document.getElementById("loading");
  overlay.classList.remove("hidden");
  startRotatingMessages(FORMULATION_MESSAGES, (msg) => {
    document.getElementById("loading-text").textContent = msg;
  });
}

function hideLoading() {
  stopRotatingMessages();
  document.getElementById("loading").classList.add("hidden");
}

// ── Sliders → Results ────────────────────────────────────────
document.getElementById("btn-formulate").addEventListener("click", async () => {
  if (!selectedCategory || !selectedSubcategory || !selectedSubcatConfig) return;

  const attrs = selectedSubcatConfig.attributes;
  const scores = attrs.map(attr => ratingValues[attr.key] !== undefined ? ratingValues[attr.key] : 5);

  showLoading();

  try {
    const res = await fetch(`${API_BASE}/formulate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        category: selectedCategory,
        subcategory: selectedSubcategory,
        target_scores: scores,
      }),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || "Request failed");

    lastFormulationResult = data;

    displayResults(data, scores);
    showScreen("screen-results");
  } catch (err) {
    const toast = document.getElementById("error-toast");
    document.getElementById("error-msg").textContent = "Could not reach NoteStack API. Please try again.";
    toast.classList.remove("hidden");
    setTimeout(() => toast.classList.add("hidden"), 4000);
  } finally {
    hideLoading();
  }
});

document.getElementById("btn-back-sliders").addEventListener("click", () => {
  showScreen("screen-sliders");
});

// ── Display results ──────────────────────────────────────────
function displayResults(data, scores) {
  const subcatName = selectedSubcatConfig ? selectedSubcatConfig.name : capitalize(data.category);
  document.getElementById("result-cat-label").textContent = `${capitalize(data.category)} · ${subcatName}`;

  // Formulation table
  const tbody = document.getElementById("formulation-body");
  tbody.innerHTML = "";
  Object.entries(data.formulation).forEach(([k, v]) => {
    const tr = document.createElement("tr");
    const label = k.replace(/_pct$/, " %").replace(/_/g, " ")
      .replace(/\b\w/g, c => c.toUpperCase());
    tr.innerHTML = `<td>${label}</td><td>${v}%</td>`;
    tbody.appendChild(tr);
  });

  // Confidence card
  const conf = data.confidence_pct;
  const confColor = conf >= 85 ? "var(--success)" : conf >= 65 ? "#b07d10" : "var(--danger)";
  const confMsg = conf >= 85
    ? "High confidence — this target is achievable with the suggested formulation."
    : conf >= 65
      ? "Moderate confidence — closest achievable formulation given the targets."
      : "Low confidence — some targets may be outside the achievable range.";

  document.getElementById("confidence-card").innerHTML = `
    <span style="font-size:13px;font-weight:600;color:${confColor}">Confidence: ${conf}%</span>
    &nbsp;<span style="font-size:11px;color:var(--ink-muted)">· Residual error: ${data.residual_error}</span>
    <p style="margin-top:6px;font-size:11px;color:var(--ink-muted);line-height:1.5">${confMsg}</p>
  `;

  // Compliance
  const c = data.compliance;
  const statusClass = c.status === "COMPLIANT" ? "status-compliant"
    : c.status === "ADVISORY" ? "status-advisory"
      : "status-noncompliant";
  let compHTML = `<span class="compliance-status ${statusClass}">${c.status}</span>`;
  c.passed.forEach(p => compHTML += complianceItem("pass", p));
  c.warnings.forEach(w => compHTML += complianceItem("warn", w));
  c.flags.forEach(f => compHTML += complianceItem("fail", f));
  document.getElementById("compliance-box").innerHTML = compHTML;

  // Score breakdown cards with descriptions
  const scoreGrid = document.getElementById("score-cards-grid");
  scoreGrid.innerHTML = "";
  const predScores = data.predicted_scores;
  const targScores = data.target_scores;
  const scoreKeys = Object.keys(predScores);

  // Build a descriptions lookup from subcategory config
  const attrDescriptions = {};
  if (selectedSubcatConfig && selectedSubcatConfig.attributes) {
    selectedSubcatConfig.attributes.forEach(attr => {
      attrDescriptions[attr.key] = attr.description;
    });
  }

  scoreKeys.forEach((key, idx) => {
    const pred = predScores[key];
    const targ = targScores[key];
    const pct = Math.round((pred / 10) * 100);
    const isLast = idx === scoreKeys.length - 1;
    const isOdd = scoreKeys.length % 2 !== 0;
    const card = document.createElement("div");
    card.className = "score-card" + (isLast && isOdd ? " full-width" : "");

    const desc = attrDescriptions[key] || "";
    const descHTML = desc ? `<div class="score-card-desc">${desc}</div>` : "";

    card.innerHTML = `
      <div class="score-card-label">${key.replace(/_/g, " ")}</div>
      ${descHTML}
      <div class="score-card-vals">
        <span class="score-predicted">${pred}</span>
        <span class="score-target">target ${targ}</span>
      </div>
      <div class="score-bar-track">
        <div class="score-bar-fill" style="width:${pct}%"></div>
      </div>
    `;
    scoreGrid.appendChild(card);
  });

  // Radar chart
  const labels = Object.keys(predScores).map(k => k.replace(/_/g, " "));
  const predVals = Object.values(predScores);
  const targVals = Object.values(targScores);

  if (radarChart) radarChart.destroy();
  const ctx = document.getElementById("radar-chart").getContext("2d");
  radarChart = new Chart(ctx, {
    type: "radar",
    data: {
      labels,
      datasets: [
        {
          label: "Target",
          data: targVals,
          borderColor: "rgba(139,69,19,0.7)",
          backgroundColor: "rgba(139,69,19,0.08)",
          pointBackgroundColor: "rgba(139,69,19,0.9)",
          pointRadius: 4,
        },
        {
          label: "Predicted",
          data: predVals,
          borderColor: "rgba(201,168,108,0.85)",
          backgroundColor: "rgba(201,168,108,0.1)",
          pointBackgroundColor: "rgba(201,168,108,1)",
          pointRadius: 4,
        },
      ],
    },
    options: {
      scales: {
        r: {
          min: 0, max: 10,
          ticks: {
            color: "#9b8b72",
            backdropColor: "transparent",
            stepSize: 2,
            font: { size: 10 }
          },
          grid: { color: "rgba(221,213,191,0.7)" },
          angleLines: { color: "rgba(221,213,191,0.5)" },
          pointLabels: { color: "#3d3326", font: { size: 11, family: "'Inter', sans-serif" } },
        },
      },
      plugins: {
        legend: {
          labels: {
            color: "#6b5c48",
            font: { size: 11, family: "'Inter', sans-serif" },
            boxWidth: 12,
          }
        },
      },
    },
  });

  // PDF download button
  document.getElementById("btn-download-pdf").onclick = async () => {
    const btn = document.getElementById("btn-download-pdf");
    btn.textContent = "Generating PDF…";
    btn.disabled = true;
    try {
      let res;
      if (lastFormulationResult) {
        res = await fetch(`${API_BASE}/report-from-result`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(lastFormulationResult),
        });
      }

      if (!res || !res.ok) {
        res = await fetch(`${API_BASE}/report`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            category: data.category,
            subcategory: data.subcategory,
            target_scores: scores,
          }),
        });
      }

      if (!res.ok) throw new Error("Failed to generate report");
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const sub_label = data.subcategory ? `_${data.subcategory}` : "";
      const filename = `notestack_${data.category}${sub_label}_report.pdf`;

      const a = document.createElement("a");
      a.href = url;
      a.download = filename;
      a.click();

      showDownloadToast(filename, url);
    } catch (e) {
      alert("Could not generate PDF. Please try again.");
    } finally {
      btn.textContent = "Download PDF report";
      btn.disabled = false;
    }
  };
}

function complianceItem(type, text) {
  const dotClass = type === "pass" ? "dot-pass" : type === "warn" ? "dot-warn" : "dot-fail";
  return `<div class="compliance-item">
    <span class="dot ${dotClass}"></span>
    <span>${text}</span>
  </div>`;
}

// ── Download success toast ──────────────────────────────────
let downloadToastTimer = null;

function showDownloadToast(filename, blobUrl) {
  const toast = document.getElementById("download-toast");
  const sub = document.getElementById("download-toast-sub");
  const openBtn = document.getElementById("download-toast-open");
  const closeBtn = document.getElementById("download-toast-close");

  sub.textContent = filename;
  toast.classList.remove("hidden");

  toast.classList.remove("show");
  void toast.offsetWidth;
  requestAnimationFrame(() => toast.classList.add("show"));

  openBtn.onclick = () => window.open(blobUrl, "_blank");
  closeBtn.onclick = () => hideDownloadToast();

  if (downloadToastTimer) clearTimeout(downloadToastTimer);
  downloadToastTimer = setTimeout(hideDownloadToast, 6000);
}

function hideDownloadToast() {
  const toast = document.getElementById("download-toast");
  toast.classList.remove("show");
  setTimeout(() => toast.classList.add("hidden"), 300);
}

// ── Reset ────────────────────────────────────────────────────
document.getElementById("btn-reset").addEventListener("click", () => {
  document.querySelectorAll(".cat-card").forEach(c => c.classList.remove("active"));
  selectedCategory = null;
  selectedSubcategory = null;
  selectedSubcatConfig = null;
  lastFormulationResult = null;
  ratingValues = {};
  showScreen("screen-welcome");
});

// ── Helpers ──────────────────────────────────────────────────
function capitalize(str) {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

// ── Start ────────────────────────────────────────────────────
init();