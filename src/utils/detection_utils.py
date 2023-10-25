import cv2
import mss
import numpy as np
import Monitor_Info
import Table

# Function to predict bboxes based on confidence threshold
def predict(model,img, confidence_threshold):
    results = model.predict(img, confidence_threshold, verbose=False)
    return results

# Function to find bboxes from an image   
def find_boxes(results,crop_img, model):
    # Iterate through model predictions
    for r in results:
        boxes = r.boxes
        boxes_conf = r.boxes.conf
        c = boxes.cls
        vals = boxes.xyxy
        
        # As long as there are more than 1 box, proceed with processing
        if len(c) > 0:
            hand = []
            for i in range(len(c)):
                # Retrieve predicted cards
                cls = int(c[i].item())
                name = model.names[cls]
                conf = str(round(boxes_conf[i].item(),2))
                #print("conf:",conf)
                
                # Draw bboxes based on found objects and add name
                x1 = int(vals[i][0].item())
                y1 = int(vals[i][1].item())
                x2 = int(vals[i][2].item())
                y2 = int(vals[i][3].item())
                cv2.rectangle(crop_img,(x1,y1),(x2,y2),(0, 0, 255),3)
                cv2.putText(crop_img, name, (x1, y1-25), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                cv2.putText(crop_img, name, (x1, y1-25), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
                cv2.putText(crop_img, conf, (x1+50, y1-25), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                cv2.putText(crop_img, conf, (x1+50, y1-25), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)
                
                # Match card with value and calculate the sum
                card = Table.get_card_string(cls)
                #print("card: ",card)
                value = Table.get_card_value(card)
                #print("value: ",value)
                hand.append(value)
                
            Sum = sum(hand)
            print("sum: ",Sum,"\n") 