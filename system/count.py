from xml.sax.saxutils import escape
from collections import defaultdict
import six.moves.urllib as urllib
from io import StringIO
from PIL import Image
import numpy as np
import tarfile
import zipfile
import string

import json
import time
import sys
import os
import glob
import tensorflow.compat.v1 as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
tf.enable_resource_variables()
import cv2






from utils import label_map_util
from utils import visualization_utils as vis_util

sys.path.append("..")






class CountEggs():

    def __init__(self, folder='teste_1', model_name="inference"):
        self.folder = folder
        
        print(model_name.lower())
        self.PATH_TO_CKPT = "config/"+model_name.lower()+".pb"
        self.pb_fname = model_name.lower()
        self.PATH_TO_LABELS = "config/label_map.pbtxt"
        self.num_classes = 1

        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        print("Modelo pronto")
        self.label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(self.label_map, max_num_classes=self.num_classes, use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)

    def load_image_into_numpy_array(self, image):
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
            (im_height, im_width, 3)).astype(np.uint8)
        
    def run_inference_for_single_image(self, image, graph):
        with graph.as_default():
            with tf.Session() as sess:
                # Get handles to input and output tensors
                ops = tf.get_default_graph().get_operations()
                all_tensor_names = {
                    output.name for op in ops for output in op.outputs}
                tensor_dict = {}
                for key in [
                    'num_detections', 'detection_boxes', 'detection_scores',
                    'detection_classes', 'detection_masks'
                ]:
                    tensor_name = key + ':0'
                    if tensor_name in all_tensor_names:
                        tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                            tensor_name)
                if 'detection_masks' in tensor_dict:
                    # The following processing is only for single image
                    detection_boxes = tf.squeeze(
                        tensor_dict['detection_boxes'], [0])
                    detection_masks = tf.squeeze(
                        tensor_dict['detection_masks'], [0])
                  
                    # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                    real_num_detection = tf.cast(
                        tensor_dict['num_detections'][0], tf.int32)
                    detection_boxes = tf.slice(detection_boxes, [0, 0], [
                                              real_num_detection, -1])
                    detection_masks = tf.slice(detection_masks, [0, 0, 0], [
                                              real_num_detection, -1, -1])
                    detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                        detection_masks, detection_boxes, image.shape[0], image.shape[1])
                    detection_masks_reframed = tf.cast(
                        tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                    # Follow the convention by adding back the batch dimension
                    tensor_dict['detection_masks'] = tf.expand_dims(
                        detection_masks_reframed, 0)
                image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

                # Run inference
                output_dict = sess.run(tensor_dict,
                                      feed_dict={image_tensor: np.expand_dims(image, 0)})

                # all outputs are float32 numpy arrays, so convert types as appropriate
                output_dict['num_detections'] = int(
                    output_dict['num_detections'][0])
                output_dict['detection_classes'] = output_dict[
                    'detection_classes'][0].astype(np.uint8)
                output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
                output_dict['detection_scores'] = output_dict['detection_scores'][0]
                output_dict['size'] = image.shape
                if 'detection_masks' in output_dict:
                    output_dict['detection_masks'] = output_dict['detection_masks'][0]
        return output_dict
    
    def count(self):
        assert os.path.isfile(self.PATH_TO_CKPT)
        assert os.path.isfile(self.PATH_TO_LABELS)
        folders = [self.folder]
        for folder in folders:
            PATH_TO_TEST_IMAGES_DIR = os.path.join("res/", folder)
            print("Folder ", folder)
            TEST_IMAGE_PATHS = glob.glob(os.path.join(PATH_TO_TEST_IMAGES_DIR, "*.*"))
            assert len(TEST_IMAGE_PATHS) > 0, 'No image found in `{}`.'.format(PATH_TO_TEST_IMAGES_DIR)
            TEST_IMAGE_PATHS = TEST_IMAGE_PATHS
            dic = []
            
            for image_path in TEST_IMAGE_PATHS:
                print("Image ", image_path )
                image = Image.open(image_path)
                image_np = self.load_image_into_numpy_array(image)
                image_np_expanded = np.expand_dims(image_np, axis=0)
                output_dict = self.run_inference_for_single_image(image_np, self.detection_graph)
                dic.append(output_dict)

        num_ovos = 0
        posi_name = 0
        cont = 0
        for ex in dic:        
            data = []
            name_folder = "data"
            name_image = TEST_IMAGE_PATHS[posi_name][16:]
            path = "/home/rodrigo/"
            width = 640
            height = 480
            depth = 3
            segmented = 0
            database = "Unknow"
            label = "ovo"
            inner_template = string.Template("""\t<object>
            \t\t<name>""" + label + """</name>
            \t\t<pose>Unspecified</pose>
            \t\t<truncated>0</truncated>
            \t\t<difficult>0</difficult>
            \t\t<bndbox>
            \t\t\t<xmin>${xmin}</xmin>
            \t\t\t<ymin>${ymin}</ymin>
            \t\t\t<xmax>${xmax}</xmax>
            \t\t\t<ymax>${ymax}</ymax>
            \t\t</bndbox>
            \t</object>""")

            outer_template = string.Template("""<annotation>
            \t<folder>""" + name_folder + """</folder>
            \t<filename>""" + name_image + """</filename>
            \t<path>""" + path + """</path>
            \t<source>
            \t\t<database>Unknown</database>
            \t</source>

            \t<size>
            \t\t<width>""" + str(width) + """</width>
            \t\t<height>""" + str(height) + """</height>
            \t\t<depth>""" + str(depth) + """</depth>
            \t</size>
            \t<segmented>""" + str(segmented) + """</segmented>
            

            ${document_list}

            </annotation>
            """)
            index = []
            scores = [] 
            lista = []

            for i, score in enumerate(ex['detection_scores']): 
                if score > 0.5:
                    index.append(i)
                    scores.append(score)
                    num_ovos += 1
            
            i = 0

            im_width, im_height, _ = ex['size']

            for box in ex['detection_boxes'][index]:
                box
                obj = {}
                obj['label'] = 'ovo'
                obj['confidence'] = float("%.2f" % scores[i])
                xmin = box[0] * im_width
                ymin = box[1] * im_height
                ymax = box[3] * im_height
                xmax = box[2] * im_width
            
                data.append((ymin, xmin, ymax, xmax))
                
                obj['topleft'] = {  
                        'y': float(xmin),
                        'x': float(ymin)
                    }
                    
                obj['bottomright'] = {  
                        'y': float(xmax),
                        'x': float(ymax)
                    }
                lista.append(obj)
                i = i + 1
            
            print("Salvando")
            inner_contents = [inner_template.substitute(xmin=xmin, ymin=ymin, xmax=xmax, ymax=ymax) for (xmin, ymin, xmax, ymax) in data]
            result = outer_template.substitute(document_list='\n'.join(inner_contents))
            myfile = open(TEST_IMAGE_PATHS[posi_name][15:].split('.')[0] + '.xml', "w")
            myfile.write("res/"+result)
            myfile.close()    
            posi_name += 1



            

