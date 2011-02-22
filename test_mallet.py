
# info2vectors --input test.vectors.txt.bin --output test.vectors.bin --use-pipe-from train.vectors.bin
# vectors2classify --training-file examples/train.vectors --testing-file examples/test.vectors --trainer "new DecisionTreeTrainer(20)" > DecisionTree.20.stdout 20> DecisionTree.20.stderr && cat DecisionTree.20.stdout
# classify --testing-file test_vectors.binary --classifier q2e_classifier --report test:accuracy test:confusion test:raw > q2e.stdout2 2> q2etest.stderr2
# vectors2classify --training-file examples/train.vectors.bin --testing-file examples/test.vectors.bin --trainer DecisionTree > DecisionTree.bin.stdout 2> DecisionTree.bin.stderr
# vectors2train --training-file training_vectors.binary --trainer MaxEnt --output-classifier q2e_classifier --report train:accuracy train:confusion > q2e.stdout 2>q2e.stderr


# The command line is: q1.sh training_data test_data output_dir > acc_file

import sys,os
training_data = sys.argv[1]
test_data = sys.argv[2]
output_dir = sys.argv[3]

train_vectors = training_data.replace(".txt","vectors")
test_vectors = test_data.replace(".txt","vectors")
classifier_name = "a_classifier"

create_training_vectors = "info2vectors --input "+training_data+" --output "+train_vectors
create_test_vectors = "info2vectors --input "+test_data+" --output "+test_vectors + " --use-pipe-from "+train_vectors
create_classifier = "vectors2train --training-file "+train_vectors+" --trainer MaxEnt --output-classifier "+classifier_name+" --report train:raw > "+classifier_name+".stdout 2>"+classifier_name+".stderr"
classify = "classify --testing-file "+test_vectors+" --classifier "+classifier_name+" --report test:raw  > "+classifier_name+".stdout 2> "+classifier_name+".stderr"

os.popen(create_training_vectors)
os.popen(create_test_vectors)
os.popen(create_classifier)
os.popen(classify)