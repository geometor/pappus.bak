from geometor.utils import *
from geometor.model import *
from geometor.render import *

sp.init_printing()
from geometor.pappus import *
from itertools import permutations

#  fig, (ax0, ax1) = plt.subplots(ncols=2, figsize=(7, 4))
#  fig, ax = plt.subplots(2, 1)
fig, (ax, ax_btm) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [10, 1]})
ax.set_aspect('equal')

NAME = 'pappus'
NAME += input(f'\nsession name: {NAME}')

pappus_lines = []
Ax = 3
Bx = 5/2
B1 = point(0, 1, classes=['B', 'start'])
B2 = point(3/2, 1, classes=['B', 'start'])

for perm_id in range(6):
    print('PERMUTATION: ', perm_id)
    print()


    A, B = pappus_start(Ax, B1, B2, Bx)
    B_perms = list(permutations(B))

    B = B_perms[perm_id]

    # add pt types based on new permuation order
    print_log('\nB points:')
    for i, pt in enumerate(B):
        pt.classes.append(types[i])
        print(i, pt, pt.classes)

    set_meet(0, 1, A, B)
    set_meet(1, 2, A, B)
    set_meet(2, 0, A, B)

    meets = get_pts_by_class('meet')

    if len(meets) >= 2:
        pappus_line = line(meets[0], meets[1], classes=['blue', 'pappus'])
        pappus_lines.append(pappus_line)
        add_element(pappus_line)
    else:
        print('no pappus line')
    if len(meets) == 3:
        pappus_line.pts.add(meets[2])
        print('collinear: ', sp.Point.is_collinear(*meets))

    #  triangle_sq = add_polygon(polygon(get_pts_by_class('square'), classes=['yellow']))
    #  triangle_cir = add_polygon(polygon(get_pts_by_class('circle'), classes=['cyan']))
    #  triangle_dia = add_polygon(polygon(get_pts_by_class('diamond'), classes=['magenta']))

    print_log(f'\nPLOT: {NAME}')
    limx, limy = get_limits_from_points(pts)
    limx, limy = adjust_lims(limx, limy)
    bounds = set_bounds(limx, limy)

    ax.clear()
    ax_btm.clear()

    ax.axis('off')
    ax_btm.axis('off')
    ax.set_aspect('equal')
    plt.tight_layout()

    title = f'G E O M E T O R • pappus • perm: {perm_id}'
    fig.suptitle(title, fontdict={'color': '#960', 'size':'small'})

    folder = f'{NAME}/{perm_id}'
    print_log('\nPlot Sequence')
    build_sequence(folder, ax, ax_btm, history, bounds)

    print_log('\nPlot Harmonic Ranges')

    print_log(f'\nPERM: {perm_id}')
    print_log(f'    elements: {len(elements)}')
    print_log(f'    points:   {len(pts)}')


# ALL *************************
print_log(f'\nShow All:')

A, B = pappus_start(Ax, B1, B2, Bx)

print('\STAR POINTS:')
pappus_ints = set()
for i, el in enumerate(pappus_lines):
    add_element(el)
    if i > 0:
        p1 = el
        p0 = pappus_lines[i-1]
        ints = p1.intersection(p0)
        if ints:
            pt = ints[0]
            print(f'    {i}  {pt}')
            pid = find_pt_index(pt)
            #  print(f'         {pid}')
            if pid > -1:
                pt = pts[pid]
                print(f'    {pid}  {pt}')
                pappus_ints.add(pt)

print_log(f'\nPappus Intersections:')
for pt in pappus_ints:
    print(' • ', pt)

star_pts = []
for i, pt in enumerate(pappus_ints):
    if len(pt.elements) == 3:
        star_pts.append(pt)
        pt.classes.append('star')
        print(i, len(pt.elements), pt)

print_log(f'\nStar Points:')
for pt in star_pts:
    print(' • ', pt)

#  print('\nPOINTS:')
#  for i, pt in enumerate(pts):
    #  print(f'    {i}  {pt}')
if len(star_pts) == 2: 
    add_element(line(star_pts[0], star_pts[1], classes=['pink']))

# ANALYZE ***************************
print_log(f'\nANALYZE: ALL')

harmonics = []
for el in get_elements_lines():
    result  = analyze_harmonics(el)
    harmonics.extend(result)

print_log('\nANALYZE Summary:')
print_log(f'    harmonics: {len(harmonics)}')

limx, limy = get_limits_from_points(pts)
limx, limy = adjust_lims(limx, limy)
bounds = set_bounds(limx, limy)

# ANALYZE ***************************
print_log(f'\PLOT: ALL')

ax.clear()
title = f'G E O M E T O R • pappus • all'
ax.set_title(title, fontdict={'color': '#960', 'size':'small'})
ax.axis(False)

folder = f'{NAME}/all'
print_log('\nPlot Sequence')
build_sequence(folder, ax, ax_btm, history, bounds)

print_log('\nPlot Harmonic Ranges')
#  folder += '/ranges'
plot_ranges(folder, ax, ax_btm, history, harmonics, bounds)
plot_all_ranges(folder, ax, ax_btm, history, harmonics, bounds)

print_log(f'\nCOMPLETE: {NAME}')
print_log(f'    elements: {len(elements)}')
print_log(f'    points:   {len(pts)}')
print_log(f'    ranges:  {len(harmonics)}')
plt.show()
