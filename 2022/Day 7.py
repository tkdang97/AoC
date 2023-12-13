from utils.data import *


class Directory:
    def __init__(self, parent, name):
        self.parent = parent
        self.files = {}
        self.size = 0
        self.name = name

    def add(self, type, name, size, ref):
        self.files[name] = (type, size, ref)

    def contains(self, name):
        return name in self.files

    def get_directory(self, name):
        if name not in self.files:
            raise KeyError(f"Object {name} is not present in the directory")
        if self.files[name][0] != 0:
            raise ValueError(f"Object {name} is not a directory")
        return self.files[name][2]

    def get_directories(self):
        return [ref for ftype, _, ref in self.files.values() if ftype == 0]

    def calculate_size(self):
        total = 0
        for file_type, size, ref in self.files.values():
            if file_type == 0:  # directory
                total += ref.size if ref.size else ref.calculate_size()
            else:  # file
                total += size
        self.size = total
        return total

    def __str__(self, depth=0):
        indentation = " " * (depth * 3)
        result = f"{indentation}- {self.name} (dir, size={self.size})\n"

        for fname, (ftype, size, ref) in self.files.items():
            if ftype == 1:
                result += f"{indentation}   - {fname} (file, size={size})\n"
            else:
                result += ref.__str__(depth + 1)

        return result


def parse(data):
    root = curr = Directory(None, "/")
    for line in data.splitlines():
        if line.startswith("$"):
            cmd = line.split()
            if cmd[1] == "cd":
                name = cmd[-1]
                if name == "..":
                    curr = curr.parent
                elif name == "/":
                    curr = root
                else:
                    if not curr.contains(name):
                        curr.add(0, name, 0, Directory(curr, name))
                    curr = curr.get_directory(name)
            else:
                continue
        else:
            info, name = line.split()
            if not curr.contains(name):
                if info == "dir":
                    curr.add(0, name, 0, Directory(curr, name))
                else:
                    curr.add(1, name, int(info), None)
    root.calculate_size()
    return root


def part1(root, limit=100000):
    queue = [root]
    total = 0
    while queue:
        next_dir = queue.pop()
        if next_dir.size <= limit:
            total += next_dir.size
        queue.extend(next_dir.get_directories())
    return total


def part2(root, free=30000000, total=70000000):
    target = free - (total - root.size)
    sizes = [root.size]
    queue = [root]
    while queue:
        next_dir = queue.pop()
        if next_dir.size >= target:
            sizes.append(next_dir.size)
            queue.extend([directory for directory in next_dir.get_directories() if directory.size >= target])
    return min(sizes)


data = get_and_write_data(7, 2022)
root_dir = parse(data)
print(root_dir)
print_output(part1(root_dir), part2(root_dir))
