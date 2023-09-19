# ElastoViscoPlastic material SIMulator

## Description

The evpsim module simulates elasto-visco-plastic mechanical behavior for a given loading path (strain/stress/mixed).

Simulation is performed at the scale of a single material point. It would be conceivable to couple the evpsim module with a finite element code for structural calculations, but this would require some work to reorganize the code, particularly in terms of memory management. What's more, it would still be prohibitively expensive in terms of calculation costs compared with a dedicated implementation.

## Installation

### From sources

```bash
git clone https://github.com/basileMarchand/evpsim.git
cd evpsim
pip install .
```

Or even simplier

```bash
pip install git+https://github.com/basileMarchand/evpsim.git
```

### From PyPi

Coming soon

## Documentation

Coming soon
