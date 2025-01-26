
import mediapipe as mp
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def detect_yoga_pose(image):
    """
    Detects the Warrior II yoga pose using MediaPipe Pose.

    Args:
        image: A numpy array representing the image.

    Returns:
        True if the pose is performed correctly, False otherwise.
    """
    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
        results = pose.process(image)

    if not results.pose_landmarks:
        return False

    landmarks = results.pose_landmarks.landmark

    # Check visibility of key landmarks
    if not all(l.visibility > 0.5 for l in [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                              landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                              landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                              landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                              landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                              landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]]):
      return False

    def calculate_angle(a, b, c):
        a = np.array([a.x, a.y])
        b = np.array([b.x, b.y])
        c = np.array([c.x, c.y])

        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(np.degrees(radians))
        return min(angle, 180 - angle)

    # Angle checks
    hip_angle = calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])
    
    knee_angle_left = calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                       landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                       landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value])

    knee_angle_right = calculate_angle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                        landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])

    #Check if legs are roughly 90 degrees apart
    leg_angle = calculate_angle(landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value])


    #Pose criteria
    if 160 <= leg_angle <= 180 and 80 <= knee_angle_left <= 110 and 160 <= hip_angle <=180:
        return True
    else:
        return False



