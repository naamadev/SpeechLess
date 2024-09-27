from Words_Function import *
# # נתיב עבור נתונים מיוצאים, מערכים numpy
DATA_PATH = os.path.join("Words_Detection\Data")
# # פעולות שאנו מנסים לזהות
labels = np.array(['hello', 'thanks','sorry','good morning','a','b','c'])
# # נתונים בשווי ארבעים סרטונים
num_seqs = 40 
# # אורך הסרטונים יהיה 30 פריימים
seq_len = 30

for label in labels:
    for seq in range(num_seqs):
        try:
            os.makedirs(os.path.join(DATA_PATH, label, str(seq)))
        except:
            pass


# איסוף נתונים 40 פריימים
# cap = cv2.VideoCapture(0)
# with mp_holistic.Holistic(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as holistic_model:
#     break_all = 0
#     for label in labels:
#         for seq in range(num_seqs):
#             for frame_num in range(seq_len):
#                 _, frame = cap.read()
#                 flipped_frame = cv2.flip(frame, 1)
#                 img, results = mediapipe_detection(flipped_frame, holistic_model)
#                 holistic_drawing(img, results)
                
#                 #  Apply wait logic
#                 if frame_num == 0:
#                     if seq == 0:
#                         # Show to screen, זה כתיבה למסך שיהיה מעקב נח אחר מה שקורה
#                         cv2.putText(img, 'Press a Key to Start Collection for {} Video Number {}'.format(label, seq), (120,200), #מיקום הטקסט לפי פיקסלים במסך, X ו Y
#                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255, 0), 4, cv2.LINE_AA)# סוג הגופן שבו יוצג הטקסט,הגודל,הצבע,רוחב הגופן
#                         cv2.imshow('OpenCV Cam Feed', img)
#                         cv2.waitKey(0)
#                     cv2.putText(img, 'STARTING COLLECTION', (120,300), 
#                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255, 0), 4, cv2.LINE_AA)
#                     cv2.putText(img, 'Collecting frames for {} Video Number {}'.format(label, seq), (15,12), 
#                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
#                     cv2.imshow('OpenCV Cam Feed', img)
#                     cv2.waitKey(2000)

#                 else: 
#                     cv2.putText(img, 'Collecting frames for {} Video Number {}'.format(label, seq), (15,12), 
#                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
#                     # Show to screen
#                     cv2.imshow('OpenCV Cam Feed', img)
                
#                 # Export keypoints
#                 keypoints = extract_keypoints(results) #הפונקציה שכתבתי בדף ה functions 
#                 npy_path = os.path.join(DATA_PATH, label, str(seq), str(frame_num))#מספר סרטון ומספר פריים
#                 np.save(npy_path, keypoints)
                
#                 if cv2.waitKey(10) & 0xFF == ord('q'):
#                     break_all = 1
#                     break
#             if break_all:
#                 break
#         if break_all:
#                 break
# cap.release()
# cv2.destroyAllWindows()
# cv2.waitKey(1)

# קידוד תוויות
label_map = {label:num for num, label in enumerate(labels)}# דרך פשוטה יותר לגשת ולספור פריטים ואיסוף נתונים
#לטעון מידע
sequences, words = [], []  # יוצרים שני מערכים רצפים ותווים
#X -- את התכונות של הנתונים,מייצג רצפים- סרטונים
#Y -- מייצג תוויות
for label in labels:# מעבר על הפעולות
    for seq in np.array(os.listdir(os.path.join(DATA_PATH, label))).astype(int): #מעבר על הסרטונים,בתוך תיקית הנתונים יצור תיקיה לפעולה
        # print(label, seq)
        window = [] # מערך לייצג את כל הפריימים השונים עבור סרטון מסוים
        for frame_num in range(seq_len):#מעבר על הפריימים
            res = np.load(os.path.join(DATA_PATH, label, str(seq), "{}.npy".format(frame_num)))
            window.append(res)#צרף את כל הפריימים לכאן , וזה וידאו אחד
        sequences.append(window)# את הוידו צרף לכאן יחד עם כולם
        words.append(label_map[label])

