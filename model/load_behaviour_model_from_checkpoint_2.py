from model.behaviour_model_1 import *

def create_behaviour_model_from_checkpoint():
    IMG_DIM = 112
    CHANNELS = 3
    LATENT_DIM = 512

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    image_shape = (CHANNELS, IMG_DIM, IMG_DIM)


    behaviour_model = ConvLSTM(
        input_shape = image_shape,
        num_classes = 8,
        latent_dim = LATENT_DIM,
        lstm_layers = 1,
        hidden_dim = 1024,
    )


    CHECK_POINT = "/root/FYP_Model_weights/ConvLSTM_240.pth"

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    if device == 'cuda':
        behaviour_model.load_state_dict(torch.load(CHECK_POINT))
    else:
        behaviour_model.load_state_dict(torch.load(CHECK_POINT, map_location=torch.device('cpu')))

    final = nn.Sequential(*list(behaviour_model.lstm.final.children())[:3])
    behaviour_model.lstm.final = final
    # print(behaviour_model)
    behaviour_model = behaviour_model.to(device)

    return behaviour_model

if __name__ == '__main__':
    create_behaviour_model_from_checkpoint()