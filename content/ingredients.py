"""Ingredient weights.

Per-cup gram figures are taken from King Arthur Baking's ingredient weight chart
(kingarthurbaking.com/learn/ingredient-weight-chart), which measures a US customary cup
(236.588 ml) of the ingredient as it is normally spooned and levelled. Where a figure is
derived from their per-tablespoon or per-half-cup value it is noted in the comment.

These are typical figures for that measuring convention, not properties of the substance:
the same flour can weigh 100 g or 155 g in the same cup depending on how it was filled.
"""

# slug, name, grams per US cup, category, note (why it varies), tip (how to measure)
INGREDIENTS = [
    # ---------- flours and starches ----------
    dict(slug="all-purpose-flour", name="All-purpose flour", short="plain flour",
         g=120, cat="flours",
         note="King Arthur's chart lists 120 g for a cup of all-purpose flour, and that is "
              "the number to use when a recipe was written by weight. The same cup scooped "
              "straight from the bag can weigh over 150 g, which is the single most common "
              "reason a cake comes out dry and crumbly.",
         tip="Fluff the flour with a spoon, sprinkle it into the cup and level it with a "
             "knife — never pack it by tapping. If you own scales, weigh: for flour it makes "
             "a bigger difference than any other change you can make."),
    dict(slug="bread-flour", name="Bread flour", short="strong flour / bread flour",
         g=120, cat="flours",
         note="Higher in protein than all-purpose, and roughly the same weight per cup — "
              "120 g on King Arthur's chart. The extra gluten is what gives bread its chew, "
              "so substituting plain flour loses structure rather than accuracy.",
         tip="Bread flour absorbs more water than all-purpose, so a dough may feel stiff for "
             "the first minute. Give it ten minutes before adding liquid."),
    dict(slug="cake-flour", name="Cake flour", short="cake flour",
         g=120, cat="flours",
         note="Milled very finely and low in protein, cake flour makes a tender crumb but it "
              "is also the flour most often mis-measured: sifted, a cup can weigh under "
              "100 g. King Arthur list 120 g per cup for their unbleached cake flour.",
         tip="Cake flour is usually sifted before measuring, which changes the weight "
             "considerably. If a recipe gives grams, trust them over the cup."),
    dict(slug="self-rising-flour", name="Self-rising flour", short="self-raising flour",
         g=113, cat="flours",
         note="Flour with baking powder and salt already blended in — about 113 g per cup on "
              "King Arthur's chart. It is a British staple, and it is why British recipes so "
              "often omit baking powder.",
         tip="Never add baking powder to a recipe that calls for self-rising flour, and do "
             "not use it as a direct substitute for plain flour unless you adjust the raising "
             "agents."),
    dict(slug="whole-wheat-flour", name="Whole wheat flour", short="wholemeal flour",
         g=113, cat="flours",
         note="Contains the bran and germ, so it is slightly lighter per cup than white flour "
              "(113 g on King Arthur's chart) but absorbs far more water. Recipes often need "
              "extra liquid or a rest before baking.",
         tip="Wholemeal flour goes rancid faster than white because of the germ. Keep it in "
             "the freezer if you bake occasionally."),
    dict(slug="pastry-flour", name="Pastry flour", short="pastry flour",
         g=106, cat="flours",
         note="Lower in protein than all-purpose and a little lighter per cup — 106 g on "
              "King Arthur's chart. It sits between all-purpose and cake flour, and is what "
              "makes pastry and biscuits short rather than chewy.",
         tip="If a recipe calls for pastry flour and you only have all-purpose, use 85% "
             "all-purpose and 15% cornstarch by weight."),
    dict(slug="oat-flour", name="Oat flour", short="oat flour",
         g=92, cat="flours",
         note="Ground oats, and noticeably lighter per cup than wheat flour — 92 g on King "
              "Arthur's chart. It is gluten-free only if milled from certified gluten-free "
              "oats, and it makes bakes dense and moist.",
         tip="Oat flour needs a binder in gluten-free baking: about a quarter teaspoon of "
             "xanthan gum per 120 g."),
    dict(slug="rice-flour", name="White rice flour", short="rice flour",
         g=142, cat="flours",
         note="Heavy and gritty compared with wheat flour — 142 g per cup on King Arthur's "
              "chart, one of the densest in the chart. It is naturally gluten-free and "
              "behaves very differently: no gluten means no stretch.",
         tip="Rice flour makes batters crisp and is excellent for shortbread and tempura, but "
             "poor for bread unless blended with other flours."),
    dict(slug="almond-flour", name="Almond flour / almond meal", short="ground almonds",
         g=84, cat="flours",
         note="Ground almonds weigh about 84 g per cup. Almond flour (blanched, finely "
              "ground) and almond meal (with skins, coarser) behave differently even at the "
              "same weight, so follow whichever the recipe names.",
         tip="Almond flour has no gluten at all, so it needs eggs for structure. It also "
             "burns quickly — drop the oven by 15 °C if the top colours too fast."),
    dict(slug="gluten-free-flour-blend", name="Gluten-free all-purpose baking mix",
         short="GF blend",
         g=120, cat="flours",
         note="Commercial gluten-free blends weigh about 120 g per cup on King Arthur's "
              "chart, close to wheat flour. Bean-flour blends are heavier and thirstier than "
              "rice-starch blends.",
         tip="Blends vary hugely between brands, so cups and grams disagree more than usual. "
             "Weigh if the recipe gives weight."),
    dict(slug="cornstarch", name="Cornstarch", short="cornflour",
         g=112, cat="flours",
         note="King Arthur list 28 g for a quarter cup, which is 112 g per cup. In the UK "
              "the same white powder is sold as cornflour, which confuses it with maize "
              "flour — a yellow wholemeal product that behaves quite differently.",
         tip="One tablespoon of cornstarch thickens about a cup of liquid. Mix it with cold "
             "water first: tipped straight into hot liquid it sets into lumps."),
    # ---------- sugars and syrups ----------
    dict(slug="granulated-sugar", name="Granulated white sugar", short="granulated sugar",
         g=198, cat="sugars",
         note="198 g per cup on King Arthur's chart — remarkably consistent, because sugar "
              "does not compact the way flour does. If a recipe was written in cups, sugar "
              "is the ingredient where cups and grams agree most closely.",
         tip="Sugar is hygroscopic and hardens with age. A slice of apple in the jar, or "
             "thirty seconds in the microwave, softens a brick."),
    dict(slug="brown-sugar", name="Brown sugar (packed)", short="light or dark brown sugar",
         g=213, cat="sugars",
         note="Brown sugar must be packed into the cup, which is why it weighs more than "
              "granulated: 213 g per packed cup on King Arthur's chart. Loose, it can weigh "
              "half that, so an unpacked cup quietly under-sweetens a recipe.",
         tip="Press it down with the back of a spoon until it holds the shape of the cup. "
             "Dark and light can be swapped one for one; dark simply carries more molasses."),
    dict(slug="confectioners-sugar", name="Confectioners' sugar", short="icing sugar",
         g=113, cat="sugars",
         note="Unsifted confectioners' sugar is 113 g per cup on King Arthur's chart — "
              "dramatically lighter than granulated because of the cornstarch and the air. "
              "Sifted, it drops further.",
         tip="Always sift before icing or dusting, both to break lumps and to measure "
             "consistently."),
    dict(slug="honey", name="Honey", short="honey",
         g=336, cat="sugars",
         note="Honey is denser than water: King Arthur give 21 g for a tablespoon, which is "
              "336 g per cup. Measuring honey in a cup is genuinely difficult — a great deal "
              "clings to the sides.",
         tip="Oil or spray the measuring cup, or measure honey in the same cup as the oil in "
             "the recipe. It also burns faster than sugar, so drop the oven by about 15 °C when "
             "substituting it."),
    dict(slug="maple-syrup", name="Maple syrup", short="maple syrup",
         g=312, cat="sugars",
         note="About 312 g per cup, from King Arthur's figure of 156 g for a half cup. Grade "
              "A / golden is milder; the darker grades taste stronger and are better for "
              "baking than for pouring.",
         tip="Replace honey with maple syrup one for one by volume, but expect a thinner "
             "batter and add a tablespoon or two of extra flour."),
    dict(slug="agave-syrup", name="Agave syrup", short="agave",
         g=336, cat="sugars",
         note="King Arthur give 84 g for a quarter cup, so a cup is about 336 g — the same "
              "as honey and noticeably heavier than maple syrup.",
         tip="Agave is sweeter than sugar, so use about three quarters of the volume the "
             "recipe calls for, and reduce other liquids slightly."),
    dict(slug="sweetened-condensed-milk", name="Sweetened condensed milk", short="condensed milk",
         g=312, cat="sugars",
         note="King Arthur list 78 g for a quarter cup, which is 312 g per cup. It is roughly "
              "40% sugar, which is why it keeps almost indefinitely in the tin.",
         tip="Do not substitute evaporated milk: it has no added sugar and behaves completely "
             "differently in fudge, caramel and cheesecake."),
    # ---------- fats, dairy and liquids ----------
    dict(slug="butter", name="Butter", short="butter",
         g=226, cat="dairy",
         note="King Arthur list 113 g for eight tablespoons, which is half a cup — so a cup "
              "of butter is 226 g, close to the density of water. An American stick is 113 g; "
              "a European block is 250 g with the fat percentage printed on the wrapper.",
         tip="Weighing butter matters more than measuring it: a cup of softened butter can be "
             "20% out. Cup measurements for butter are the least reliable in baking."),
    dict(slug="vegetable-oil", name="Vegetable oil", short="oil",
         g=198, cat="dairy",
         note="198 g per cup on King Arthur's chart — lighter than water, and about 12% "
              "lighter than butter. Swapping oil for butter by volume therefore adds fat, and "
              "swapping the other way removes it.",
         tip="For cake, replace butter with oil at about 80% of the volume and expect a "
             "moister crumb and less rise."),
    dict(slug="sour-cream", name="Sour cream", short="sour cream",
         g=227, cat="dairy",
         note="227 g per cup on King Arthur's chart, essentially the weight of water. Full-fat "
              "and reduced-fat weigh the same but split differently when heated.",
         tip="Keep the pan below a simmer or reduced-fat sour cream curdles. Bring it to room "
             "temperature first."),
    dict(slug="yogurt", name="Yogurt", short="plain yogurt",
         g=227, cat="dairy",
         note="Plain yogurt weighs 227 g per cup. Greek-style yogurt is strained, so it is "
              "thicker and marginally denser — for baking the difference is small, but in a "
              "sauce it changes the texture noticeably.",
         tip="Yogurt substitutes for sour cream one for one in baking, and for buttermilk when "
             "thinned with a little milk."),
    dict(slug="buttermilk", name="Buttermilk", short="buttermilk",
         g=227, cat="dairy",
         note="227 g per cup — the same as milk, since buttermilk is milk with the fat partly "
              "removed and acid added. Its acidity is the point: it reacts with baking soda to "
              "make soda bread and pancakes rise.",
         tip="No buttermilk? Stir a tablespoon of lemon juice or vinegar into a cup of milk and "
             "leave it ten minutes. The acidity, not the flavour, is what the recipe needs."),
    dict(slug="cream-cheese", name="Cream cheese", short="cream cheese",
         g=227, cat="dairy",
         note="227 g per cup on King Arthur's chart, and a standard American block is exactly "
              "that. British and European cream cheese is often sold in 200 g tubs and is "
              "softer, so a 'cup' is a poor guide.",
         tip="Use full-fat for cheesecake; the low-fat versions are stabilised differently and "
             "grain when baked."),
    dict(slug="water", name="Water", short="water",
         g=227, cat="dairy",
         note="227 g per cup by King Arthur's convention, though a US customary cup holds "
              "236.588 ml and water is almost exactly 1 g/ml at room temperature. The chart's "
              "figure is rounded for kitchen use.",
         tip="Use the 236 ml figure when converting between cups and millilitres for liquids, "
             "and 227 g for water by weight — the two conventions differ by about 4%."),
    # ---------- spreads, grains and other solids ----------
    dict(slug="peanut-butter", name="Peanut butter", short="peanut butter",
         g=270, cat="other",
         note="King Arthur list 135 g for a half cup, so a cup is about 270 g. Natural peanut "
              "butter that separates is easier to measure by weight than by cup, and the oil "
              "must be stirred back in first.",
         tip="For baking, use a conventional smooth peanut butter rather than a natural one: "
             "the latter makes cookies greasy and crumbly."),
    dict(slug="rolled-oats", name="Rolled oats", short="oats",
         g=89, cat="other",
         note="Old-fashioned and quick-cooking oats both weigh about 89 g per cup on King "
              "Arthur's chart; their own thicker rolled oats weigh 113 g. The difference is "
              "the flake, so the same cup can be 25% heavier.",
         tip="Oats are the easiest ingredient to weigh and the hardest to measure by volume. "
             "If you are making flapjacks, use grams."),
    dict(slug="cornmeal", name="Cornmeal (whole)", short="cornmeal",
         g=138, cat="other",
         note="Whole cornmeal is 138 g per cup; the finer, degerminated yellow cornmeal many "
              "US brands sell is heavier still at 156 g. Polenta, cornmeal and maize flour all "
              "differ in grind.",
         tip="Coarse polenta needs a long simmer and absorbs about four times its volume in "
             "water; fine cornmeal sets much faster."),
    dict(slug="chocolate-chips", name="Chocolate chips", short="chocolate chips",
         g=170, cat="other",
         note="170 g per cup on King Arthur's chart, whatever the cocoa percentage — the chips "
              "stack with air between them. Chopped chocolate from a bar is around the same "
              "weight but melts differently.",
         tip="Chips hold their shape because they contain less cocoa butter; a bar chopped by "
             "hand will pool and marble through a cake instead."),
    dict(slug="shredded-coconut", name="Unsweetened shredded coconut", short="desiccated coconut",
         g=53, cat="other",
         note="Only 53 g per cup on King Arthur's chart — the lightest ingredient here, because "
              "shreds trap a great deal of air. Sweetened and desiccated coconut weigh "
              "differently again, so check which one the recipe means.",
         tip="Toasting takes six to eight minutes at 160 °C, and it will go from pale to burnt "
             "in under a minute. Stay with the tray."),
    dict(slug="walnuts", name="Walnuts (chopped)", short="walnuts",
         g=113, cat="other",
         note="Chopped walnuts are 113 g per cup; whole halves weigh much less per cup because "
              "of the gaps. Toasting first deepens the flavour and removes some bitterness.",
         tip="Toast nuts at 160 °C for eight to ten minutes and cool them completely before "
             "folding into a batter."),
    dict(slug="pecans", name="Pecans (whole)", short="pecans",
         g=105, cat="other",
         note="Whole pecan halves are 105 g per cup. Chopped they pack down to roughly 120 g, "
              "so the same volume of the same nut goes two ways depending on the knife.",
         tip="Pecans freeze well for a year, which is the cheapest way to buy them."),
    dict(slug="mashed-banana", name="Mashed banana", short="mashed banana",
         g=227, cat="other",
         note="A cup of mashed banana is about 227 g, or two to three medium bananas. The "
              "weight varies with ripeness: a very ripe banana holds more water and mashes "
              "smoother.",
         tip="The blacker the skin, the sweeter the loaf. Freeze over-ripe bananas whole and "
             "thaw them when you bake."),
    dict(slug="pumpkin-puree", name="Pumpkin purée", short="pumpkin puree",
         g=227, cat="other",
         note="227 g per cup, the same as water — canned purée is a thick slurry. Home-roasted "
              "pumpkin is often wetter, so drain it before measuring or the batter will be "
              "loose.",
         tip="Do not use sweetened pumpkin pie filling in place of purée; it already contains "
             "sugar, spices and starch."),
    dict(slug="table-salt", name="Table salt", short="salt",
         g=288, cat="other",
         note="A tablespoon of table salt is 18 g on King Arthur's chart, so a cup is about "
              "288 g. Salts are not interchangeable by volume: a tablespoon of Morton kosher "
              "salt is 16 g, of Diamond Crystal only 8 g.",
         tip="When swapping salts by volume, assume half the kosher salt is needed if it is a "
             "Diamond Crystal style flake, and adjust to taste."),
    dict(slug="baking-powder", name="Baking powder", short="baking powder",
         g=192, cat="other",
         note="A teaspoon of baking powder is 4 g, so a cup is about 192 g. It loses its "
              "fizzing power about six months after opening, which is why old tins give flat "
              "cakes.",
         tip="Test it: a teaspoon in hot water should foam immediately. If it does not, "
             "replace the tin."),
]

CATEGORIES = [
    ("flours", "Flours and starches",
     "The most variable ingredients in the kitchen — and the ones where cups and grams "
     "disagree most."),
    ("sugars", "Sugars and syrups",
     "Sugar measures consistently; syrups do not, which is why they are usually weighed."),
    ("dairy", "Fats, dairy and liquids",
     "Butter and water are close in density, oil is not, and butter in cups is the least "
     "reliable measurement in baking."),
    ("other", "Spreads, grains and other solids",
     "Nuts, oats and purées: light, airy and very sensitive to how the cup is filled."),
]
