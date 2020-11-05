from CVND_Exercises_2_2_YOLO.get_cropped_human_frames import *
from model.get_behaviour_features_6 import *
from model.face_detector_8 import *
# from model.create_gsom_object_10 import *
from Parallel_GSOM_for_HAAP.create_gsom_objects import *
from model.bounding_box_11 import *




def annotateVideo(APP_ROOT, video_path, emo_annotation, behav_annotation, threat_annotation, video_id, behaviour_model, emotion_model):
    # TODO  - save download_req_id,task_status and download_allocation_time(current time when updating status)

    print("emo_annotation, behav_annotation, threat_annotation ", emo_annotation, behav_annotation, threat_annotation)

    target = "/".join([APP_ROOT, "temp"])

    temp_save_path = target + '/' + video_id + '/'

    frames_list = convert_to_frames(video_path,temp_save_path)
    print("len frames_list ", len(frames_list))

    cropped_image_sequence_for_behaviour, coordinates_array, cropped_image_sequence_for_emotion = get_cropped_frames(
        frames_list)

    chunks = int(len(frames_list)/15)
    mini_chunk_size = len(frames_list) % 15
    mini_chunk_present = 1 if (len(frames_list) % 15 !=0)  else 0

    for j in range(chunks):

        behaviour_features = get_behaviour_features(behaviour_model, cropped_image_sequence_for_behaviour[j:j+15])
        print("behaviour_features shape ",behaviour_features.shape)

        detected_face = detect_face(cropped_image_sequence_for_emotion[j:j+15])
        print("detected_face shape ",detected_face.shape)

        emotion_features = get_emotion_features(emotion_model, detected_face)
        print("emotion_features shape ",emotion_features.shape)

        behaviour_predicted, behaviour_winner_weights = BehaviourGSOM.predict_x(behaviour_features[[0], :])
        print("behaviour_predicted, behaviour_winner_weights ", behaviour_predicted, behaviour_winner_weights)

        emotion_predicted, emotion_winner_weights = EmotionGSOM.predict_x(emotion_features[[0], :])
        print("emotion_predicted, emotion_winner_weights ",emotion_predicted, emotion_winner_weights)

        ALPHA1, ALPHA2 = 1, 1

        threat_feature = np.hstack((ALPHA1 * emotion_winner_weights[0][0], ALPHA2 * behaviour_winner_weights[0][0]))

        threat_feature = threat_feature.reshape(1, 9216)
        print("threat_feature shape ",threat_feature.shape)

        threat_predicted, threat_winner_weights = ThreatGSOM.predict_x(threat_feature)
        print("threat_predicted,threat_winner_weights ",threat_predicted,threat_winner_weights)

        predictions = [str(int(emotion_predicted[0])), str(int(behaviour_predicted[0])), str(int(threat_predicted[0]))]

        print("model predicitons ", predictions)

        what_to_plot = [emo_annotation, behav_annotation, threat_annotation]
        print("what_to_plot", what_to_plot)

        plot_bounding_boxes(predictions, frames_list[j:j+15], coordinates_array[j:j+15], what_to_plot, j)


    if mini_chunk_present:
        is_mini_chunk = True

        behaviour_features = get_behaviour_features(behaviour_model, cropped_image_sequence_for_behaviour[-1 * mini_chunk_size:])
        print("behaviour_features shape ", behaviour_features.shape)

        detected_face = detect_face(cropped_image_sequence_for_emotion[-1 * mini_chunk_size:])
        print("detected_face shape ", detected_face.shape)

        emotion_features = get_emotion_features(emotion_model, detected_face)
        print("emotion_features shape ", emotion_features.shape)

        behaviour_predicted, behaviour_winner_weights = BehaviourGSOM.predict_x(behaviour_features[[0], :])
        print("behaviour_predicted, behaviour_winner_weights ", behaviour_predicted, behaviour_winner_weights)

        emotion_predicted, emotion_winner_weights = EmotionGSOM.predict_x(emotion_features[[0], :])
        print("emotion_predicted, emotion_winner_weights ", emotion_predicted, emotion_winner_weights)

        ALPHA1, ALPHA2 = 1, 1

        threat_feature = np.hstack((ALPHA1 * emotion_winner_weights[0][0], ALPHA2 * behaviour_winner_weights[0][0]))

        threat_feature = threat_feature.reshape(1, 9216)
        print("threat_feature shape ", threat_feature.shape)

        threat_predicted, threat_winner_weights = ThreatGSOM.predict_x(threat_feature)
        print("threat_predicted,threat_winner_weights ", threat_predicted, threat_winner_weights)

        predictions = [str(int(emotion_predicted[0])), str(int(behaviour_predicted[0])), str(int(threat_predicted[0]))]

        print("model predicitons ", predictions)

        what_to_plot = [emo_annotation, behav_annotation, threat_annotation]
        print("what_to_plot", what_to_plot)

        plot_bounding_boxes(predictions, frames_list[-1 * mini_chunk_size:], coordinates_array[-1 * mini_chunk_size:], what_to_plot, chunks+1)

    make_video(APP_ROOT, video_id, len(frames_list))
    return "Video annotated successfully!"


if __name__ == '__main__':
    annotateVideo()