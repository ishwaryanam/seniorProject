
#for pipeline w/ model
import sys
'''
the Plan:

Take 2 files from command line, file1 #secs file2 #secs 

	- by default take last and first seconds 
 
 Merge the 2 audios to use as the input  

Opencv – good at handling video files and merging, find an audio alternative? 

Make a joint github in python - Create a merging tool based on user defined segments that will merge based on like opencv 
 
 '''
 



def main():
    file1 = sys.argv[1] #28 seconds
    file1_seconds = sys.argv[2]
    file2 = sys.argv[3] #23 seconds
    file2_seconds = sys.argv[4]
    
    print(file1)
    print(file1_seconds)
    print(file2)
    print(file2_seconds)

main()