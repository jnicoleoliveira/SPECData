def recurse(list, i):
    if(i == len(list)):
        return

    new_list = []
    for j in range(i, len(list)):
        new_list.append(list[j])
        print new_list
    recurse(list, i+1)

#test = [1, 2, 3, 4, 5, 6]
#recurse(test, 0)

from tests.example.time_warping_combination import TimeWarpExperiment

timewarp = TimeWarpExperiment(145)
#timewarp.do_the_time_warp()
timewarp.find_lowest()
#print timewarp.min_distance
#print timewarp.min_path
#print timewarp.combination_list