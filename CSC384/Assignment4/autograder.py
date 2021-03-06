"""This is the main program file for the auto grader program.
The auto grader assumes that the following files are in the same directory as the autograder:
  - autotraining.txt  --> file of tagged words used to train the HMM tagger
  - autotest.txt      --> file of untagged words to be tagged by the HMM
  - autosolution.txt  --> file with correct tags for autotest words
This auto grader generates a file called results.txt that records the test results.
"""
import os
import time
if __name__ == '__main__':

    start_time = time.time()
    # Invoke the shell command to train and test the HMM tagger
    print("Training on autotraining.txt, running tests on autotest.txt. "
          "Output --> autooutput.txt")

    #os.system("python3 tagger.py -d autotraining.txt -t autotest.txt -o autooutput.txt")
    os.system("python3 tagger.py -d training1.txt training2.txt training3.txt -t test10.txt -o myoutput.txt")

    # Compare the contents of the HMM tagger output with the reference solution.
    # Store the missed cases and overall stats in results.txt

    #with open("autooutput.txt", "r") as output_file, \
         #open("autosolution.txt", "r") as solution_file, \
         #open("results.txt", "w") as results_file:

    with open("myoutput.txt", "r") as output_file, \
         open("training10.txt", "r") as solution_file, \
         open("myresults.txt", "w") as results_file:
        # Each word is on a separate line in each file.
        output = output_file.readlines()
        solution = solution_file.readlines()
        total_matches = 0

        # generate the report
        for index in range(len(output)):
            if output[index] != solution[index]:
                results_file.write(f"Line {index + 1}: "
                                   f"expected <{solution[index].strip()}> "
                                   f"but got <{output[index].strip()}>\n")
            else:
                total_matches = total_matches + 1

        # Add stats at the end of the results file.
        results_file.write(f"Total words seen: {len(output)}.\n")
        results_file.write(f"Total matches: {total_matches}.\n")

    end_time = time.time()
    total_time = end_time - start_time

    accuracy = total_matches*100/len(output)

    print("Accuracy: " + str(accuracy) + "%")
    print("Total time: " + str(total_time))