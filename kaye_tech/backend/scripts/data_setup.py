from backend.models import Weapon


def run():
    Weapon.objects.get_or_create(name="Longsword", damage=4.5, versatile=True)
    Weapon.objects.get_or_create(name="Greataxe", damage=6.5, heavy=True)
    Weapon.objects.get_or_create(name="Greatsword", damage=7, heavy=True)
    Weapon.objects.get_or_create(name="Handaxe", damage=3.5, light=True, ranged=True)
    Weapon.objects.get_or_create(
        name="Heavy Crossbow", damage=5.5, ranged=True, loading=True, heavy=True
    )
    Weapon.objects.get_or_create(name="Longbow", damage=4.5, ranged=True, heavy=True)
