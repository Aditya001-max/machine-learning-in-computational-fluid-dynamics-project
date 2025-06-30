#!/usr/bin/env python3
python3
from smartsim import Experiment
exp = Experiment("mesh-motion", launcher="local")
db = exp.create_database(port=8010, interface="lo")
exp.start(db)

