train:
	rasa train --domain domain.yml --data data --config config.yml --out models

train-nlu:
	rasa train nlu --nlu split_data/nlu --config configs.yml --out models/nlu

run-actions:
	rasa run actions

shell:
	make run-actions &
	rasa shell -m models --endpoints configs/endpoints.yml

run:
	make run-actions &
	rasa run --enable-api -m models --endpoints configs/endpoints.yml -p 5005

run-x:
	make run-actions &
	rasa x --no-prompt -c configs.yml --cors "*" --endpoints configs/endpoints.yml --enable-api