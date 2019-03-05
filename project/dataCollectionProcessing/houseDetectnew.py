# Code adapted from Tensorflow Object Detection Framework
# https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb
# Tensorflow Object Detection Detector

import numpy as np
import tensorflow as tf
import cv2
import time
import csv

class DetectorAPI:
    def __init__(self, path_to_ckpt):
        self.path_to_ckpt = path_to_ckpt

        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.path_to_ckpt, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        self.default_graph = self.detection_graph.as_default()
        self.sess = tf.Session(graph=self.detection_graph)

        # Definite input and output Tensors for detection_graph
        self.image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        # Each box represents a part of the image where a particular object was detected.
        self.detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        # Each score represent how level of confidence for each of the objects.
        # Score is shown on the result image, together with the class label.
        self.detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        self.detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        self.num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

    def processFrame(self, image):
        # Expand dimensions since the trained_model expects images to have shape: [1, None, None, 3]
        image_np_expanded = np.expand_dims(image, axis=0)
        # Actual detection.
        start_time = time.time()
        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})
        end_time = time.time()

        print("Elapsed Time:", end_time-start_time)

        im_height, im_width,_ = image.shape
        boxes_list = [None for i in range(boxes.shape[1])]
        for i in range(boxes.shape[1]):
            boxes_list[i] = (int(boxes[0,i,0] * im_height),
                        int(boxes[0,i,1]*im_width),
                        int(boxes[0,i,2] * im_height),
                        int(boxes[0,i,3]*im_width))

        return boxes_list, scores[0].tolist(), [int(x) for x in classes[0].tolist()], int(num[0])

    def close(self):
        self.sess.close()
        self.default_graph.close()

if __name__ == "__main__":
    model_path = '/Users/levistringer/Documents/GitHub/Projects/anomaly-detection/frozen_inference_graph.pb' # path to frozen_interface_graph.pb
    odapi = DetectorAPI(path_to_ckpt=model_path)
    threshold = 0.50
    new_count = 0
    indices = []
    for count in range(0, 1001):
        print("Beginning round " + str(count))
        imageIn = '/Users/levistringer/Documents/GitHub/Projects/anomaly-detection/project/data/Street-View/{}_streetview.jpeg'.format(count) # path to housing images, put this in a different folder than working directory
        image = cv2.imread(imageIn)
        # image = cv2.resize(image, (350, 350))
        boxes, scores, classes, num = odapi.processFrame(image)
        print (classes)
        print (scores)
        maxthresh = 0
        # Visualization of the results of a detection.
        for i in range(len(boxes)):
             # Class 20 represents house
             if classes[i] == 20 and scores[i] > threshold:
                 if scores[i] > maxthresh:
                     maxthresh = scores[i]
                     index = i
        
        if classes[index] == 20:      
            indices.append(count)
            box = boxes[index]
            # cv2.rectangle(image,(box[1],box[0]),(box[3],box[2]),(255,0,0),2)
            x = box[1]
            y = box[0]
            w = box[3]
            h = box[2]
            new_img=image[y:h,x:w]
            cv2.imwrite('/Users/levistringer/Documents/GitHub/Projects/anomaly-detection/project/data/cropped/' + str(new_count) +'_streetview' + '.jpeg', new_img)
            cv2.waitKey()
            new_count += 1
    print(indices)
    ind_Out = open("indices.txt", "w")
    for number in indices:
        ind_Out.write(number)
        ind_Out.write(",")
    ind_Out.close()
    #Save indices into a text file 


        # cv2.imshow("preview", new_img)
        # key = cv2.waitKey(1)
        # if key & 0xFF == ord('q'):
            # cv2.destroyAllWindows()
            # break
