from Words_Function import *
from Words_CreateData import *
from keras.models import load_model
from flask import Flask, request # ספריה לשרת

model = load_model('Words_Detection\sign4_lang_model.h5')
model.load_weights("Words_Detection\SLD_val_loss")

#לצד לקוח 
#json_model = model.to_json()
#with open('json_model.json', 'w') as json_file:
#    json_file.write(json_model)

# הדמיה של הסתברות
colors = [(245,117,16), (117,245,16), (16,117,245),(250,54,16), (180,78,16), (20,45,245),(210,20,16)]#מערך של צבעים עבור כל אחת מהפעולות
def prob_viz(res, actions, input_frame, colors):
    output_frame = input_frame.copy()# עותק של מסגרת אחת שישמש לציור המלבנים וההסתברות
    for num, prob in enumerate(res):
        #המלבן ממולא בצבע המתאים לפעולה, ורוחב וגובהו פרופורציונליים להסתברות החזויה של הפעולה.
        cv2.rectangle(output_frame, (0,60+num*40), (int(prob*100), 90+num*40), colors[num], -1)
        cv2.putText(output_frame, actions[num], (0, 85+num*40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2, cv2.LINE_AA)
        
    return output_frame#  הפונקציה מחזירה את מסגרת הפלט, המכילה כעת את ההסתברויות החזויות המוצגות עבור כל פעולה

#בדיקה בזמן אמת
import speech_recognition as sr
degel=0
sequence = [] # מערך לאיסוף 30 פריימים 
sentence = [] # שרשור התוצאות שהתקבלו מהמודל
predictions = []# מערך החיזוי
# נבדוק על 10 התחזיות האחרונות לוודא שכולן שם אותו דבר
threshold = 0.7 # נציג תוצאות רק אם הן מעל המספר הזה (בעברית סף)
ifyourecognizefirstletter=0 # דגל
capital=0
f = open("Words_Detection\Words.txt", "a")
f.write("Person A: ") 
f.close()
cap = cv2.VideoCapture(0)
# גישה ל mediapipe model 
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    # ברירת מחדל להגדיר את ערך הסף של רמת הביטחון ורמת המעקב (אם תזהה את האדם או לא) ל 0.5 שנע בין 0 ל1
    while cap.isOpened():

        # Read feed
        ret, frame = cap.read()# קרא את הפריים מהמצלמה 
        flipped_frame = cv2.flip(frame, 1)
        # Make detections התוצאות שהתקבלו עם הצינורות
        image, results = mediapipe_detection(flipped_frame, holistic)      
        
        # Draw landmarks - ציוני דרך, העיבוד של הצינורות שיוצג ויזואלית על הפריים
        # ע"י שלוש ממדים ביחס למצלמה רוחב,גובה ועומק והם בהתאמה X,Y,Z
        holistic_drawing(image, results)
        
        # 2. חילוץ נקודות מפתח
        keypoints = extract_keypoints(results)
        sequence.append(keypoints)
        sequence = sequence[-30:]# בוחר את שלושת האלמנטים האחרונים
        if len(sequence) == 30:
            # הפונקציה predict מצפה שהקלט יהיה בעל שלושה ממדים אבל הוא בעל 2
            # אומר שהוא יוסף בהתחלה  axis=0  מוסיף מימד נוסף ו expand_dims ולכן 
            res = model.predict(np.expand_dims(sequence, axis=0))[0]            
            predictions.append(np.argmax(res))
            
            
        #3. Viz logic
        #כדי לטפל במעבר בין התנועות שלא יזהה את זה גם כתנועה
            if np.unique(predictions[-10:])[0]==np.argmax(res): 
                if res[np.argmax(res)] > threshold: # הבדיקה מעל הסף?
                    
                    if len(sentence) > 0: # אתה לא המילה או האות הראשונה במערך
                        f = open("Words_Detection\Words.txt", "a") # פתיחת קובץ
                        # אם אתה שונה מהמילה או האות האחרונה במערך וגם אתה מילה
                        if labels[np.argmax(res)] != sentence[-1].lower() and len(labels[np.argmax(res)])>1:
                            sentence.append(labels[np.argmax(res)])
                            # כתיבה לקובץ עם רווח לפני ואחר
                            f.write(" "+sentence[-1]+" ")   # TypeError: can only concatenate str (not "type") to str   פתרנו על ידי שהוספנו המרה ל str
                            ifyourecognizefirstletter=0 # ז"א שפעם הבאה שיזהה אות היא האות הראשונה במילה שתשורשר   
                        else:
                            # אם אתה שונה מהאות או המילה האחורנה במערך וגם אתה אות
                            # כאשר מזהה אות משרשר עד לזיהוי מילה
                            if labels[np.argmax(res)] != sentence[-1].lower() and len(labels[np.argmax(res)]) ==1:
                                if  ifyourecognizefirstletter==0:# אתה האות הראשונה
                                    word=labels[np.argmax(res)]
                                    word=word.upper()  # ולכן נהפוך אותך לאות גדולה
                                    sentence.append(word)                            
                                    ifyourecognizefirstletter=1# הואת הבאה כבר לא תהפוך לאות גדולה ותשורשר עד לזיהוי מילה
                                else:       
                                    sentence.append(labels[np.argmax(res)])
                                f.write(sentence[-1]) # תכתוב לקובץ ללא רווח על מנת לשרשר

                    else: # אתה המילה הראשונה במערך
                        f = open("Words_Detection\Words.txt", "a")
                        if len(labels[np.argmax(res)])>1:
                            sentence.append(labels[np.argmax(res)])                            
                            sentence[0]=sentence[0].capitalize()#אז תכתוב את המילה כך שהאות הראשונה תהיה אות גדולה
                            f.write(sentence[-1]+" ") 
                        else:
                            word=labels[np.argmax(res)]
                            word=word.upper()  
                            sentence.append(word) 
                            f.write(sentence[-1]) 
                f.close()#לסגור את הקובץ


            if len(sentence) > 5: # עבור העיבוד שיוצג עם המשפט גדול מחמש
                sentence = sentence[-5:]# קח רק את חמשת האחרונים כדי לא להתמודד עם עיבוד גדול מידי

           # כלומר הסתברויות
            #image = prob_viz(res, labels, image, colors)
            
        cv2.rectangle(image, (0,0), (640, 40), (245, 117, 16), -1) #   ריבוע שיכיל את המצלמה ,2 נקודות ראשונות אומר שיכיל מקצה לקצה, הערך השלישי זה צבע ו-1 אור שיכיל את כולו
        cv2.putText(image, ' '.join(sentence), (3,30),cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)# תראה את המשפט את הריבוע
        # הערכים הם מיקום הגופן, גודל הגופן, צבע הגופן, רוחב וסוג

        # Show to screen
        cv2.imshow('OpenCV Feed', image)# הצגה על המסך את הפריים שנלכד והשם שנבחר לתת לו

        # Break gracefully
        if cv2.waitKey(10) & 0xFF == ord('q'):# ממתינה לאירוע מקלדת בזמן מוגדר של אלפית השניה 
           #הפעולה and בשיטת סיביות מחלץ 8 סיביות ובודק אם שווה לקוד האסקי שהתקבל
           #(כי watekey מחזיר מספר של 32 סיביות)
            f = open("Words_Detection\Words.txt", "a")
            f.write("\n")# תרד שורה כי עכשיו זה האדם השני בתקשורת
            f.close()
            degel=1   # סיימתי לדבר עכשיו האדם השני יגיב בקולו
            break
    cap.release()# משחררת את המשאבים המשמים ללכידת וידאו
    cv2.destroyAllWindows()

    if degel==1:
        r=sr.Recognizer()# יוצרת מופע של המחלקה המאפשרת לזהות קול ולהמירו לטקסט
        with sr.Microphone() as source:# יוצרת מופע של המיקרופון כמקור קלט לזיהוי קול
            r.adjust_for_ambient_noise(source)# מסדרת את הרעש ברקע
            print("Please say somthing...")
            audio=r.listen(source)# מקליטה מהמיקרופן
            try:
                print("You have said: \n"+r.recognize_google(audio))
                with open("Words_Detection\Words.txt","a") as f:
                    f.write("Person B: "+r.recognize_google(audio)+"\n")# מזהה את המלל באמצעות שירות הזיהוי של גוגל וממירה לטקסט וכותבת לטקסט

            except Exception as e:
                print("Error :"+str(e))