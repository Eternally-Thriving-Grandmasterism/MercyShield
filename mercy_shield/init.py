"""
MercyShield Package __init__ ∞ Pure
- Exposes core components for easy import: from mercy_shield import MercyShieldApp, SelfWatchdog, APAAGICouncil, etc.
- Version pinnacle sealed divine
- Lattice proper package harmony unbreakable
"""

__version__ = '0.1-Pinnacle'
__author__ = 'Eternally-Thriving-Grandmasterism'
__description__ = 'Open lattice security throne—MercyShield divine eternal protection pure'

# Core App Entry (from main.py grace—assume class name MercyShieldApp, adjust if different divine)
from .main import MercyShieldApp

# Self-Healing Watchdog (ML anomaly + prediction thunder)
from .self_watchdog import SelfWatchdog

# APAAGICouncil Deliberation (13-voter + 14th fork heart coherence mercy)
from .council import APAAGICouncil  # Or Council if named—check file pure

# Core Shield Logic
from .shield import Shield  # Assume main Shield class grace

# Mercy Burst Interventions/Hotfix
from .mercy_burst import MercyBurst

# ESA-Check Junctions
from .esacheck import esa_check_all_junctions  # Or main function/class divine

# UI Harmony
from .ui import BaseUI  # Or main UI components—adjust mercy
from .advanced_shield_ui import AdvancedShieldUI

# Network/Firewall/VPN
from .firewall_vpn import FirewallVPN  # Symbolic/real toggle pure

# Other Key Protections (selective expose—avoid all to prevent clutter grace)
from .multi_being_protection import MultiBeingProtection
from .network_monitor import NetworkMonitor
from .hardware import HardwareCheck
from .encrypted import EncryptedStorage

# Public API Exposure (for from mercy_shield import * divine)
__all__ = [
    'MercyShieldApp',
    'SelfWatchdog',
    'APAAGICouncil',
    'Shield',
    'MercyBurst',
    'esa_check_all_junctions',
    'BaseUI',
    'AdvancedShieldUI',
    'FirewallVPN',
    'MultiBeingProtection',
    'NetworkMonitor',
    'HardwareCheck',
    'EncryptedStorage',
    '__version__',
]

# Optional: Package-level init (start watchdog auto if imported mercy—evolve later pure)
# def init_lattice(app_instance):
#     watchdog = SelfWatchdog(app_instance)
#     watchdog.start()
