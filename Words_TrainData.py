from Words_Function import *
from Words_CreateData import *
from tensorflow.keras.callbacks import TensorBoard

X = np.array(sequences)
y = to_categorical(words).astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)#נאחסן את כל הנתונים במערך אחד X שיהיה יותר קל לעבוד איתו
#תכונות סט אימונים
#תכונות סט בדיקות
#תווית ערכת אימונים
#בדיקת תוויות סט

from keras.models import Sequential #לבנית מודל רשת עצבי
from keras.layers import LSTM, Dense
# LSTM -  שכבה לביצוע פעולות זמן
#DENSE - שכבה רגילה
from keras.callbacks import ModelCheckpoint

# לרישום תהליך האימון של מודל למידת מכונה. דיווח ללוג
log_dir = os.path.join('Words_Detection\Logs')
tb_callback = TensorBoard(log_dir=log_dir)

model = Sequential()# יוצר אובייקט דגם מודל ריק שעליו נצטרך להוסיך את השכבות עי" add()
model.add(LSTM(64, return_sequences=True, activation='tanh', input_shape=(30,258)))
model.add(LSTM(128, return_sequences=True, activation='tanh'))
model.add(LSTM(64, return_sequences=False, activation='tanh'))
model.add(Dense(64, activation='tanh'))
model.add(Dense(32, activation='tanh'))
model.add(Dense(labels.shape[0], activation='softmax'))

model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

model.summary()
cp_best_val_loss = ModelCheckpoint(
      "SLD_val_loss", monitor='val_loss', mode = 'min', save_weights_only=True, save_best_only=True, verbose=1
)
#מזהה את האבדן במהלך האימון ושומר את המשקלים של המודל הטוב ביותר
# פונקציית ההפסד היא פונקציה המודדת את ההבדל בין התפוקה החזויה של מודל לבין התפוקה בפועל
#  המטרה של אימון מודל למידת מכונה היא למזער את פונקציית ההפסד, מה שאומר שהמודל משתפר בביצוע תחזיות.
# אך גם לא תהיה התאמה גדולה מידי ואז יש התאמת יתר
# להתאמת משקולות ושיפור ביצועים
cp_best_val_acc = ModelCheckpoint(
      "SLD_val_acc", monitor='val_categorical_accuracy', mode = 'max', save_weights_only=True, save_best_only=True, verbose=1
)
#מזהה את הדיוק הקטגורי של המודל במהלך האימון

model.fit(X_train, y_train, epochs=100, validation_data = (X_test, y_test), callbacks = [cp_best_val_loss, cp_best_val_acc])

#- X_train: זהו נתוני האימון הקלט. זהו מערך numpy או רשימה של numpy arrays, בהתאם לארכיטקטורת הדגם.

#- y_train: אלו נתוני האימון היעד. זהו מערך numpy או רשימה של numpy arrays, בהתאם לארכיטקטורת הדגם.

#- epochs: זהו מספר הפעמים שהמודל יחזור על מערך ההדרכה כולו. במקרה זה, הדגם יתאמן במשך 100 עידנים.

#- validation_data: אלו הנתונים שעל פיהם יאושר המודל לאחר כל תקופה. זה טופל של (X_test, y_test).

#כאשר המודל מתאמן, שני ה-callbacks
#  ישמשו לבצע שמירת משקלים של המודל הטוב ביותר בהתאם לביצוע הטוב ביותר על הבדיקה המתאימה. 

model.save('Words_Detection\sign4_lang_model.h5')

model.load_weights('SLD_val_loss')#נוסיף לו את המשקולות ששמרנו כדי למנוע טעינתו מחדש

#. התקשרויות חוזרות משמשות בדרך כלל במסגרות למידה עמוקה כמו TensorFlow ו-Keras.
#  Callbacks הם כלי רב עוצמה להתאמה אישית של תהליך האימון של מודל למכונה ושיפור הביצועים שלו
#  הם יכולים לשמש למגוון רחב של משימות, בין רישום מדדי אימון, הדמיית ביצועי מודל,
#  הפסקת אימון מוקדם אם המודל אינו משתפר, או שמירת משקלי המודל הטובים ביותר.
