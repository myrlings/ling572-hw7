import sys
from operator import itemgetter

# functions
def read_in_sys(output_dirname, class_map, filename):
    sys_data = {}
    for index in class_map:
        for other_index in class_map:
            if index != other_index:
                # sys_filename = output_dirname  + index + "-vs-" + other_index +"/"+ filename
                sys_filename = output_dirname + filename
                sys_file = open(sys_filename, 'r')
                for line in sys_file:
                    line_array = line.split()
                    if not line_array[0] in sys_data:
                        sys_data[line_array[0]] = {}
                    if line_array[1] == "1":
                        # store the answer if this is it
                        sys_data[line_array[0]]["goldClass"] = class_map[index]
                    prob1 = line_array[2]
                    prob2 = line_array[3]
                    pos_prob = ""
                    if prob1.startswith("-"):
                        pos_prob = prob2
                    else:
                        pos_prob = prob1
                    pos_prob_split = pos_prob.split(":")
                    sys_data[line_array[0]][class_map[index]] = float(pos_prob_split[1])
    return sys_data


		# def read_in_sys(output_dirname, class_map, filename):
		#     sys_data = {}
		#     for index in class_map:
		#         sys_filename = output_dirname + "/" + index + "-vs-all/" + filename
		#         sys_file = open(sys_filename, 'r')
		#         for line in sys_file:
		#             line_array = line.split()
		#             if not line_array[0] in sys_data:
		#                 sys_data[line_array[0]] = {}
		#             if line_array[1] == "1":
		#                 # store the answer if this is it
		#                 sys_data[line_array[0]]["goldClass"] = class_map[index]
		#             prob1 = line_array[2]
		#             prob2 = line_array[3]
		#             pos_prob = ""
		#             if prob1.startswith("-"):
		#                 pos_prob = prob2
		#             else:
		#                 pos_prob = prob1
		#             pos_prob_split = pos_prob.split(":")
		#             sys_data[line_array[0]][class_map[index]] = float(pos_prob_split[1])
		#     return sys_data

def print_sys(sys_data, output_dirname):
    sys_file = open(output_dirname, 'w')
    for instance in sys_data:
        print sys_file
        print instance
        print "sys_data[instance]"
        print sys_data[instance]
        sys_file.write(instance + " ")
        sys_file.write(sys_data[instance]["goldClass"] + " ")
        temp = sys_data[instance].pop('goldClass')
        sorted_votes = sorted(sys_data[instance].iteritems()\
        , key=itemgetter(1), reverse=True)
        temp2 = sorted_votes[0][0]
        for tup in sorted_votes:
            sys_file.write(tup[0] + " ")
            sys_file.write(str(tup[1]) + " ")
        sys_file.write("\n")
        sys_data[instance]['winner'] = temp2
        sys_data[instance]['goldClass'] = temp

def print_acc(sys_data, class_map):
    counts = {}
    num_right = 0
    for actuallabel in class_map.values():
        sys.stdout.write("\t" + actuallabel)
        counts[actuallabel] = {}
        for expectedlabel in class_map.values():
            counts[actuallabel][expectedlabel] = 0
    for instance in sys_data:
        actual_label = sys_data[instance]['goldClass']
        expected_label = sys_data[instance]['winner']
        counts[actual_label][expected_label] += 1
        if actual_label == expected_label:
            num_right += 1

    sys.stdout.write("\n")
    for actuallabel in class_map.values():
        sys.stdout.write(actuallabel)
        for expectedlabel in class_map.values():
            sys.stdout.write("\t" + str(counts[actuallabel][expectedlabel]))
        sys.stdout.write("\n")
    accuracy = float(num_right) / len(sys_data)
    return accuracy
# main
output_dirname = sys.argv[1]

#bad code alert!
root_dirname = output_dirname.split("/")[0]

class_map_file = open(root_dirname + "/class_map", 'r')
class_map = {}
for line in class_map_file:
    line_array = line.split()
    class_map[line_array[1]] = line_array[0]

# training accuracy
sys_data_train = read_in_sys(output_dirname, class_map, "train_output_pared")
# the file this creates will get overwritten, terrible way to do it
print_sys(sys_data_train, output_dirname + "train_sys_output")
print "\nConfusion matrix for the training data:"
print "row is the truth, column is the system output\n"
training_acc = print_acc(sys_data_train, class_map)
print "Training accuracy:", training_acc


sys_data = read_in_sys(output_dirname, class_map, "sys_output")
print_sys(sys_data, output_dirname+"/final_sys_output")
print "\nConfusion matrix for the testing data:"
print "row is the truth, column is the system output\n"
testing_acc = print_acc(sys_data, class_map)
print "\n"
print "Testing accuracy:", testing_acc
