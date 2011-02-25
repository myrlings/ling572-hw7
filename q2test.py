import sys
import os
import subprocess

###### functions

# get vectors
def get_vectors(data_filename):
    data_file = open(data_filename, 'r')

    instances = {}
    labels = set()
    all_features = set()
    for line in data_file:
        line_array = line.split()
        instance_name = line_array[0]
        label = line_array[1]
    
        instances[instance_name] = {}
        instances[instance_name]['_label_'] = label
        labels.add(label)
            
        features = line_array[2::2] # every other word in line starting with third
        values = line_array[3::2] # every other word in line starting with fourth
            
        for f, v in zip(features, values):
            all_features.add(f)
            if not (f in instances[instance_name]):
                instances[instance_name][f] = v
            else:
                instances[instance_name][f] += v
        
    data_file.close()
    return [instances, labels, all_features]


# create and output class map
# labels : a set of all possible labels
def get_class_map(labels):
    class_map = {}
    label_list = list(labels)

    for index in range(1, len(label_list)+1):
        class_map[str(index)] = label_list[index-1]

    return class_map

# create output directories for each m-vs-all
# output_dirname : the name of the directory to store them under
# class_map      : the numbers of the class labels
def create_dirs(output_dirname, class_map):
    dir_list = []
    if not os.path.exists(output_dirname) or not os.path.isdir(output_dirname):
        os.mkdir(output_dirname)
    cmap = open(output_dirname + "/class_map", 'w')
    for number in class_map:
        number = str(number)
        for second_number in class_map:
            second_number = str(second_number)
            if number != second_number:
                dirname = output_dirname + "/" + number + "-vs-" + second_number
                if not os.path.isdir(dirname):
                    os.mkdir(dirname)
        cmap.write(class_map[number] + " " + number + "\n")

# store train and test vectors in m-vs-all format
# vectors        : dictionary of vectors to be stored 
# dirname        : where to put the output files
# m              : the number of the current class label
# class_map      : dictionary of classes with their number
# filename       : place to store the new vectors
def store_vectors(vectors, dirname, m, n, class_map, filename):
    # open file
    temp_path = dirname + "/" + m + "-vs-" + n + "/" + filename
    output = open(temp_path, 'w')
    # loop through vectors
    for vector in vectors:
        # string for writing: instance name
        out_str = vector
        # string for writing: 1 if the class is the same, -1 if not
        if class_map[m] == vectors[vector]["_label_"]:
            out_str += " 1"
        else:
            out_str += " -1"
        # string for writing: add features and values
        for f in vectors[vector]:
            # skip _label_
            if f != "_label_":
                out_str += " " + f + " " + vectors[vector][f]
        # write line to file
        output.write(out_str + "\n")

def run_mallet(output_dirname, class_map):
    # in each directory, create a classifier using mallet
    #for index in class_map:
    if True:
        index = 1
        dirname = output_dirname
        dirname += "/" 
        dirname += str(index) 
        dirname += "-vs-all/"
        # run mallet commands for training results
        command = "info2vectors --input " + dirname + "train --output " + dirname + "train.vectors"
        p = subprocess.Popen(command, shell=True)
        command = "vectors2train --trainer MaxEnt --output-classifier "
        command += dirname + "mallet.model --training-file "
        command += dirname + "train.vectors --report train:raw"
        out = open(dirname + "/train_output", 'w')
        p = subprocess.Popen(command, shell=True, stdout=out)

        # run mallet commands for testing results
#        command = "info2vectors --input " + dirname + "test --output " + dirname + "test.vectors"
#        #command += " --use-pipe-from " + dirname + "train.vectors"
#        p = subprocess.Popen(command, shell=True)
#        command = "classify --classifier " + dirname + "mallet.model "
#        command += "--testing-file " + dirname 
#        command += "test.vectors --report test:raw"
#        test_out = open(dirname + "/test_output", 'w')
#        p = subprocess.Popen(command, shell=True, stdout=test_out)

###### main

# check for arguments
if len(sys.argv) < 4:
    sys.stderr.write("Arguments are: training_data test_data output_dir\n")
    sys.exit()

# import arguments
train_filename = sys.argv[1]
test_filename = sys.argv[2]
output_dirname = sys.argv[3]

# read in training vectors
train_list = get_vectors(train_filename)
# organize list into variables we need
train_vectors = train_list[0]
labels = train_list[1]
# read in test vectors
test_list = get_vectors(test_filename)
# organize list into variables we need
test_vectors = test_list[0]

# get class map fr list of labels
class_map = get_class_map(labels)
# create directory for each m-vs-n
# create_dirs(output_dirname, class_map)
# output train and test for the each m-vs-n
for index in class_map:
    for second_index in class_map:
        if index != second_index:
            # store_vectors(train_vectors, output_dirname, index, second_index, class_map, "train")
            store_vectors(test_vectors, output_dirname, index, second_index, class_map, "test")


# use the model from mallet to get probabilities for 1 and -1 of the class
#run_mallet(output_dirname, class_map)


# write the probabilities and winner to the sys_file in the dir
