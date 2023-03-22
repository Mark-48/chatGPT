config = transformers.GPT2Config.from_json_file("config.json")
model = transformers.GPT2LMHeadModel(config=config)
model.load_state_dict(torch.load("pytorch_model.bin", map_location=torch.device('cpu')))