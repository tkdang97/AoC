import os
import shutil
from pathlib import Path


# Create directory with one file per day (1 - 25) for the given year with a minimal skeleton
if __name__ == "__main__":
    year = input("Enter the year: ")
    target_path = Path(__file__).parent.parent / year
    if not target_path.exists():
        os.makedirs(target_path)
    for day in range(1, 26):
        if not Path(f"{target_path}/Day {day}.py").is_file():
            with open(f"{target_path}/Day {day}.py", "w") as f:
                f.write("from utils.data import *\n\n\n")
                f.write("def parse(data):\n\n\n")
                f.write("def part1():\n\n\n")
                f.write("def part2():\n\n\n")
                f.write("test = \"\"\"\"\"\"\n\n")
                f.write(f"data = get_and_write_data({day}, {year})\n\n")
                f.write(f"print_output(part1(), part2())\n")
    utils_path = target_path / "utils"
    if not (utils_path).exists():
        os.makedirs(utils_path)
    shutil.copy2(Path(__file__).parent / "data.py", utils_path)
    shutil.copy2(Path(__file__).parent / "grid.py", utils_path)
    
    print("Finished creating templates!")
