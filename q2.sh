#!/bin/bash

python q2.py $@
output_dir=$3
map_file=$3"/class_map"

while read line
do
    set -- $line
    label=$1
    shift
    index=$1
    
    while read line2
    do
        set -- $line2
        label2=$1
        shift
        index2=$1
        if [ "$index" != "$index2" ] ; then
		        dirname=${output_dir}/${index}-vs-${index2}/
		        test_file=${dirname}test
		        train_file=${dirname}train
		        info2vectors --input $train_file --output ${dirname}train.vectors
		        info2vectors --input $test_file --output ${dirname}test.vectors --use-pipe-from ${dirname}train.vectors
		        # run vectors2train on train file
		        vectors2train --trainer MaxEnt --output-classifier ${dirname}mallet.model --training-file ${dirname}train.vectors --report train:raw  > ${dirname}train_output
		        # run classify with train model on test vectors
		        classify --classifier ${dirname}mallet.model --testing-file ${dirname}test.vectors --report test:raw > ${dirname}test_output

		        # turns out we only need sys output for test files
		        #grep "^\." <${dirname}train_output >${dirname}train_output_pared
		    		grep "^\." <${dirname}train_output >${dirname}train_output_pared
		        grep "^\." <${dirname}test_output >${dirname}sys_output
		        #cat ${dirname}train_output_pared ${dirname}test_output_pared >> ${dirname}sys_output
						python q2a.py $dirname
		   fi
    done <$map_file
done <$map_file
