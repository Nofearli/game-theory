"""gtlib — reusable library for differential / pursuit-evasion game research.

Modules
-------
geometry    : Apollonius inequality, breakthrough point, interception judgement
uncertainty : distance-dependent uncertainty model, robust Monte-Carlo judgement
filters     : Kalman filters (position-state, constant-velocity)
barrier     : 1v1 / 2v1 barriers, Cartesian-oval parameterisation
assignment  : feasibility matrix, 0-1 ILP assignment, maximum-weight matching
partial_info: capture law, optimal deployment point, ambiguity region
tad         : TAD Apollonius oval, optimal capture point, HJI residual
recon       : virtual evader, dome / wedge barrier, max dwell time
plotting    : IEEE-style figure helpers
simulate    : generic closed-loop simulation framework

Everything is pure NumPy/SciPy. No module imports another module's plotting code.
"""

from . import (  # noqa: F401
    geometry, uncertainty, filters, barrier, assignment,
    partial_info, tad, recon, plotting, simulate,
)

__all__ = [
    "geometry", "uncertainty", "filters", "barrier", "assignment",
    "partial_info", "tad", "recon", "plotting", "simulate",
]
__version__ = "1.0.0"
