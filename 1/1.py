# Load input file
with open("input.txt", "r") as f:
    lines = f.readlines()
inputs = [float(v) for v in lines]

modules_fuel = []
for v in inputs:
    fuel = v // 3 - 2
    total_fuel_of_module = fuel

    while fuel > 0.0:
        fuel = fuel // 3 - 2
        if fuel > 0.0:
            total_fuel_of_module += fuel

    modules_fuel.append(total_fuel_of_module)

print(sum(modules_fuel))
