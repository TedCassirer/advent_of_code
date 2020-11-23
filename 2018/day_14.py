def combineRecipes():
    recipes = [3, 7]
    yield from (r for r in recipes)
    elf1, elf2 = 0, 1
    while True:
        newRecipe = recipes[elf1] + recipes[elf2]
        if newRecipe >= 10:
            recipes.append(newRecipe//10)
            recipes.append(newRecipe-10)
            yield newRecipe//10
            yield newRecipe-10
        else:
            recipes.append(newRecipe)
            yield newRecipe
        elf1 = (elf1 + recipes[elf1] + 1) % len(recipes)
        elf2 = (elf2 + recipes[elf2] + 1) % len(recipes)


def part1():
    input = '260321'
    recipes = combineRecipes()
    [next(recipes) for _ in range(int(input))]
    result = [next(recipes) for _ in range(10)]
    return ''.join(map(str, result))

def part2():
    input = '260321'
    recipes = combineRecipes()
    seen = ''.join([str(next(recipes)) for _ in range(len(input))])
    for i, r in enumerate(recipes):
        seen = seen[1:] + str(r)
        if seen == input:
            return i + 1
if __name__ == '__main__':
    print('Part 1:', part1())
    print('Part 2:', part2())