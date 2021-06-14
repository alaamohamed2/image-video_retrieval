import rgb_feature
import searcher_histo
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--index", default="index1.csv",
                help="Path to where the computed index will be stored")
ap.add_argument("-q", "--query", default="query/0002_c2s1_068496_01.jpg",
                help="Path to the query image")
ap.add_argument("-r", "--result-path", default="./test_images",
                help="Path to the result path")
args = vars(ap.parse_args())

rf = rgb_feature.ColorDescriptor((8, 8, 8))

# load the query image and describe it

query = cv2.imread(args["query"])
features = rf.describe(query)
myWindow = cv2.resize(query,(960,960))
cv2.imshow("query",myWindow)
# execute the serch
s = searcher_histo.Searcher(args["index"])
results = s.search(features)

i = 0
for (score, resultID) in results:
    print("ResultID ", resultID)
    print(args["index"]+"/"+resultID)
    result = cv2.imread(resultID)
    cv2.imshow("Result", result)
    cv2.imwrite("Result/"+"result" + str(i) + ".jpg", result)
    i = i + 1
    cv2.waitKey(0)
