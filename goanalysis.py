import os
from pydriller import RepositoryMining
from golang_parser import GolangParser
from collections import defaultdict

repo_path = 'path/to/your/repo'

def analyze_file(file_content):
    parser = GolangParser()
    ast = parser.parse(file_content)
    inventory = defaultdict(set)

    for decl in ast.declarations:
        if isinstance(decl, (parser.Variable, parser.Constant)):
            for name in decl.names:
                inventory[name].add(decl)
        elif isinstance(decl, parser.StructType):
            for field in decl.fields:
                for name in field.names:
                    inventory[name].add(decl)
        elif isinstance(decl, parser.Function):
            for name, obj in inventory.items():
                if name in decl.body or name in decl.signature:
                    inventory[name].add(decl)

    return inventory

def main():
    data_inventory = defaultdict(set)

    for commit in RepositoryMining(repo_path).traverse_commits():
        for modified_file in commit.modifications:
            if modified_file.filename.endswith('.go'):
                inventory = analyze_file(modified_file.source_code)
                for name, objects in inventory.items():
                    data_inventory[name].update(objects)

    for name, objects in data_inventory.items():
        print(f"{name}:")
        for obj in objects:
            print(f"  {obj}")

if __name__ == '__main__':
    main()