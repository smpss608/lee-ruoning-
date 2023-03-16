import speech_recognition as sr
import wave
import csv

# Get the length of audio
def audioLength(path):
    # Open the WAV file in read-only mode
    with wave.open(path, "rb") as wav_file:
        # Get the number of frames in the WAV file
        num_frames = wav_file.getnframes()
        # Get the sample rate of the WAV file
        sample_rate = wav_file.getframerate()
        # Calculate the duration of the WAV file in seconds
        duration = float(num_frames) / float(sample_rate)
        print("Duration: {:.2f} seconds".format(duration))
    return duration



def speech2text(path, file, time, dur):
    off=0
    r = sr.Recognizer()
    WAV = sr.AudioFile(path)
    # Output file
    fh = open("./output_audio_time_dur/"+file+"_output_"+str(time)+"_"+str(dur)+".csv","w", newline='', encoding='utf-8-sig') 
    writer = csv.writer(fh)
    len=audioLength(path)
    for i in range (int(len)//10):
        # Audio time
        min, sec = divmod(off, 60)
        hour, min=divmod(min, 60)
        with WAV as source:
            audio = r.record(source,  offset=off, duration=dur)
            #fh.write(audio+". \n") 
        off+=time
        try:
            text=r.recognize_google(audio,  language="zh")
            # Write into .csv
            writer.writerow(["%02d:%02d:%02d"%(hour,min,sec),text])
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
    WAV.close()
    fh.close()



if __name__ == '__main__':
    time=10
    dur=12
    # Recognize each file
    for i in range(1,9):
        for j in range(1,4):
            file=str(i)+'-'+str(j)+'audio'
            path="./recording/"+str(i)+"/"+file+".wav"
            speech2text(path, file, time, dur)
