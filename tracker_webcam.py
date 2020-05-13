"""
    File name         : object_tracking.py
    File Description  : Multi Object Tracker Using Kalman Filter
                        and Hungarian Algorithm
    Author            : Srini Ananthakrishnan
    Date created      : 07/14/2017
    Date last modified: 07/16/2017
    Python Version    : 2.7
"""

import cv2
from detectors import Detectors
from tracker import Tracker


def main():
    cap = cv2.VideoCapture(0)
    detector = Detectors()
    tracker = Tracker(160, 30, 5, 100)

    skip_frame_count = 0
    track_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
                    (0, 255, 255), (255, 0, 255), (255, 127, 255),
                    (127, 0, 255), (127, 0, 127)]
    pause = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        orig_frame = frame.copy()

        # Detect and return centeroids of the objects in the frame
        centers = detector.Detect(frame)

        # If centroids are detected then track them
        if len(centers) > 0:
            tracker.Update(centers)

            # For identified object tracks draw tracking line
            # Use various colors to indicate different track_id
            for i in range(len(tracker.tracks)):
                if len(tracker.tracks[i].trace) > 1:
                    for j in range(len(tracker.tracks[i].trace)-1):
                        # Draw trace line
                        x1 = tracker.tracks[i].trace[j][0][0]
                        y1 = tracker.tracks[i].trace[j][1][0]
                        x2 = tracker.tracks[i].trace[j+1][0][0]
                        y2 = tracker.tracks[i].trace[j+1][1][0]
                        clr = tracker.tracks[i].track_id % 9
                        cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)),
                                 track_colors[clr], 2)

            # Display the resulting tracking frame
            cv2.imshow('Tracking', frame)

        # Display the original frame
        cv2.imshow('Original', orig_frame)

        # Slower the FPS
        cv2.waitKey(50)

        # Check for key strokes
        k = cv2.waitKey(50) & 0xff
        if k == 27:  # 'esc' key has been pressed, exit program.
            break
        if k == 112:  # 'p' has been pressed. this will pause/resume the code.
            pause = not pause
            if pause is True:
                print("Code is paused. Press 'p' to resume..")
                while pause is True:
                    # stay in this loop until
                    key = cv2.waitKey(30) & 0xff
                    if key == 112:
                        pause = False
                        print("Resume code..!!")
                        break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
