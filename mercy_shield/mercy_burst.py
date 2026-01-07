def mercy_burst_confirm(threat: dict) -> bool:
    print(f"Mercy burst: {threat['desc']} — shadow detected")
    # In UI: popup confirm
    confirm = input("Human override? Allow anyway? (y/n): ").lower() == 'y'
    return confirm  # False = block divine
