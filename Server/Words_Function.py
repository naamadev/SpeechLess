import mediapipe as mp # ספריה לראיה ממוחשבת  לצורך זיהוי פנים וידיים
import numpy as np # עבודה על מערכים קריטי ללמידת מכונה
import cv2 # ספריית קוד פתוח לזיהוי פנים ועיבוד תמונה
import pandas as pd # עבודה על קבצים קריאה כתיבה וכו
import os# מאפשר ליצור אינטראקציה עם מספר פונקציות של מערכת ההפעלה,עבודה עם נתיבי קבצים
from sklearn.model_selection import train_test_split #   אלגורתמים + משמש לבניית מודלים של למידת מכונה
from keras.utils import to_categorical # משמש ללמידה עמוקה ולבניית השכבות במודלים
from scipy import stats # היא ספריית קוד פתוח המשמשת לפתרון בעיות מתמטיות, מדעיות, הנדסיות וטכניות
from matplotlib import pyplot as plt # היא ספרייה מקיפה ליצירת הדמיות סטטיות


# Mediapipe Holistic הוא אחד מהצינורות המכילים רכיבי פנים, ידיים ותנוחה 
#מודל הולסטי 
mp_holistic = mp.solutions.holistic      
#כלי עזר לציור
mp_drawing = mp.solutions.drawing_utils

def mediapipe_detection(img, mp_holistic):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # המרת צבע BGR 2 RGB
    # המרת הצבע הכרחית עובר מודל ה mediapipe, ככה הוא עובד 
    img.flags.writeable = False# תמונה כבר לא ניתנת לכתיבה
    res = mp_holistic.process(img)# לבצע חיזוי 
    img.flags.writeable = True  # התמונה ניתנת לכתיבה
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)#  המרת צבע בחזרה RGB 2 BGR
    return img, res

def holistic_drawing(img, holistic_res):
    # צייר חיבורי פנים
    # mp_drawing.draw_landmarks(img, holistic_res.face_landmarks, mp_holistic.FACEMESH_TESSELATION, 
    #                          mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), 
    #                          mp_drawing.DrawingSpec(color=(80,256,120), thickness=1, circle_radius=1)
    #                          ) 
    # צייר חיבורי תנוחה
    mp_drawing.draw_landmarks(img, holistic_res.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(200,50,50), thickness=2, circle_radius=4), #  שורה ראשונה נקודות ושניה קווים,הוספת עיצוב וסטייל
                             mp_drawing.DrawingSpec(color=(200,25,25), thickness=2, circle_radius=2)
                             ) 
       # צייר חיבורים ביד שמאל
    mp_drawing.draw_landmarks(img, holistic_res.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(25,25,200), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(50,50,200), thickness=2, circle_radius=2)
                             ) 
     # צייר חיבורים ביד ימין
    mp_drawing.draw_landmarks(img, holistic_res.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(25,25,200), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(50,50,200), thickness=2, circle_radius=2)
                             )
    
def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    # החזיר 33 נקודות ציון עם 4 ערכים
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, lh, rh])
#אפשר לראות כמה נק' ציון ע"י len(results.right_hand_landmarks.landmark) אחרי שנתפס בפריים כמובן