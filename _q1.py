
# info2vectors --input test.vectors.txt.bin --output test.vectors.bin --use-pipe-from train.vectors.bin
# vectors2classify --training-file examples/train.vectors --testing-file examples/test.vectors --trainer "new DecisionTreeTrainer(20)" > DecisionTree.20.stdout 20> DecisionTree.20.stderr && cat DecisionTree.20.stdout
# classify --testing-file test_vectors.binary --classifier q2e_classifier --report test:accuracy test:confusion test:raw > q2e.stdout2 2> q2etest.stderr2
# vectors2classify --training-file examples/train.vectors.bin --testing-file examples/test.vectors.bin --trainer DecisionTree > DecisionTree.bin.stdout 2> DecisionTree.bin.stderr
# vectors2train --training-file training_vectors.binary --trainer MaxEnt --output-classifier q2e_classifier --report train:accuracy train:confusion > q2e.stdout 2>q2e.stderr


# The command line is: q1.sh training_data test_data output_dir > acc_file


#imports
import sys,os

#arguments, variable declarations############################################################
training_data = sys.argv[1]
test_data = sys.argv[2]
output_dir = sys.argv[3]
train_vectors = "train"
test_vectors = "test"
total_classes = [] #initializing up top for visibility

#parse through training data and find out how many classes there are, map them in a file#####
total_classes = []
training_data = open(training_data,'r')
for line in training_data.readlines():
	line = line.split()
	classification = line[1]
	total_classes.append(classification) #appending to list, rather than adding to set (quicker)
total_classes=set() #remove duplicates
total_classes=list(total_classes) #back to list for indexing
i=1
class_map=open(output_dir+"/class_map","w")
for classification in total_classes:
	class_map.write(classification,i,"\n")
	i+=1
class_map.close()
#############################################################################################
#create training and test vectors############################################################


#loop through classes########################################################################
i=1
for classification in total_classes: #
	classifier_name = str(i)+"_vs_all"
	i+=1
	create_training_vectors = "info2vectors --input "+training_data+" --output "+classifier_name+"/"+train_vectors
	create_test_vectors = "info2vectors --input "+test_data+" --output "+classifier_name+"/"+test_vectors + " --use-pipe-from "+classifier_name+"/"+train_vectors
	create_classifier = "vectors2train --training-file "+classifier_name+"/"+train_vectors+" --trainer MaxEnt --output-classifier "+classifier_name+"/"+classifier_name+" --report train:raw > "+classifier_name+"/"+classifier_name+".stdout2 2>"+classifier_name+"/"+classifier_name+".stderr2"
	classify = "classify --testing-file "+test_vectors+" --classifier "+classifier_name+" --report test:raw  > "+classifier_name+"/"+classifier_name+".stdout 2> "+classifier_name+"/"+classifier_name+".stderr"
	os.popen(create_training_vectors)
	os.popen(create_test_vectors)
	os.popen(create_classifier)
	os.popen(classify)
# 