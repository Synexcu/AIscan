# contours = [
#     [[[441, 468]], [[441, 623]], [[640, 622]], [[639, 467]]],  # 3th answer box (Blue) | Biggest Contour [in blue] kiri atas | kiri bawah | kanan bawah | kanan atas
#     [[[441, 139]], [[441, 294]], [[640, 293]], [[639, 138]]],  # 1st answer box (Green) | 2nd biggest contour [in green]
#     [[[441, 797]], [[638, 796]], [[441, 952]], [[640, 951]]],  # 5th answer box (Red) | 3rd biggest contour [in red]
#     [[[441, 304]], [[442, 459]], [[640, 458]], [[639, 303]]],  # 2nd answer box (Gray) | 4th biggest contour [in gray]
#     [[[441, 633]], [[442, 788]], [[640, 787]], [[639, 632]]],  # 4th answer box (Blue ish gray) | 5th biggest contour [in blue-ish gray]
#     [[[722, 138]], [[722, 294]], [[919, 294]], [[919, 138]]],  # 6nd answer box (Blue ish gray) | 6th biggest contour [in blue-ish gray]
#     [[[722, 467]], [[722, 623]], [[919, 623]], [[918, 467]]],  # 8th answer box (Gray) | 7th biggest contour [in gray]
#     [[[721, 633]], [[722, 788]], [[919, 788]], [[919, 632]]],  # 9th answer box (Yellow) | 8th biggest contour [in yellow]
#     [[[722, 303]], [[722, 459]], [[919, 459]], [[919, 303]]],  # 7th answer box (Pink) | 9th biggest contour [in pink]
#     [[[722, 797]], [[722, 952]], [[919, 952]], [[919, 797]]]   # 10th answer box (Purple) | 10th biggest contour [in purple]
# ]

contours = [
    [[[441, 468]], [[441, 623]], [[640, 622]], [[639, 467]]],  # 3th answer box (Blue) | Biggest Contour [in blue] kiri atas | kiri bawah | kanan bawah | kanan atas |
    [[[441, 139]], [[441, 294]], [[640, 293]], [[639, 138]]],  # 1st answer box (Green) | 2nd biggest contour [in green] |
    [[[441, 797]], [[441, 952]], [[640, 951]], [[638, 796]]],  # 5th answer box (Red) | 3rd biggest contour [in red] |
    [[[441, 304]], [[442, 459]], [[640, 458]], [[639, 303]]],  # 2nd answer box (Gray) | 4th biggest contour [in gray] |
    [[[441, 633]], [[442, 788]], [[640, 787]], [[639, 632]]],  # 4th answer box (Blue ish gray) | 5th biggest contour [in blue-ish gray] |
    [[[722, 138]], [[722, 294]], [[919, 294]], [[919, 138]]],  # 6nd answer box (Blue ish gray) | 6th biggest contour [in blue-ish gray] | 
    [[[722, 467]], [[722, 623]], [[919, 623]], [[918, 467]]],  # 8th answer box (Gray) | 7th biggest contour [in gray] |
    [[[721, 633]], [[722, 788]], [[919, 788]], [[919, 632]]],  # 9th answer box (Yellow) | 8th biggest contour [in yellow] |
    [[[722, 303]], [[722, 459]], [[919, 459]], [[919, 303]]],  # 7th answer box (Pink) | 9th biggest contour [in pink] |
    [[[722, 797]], [[722, 952]], [[919, 952]], [[919, 797]]]   # 10th answer box (Purple) | 10th biggest contour [in purple] |
]

# Extract the first sub-array from each contour
first_sub_arrays = [contour[0][0] for contour in contours]

# Split the list into the first 5 elements and the last 5 elements
first_half = first_sub_arrays[:5]
second_half = first_sub_arrays[5:]

# Sort each half by the y-coordinate
first_half_sorted = sorted(first_half, key=lambda point: point[1])
second_half_sorted = sorted(second_half, key=lambda point: point[1])

# Combine the sorted halves
sorted_first_sub_arrays = first_half_sorted + second_half_sorted

print("The sorted array of the first sub-arrays based on y-coordinate is:")
print(sorted_first_sub_arrays)