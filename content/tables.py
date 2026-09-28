"""Reference tables: oven temperatures, pan sizes, volume measures, general units.

Everything here is either a defined constant (an inch is 2.54 cm exactly; a US cup is
236.5882365 ml) or a conventional kitchen mapping (gas mark 4 = 180 C). Figures that are
conventions rather than definitions are labelled as such in the generated pages.
"""

# ---------------------------------------------------------------- oven temperatures
# (celsius, gas mark, fahrenheit, what it is used for). Fan temperatures are celsius - 20,
# which is the usual rule of thumb; oven thermostats are far less accurate than this.
OVEN = [
    (110, "1/4", 225, "Drying, meringues, slow-roasting meat"),
    (120, "1/2", 250, "Meringues, drying, yoghurt-making"),
    (130, "1", 265, "Very slow roasting, custards (some cookers label this gas 1)"),
    (140, "1", 275, "Slow roasting, meringues, rich fruit cake"),
    (150, "2", 300, "Delicate bakes, meringues, shortbread"),
    (160, "3", 325, "Biscuits, scones, sponge fingers"),
    (170, "3", 340, "Fruit cakes and bakes needing slow, even heat"),
    (180, "4", 350, "The workhorse: cakes, muffins, sponges (the most common setting in "
                    "British recipes)"),
    (190, "5", 375, "Cookies, traybakes, choux pastry"),
    (200, "6", 400, "Bread, pastry, roasting vegetables"),
    (210, "6", 410, "Scones, bread rolls, quick roasting"),
    (220, "7", 425, "Pizza, roast potatoes, crisp pastry"),
    (230, "8", 450, "High-heat pizza, hot roasting, browning"),
    (240, "9", 475, "Naan, blistering pizza, very high heat"),
    (250, "9", 480, "Above most domestic ovens' useful range; check the manual"),
]

# ---------------------------------------------------------------- pans
# Standard round pans. Areas and volumes are computed from the diameter, so they are
# geometry rather than guesswork; the "fills" figure notes how much batter a pan of that
# size typically takes at 2 inches / 5 cm deep.
PAN_DIAMETERS_IN = [6, 7, 8, 9, 10, 11]

PAN_NOTES = {
    6: "Two 6 in tins make a small layer cake; the same batter makes about 12 cupcakes.",
    7: "A 7 in tin is the British standard for a single-tier sponge and takes one batch of "
       "a classic 4-egg cake mixture.",
    8: "The most common American layer cake size, and the one most US recipes assume.",
    9: "A 9 in round tin holds about the same area as an 8 in square, which is why the two "
       "are the usual substitution pair.",
    10: "A 10 in tin needs roughly 1.5x a 8 in recipe. Reduce the oven by 10 C and add "
        "ten minutes.",
    11: "Large celebration tins: expect a longer, slower bake, not just a bigger one.",
}

# ---------------------------------------------------------------- volume measures
# Millilitres. The US figures are definitions; the UK ones reflect what is sold.
VOLUME_MEASURES = [
    ("US teaspoon", 4.92892159, "1/6 US fluid ounce — the base US cooking measure"),
    ("US tablespoon", 14.7867648, "3 US teaspoons"),
    ("US fluid ounce", 29.5735296, "2 US tablespoons — a volume, not a weight"),
    ("US cup", 236.5882365, "16 US tablespoons; the US customary cup, 8 US fluid ounces"),
    ("US pint", 473.176473, "2 US cups"),
    ("US quart", 946.352946, "4 US cups"),
    ("US gallon", 3785.411784, "16 US cups"),
    ("Metric cup (AU/NZ/CA)", 250.0, "A round 250 ml cup — 5.6% larger than the US cup"),
    ("UK/imperial cup", 284.130625, "10 imperial fluid ounces; obsolete in recipes but still "
                                    "found in older British books"),
    ("UK tablespoon", 15.0, "Modern UK and EU tablespoon"),
    ("Australian tablespoon", 20.0, "Four teaspoons, not three — a real source of error in "
                                    "Australian recipes"),
    ("Imperial fluid ounce", 28.4130625, "UK fluid ounce; 4% smaller than the US one"),
    ("UK pint", 568.26125, "20 imperial fluid ounces — 20% larger than a US pint"),
    ("UK gallon", 4546.09, "Defined as 4.54609 litres since 1985"),
]

# ---------------------------------------------------------------- general units
# Base units: metre, kilogram, litre, degree Celsius.
UNIT_SYSTEMS = {
    "length": {
        "base": "metre",
        "units": {
            "millimetres (mm)": 0.001,
            "centimetres (cm)": 0.01,
            "metres (m)": 1.0,
            "kilometres (km)": 1000.0,
            "inches (in)": 0.0254,
            "feet (ft)": 0.3048,
            "yards (yd)": 0.9144,
            "miles (mi)": 1609.344,
        },
    },
    "mass": {
        "base": "kilogram",
        "units": {
            "milligrams (mg)": 1e-06,
            "grams (g)": 0.001,
            "kilograms (kg)": 1.0,
            "ounces (oz)": 0.028349523125,
            "pounds (lb)": 0.45359237,
            "stone (st)": 6.35029318,
            "tonnes (t)": 1000.0,
        },
    },
    "volume": {
        "base": "litre",
        "units": {
            "millilitres (ml)": 0.001,
            "litres (l)": 1.0,
            "US cups": 0.2365882365,
            "US fluid ounces": 0.0295735296,
            "US pints": 0.473176473,
            "US gallons": 3.785411784,
            "UK pints": 0.56826125,
            "UK gallons": 4.54609,
        },
    },
}

# Individual converter pages: (slug, from, to, category, why-this-query-matters)
GENERAL_CONVERSIONS = [
    ("cm-to-inches", "centimetres (cm)", "inches (in)", "length",
     "One inch is exactly 2.54 cm, fixed by the international yard and pound agreement of "
     "1959. The conversion is a definition, not a measurement, so any rounding you see is "
     "only in the display."),
    ("inches-to-cm", "inches (in)", "centimetres (cm)", "length",
     "Multiply by 2.54 exactly. This is the conversion behind every clothing size chart, "
     "screen diagonal and timber measurement that crosses the Atlantic."),
    ("mm-to-inches", "millimetres (mm)", "inches (in)", "length",
     "Millimetres are the unit of engineering drawings and drill bits; inches are the unit of "
     "hardware sold in the UK and US. 25.4 mm to the inch, exactly."),
    ("m-to-feet", "metres (m)", "feet (ft)", "length",
     "A metre is 3.28084 feet. The metre was originally defined as one ten-millionth of the "
     "distance from the equator to the north pole; the foot has been 0.3048 m since 1959."),
    ("km-to-miles", "kilometres (km)", "miles (mi)", "length",
     "A mile is 1.609344 km exactly. A useful approximation: multiply by 8 and divide by 5."),
    ("miles-to-km", "miles (mi)", "kilometres (km)", "length",
     "Multiply by 1.609344. The Roman mile was a thousand paces; the modern one has been tied "
     "to the metre since 1959."),
    ("kg-to-pounds", "kilograms (kg)", "pounds (lb)", "mass",
     "One pound is 0.45359237 kg exactly, so a kilogram is about 2.2046 lb."),
    ("pounds-to-kg", "pounds (lb)", "kilograms (kg)", "mass",
     "Multiply by 0.45359237. The avoirdupois pound has 16 ounces and has been defined "
     "against the kilogram since 1959."),
    ("grams-to-ounces", "grams (g)", "ounces (oz)", "mass",
     "An ounce is 28.349523125 g. Useful in the kitchen and at the post office, where both "
     "systems are still in daily use."),
    ("stone-to-kg", "stone (st)", "kilograms (kg)", "mass",
     "A stone is 14 pounds, so 6.35029318 kg. Body weight in Britain is still mostly quoted "
     "in stones and pounds."),
    ("ml-to-cups", "millilitres (ml)", "US cups", "volume",
     "A US cup is 236.5882365 ml, while a metric cup is 250 ml — a 5.6% difference that "
     "matters in baking and not much anywhere else."),
    ("cups-to-ml", "US cups", "millilitres (ml)", "volume",
     "One US cup is 236.588 ml; one metric cup is 250 ml. British recipes using 'a cup' "
     "usually mean the metric measure these days."),
    ("litres-to-us-pints", "litres (l)", "US pints", "volume",
     "A US pint is 473.176 ml, so a litre is about 2.11 US pints. The British pint is 20% "
     "larger at 568 ml."),
]
