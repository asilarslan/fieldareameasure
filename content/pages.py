# Tool pages and guides for fieldareameasure.com.

# Area units for the converter: key -> (m² per unit, label per language). "extra" units only show in some languages.
UNITS = [
    ("m2", 1.0, {"en": "Square metres (m²)", "es": "Metros cuadrados (m²)", "fr": "Mètres carrés (m²)", "de": "Quadratmeter (m²)", "pt": "Metros quadrados (m²)"}),
    ("ha", 10_000.0, {"en": "Hectares (ha)", "es": "Hectáreas (ha)", "fr": "Hectares (ha)", "de": "Hektar (ha)", "pt": "Hectares (ha)"}),
    ("ac", 4_046.8564224, {"en": "Acres (ac)", "es": "Acres (ac)", "fr": "Acres (ac)", "de": "Acre (ac)", "pt": "Acres (ac)"}),
    ("a", 100.0, {"en": "Ares (a)", "es": "Áreas (a)", "fr": "Ares (a)", "de": "Ar (a)", "pt": "Ares (a)"}),
    ("km2", 1_000_000.0, {"en": "Square kilometres (km²)", "es": "Kilómetros cuadrados (km²)", "fr": "Kilomètres carrés (km²)", "de": "Quadratkilometer (km²)", "pt": "Quilômetros quadrados (km²)"}),
    ("ft2", 0.09290304, {"en": "Square feet (ft²)", "es": "Pies cuadrados (ft²)", "fr": "Pieds carrés (ft²)", "de": "Quadratfuß (ft²)", "pt": "Pés quadrados (ft²)"}),
    ("yd2", 0.83612736, {"en": "Square yards (yd²)", "es": "Yardas cuadradas (yd²)", "fr": "Yards carrés (yd²)", "de": "Quadratyard (yd²)", "pt": "Jardas quadradas (yd²)"}),
    ("mi2", 2_589_988.110336, {"en": "Square miles (mi²)", "es": "Millas cuadradas (mi²)", "fr": "Miles carrés (mi²)", "de": "Quadratmeilen (mi²)", "pt": "Milhas quadradas (mi²)"}),
]
EXTRA_UNITS = {
    "pt": [("alq_sp", 24_200.0, "Alqueire paulista (24.200 m²)"), ("alq_mg", 48_400.0, "Alqueire mineiro (48.400 m²)")],
}

TOOL = {
    "en": dict(path="/area-converter/", title="Area Converter: Acres, Hectares, Square Feet & m² (Free Calculator)",
               desc="Convert land area instantly between acres, hectares, square metres, square feet, square yards, ares, km² and square miles. Plus a length × width area calculator.",
               h1="Area converter", intro="Type a value in any unit and see every other unit at once. Below it, work out the area of a rectangular plot from its length and width.",
               rect_h="Rectangle area calculator", length="Length", width="Width", in_unit="Unit", result="Area",
               table_h="Quick reference", note="Calculations run in your browser.",
               body="""<h2>Common land area conversions</h2>
<div class="table-scroll"><table>
<tr><th>From</th><th>To</th></tr>
<tr><td>1 acre</td><td>43,560 ft² · 4,046.86 m² · 0.4047 ha</td></tr>
<tr><td>1 hectare</td><td>10,000 m² · 2.471 acres · 107,639 ft²</td></tr>
<tr><td>1 square mile</td><td>640 acres · 259 ha</td></tr>
<tr><td>1 square metre</td><td>10.764 ft² · 1.196 yd²</td></tr>
<tr><td>1 are</td><td>100 m²</td></tr>
</table></div>
<h2>Acres or hectares?</h2>
<p>The United States, the UK (for land) and a few other countries use acres; most of the world uses hectares. An acre is about 40% of a hectare, so to go from acres to hectares, multiply by 0.4047; from hectares to acres, multiply by 2.471.</p>""",
               faq=[("How many square feet are in an acre?", "43,560 square feet."), ("How many acres are in a hectare?", "About 2.471 acres."),
                    ("How do I find the area of an irregular field?", "Split it into triangles, or mark its corners on a satellite map with a measuring app. See our guide to irregular plots.")]),
    "es": dict(path="/es/conversor-de-superficie/", title="Conversor de superficie: hectáreas, acres, m² y pies² (gratis)",
               desc="Convierte superficies al instante entre hectáreas, metros cuadrados, acres, áreas, pies², yardas², km² y millas². Incluye calculadora de largo × ancho.",
               h1="Conversor de superficie", intro="Escribe un valor en cualquier unidad y ve todas las demás. Debajo, calcula la superficie de una parcela rectangular.",
               rect_h="Calculadora de superficie rectangular", length="Largo", width="Ancho", in_unit="Unidad", result="Superficie",
               table_h="Referencia rápida", note="Los cálculos se hacen en tu navegador.",
               body="""<h2>Equivalencias habituales</h2><ul><li>1 hectárea = 10.000 m² = 100 áreas = 2,471 acres</li><li>1 acre = 4.046,86 m² = 0,4047 ha</li><li>1 km² = 100 ha</li></ul>""",
               faq=[("¿Cuántos m² tiene una hectárea?", "10.000 m²."), ("¿Cuántas hectáreas son un acre?", "Unas 0,4047 hectáreas.")]),
    "fr": dict(path="/fr/convertisseur-de-surface/", title="Convertisseur de surface : hectares, ares, m², acres (gratuit)",
               desc="Convertissez une surface entre hectares, ares, mètres carrés, acres, pieds², yards², km² et miles². Avec calculateur longueur × largeur.",
               h1="Convertisseur de surface", intro="Saisissez une valeur dans n'importe quelle unité et voyez toutes les autres. En dessous, calculez la surface d'une parcelle rectangulaire.",
               rect_h="Surface d'un rectangle", length="Longueur", width="Largeur", in_unit="Unité", result="Surface",
               table_h="Repères", note="Les calculs se font dans votre navigateur.",
               body="""<h2>Équivalences courantes</h2><ul><li>1 hectare = 10 000 m² = 100 ares = 2,471 acres</li><li>1 are = 100 m²</li><li>1 acre = 4 046,86 m²</li></ul>""",
               faq=[("Combien de m² dans un hectare ?", "10 000 m²."), ("Combien d'ares dans un hectare ?", "100 ares.")]),
    "de": dict(path="/de/flaechenrechner/", title="Flächenrechner: Hektar, Ar, m² und Acre umrechnen (kostenlos)",
               desc="Rechne Flächen sofort um zwischen Hektar, Ar, Quadratmetern, Acre, Quadratfuß, Quadratyard, km² und Quadratmeilen. Mit Länge-×-Breite-Rechner.",
               h1="Flächenrechner", intro="Gib einen Wert in einer Einheit ein und sieh alle anderen. Darunter berechnest du die Fläche eines rechteckigen Grundstücks.",
               rect_h="Rechteckfläche berechnen", length="Länge", width="Breite", in_unit="Einheit", result="Fläche",
               table_h="Schnellübersicht", note="Die Berechnung läuft in deinem Browser.",
               body="""<h2>Gängige Umrechnungen</h2><ul><li>1 Hektar = 10.000 m² = 100 Ar = 2,471 Acre</li><li>1 Ar = 100 m²</li><li>1 Acre = 4.046,86 m²</li></ul>""",
               faq=[("Wie viele m² hat ein Hektar?", "10.000 m²."), ("Wie viel ist ein Ar?", "100 m².")]),
    "pt": dict(path="/pt/conversor-de-area/", title="Conversor de área: hectare, alqueire, m² e acre (grátis)",
               desc="Converta áreas entre hectares, metros quadrados, alqueires paulista e mineiro, acres, pés², km² e mais. Com calculadora de comprimento × largura.",
               h1="Conversor de área", intro="Digite um valor em qualquer unidade e veja todas as outras. Abaixo, calcule a área de um lote retangular.",
               rect_h="Área de um retângulo", length="Comprimento", width="Largura", in_unit="Unidade", result="Área",
               table_h="Referência rápida", note="Os cálculos são feitos no seu navegador.",
               body="""<h2>Conversões comuns</h2><ul><li>1 hectare = 10.000 m² = 2,471 acres</li><li>1 alqueire paulista = 24.200 m² = 2,42 ha</li><li>1 alqueire mineiro (goiano) = 48.400 m² = 4,84 ha</li></ul><p>O alqueire varia por região; confira o padrão usado na sua.</p>""",
               faq=[("Quantos m² tem um hectare?", "10.000 m²."), ("Quanto é um alqueire?", "Depende da região: o paulista tem 24.200 m² e o mineiro (goiano) 48.400 m².")]),
}

GUIDES = [
    dict(path="/guides/how-to-measure-land-area/", shot="measure", alts={"tr": "https://arazi.app/rehber/arsa-olcumu-nasil-yapilir/"},
         title="How to Measure Land Area: 4 Methods From Phone to Survey",
         desc="How to measure the area of a field, garden or plot: satellite map apps, walking with GPS, tape and triangles, and official surveys — with accuracy for each.",
         h1="How to measure land area",
         intro="You can find the area of almost any piece of land without special equipment. Here are four methods, from quickest to most precise.",
         body="""<ol class="checks">
<li><b>Mark the corners on a satellite map</b>The fastest way for fields and plots you can see from above. Find the land in a measuring app, tap each corner and read the area and perimeter. Accuracy depends on the image and how carefully you place the corners — usually within a few percent.</li>
<li><b>Walk the boundary with GPS</b>Useful under trees or where the edges aren't visible from above. Phone GPS is typically accurate to a few metres, which matters more on small plots.</li>
<li><b>Tape measure and triangles</b>For small gardens: measure the sides, split the shape into rectangles and triangles, and add them up (see our guide to irregular plots).</li>
<li><b>Official survey</b>For legal boundaries, sales and building permits, only a licensed surveyor's measurement counts.</li>
</ol>
<h2>Tips for better results</h2>
<ul><li>Zoom in before placing corners; place them where the boundary actually is (fence, hedge, ditch), not on shadows.</li><li>Add extra points on curved edges.</li><li>Compare your result with the area on the deed or land registry; small differences are normal.</li></ul>""",
         faq=[("Can I measure land area with my phone?", "Yes. Mark the corners on a satellite map in an app, or walk the boundary with GPS."),
              ("Why is my measurement different from the deed?", "Deeds may use older surveys, different boundaries or rounding. For a legal figure, ask a surveyor.")]),
    dict(path="/guides/how-big-is-an-acre/", shot="detail",
         title="How Big Is an Acre? Acre vs Hectare, Football Fields and m²",
         desc="An acre is 43,560 square feet or 4,047 m² — about three-quarters of an American football field. Compare acres, hectares and everyday sizes.",
         h1="How big is an acre?",
         intro="An acre is 43,560 square feet, or about 4,047 square metres. It's easier to picture with a few comparisons.",
         body="""<h2>An acre in numbers</h2>
<ul><li>43,560 ft² · 4,840 yd² · 4,046.86 m²</li><li>0.4047 hectares (a hectare is about 2.47 acres)</li><li>A square acre is about 208.7 ft (63.6 m) on each side</li></ul>
<h2>Everyday comparisons</h2>
<ul><li>An American football field including end zones is 57,600 ft², about 1.32 acres — so an acre is roughly three-quarters of it.</li><li>A standard 105 × 68 m soccer pitch is about 7,140 m², roughly 1.76 acres.</li><li>A doubles tennis court's playing area is 23.77 × 10.97 m (about 261 m²), so roughly 15 courts' worth of playing area fit in an acre.</li></ul>
<h2>Acre or hectare?</h2>
<p>The US and UK (for land) use acres; most other countries use hectares. Use our <a href="/area-converter/">area converter</a> to switch between them.</p>""",
         faq=[("How many square feet in an acre?", "43,560."), ("Is an acre bigger than a hectare?", "No. A hectare is about 2.47 acres.")]),
    dict(path="/guides/area-of-an-irregular-plot/", shot="measure",
         title="How to Calculate the Area of an Irregular Plot (3 Easy Ways)",
         desc="Find the area of an irregular field or plot: split it into triangles, use the shoelace formula with corner coordinates, or mark it on a satellite map.",
         h1="How to calculate the area of an irregular plot",
         intro="Few fields are perfect rectangles. These three methods work for any shape with straight sides.",
         body="""<h2>1. Split it into triangles</h2>
<p>Draw diagonals from one corner to split the plot into triangles. Measure the three sides of each and use Heron's formula: with sides a, b, c and s = (a + b + c) / 2, the area is √(s(s−a)(s−b)(s−c)). Add the triangles together.</p>
<h2>2. Use corner coordinates (shoelace formula)</h2>
<p>If you know the x and y coordinates of each corner in metres, in order around the plot, the area is half the absolute value of Σ(xᵢ·yᵢ₊₁ − xᵢ₊₁·yᵢ). This is how measuring apps compute area from the points you place.</p>
<h2>3. Mark it on a satellite map</h2>
<p>The quickest option: tap each corner on a satellite image and let the app do the maths. Add extra points along curved edges.</p>""",
         faq=[("What about curved boundaries?", "Approximate them with several short straight segments; the more points, the closer the result.")]),
    dict(path="/guides/sun-orientation-for-a-house-plot/", shot="site0",
         title="Sun Orientation for a House Plot: What to Check Before You Buy",
         desc="How the sun moves over a building plot in summer and winter, which side should get the living room and garden, and how roof overhangs help.",
         h1="Sun orientation for a house plot",
         intro="Where the sun falls on a plot shapes everything from the garden to heating bills. Here's what to check before you buy or design.",
         body="""<h2>The sun's path changes with the seasons</h2>
<p>In the northern hemisphere the sun is due south at noon (due north in the southern hemisphere). It's high in summer and low in winter, so a south-facing side gets warm, low winter light and easily shaded summer light.</p>
<h2>What to place on the sunny side</h2>
<ul><li>Living room, kitchen and big windows</li><li>The garden and terrace — push the house towards the shadier edge</li></ul>
<h2>Overhangs: shade in summer, sun in winter</h2>
<p>A roof overhang sized for your latitude shades high summer sun but lets low winter sun reach the windows. The right depth depends on window height and the gap above it.</p>
<h2>Check the slope too</h2>
<p>A plot that slopes towards the sun gets bright rooms easily; one that slopes away can stay shaded in winter.</p>""",
         faq=[("Which direction should a house face?", "In the northern hemisphere, main living spaces usually benefit from facing south; in the southern hemisphere, north.")]),
    dict(path="/guides/building-setbacks-and-buildable-area/", shot="site1",
         title="Building Setbacks and Buildable Area Explained (With Examples)",
         desc="What setbacks and coverage ratios are, how they shrink a plot to its buildable area, and how to estimate it before buying.",
         h1="Setbacks and buildable area",
         intro="A plot's size isn't the space you can build on. Setbacks and coverage rules decide the footprint — check them before you buy.",
         body="""<h2>Setbacks</h2>
<p>Setbacks are minimum distances between a building and the plot boundaries: usually a front setback from the street and side and rear setbacks from neighbours. Local zoning rules set the values.</p>
<h2>Coverage ratio</h2>
<p>Many places also limit the share of the plot a building may cover (for example 30%). The smaller of “area inside the setbacks” and “coverage limit × plot area” is your maximum footprint.</p>
<h2>Example</h2>
<p>A 30 × 40 m plot (1,200 m²) with a 5 m front setback and 3 m side and rear setbacks leaves 24 × 32 m = 768 m² inside the setbacks. With a 30% coverage limit, the footprint is capped at 360 m².</p>
<div class="note-box">Zoning rules vary by municipality and plan. Always check the official zoning certificate for the plot.</div>""",
         faq=[("What is a setback?", "The minimum distance a building must keep from a property line."), ("What is a coverage ratio?", "The maximum share of the plot that buildings may cover.")]),
]

HUB = dict(path="/guides/", title="Land Measuring Guides: Acres, Irregular Plots, Setbacks & Sun | Field Area Measure",
           desc="Practical guides to measuring land: methods, acre and hectare sizes, irregular plots, building setbacks and sun orientation.",
           h1="Land measuring guides", intro="Practical guides for farmers, buyers and builders.")
