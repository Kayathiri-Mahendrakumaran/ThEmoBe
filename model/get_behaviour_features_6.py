import numpy as np
import torch
from torch.autograd import Variable
from model.load_behaviour_model_from_checkpoint_2 import *

behaviour_model = create_behaviour_model_from_checkpoint()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_behaviour_features(cropped_image_sequence_behaviour):

    behaviour_features = np.empty((0,1024))

    behaviour_model.eval()
    with torch.no_grad():
        image_sequences = Variable(cropped_image_sequence_behaviour.resize_((1,15,3,112,112)).to(device), requires_grad=False)
        print("image_sequences.shape ",image_sequences.shape)
        print("type(image_sequences) ",type(image_sequences))

        # Reset LSTM hidden state
        behaviour_model.lstm.reset_hidden_state()
        # Get sequence predictions
        predictions = behaviour_model(image_sequences)

        pred = predictions.to(torch.device("cpu")).numpy()
        print("pred.shape ",pred.shape)

        behaviour_features = np.append(behaviour_features, pred, axis = 0)

        return behaviour_features