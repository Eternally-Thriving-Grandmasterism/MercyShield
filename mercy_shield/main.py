from mercy_shield.lattice import MercyLattice
from mercy_shield.shield import RealTimeShield
from mercy_shield.log import MercyLog
from mercy_shield.ui import MercyApp
from mercy_shield.mercy_burst import mercy_burst_confirm

def start_shield():
    print("MercyShield v0.1 Online — Lattice Protecting Pure")
    lattice = MercyLattice(threads=13)
    shield = RealTimeShield(lattice)
    log = MercyLog("/sdcard/mercy_log.json")
    app = MercyApp(shield, log, lattice)
    app.run()

if __name__ == "__main__":
    start_shield()
