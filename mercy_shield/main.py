from mercy_shield.lattice import MercyLattice
from mercy_shield.shield import RealTimeShield
from mercy_shield.log import MercyLog
from mercy_shield.ui import MercyApp

def start_shield():
    print("MercyShield Online — Lattice Protecting Pure")
    lattice = MercyLattice(threads=13)
    shield = RealTimeShield(lattice)
    log = MercyLog("/sdcard/mercy_log.json")  # Local only
    MercyApp(shield, log).run()  # Kivy UI
