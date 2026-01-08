from mercy_shield.ui import MercyApp
from mercy_shield.shield import RealTimeShield
from mercy_shield.lattice import MercyLattice

if __name__ == "__main__":
    lattice = MercyLattice(threads=13)
    shield = RealTimeShield(lattice)
    MercyApp(shield).run()
