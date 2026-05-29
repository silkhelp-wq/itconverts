/* Karo Convert — shared conversion engine (no dependencies, ES2015)
 * Exposes a global: window.ITC
 * Linear units declare a `factor` (value-in-base = value * factor).
 * Non-linear categories (temperature, fuel economy, numeric base)
 * declare explicit to()/from() functions instead.
 */
(function (global) {
  'use strict';

  // Helper to build a linear unit list quickly.
  function U(id, name, symbol, factor) {
    return { id: id, name: name, symbol: symbol, factor: factor };
  }

  var CATEGORIES = [
    {
      id: 'length', name: 'Length', icon: 'ruler',
      base: 'm', blurb: 'Distance & dimensions',
      units: [
        U('nm', 'Nanometer', 'nm', 1e-9),
        U('um', 'Micrometer', 'µm', 1e-6),
        U('mm', 'Millimeter', 'mm', 0.001),
        U('cm', 'Centimeter', 'cm', 0.01),
        U('m', 'Meter', 'm', 1),
        U('km', 'Kilometer', 'km', 1000),
        U('in', 'Inch', 'in', 0.0254),
        U('ft', 'Foot', 'ft', 0.3048),
        U('yd', 'Yard', 'yd', 0.9144),
        U('mi', 'Mile', 'mi', 1609.344),
        U('nmi', 'Nautical mile', 'nmi', 1852),
        U('ly', 'Light-year', 'ly', 9.4607304725808e15),
        U('au', 'Astronomical unit', 'AU', 1.495978707e11)
      ],
      presets: [
        { label: 'Marathon', value: 42.195, from: 'km', to: 'mi' },
        { label: "Person's height", value: 6, from: 'ft', to: 'cm' }
      ]
    },
    {
      id: 'mass', name: 'Mass / Weight', icon: 'scale',
      base: 'kg', blurb: 'Weight & mass',
      units: [
        U('mg', 'Milligram', 'mg', 1e-6),
        U('g', 'Gram', 'g', 0.001),
        U('kg', 'Kilogram', 'kg', 1),
        U('t', 'Tonne (metric)', 't', 1000),
        U('oz', 'Ounce', 'oz', 0.0283495231),
        U('lb', 'Pound', 'lb', 0.45359237),
        U('st', 'Stone', 'st', 6.35029318),
        U('uston', 'Ton (US)', 'ton', 907.18474),
        U('ukton', 'Ton (UK)', 'long ton', 1016.0469088),
        U('ct', 'Carat', 'ct', 0.0002)
      ],
      presets: [
        { label: 'Bag of sugar', value: 1, from: 'kg', to: 'lb' },
        { label: 'Body weight', value: 11, from: 'st', to: 'kg' }
      ]
    },
    {
      id: 'temperature', name: 'Temperature', icon: 'thermometer',
      base: 'c', blurb: 'Celsius, Fahrenheit, Kelvin', nonlinear: true,
      units: [
        { id: 'c', name: 'Celsius', symbol: '°C', to: function (v) { return v; }, from: function (v) { return v; } },
        { id: 'f', name: 'Fahrenheit', symbol: '°F', to: function (v) { return (v - 32) * 5 / 9; }, from: function (v) { return v * 9 / 5 + 32; } },
        { id: 'k', name: 'Kelvin', symbol: 'K', to: function (v) { return v - 273.15; }, from: function (v) { return v + 273.15; } },
        { id: 'r', name: 'Rankine', symbol: '°R', to: function (v) { return (v - 491.67) * 5 / 9; }, from: function (v) { return v * 9 / 5 + 491.67; } }
      ],
      presets: [
        { label: 'Body temp', value: 37, from: 'c', to: 'f' },
        { label: 'Oven 350°F', value: 350, from: 'f', to: 'c' },
        { label: 'Freezing', value: 0, from: 'c', to: 'f' }
      ]
    },
    {
      id: 'area', name: 'Area', icon: 'square',
      base: 'm2', blurb: 'Surface area',
      units: [
        U('mm2', 'Square millimeter', 'mm²', 1e-6),
        U('cm2', 'Square centimeter', 'cm²', 1e-4),
        U('m2', 'Square meter', 'm²', 1),
        U('ha', 'Hectare', 'ha', 10000),
        U('km2', 'Square kilometer', 'km²', 1e6),
        U('in2', 'Square inch', 'in²', 0.00064516),
        U('ft2', 'Square foot', 'ft²', 0.09290304),
        U('yd2', 'Square yard', 'yd²', 0.83612736),
        U('ac', 'Acre', 'ac', 4046.8564224),
        U('mi2', 'Square mile', 'mi²', 2589988.110336)
      ],
      presets: [
        { label: 'Football pitch', value: 1, from: 'ac', to: 'm2' }
      ]
    },
    {
      id: 'volume', name: 'Volume', icon: 'beaker',
      base: 'l', blurb: 'Capacity & volume',
      units: [
        U('ml', 'Milliliter', 'mL', 0.001),
        U('l', 'Liter', 'L', 1),
        U('m3', 'Cubic meter', 'm³', 1000),
        U('cm3', 'Cubic centimeter', 'cm³', 0.001),
        U('tsp', 'Teaspoon (US)', 'tsp', 0.00492892159),
        U('tbsp', 'Tablespoon (US)', 'tbsp', 0.0147867648),
        U('floz', 'Fluid ounce (US)', 'fl oz', 0.0295735296),
        U('cup', 'Cup (US)', 'cup', 0.2365882365),
        U('pt', 'Pint (US)', 'pt', 0.473176473),
        U('qt', 'Quart (US)', 'qt', 0.946352946),
        U('gal', 'Gallon (US)', 'gal', 3.785411784),
        U('galuk', 'Gallon (UK)', 'gal UK', 4.54609),
        U('bbl', 'Oil barrel', 'bbl', 158.987294928)
      ],
      presets: [
        { label: 'Gallon to liters', value: 1, from: 'gal', to: 'l' }
      ]
    },
    {
      id: 'speed', name: 'Speed', icon: 'gauge',
      base: 'mps', blurb: 'Velocity',
      units: [
        U('mps', 'Meter / second', 'm/s', 1),
        U('kph', 'Kilometer / hour', 'km/h', 0.277777778),
        U('mph', 'Mile / hour', 'mph', 0.44704),
        U('fps', 'Foot / second', 'ft/s', 0.3048),
        U('knot', 'Knot', 'kn', 0.514444444),
        U('mach', 'Mach (sea level)', 'Mach', 340.29)
      ],
      presets: [
        { label: 'Highway 60 mph', value: 60, from: 'mph', to: 'kph' }
      ]
    },
    {
      id: 'time', name: 'Time', icon: 'clock',
      base: 's', blurb: 'Duration',
      units: [
        U('ns', 'Nanosecond', 'ns', 1e-9),
        U('ms', 'Millisecond', 'ms', 0.001),
        U('s', 'Second', 's', 1),
        U('min', 'Minute', 'min', 60),
        U('h', 'Hour', 'h', 3600),
        U('day', 'Day', 'd', 86400),
        U('wk', 'Week', 'wk', 604800),
        U('mo', 'Month (30d)', 'mo', 2592000),
        U('yr', 'Year (365d)', 'yr', 31536000)
      ]
    },
    {
      id: 'data', name: 'Digital storage', icon: 'database',
      base: 'B', blurb: 'Bytes & bits',
      units: [
        U('bit', 'Bit', 'bit', 0.125),
        U('B', 'Byte', 'B', 1),
        U('KB', 'Kilobyte', 'KB', 1e3),
        U('MB', 'Megabyte', 'MB', 1e6),
        U('GB', 'Gigabyte', 'GB', 1e9),
        U('TB', 'Terabyte', 'TB', 1e12),
        U('PB', 'Petabyte', 'PB', 1e15),
        U('KiB', 'Kibibyte', 'KiB', 1024),
        U('MiB', 'Mebibyte', 'MiB', 1048576),
        U('GiB', 'Gibibyte', 'GiB', 1073741824),
        U('TiB', 'Tebibyte', 'TiB', 1099511627776)
      ],
      presets: [
        { label: 'GB vs GiB', value: 1, from: 'GB', to: 'GiB' }
      ]
    },
    {
      id: 'energy', name: 'Energy', icon: 'bolt',
      base: 'j', blurb: 'Work & heat',
      units: [
        U('j', 'Joule', 'J', 1),
        U('kj', 'Kilojoule', 'kJ', 1000),
        U('cal', 'Calorie', 'cal', 4.184),
        U('kcal', 'Kilocalorie', 'kcal', 4184),
        U('wh', 'Watt-hour', 'Wh', 3600),
        U('kwh', 'Kilowatt-hour', 'kWh', 3600000),
        U('btu', 'British thermal unit', 'BTU', 1055.05585),
        U('ftlb', 'Foot-pound', 'ft·lb', 1.3558179483),
        U('ev', 'Electronvolt', 'eV', 1.602176634e-19)
      ]
    },
    {
      id: 'power', name: 'Power', icon: 'plug',
      base: 'w', blurb: 'Rate of energy',
      units: [
        U('w', 'Watt', 'W', 1),
        U('kw', 'Kilowatt', 'kW', 1000),
        U('mw', 'Megawatt', 'MW', 1e6),
        U('hp', 'Horsepower (mech)', 'hp', 745.699872),
        U('ps', 'Metric horsepower', 'PS', 735.49875),
        U('btuh', 'BTU / hour', 'BTU/h', 0.29307107)
      ]
    },
    {
      id: 'pressure', name: 'Pressure', icon: 'gauge',
      base: 'pa', blurb: 'Force per area',
      units: [
        U('pa', 'Pascal', 'Pa', 1),
        U('kpa', 'Kilopascal', 'kPa', 1000),
        U('bar', 'Bar', 'bar', 100000),
        U('psi', 'Pound / sq inch', 'psi', 6894.757293),
        U('atm', 'Atmosphere', 'atm', 101325),
        U('mmhg', 'mm of mercury', 'mmHg', 133.322387),
        U('torr', 'Torr', 'Torr', 133.322368)
      ]
    },
    {
      id: 'fuel', name: 'Fuel economy', icon: 'fuel',
      base: 'kmpl', blurb: 'Efficiency', nonlinear: true,
      units: [
        { id: 'kmpl', name: 'Kilometers / liter', symbol: 'km/L', to: function (v) { return v; }, from: function (v) { return v; } },
        { id: 'mpgus', name: 'Miles / gallon (US)', symbol: 'mpg', to: function (v) { return v * 0.425143707; }, from: function (v) { return v / 0.425143707; } },
        { id: 'mpguk', name: 'Miles / gallon (UK)', symbol: 'mpg UK', to: function (v) { return v * 0.354006042; }, from: function (v) { return v / 0.354006042; } },
        { id: 'l100', name: 'Liters / 100 km', symbol: 'L/100km', to: function (v) { return v === 0 ? 0 : 100 / v; }, from: function (v) { return v === 0 ? 0 : 100 / v; } }
      ],
      presets: [
        { label: '40 mpg → L/100km', value: 40, from: 'mpgus', to: 'l100' }
      ]
    },
    {
      id: 'angle', name: 'Angle', icon: 'angle',
      base: 'deg', blurb: 'Rotation',
      units: [
        U('deg', 'Degree', '°', 1),
        U('rad', 'Radian', 'rad', 57.295779513),
        U('grad', 'Gradian', 'grad', 0.9),
        U('arcmin', 'Arcminute', "'", 1 / 60),
        U('arcsec', 'Arcsecond', '"', 1 / 3600),
        U('turn', 'Turn', 'turn', 360)
      ]
    },
    {
      id: 'frequency', name: 'Frequency', icon: 'wave',
      base: 'hz', blurb: 'Cycles per second',
      units: [
        U('hz', 'Hertz', 'Hz', 1),
        U('khz', 'Kilohertz', 'kHz', 1000),
        U('mhz', 'Megahertz', 'MHz', 1e6),
        U('ghz', 'Gigahertz', 'GHz', 1e9),
        U('rpm', 'Revolutions / min', 'rpm', 1 / 60)
      ]
    },
    {
      id: 'force', name: 'Force', icon: 'arrow',
      base: 'n', blurb: 'Push & pull',
      units: [
        U('n', 'Newton', 'N', 1),
        U('kn', 'Kilonewton', 'kN', 1000),
        U('lbf', 'Pound-force', 'lbf', 4.448221615),
        U('kgf', 'Kilogram-force', 'kgf', 9.80665),
        U('dyn', 'Dyne', 'dyn', 1e-5)
      ]
    },
    {
      id: 'datarate', name: 'Data rate', icon: 'wifi',
      base: 'bps', blurb: 'Bandwidth',
      units: [
        U('bps', 'Bit / second', 'bit/s', 1),
        U('kbps', 'Kilobit / second', 'kbit/s', 1000),
        U('mbps', 'Megabit / second', 'Mbit/s', 1e6),
        U('gbps', 'Gigabit / second', 'Gbit/s', 1e9),
        U('Bps', 'Byte / second', 'B/s', 8),
        U('MBps', 'Megabyte / second', 'MB/s', 8e6)
      ]
    },
    {
      id: 'numbase', name: 'Number base', icon: 'hash',
      base: 'dec', blurb: 'Binary, octal, hex', nonlinear: true, integer: true,
      units: [
        { id: 'bin', name: 'Binary', symbol: 'base 2', radix: 2 },
        { id: 'oct', name: 'Octal', symbol: 'base 8', radix: 8 },
        { id: 'dec', name: 'Decimal', symbol: 'base 10', radix: 10 },
        { id: 'hex', name: 'Hexadecimal', symbol: 'base 16', radix: 16 }
      ]
    }
  ];

  var byId = {};
  for (var i = 0; i < CATEGORIES.length; i++) {
    var c = CATEGORIES[i];
    c.unitMap = {};
    for (var j = 0; j < c.units.length; j++) { c.unitMap[c.units[j].id] = c.units[j]; }
    byId[c.id] = c;
  }

  function getCategory(id) { return byId[id]; }

  // Core conversion. Returns a Number (or NaN), except number-base which
  // is handled by convertString below.
  function convert(catId, value, fromId, toId) {
    var cat = byId[catId];
    if (!cat) { return NaN; }
    var from = cat.unitMap[fromId], to = cat.unitMap[toId];
    if (!from || !to) { return NaN; }
    if (cat.nonlinear && from.to) {
      var inBase = from.to(value);
      return to.from(inBase);
    }
    // linear
    var base = value * from.factor;
    return base / to.factor;
  }

  // String-aware conversion used by the number-base category.
  function convertString(catId, raw, fromId, toId) {
    var cat = byId[catId];
    if (cat && cat.id === 'numbase') {
      var from = cat.unitMap[fromId], to = cat.unitMap[toId];
      var n = parseInt(String(raw).trim(), from.radix);
      if (isNaN(n)) { return ''; }
      return n.toString(to.radix).toUpperCase();
    }
    var num = parseFloat(raw);
    if (isNaN(num)) { return ''; }
    return format(convert(catId, num, fromId, toId));
  }

  // Pretty number formatting: trims noise, uses exponential for extremes,
  // groups thousands for readable magnitudes.
  function format(n) {
    if (n === null || n === undefined || isNaN(n)) { return ''; }
    if (n === 0) { return '0'; }
    var abs = Math.abs(n);
    if (abs !== 0 && (abs < 1e-6 || abs >= 1e15)) {
      return n.toExponential(6).replace(/\.?0+e/, 'e');
    }
    // Round to 8 significant-ish digits, then strip trailing zeros.
    var rounded = parseFloat(n.toPrecision(10));
    var str = rounded.toString();
    if (str.indexOf('e') !== -1) { return str; }
    var parts = str.split('.');
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ',');
    return parts.join('.');
  }

  global.ITC = {
    categories: CATEGORIES,
    getCategory: getCategory,
    convert: convert,
    convertString: convertString,
    format: format
  };
})(window);
