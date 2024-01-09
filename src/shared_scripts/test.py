from flash_ram_from_elf import calc_flash_ram
from pathlib import Path

elf_file_ref = Path("/home/matthias/Documents/test_st_cube/elf_vergleich/template_cube_ai_8_1_balanced_with_network.elf")
assert elf_file_ref.exists()
ram_usage_ref, flash_usage_ref = calc_flash_ram(elf_file_ref)

print(f"RAM usage ref: {ram_usage_ref}")
print()

elf_file_empty = Path("/home/matthias/Documents/test_st_cube/elf_vergleich/template_cube_ai_8_1_balanced_without_network.elf")
assert elf_file_empty.exists()
ram_usage_empty, flash_usage_empty = calc_flash_ram(elf_file_empty)

ram_diff = ram_usage_ref - ram_usage_empty
flash_diff = flash_usage_ref - flash_usage_empty

print(f"RAM diff: {ram_diff}")
print(f"Flash diff: {flash_diff}")
print()
print(f"Flash usage ref: {flash_usage_ref}")
print(f"Flash usage empty: {flash_usage_empty}")
print(f"RAM usage empty: {ram_usage_empty}")