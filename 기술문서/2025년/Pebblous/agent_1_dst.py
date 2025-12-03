import csv
import random

TOTAL_ROWS = 3000
OUTPUT_FILENAME = './agent/agent_from_1km.csv'

from_list = [
    1450011901, 1450011902, 1450011903, 1450012001, 1450012002, 1450012003, 1450012100, 1450012200, 
    1450012300, 1450012400, 1450012500, 1450012600, 1450012700, 1450012800, 1450057700, 1450057800, 
    1450057900, 1450058000, 1450058100, 1450058200, 1450058300, 1450058400, 1450058500, 1450058600, 
    1450058700, 1450058800, 1450058900, 1450059000, 1450059100, 1450059200, 1450059300, 1450059400, 
    1450059500, 1450059600, 1450059700, 1450059800, 1450059900, 1450060000, 1450060100, 1450060200, 
    1450060300, 1450060400, 1450060500, 1450060600, 1450060700, 1450060800, 1450060900, 1450061000, 
    1450061100, 1450061200, 1450061300, 1450061400, 1451164101, 1451164201
]

with open(OUTPUT_FILENAME, 'w', newline='', encoding='utf-8-sig') as file:
    writer = csv.writer(file)

    header = ['id', 'departtime', 'from', 'to', 'vehicleClass', 'algorithm']
    writer.writerow(header)

    for i in range(1, TOTAL_ROWS + 1):
        current_id = i

        depart_time = random.randint(3600, 4500)

        from_location = random.choice(from_list)

        to_location = random.choice([1960056002, 1450573503])

        vehicle_class = 'E'

        # 0 = Minimum time
        # 1 = Alleyway
        # 2 = Main road
        algorithm = random.choices(['0', '1', '2'], weights=[70, 10, 20], k=1)[0]

        row = [current_id, depart_time, from_location, to_location, vehicle_class, algorithm]

        writer.writerow(row)

print(f"'{OUTPUT_FILENAME}' 파일 생성이 완료되었습니다. {TOTAL_ROWS}개 데이터)")