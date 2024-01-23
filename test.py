import time
from ui_clicker import check_element_in_warcraft_window
from ui_clicker import collect_image_paths

paths = collect_image_paths()
final_paths = dict(paths)  # Create a new dictionary with the same initial values

for key, path in paths.items():
    print(key)
    print(path)
    time.sleep(5)

    value = 1.0
    while check_element_in_warcraft_window(element_image_path=path, confidence_threshold=value) != True and value > 0:
        value -= 0.01
        print(value)

    print("add")
    final_paths[str(key + "_threshold")] = value

print(final_paths)
